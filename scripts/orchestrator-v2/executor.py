#!/usr/bin/env python3
"""
Executor — Task graph execution with dependency resolution, parallel dispatch, failure handling.

Dispatches tasks as OpenClaw subagents, monitors progress, handles failures with retries.
"""

import json
import os
import subprocess
import time
import threading
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from datetime import datetime, timezone
from decomposer import Task, TaskGraph

MAX_PARALLEL = 5  # OpenClaw subagent limit
MAX_RETRIES = 2
POLL_INTERVAL = 30  # seconds


@dataclass
class RunningTask:
    task: Task
    session_id: Optional[str] = None
    started_at: Optional[str] = None
    retries: int = 0


class Executor:
    """Execute a task graph with dependency resolution and parallel dispatch."""

    def __init__(self, graph: TaskGraph, on_complete: Optional[Callable] = None,
                 on_fail: Optional[Callable] = None, dry_run: bool = False):
        self.graph = graph
        self.on_complete = on_complete
        self.on_fail = on_fail
        self.dry_run = dry_run
        self.running: Dict[str, RunningTask] = {}
        self.results: Dict[str, dict] = {}

    def execute(self) -> TaskGraph:
        """Execute the full task graph. Returns updated graph."""
        print(f"⚡ Executing goal: {self.graph.goal}")
        print(f"   {len(self.graph.tasks)} tasks, max parallel: {MAX_PARALLEL}")
        print()

        while not self.graph.is_complete():
            # Check for hard failure (dependency chain broken)
            if self._has_broken_deps():
                print("❌ Execution halted: broken dependency chain")
                break

            # Dispatch ready tasks
            ready = self.graph.ready_tasks()
            slots = MAX_PARALLEL - len(self.running)
            to_dispatch = ready[:slots]

            for task in to_dispatch:
                self._dispatch(task)

            # Poll running tasks
            if self.running:
                self._poll_running()

            # Wait before next cycle
            if not self.graph.is_complete() and self.running:
                time.sleep(POLL_INTERVAL)

        # Summary
        self._print_summary()
        return self.graph

    def _dispatch(self, task: Task):
        """Dispatch a single task as a subagent."""
        task.status = "running"
        now = datetime.now(timezone.utc).isoformat()

        print(f"  🚀 Dispatching: {task.id} → {task.model}")
        print(f"     {task.description}")

        if self.dry_run:
            task.status = "completed"
            task.result = "[DRY RUN] Would have executed"
            print(f"  ✅ [DRY RUN] {task.id}")
            return

        # Build the agent prompt
        agent_prompt = self._build_prompt(task)

        # Map model to OpenClaw agent alias
        agent_alias = self._model_to_alias(task.model)

        try:
            # Use orchestrator v1's dispatch mechanism or direct subagent spawn
            result = subprocess.run(
                ["python3", "/data/workspace/scripts/orchestrator.py",
                 "dispatch", "--task", agent_prompt, "--agent", agent_alias],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout.strip()
            # Try to extract task ID from output
            task_id = None
            try:
                data = json.loads(output)
                task_id = data.get("task_id") or data.get("id")
            except (json.JSONDecodeError, TypeError):
                # Parse from text output
                for line in output.split("\n"):
                    if "task_id" in line or "Task ID" in line:
                        task_id = line.split(":")[-1].strip()

            self.running[task.id] = RunningTask(
                task=task, session_id=task_id, started_at=now
            )
        except Exception as e:
            print(f"  ⚠️  Dispatch failed for {task.id}: {e}")
            task.error = str(e)
            running_task = RunningTask(task=task, started_at=now)
            self._handle_failure(running_task)

    def _poll_running(self):
        """Check status of running tasks."""
        completed = []
        for task_id, rt in self.running.items():
            status = self._check_task_status(rt)
            if status == "completed":
                rt.task.status = "completed"
                rt.task.result = self.results.get(task_id, {}).get("result", "Completed")
                completed.append(task_id)
                print(f"  ✅ Completed: {task_id}")
                if self.on_complete:
                    self.on_complete(rt.task)
            elif status == "failed":
                self._handle_failure(rt)
                if rt.task.status == "failed":
                    completed.append(task_id)

        for tid in completed:
            self.running.pop(tid, None)

    def _handle_failure(self, rt: RunningTask):
        """Handle a failed task — retry or mark failed."""
        if rt.retries < MAX_RETRIES:
            rt.retries += 1
            rt.task.status = "pending"
            print(f"  🔄 Retrying {rt.task.id} (attempt {rt.retries + 1}/{MAX_RETRIES + 1})")
        else:
            rt.task.status = "failed"
            print(f"  ❌ Failed: {rt.task.id} after {MAX_RETRIES + 1} attempts")
            if self.on_fail:
                self.on_fail(rt.task)

    def _check_task_status(self, rt: RunningTask) -> str:
        """Check if a dispatched task has completed."""
        if not rt.session_id:
            return "failed"
        try:
            result = subprocess.run(
                ["python3", "/data/workspace/scripts/orchestrator.py", "status"],
                capture_output=True, text=True, timeout=15
            )
            # Parse status output for our task
            for line in result.stdout.split("\n"):
                if rt.session_id and rt.session_id in line:
                    if "completed" in line.lower():
                        return "completed"
                    elif "failed" in line.lower() or "error" in line.lower():
                        return "failed"
            return "running"
        except Exception:
            return "running"  # Assume still running on check failure

    def _has_broken_deps(self) -> bool:
        """Check if any pending task has a failed dependency."""
        failed_ids = {t.id for t in self.graph.tasks if t.status == "failed"}
        for task in self.graph.tasks:
            if task.status == "pending" and any(d in failed_ids for d in task.dependencies):
                task.status = "skipped"
                task.error = f"Skipped: dependency failed"
                print(f"  ⏭️  Skipped: {task.id} (dependency failed)")
        return all(
            t.status in ("completed", "failed", "skipped")
            for t in self.graph.tasks
        ) and any(t.status == "failed" for t in self.graph.tasks)

    def _build_prompt(self, task: Task) -> str:
        """Build a detailed prompt for the executing agent."""
        parts = [
            f"# Task: {task.description}",
            "",
            task.prompt,
            "",
            "## Acceptance Criteria",
        ]
        for i, c in enumerate(task.acceptance_criteria, 1):
            parts.append(f"{i}. {c}")
        parts.append("")
        parts.append(f"Effort estimate: {task.effort}")
        return "\n".join(parts)

    def _model_to_alias(self, model: str) -> str:
        """Map full model name to orchestrator alias."""
        aliases = {
            "anthropic/claude-opus-4-6": "opus",
            "anthropic/claude-sonnet-4": "sonnet",
            "anthropic/claude-sonnet-4-5": "sonnet",
            "deepseek/deepseek-chat": "deepseek",
            "openai-codex/gpt-5.3-codex": "codex",
            "x-ai/grok-code-fast-1": "grok",
            "google/gemini-3-flash-preview": "sonnet",  # fallback
            "kimi/kimi-k2.5": "deepseek",  # fallback
        }
        return aliases.get(model, "sonnet")

    def _print_summary(self):
        """Print execution summary."""
        completed = sum(1 for t in self.graph.tasks if t.status == "completed")
        failed = sum(1 for t in self.graph.tasks if t.status == "failed")
        skipped = sum(1 for t in self.graph.tasks if t.status == "skipped")
        total = len(self.graph.tasks)

        print()
        print("═" * 50)
        print(f"  Goal: {self.graph.goal}")
        print(f"  ✅ {completed}/{total} completed  ❌ {failed} failed  ⏭️ {skipped} skipped")
        print("═" * 50)


if __name__ == "__main__":
    # Test with a simple graph
    graph = TaskGraph(
        goal="Test execution",
        tasks=[
            Task(id="t1", description="First task", model="deepseek/deepseek-chat",
                 effort="small", prompt="Do thing 1", acceptance_criteria=["Done"]),
            Task(id="t2", description="Second task", model="deepseek/deepseek-chat",
                 effort="small", prompt="Do thing 2", acceptance_criteria=["Done"],
                 dependencies=["t1"]),
        ]
    )
    executor = Executor(graph, dry_run=True)
    executor.execute()
