"""
Temporal Workflow Definitions for Honey AI.
Workflows are durable, fault-tolerant orchestrations of activities.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Dict, List, Optional

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import (
        SpawnAgentInput, SpawnAgentOutput,
        HealthCheckInput, HealthCheckOutput,
        ShellInput, ShellOutput,
        ScoreProjectInput,
        PublishEventInput,
        NotificationInput,
        SteerAgentInput,
        GitPushInput,
        WaitForAgentInput, WaitForAgentOutput,
        spawn_agent, check_service_health, run_shell,
        score_project, publish_event, send_notification,
        steer_agent, git_push, wait_for_agent,
    )


# Shared retry policies
DEFAULT_RETRY = RetryPolicy(
    initial_interval=timedelta(seconds=5),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(minutes=2),
    maximum_attempts=3,
)

AGENT_RETRY = RetryPolicy(
    initial_interval=timedelta(seconds=10),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(minutes=5),
    maximum_attempts=2,
)


# ---------------------------------------------------------------------------
# Input data classes
# ---------------------------------------------------------------------------

@dataclass
class SelfHealingInput:
    services: List[Dict[str, str]]  # [{"name": "...", "url": "..."}]
    check_interval_seconds: int = 300
    max_retries: int = 3


@dataclass
class JudgeSwarmInput:
    repos: List[str]
    model: str = "anthropic/claude-sonnet-4-20250514"
    judge_model: str = "anthropic/claude-sonnet-4-20250514"


@dataclass
class OrchestratorInput:
    goal: str
    model: str = "anthropic/claude-sonnet-4-20250514"
    max_parallel: int = 3


@dataclass
class HealthMonitorInput:
    services: List[Dict[str, str]]
    interval_seconds: int = 60
    alert_after_failures: int = 3


# ---------------------------------------------------------------------------
# SelfHealingWorkflow
# ---------------------------------------------------------------------------

@workflow.defn
class SelfHealingWorkflow:
    """Monitor services → detect failure → spawn debug+ops agents → verify → retry/escalate."""

    def __init__(self):
        self._should_stop = False

    @workflow.signal
    async def stop(self):
        self._should_stop = True

    @workflow.query
    def status(self) -> str:
        return "running" if not self._should_stop else "stopped"

    @workflow.run
    async def run(self, input: SelfHealingInput) -> Dict[str, Any]:
        results = {"healed": [], "escalated": [], "iterations": 0}

        while not self._should_stop:
            results["iterations"] += 1

            # Check all services
            checks = []
            for svc in input.services:
                checks.append(
                    workflow.execute_activity(
                        check_service_health,
                        HealthCheckInput(service_name=svc["name"], url=svc["url"]),
                        start_to_close_timeout=timedelta(seconds=30),
                        retry_policy=DEFAULT_RETRY,
                    )
                )
            health_results: List[HealthCheckOutput] = await asyncio.gather(*checks)

            # Process failures
            for result in health_results:
                if result.healthy:
                    continue

                workflow.logger.warn(f"Service unhealthy: {result.service_name} — {result.error}")
                healed = False

                for attempt in range(input.max_retries):
                    # Spawn debug agent
                    debug_result = await workflow.execute_activity(
                        spawn_agent,
                        SpawnAgentInput(
                            model="anthropic/claude-sonnet-4-20250514",
                            task=f"Debug failing service: {result.service_name}. Error: {result.error}. "
                                 f"Check logs, identify root cause, and fix if possible.",
                            label=f"self-heal-debug-{result.service_name}-{attempt}",
                        ),
                        start_to_close_timeout=timedelta(minutes=10),
                        retry_policy=AGENT_RETRY,
                    )

                    if debug_result.success:
                        # Wait for debug agent
                        await workflow.execute_activity(
                            wait_for_agent,
                            WaitForAgentInput(
                                label=f"self-heal-debug-{result.service_name}-{attempt}",
                                timeout_seconds=300,
                            ),
                            start_to_close_timeout=timedelta(minutes=6),
                            heartbeat_timeout=timedelta(seconds=30),
                        )

                    # Verify fix
                    recheck = await workflow.execute_activity(
                        check_service_health,
                        HealthCheckInput(service_name=result.service_name, url=[s["url"] for s in input.services if s["name"] == result.service_name][0]),
                        start_to_close_timeout=timedelta(seconds=30),
                        retry_policy=DEFAULT_RETRY,
                    )

                    if recheck.healthy:
                        healed = True
                        results["healed"].append(result.service_name)
                        await workflow.execute_activity(
                            send_notification,
                            NotificationInput(target="telegram", message=f"✅ Self-healed: {result.service_name}"),
                            start_to_close_timeout=timedelta(seconds=15),
                        )
                        break

                if not healed:
                    results["escalated"].append(result.service_name)
                    await workflow.execute_activity(
                        send_notification,
                        NotificationInput(
                            target="telegram",
                            message=f"🚨 ESCALATION: {result.service_name} still unhealthy after {input.max_retries} attempts. Manual intervention needed."
                        ),
                        start_to_close_timeout=timedelta(seconds=15),
                    )

            # Wait before next cycle
            await workflow.sleep(timedelta(seconds=input.check_interval_seconds))

        return results


# ---------------------------------------------------------------------------
# JudgeSwarmWorkflow
# ---------------------------------------------------------------------------

@workflow.defn
class JudgeSwarmWorkflow:
    """Fan-out judges per repo → fan-out brainstorm+plan+optimize → consolidate."""

    @workflow.run
    async def run(self, input: JudgeSwarmInput) -> Dict[str, Any]:
        results = {}

        # Fan-out: one judge per repo
        judge_tasks = []
        for repo in input.repos:
            judge_tasks.append(self._judge_repo(repo, input))

        repo_results = await asyncio.gather(*judge_tasks)
        for repo, result in zip(input.repos, repo_results):
            results[repo] = result

        # Consolidate: publish summary
        await workflow.execute_activity(
            publish_event,
            PublishEventInput(channel="honey:judge-results", data=results),
            start_to_close_timeout=timedelta(seconds=15),
        )

        return results

    async def _judge_repo(self, repo: str, input: JudgeSwarmInput) -> Dict[str, Any]:
        """Judge a single repo, then fan-out improvement agents."""

        # Step 1: Judge
        judge = await workflow.execute_activity(
            spawn_agent,
            SpawnAgentInput(
                model=input.judge_model,
                task=f"Judge the codebase at /data/workspace/repos/{repo}. "
                     f"Evaluate: code quality, architecture, test coverage, documentation, security. "
                     f"Output a JSON score object.",
                label=f"judge-{repo}",
            ),
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=AGENT_RETRY,
        )

        judge_result = await workflow.execute_activity(
            wait_for_agent,
            WaitForAgentInput(label=f"judge-{repo}", timeout_seconds=300),
            start_to_close_timeout=timedelta(minutes=6),
            heartbeat_timeout=timedelta(seconds=30),
        )

        # Step 2: Fan-out improvement agents (brainstorm, plan, optimize)
        improvement_tasks = []
        for phase in ["brainstorm", "plan", "optimize"]:
            improvement_tasks.append(
                workflow.execute_activity(
                    spawn_agent,
                    SpawnAgentInput(
                        model=input.model,
                        task=f"{phase.capitalize()} improvements for {repo} based on judge feedback: {judge_result.result or 'no feedback'}",
                        label=f"{phase}-{repo}",
                    ),
                    start_to_close_timeout=timedelta(minutes=10),
                    retry_policy=AGENT_RETRY,
                )
            )

        await asyncio.gather(*improvement_tasks)

        # Wait for all improvement agents
        wait_tasks = []
        for phase in ["brainstorm", "plan", "optimize"]:
            wait_tasks.append(
                workflow.execute_activity(
                    wait_for_agent,
                    WaitForAgentInput(label=f"{phase}-{repo}", timeout_seconds=300),
                    start_to_close_timeout=timedelta(minutes=6),
                    heartbeat_timeout=timedelta(seconds=30),
                )
            )

        improvements = await asyncio.gather(*wait_tasks)

        return {
            "judge": judge_result.result,
            "improvements": {
                phase: imp.result
                for phase, imp in zip(["brainstorm", "plan", "optimize"], improvements)
            },
        }


# ---------------------------------------------------------------------------
# OrchestratorWorkflow
# ---------------------------------------------------------------------------

@workflow.defn
class OrchestratorWorkflow:
    """Decompose goal → execute task graph with dependencies → learn."""

    @workflow.run
    async def run(self, input: OrchestratorInput) -> Dict[str, Any]:
        # Step 1: Decompose goal into tasks
        decompose = await workflow.execute_activity(
            spawn_agent,
            SpawnAgentInput(
                model=input.model,
                task=f"Decompose this goal into a task list with dependencies. "
                     f"Output JSON: {{\"tasks\": [{{\"id\": 1, \"name\": \"...\", \"depends_on\": [], \"model\": \"...\"}}]}}. "
                     f"Goal: {input.goal}",
                label="orchestrator-decompose",
            ),
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=AGENT_RETRY,
        )

        decompose_result = await workflow.execute_activity(
            wait_for_agent,
            WaitForAgentInput(label="orchestrator-decompose", timeout_seconds=300),
            start_to_close_timeout=timedelta(minutes=6),
            heartbeat_timeout=timedelta(seconds=30),
        )

        # Step 2: Execute tasks respecting dependencies
        # Parse tasks from agent output (best-effort)
        import json as _json
        tasks = []
        try:
            raw = decompose_result.result or "{}"
            # Find JSON in output
            start_idx = raw.find("{")
            end_idx = raw.rfind("}") + 1
            if start_idx >= 0:
                parsed = _json.loads(raw[start_idx:end_idx])
                tasks = parsed.get("tasks", [])
        except Exception:
            workflow.logger.warn("Could not parse decomposed tasks, executing goal as single task")
            tasks = [{"id": 1, "name": input.goal, "depends_on": [], "model": input.model}]

        completed = {}
        while len(completed) < len(tasks):
            # Find ready tasks
            ready = [
                t for t in tasks
                if t["id"] not in completed
                and all(d in completed for d in t.get("depends_on", []))
            ]

            if not ready:
                workflow.logger.error("Deadlock in task graph")
                break

            # Execute ready tasks in parallel (up to max_parallel)
            batch = ready[:input.max_parallel]
            spawn_tasks = []
            for task in batch:
                label = f"orch-task-{task['id']}"
                spawn_tasks.append(
                    workflow.execute_activity(
                        spawn_agent,
                        SpawnAgentInput(
                            model=task.get("model", input.model),
                            task=task["name"],
                            label=label,
                        ),
                        start_to_close_timeout=timedelta(minutes=10),
                        retry_policy=AGENT_RETRY,
                    )
                )

            await asyncio.gather(*spawn_tasks)

            # Wait for batch
            wait_tasks = []
            for task in batch:
                wait_tasks.append(
                    workflow.execute_activity(
                        wait_for_agent,
                        WaitForAgentInput(
                            label=f"orch-task-{task['id']}",
                            timeout_seconds=600,
                        ),
                        start_to_close_timeout=timedelta(minutes=11),
                        heartbeat_timeout=timedelta(seconds=30),
                    )
                )

            wait_results = await asyncio.gather(*wait_tasks)
            for task, result in zip(batch, wait_results):
                completed[task["id"]] = {
                    "name": task["name"],
                    "completed": result.completed,
                    "result": result.result,
                    "error": result.error,
                }

        # Step 3: Learn — commit results
        await workflow.execute_activity(
            publish_event,
            PublishEventInput(
                channel="honey:orchestrator-complete",
                data={"goal": input.goal, "tasks_completed": len(completed), "total": len(tasks)},
            ),
            start_to_close_timeout=timedelta(seconds=15),
        )

        return {"goal": input.goal, "tasks": completed}


# ---------------------------------------------------------------------------
# HealthMonitorWorkflow
# ---------------------------------------------------------------------------

@workflow.defn
class HealthMonitorWorkflow:
    """Continuous health monitoring with durable timers and alerting."""

    def __init__(self):
        self._should_stop = False
        self._failure_counts: Dict[str, int] = {}
        self._status = "starting"

    @workflow.signal
    async def stop(self):
        self._should_stop = True

    @workflow.signal
    async def update_services(self, services: List[Dict[str, str]]):
        """Dynamically update monitored services."""
        self._services = services

    @workflow.query
    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self._status,
            "failure_counts": dict(self._failure_counts),
        }

    @workflow.run
    async def run(self, input: HealthMonitorInput) -> Dict[str, Any]:
        self._services = input.services
        self._status = "running"
        total_checks = 0

        while not self._should_stop:
            total_checks += 1

            # Check all services in parallel
            checks = []
            for svc in self._services:
                checks.append(
                    workflow.execute_activity(
                        check_service_health,
                        HealthCheckInput(service_name=svc["name"], url=svc["url"]),
                        start_to_close_timeout=timedelta(seconds=30),
                        retry_policy=DEFAULT_RETRY,
                    )
                )

            results: List[HealthCheckOutput] = await asyncio.gather(*checks)

            for result in results:
                if result.healthy:
                    # Reset failure count on success
                    if result.service_name in self._failure_counts:
                        if self._failure_counts[result.service_name] >= input.alert_after_failures:
                            await workflow.execute_activity(
                                send_notification,
                                NotificationInput(
                                    target="telegram",
                                    message=f"✅ {result.service_name} recovered ({result.response_time_ms}ms)"
                                ),
                                start_to_close_timeout=timedelta(seconds=15),
                            )
                        self._failure_counts[result.service_name] = 0
                else:
                    count = self._failure_counts.get(result.service_name, 0) + 1
                    self._failure_counts[result.service_name] = count

                    if count == input.alert_after_failures:
                        await workflow.execute_activity(
                            send_notification,
                            NotificationInput(
                                target="telegram",
                                message=f"🔴 {result.service_name} DOWN ({count} consecutive failures): {result.error}"
                            ),
                            start_to_close_timeout=timedelta(seconds=15),
                        )

            # Publish metrics
            await workflow.execute_activity(
                publish_event,
                PublishEventInput(
                    channel="honey:health-metrics",
                    data={
                        "check_number": total_checks,
                        "results": [
                            {"name": r.service_name, "healthy": r.healthy, "ms": r.response_time_ms}
                            for r in results
                        ],
                    },
                ),
                start_to_close_timeout=timedelta(seconds=15),
            )

            # Durable timer — survives crashes
            await workflow.sleep(timedelta(seconds=input.interval_seconds))

        self._status = "stopped"
        return {"total_checks": total_checks, "final_failures": dict(self._failure_counts)}


# All workflows for registration
ALL_WORKFLOWS = [
    SelfHealingWorkflow,
    JudgeSwarmWorkflow,
    OrchestratorWorkflow,
    HealthMonitorWorkflow,
]
