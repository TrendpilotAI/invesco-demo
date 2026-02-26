#!/usr/bin/env python3
"""
Decomposer — Goal → Task Graph with dependencies.

Each task has: id, description, model, effort, prompt, acceptance_criteria, dependencies, status.
Uses an LLM to decompose complex goals into structured task graphs.
"""

import json
import os
import subprocess
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from model_router import route, TaskProfile, classify_task_type, estimate_complexity


@dataclass
class Task:
    id: str
    description: str
    model: str
    effort: str  # "small" (<30min), "medium" (30min-2h), "large" (2h+)
    prompt: str
    acceptance_criteria: List[str]
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, running, completed, failed, skipped
    result: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class TaskGraph:
    goal: str
    tasks: List[Task] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "goal": self.goal,
            "tasks": [t.to_dict() for t in self.tasks],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            goal=d["goal"],
            tasks=[Task.from_dict(t) for t in d.get("tasks", [])],
            metadata=d.get("metadata", {}),
        )

    def ready_tasks(self) -> List[Task]:
        """Tasks whose dependencies are all completed."""
        completed = {t.id for t in self.tasks if t.status == "completed"}
        return [
            t for t in self.tasks
            if t.status == "pending" and all(d in completed for d in t.dependencies)
        ]

    def is_complete(self) -> bool:
        return all(t.status in ("completed", "skipped") for t in self.tasks)

    def is_failed(self) -> bool:
        return any(t.status == "failed" for t in self.tasks)

    def summary(self) -> str:
        lines = [f"Goal: {self.goal}"]
        for t in self.tasks:
            deps = f" (deps: {', '.join(t.dependencies)})" if t.dependencies else ""
            lines.append(f"  [{t.status:>9}] {t.id[:8]}.. {t.description} → {t.model} [{t.effort}]{deps}")
        return "\n".join(lines)


# ── LLM-based decomposition ───────────────────────────────────

DECOMPOSE_PROMPT = """You are a task decomposition engine. Given a goal, break it into a directed acyclic graph of tasks.

GOAL: {goal}

CONTEXT (if any): {context}

Output ONLY valid JSON with this structure:
{{
  "tasks": [
    {{
      "id": "unique-short-id",
      "description": "What this task does",
      "effort": "small|medium|large",
      "prompt": "Detailed prompt to give the executing agent",
      "acceptance_criteria": ["criterion 1", "criterion 2"],
      "dependencies": ["id-of-dependency"] 
    }}
  ]
}}

Rules:
- IDs should be short kebab-case (e.g. "setup-db", "build-api")
- Dependencies reference other task IDs (empty list for root tasks)
- Order tasks so dependencies come first
- Each task should be independently executable by an AI agent
- Prompt should be detailed enough for a fresh agent with no context
- 3-10 tasks is ideal for most goals
- Effort: small (<30min coding), medium (30min-2h), large (2h+)
"""


def decompose_with_llm(goal: str, context: str = "") -> TaskGraph:
    """Use an LLM to decompose a goal into tasks."""
    prompt = DECOMPOSE_PROMPT.format(goal=goal, context=context)

    # Use OpenClaw's CLI or a direct API call
    # Try subprocess first (works in OpenClaw environment)
    try:
        result = _call_llm(prompt)
        data = json.loads(result)
        tasks = []
        for t in data["tasks"]:
            task_type = classify_task_type(t["description"])
            complexity = estimate_complexity(t["description"])
            profile = TaskProfile(
                description=t["description"],
                task_type=task_type,
                complexity=complexity,
            )
            model = route(profile)
            tasks.append(Task(
                id=t["id"],
                description=t["description"],
                model=model,
                effort=t.get("effort", "medium"),
                prompt=t["prompt"],
                acceptance_criteria=t.get("acceptance_criteria", []),
                dependencies=t.get("dependencies", []),
            ))
        return TaskGraph(goal=goal, tasks=tasks)
    except Exception as e:
        # Fallback: single-task graph
        profile = TaskProfile(description=goal)
        return TaskGraph(
            goal=goal,
            tasks=[Task(
                id="single-task",
                description=goal,
                model=route(profile),
                effort="large",
                prompt=goal,
                acceptance_criteria=["Goal is achieved"],
                dependencies=[],
            )],
            metadata={"fallback": True, "error": str(e)},
        )


def decompose_manual(goal: str, task_specs: List[Dict]) -> TaskGraph:
    """Create a task graph from manually specified tasks."""
    tasks = []
    for spec in task_specs:
        profile = TaskProfile(description=spec["description"])
        tasks.append(Task(
            id=spec.get("id", str(uuid.uuid4())[:8]),
            description=spec["description"],
            model=spec.get("model") or route(profile),
            effort=spec.get("effort", "medium"),
            prompt=spec.get("prompt", spec["description"]),
            acceptance_criteria=spec.get("acceptance_criteria", ["Task completed"]),
            dependencies=spec.get("dependencies", []),
        ))
    return TaskGraph(goal=goal, tasks=tasks)


def _call_llm(prompt: str) -> str:
    """Call LLM via OpenClaw or direct API."""
    # Strategy 1: Use environment's API directly via curl
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if api_key:
        import urllib.request
        import urllib.error
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps({
                "model": "anthropic/claude-sonnet-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
            }).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"]
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            return content.strip()

    # Strategy 2: Use a simple heuristic decomposition
    raise RuntimeError("No API key available for LLM decomposition")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        goal = " ".join(sys.argv[1:])
        graph = decompose_with_llm(goal)
        print(json.dumps(graph.to_dict(), indent=2))
    else:
        print("Usage: python3 decomposer.py <goal description>")
