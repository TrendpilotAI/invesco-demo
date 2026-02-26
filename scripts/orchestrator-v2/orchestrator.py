#!/usr/bin/env python3
"""
Agentic Orchestrator v2 — Main reasoning loop.

Receives goals, decomposes them into task graphs, dispatches to optimal models,
monitors execution, and learns from outcomes.

CLI:
  python3 orchestrator.py goal "Make Invesco demo work end-to-end"
  python3 orchestrator.py status
  python3 orchestrator.py learn --report
  python3 orchestrator.py decompose "Build feature X"  (preview without executing)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add this directory to path for sibling imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decomposer import decompose_with_llm, decompose_manual, TaskGraph, Task
from model_router import route, TaskProfile, classify_task_type
from executor import Executor
from learner import (
    init_schema, record_outcome, record_goal,
    generate_report, get_model_stats, get_model_recommendations
)

STATE_DIR = Path(os.environ.get("OPENCLAW_WORKSPACE_DIR", "/data/workspace")) / ".orchestrator-v2"
GOALS_FILE = STATE_DIR / "goals.json"


def ensure_state():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not GOALS_FILE.exists():
        GOALS_FILE.write_text("[]")


def load_goals():
    ensure_state()
    return json.loads(GOALS_FILE.read_text())


def save_goals(goals):
    ensure_state()
    GOALS_FILE.write_text(json.dumps(goals, indent=2))


# ── Commands ───────────────────────────────────────────────────

def cmd_goal(args):
    """Main entry: decompose a goal and execute it."""
    goal_text = args.goal
    print(f"🎯 Goal: {goal_text}")
    print()

    # Step 1: Decompose
    print("🧩 Decomposing goal into tasks...")
    graph = decompose_with_llm(goal_text, context=args.context or "")
    print(f"   Generated {len(graph.tasks)} tasks:")
    print()
    print(graph.summary())
    print()

    # Step 2: Confirm (unless --yes)
    if not args.yes:
        resp = input("Execute this plan? [Y/n] ").strip().lower()
        if resp and resp != "y":
            print("Aborted.")
            return

    # Step 3: Save goal state
    goal_record = {
        "id": datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        "goal": goal_text,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "graph": graph.to_dict(),
    }
    goals = load_goals()
    goals.append(goal_record)
    save_goals(goals)

    # Step 4: Execute
    start_time = time.time()

    def on_task_complete(task: Task):
        try:
            record_outcome(
                task_id=task.id, goal=goal_text, description=task.description,
                task_type=classify_task_type(task.description), model=task.model,
                effort=task.effort, success=True, result_summary=task.result,
            )
        except Exception as e:
            print(f"  ⚠️  Failed to record outcome: {e}")

    def on_task_fail(task: Task):
        try:
            record_outcome(
                task_id=task.id, goal=goal_text, description=task.description,
                task_type=classify_task_type(task.description), model=task.model,
                effort=task.effort, success=False, error=task.error,
            )
        except Exception as e:
            print(f"  ⚠️  Failed to record outcome: {e}")

    executor = Executor(
        graph, on_complete=on_task_complete, on_fail=on_task_fail,
        dry_run=args.dry_run
    )
    result_graph = executor.execute()
    duration = time.time() - start_time

    # Step 5: Record goal outcome
    completed = sum(1 for t in result_graph.tasks if t.status == "completed")
    failed = sum(1 for t in result_graph.tasks if t.status == "failed")
    skipped = sum(1 for t in result_graph.tasks if t.status == "skipped")
    success = failed == 0

    try:
        record_goal(goal_text, len(result_graph.tasks), completed, failed,
                    skipped, duration, success)
    except Exception as e:
        print(f"⚠️  Failed to record goal: {e}")

    # Update goal state
    goal_record["status"] = "completed" if success else "failed"
    goal_record["finished_at"] = datetime.now(timezone.utc).isoformat()
    goal_record["duration"] = duration
    goal_record["graph"] = result_graph.to_dict()
    goals = load_goals()
    for i, g in enumerate(goals):
        if g["id"] == goal_record["id"]:
            goals[i] = goal_record
            break
    save_goals(goals)


def cmd_decompose(args):
    """Preview decomposition without executing."""
    graph = decompose_with_llm(args.goal, context=args.context or "")
    print(graph.summary())
    print()
    if args.json:
        print(json.dumps(graph.to_dict(), indent=2))


def cmd_status(args):
    """Show status of all goals."""
    goals = load_goals()
    if not goals:
        print("No goals tracked yet.")
        return
    for g in goals[-10:]:  # Last 10
        status_icon = {"running": "🔄", "completed": "✅", "failed": "❌"}.get(g["status"], "❓")
        dur = f" ({g.get('duration', 0):.0f}s)" if g.get("duration") else ""
        print(f"  {status_icon} [{g['id']}] {g['goal'][:60]}{dur}")
        graph = TaskGraph.from_dict(g["graph"])
        c = sum(1 for t in graph.tasks if t.status == "completed")
        f = sum(1 for t in graph.tasks if t.status == "failed")
        print(f"     {c}/{len(graph.tasks)} tasks completed, {f} failed")


def cmd_learn(args):
    """Learning commands — report, stats, init."""
    if args.init:
        init_schema()
    elif args.report:
        print(generate_report(days=args.days))
    elif args.recommend:
        recs = get_model_recommendations()
        if recs:
            print("🎯 Model Recommendations (based on history):")
            for tt, model in recs.items():
                print(f"  {tt} → {model}")
        else:
            print("No data yet.")
    else:
        stats = get_model_stats(days=args.days)
        print(json.dumps(stats, indent=2, default=str))


def cmd_route(args):
    """Test model routing for a description."""
    profile = TaskProfile(description=args.description)
    model = route(profile)
    print(json.dumps({
        "description": args.description,
        "task_type": classify_task_type(args.description),
        "model": model,
    }, indent=2))


# ── CLI ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Agentic Orchestrator v2 — Intelligent task decomposition & execution"
    )
    sub = parser.add_subparsers(dest="command")

    # goal
    p_goal = sub.add_parser("goal", help="Decompose and execute a goal")
    p_goal.add_argument("goal", help="Goal description")
    p_goal.add_argument("--context", help="Additional context")
    p_goal.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    p_goal.add_argument("--dry-run", action="store_true", help="Preview without executing")

    # decompose
    p_dec = sub.add_parser("decompose", help="Preview task decomposition")
    p_dec.add_argument("goal", help="Goal description")
    p_dec.add_argument("--context", help="Additional context")
    p_dec.add_argument("--json", action="store_true", help="Output full JSON")

    # status
    sub.add_parser("status", help="Show goal status")

    # learn
    p_learn = sub.add_parser("learn", help="Learning & analytics")
    p_learn.add_argument("--report", action="store_true", help="Generate report")
    p_learn.add_argument("--init", action="store_true", help="Initialize DB schema")
    p_learn.add_argument("--recommend", action="store_true", help="Show model recommendations")
    p_learn.add_argument("--days", type=int, default=30, help="Lookback days")

    # route
    p_route = sub.add_parser("route", help="Test model routing")
    p_route.add_argument("description", help="Task description")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "goal": cmd_goal,
        "decompose": cmd_decompose,
        "status": cmd_status,
        "learn": cmd_learn,
        "route": cmd_route,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
