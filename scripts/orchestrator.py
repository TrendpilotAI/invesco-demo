#!/usr/bin/env python3
"""
Multi-Agent Orchestrator — dmux-like capabilities for headless OpenClaw.

Manages parallel agent tasks with isolated workspaces, state tracking,
and merge-back. Works through OpenClaw's subagent system.

Usage:
  python3 orchestrator.py dispatch --task "Build feature X" --agent sonnet --workspace /path
  python3 orchestrator.py status
  python3 orchestrator.py list
  python3 orchestrator.py merge --task-id <id>
  python3 orchestrator.py cancel --task-id <id>
"""

import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE_DIR", "/data/workspace")
STATE_DIR = Path(WORKSPACE) / ".orchestrator"
TASKS_FILE = STATE_DIR / "tasks.json"
BLACKBOARD_FILE = STATE_DIR / "blackboard.json"


def ensure_dirs():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]")
    if not BLACKBOARD_FILE.exists():
        BLACKBOARD_FILE.write_text("{}")


def load_tasks():
    ensure_dirs()
    return json.loads(TASKS_FILE.read_text())


def save_tasks(tasks):
    ensure_dirs()
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))


def load_blackboard():
    ensure_dirs()
    return json.loads(BLACKBOARD_FILE.read_text())


def save_blackboard(bb):
    ensure_dirs()
    BLACKBOARD_FILE.write_text(json.dumps(bb, indent=2))


MODEL_MAP = {
    "opus": "anthropic/claude-opus-4-6",
    "sonnet": "anthropic/claude-sonnet-4-5",
    "deepseek": "deepseek/deepseek-chat",
    "codex": "openai/gpt-5.3-codex-spark",
    "grok": "grok/grok-3",
}


def dispatch(args):
    tasks = load_tasks()
    task_id = str(uuid.uuid4())[:8]
    
    model = MODEL_MAP.get(args.agent, args.agent)
    workspace = args.workspace or WORKSPACE
    
    # Create isolated workspace if requested
    task_dir = None
    if args.isolate:
        task_dir = str(STATE_DIR / "workspaces" / task_id)
        os.makedirs(task_dir, exist_ok=True)
    
    task = {
        "id": task_id,
        "task": args.task,
        "model": model,
        "agent_alias": args.agent,
        "workspace": task_dir or workspace,
        "isolated": args.isolate,
        "status": "dispatched",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": None,
        "result": None,
        "branch": f"agent/{task_id}" if args.branch else None,
    }
    
    tasks.append(task)
    save_tasks(tasks)
    
    # Write to blackboard
    bb = load_blackboard()
    bb[task_id] = {
        "status": "dispatched",
        "task": args.task,
        "model": model,
        "updates": [],
    }
    save_blackboard(bb)
    
    print(json.dumps({
        "task_id": task_id,
        "model": model,
        "workspace": task_dir or workspace,
        "status": "dispatched",
        "message": f"Task dispatched. Use sessions_spawn with model={model} and this task description.",
    }, indent=2))


def status(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    
    active = [t for t in tasks if t["status"] in ("dispatched", "running")]
    done = [t for t in tasks if t["status"] in ("completed", "merged")]
    failed = [t for t in tasks if t["status"] == "failed"]
    
    print(f"📊 Orchestrator Status")
    print(f"   Active: {len(active)} | Done: {len(done)} | Failed: {len(failed)}")
    print()
    
    for t in tasks[-10:]:
        icon = {"dispatched": "📤", "running": "🔄", "completed": "✅", "merged": "🔀", "failed": "❌", "cancelled": "⛔"}.get(t["status"], "❓")
        print(f"  {icon} [{t['id']}] {t['task'][:60]}")
        print(f"     Model: {t['model']} | Status: {t['status']}")
        if t.get("branch"):
            print(f"     Branch: {t['branch']}")
        print()


def update_task(args):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == args.task_id:
            t["status"] = args.status
            if args.result:
                t["result"] = args.result
            if args.status in ("completed", "failed", "cancelled"):
                t["completed_at"] = datetime.now(timezone.utc).isoformat()
            save_tasks(tasks)
            
            # Update blackboard
            bb = load_blackboard()
            if t["id"] in bb:
                bb[t["id"]]["status"] = args.status
                bb[t["id"]]["updates"].append({
                    "time": datetime.now(timezone.utc).isoformat(),
                    "status": args.status,
                    "note": args.result or "",
                })
                save_blackboard(bb)
            
            print(f"✅ Task {args.task_id} → {args.status}")
            return
    print(f"❌ Task {args.task_id} not found")


def list_tasks(args):
    tasks = load_tasks()
    print(json.dumps(tasks[-20:], indent=2))


def blackboard(args):
    bb = load_blackboard()
    print(json.dumps(bb, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Orchestrator")
    sub = parser.add_subparsers(dest="command")
    
    d = sub.add_parser("dispatch")
    d.add_argument("--task", required=True)
    d.add_argument("--agent", default="sonnet", help="Model alias: opus, sonnet, deepseek, codex, grok")
    d.add_argument("--workspace", default=None)
    d.add_argument("--isolate", action="store_true", help="Create isolated workspace")
    d.add_argument("--branch", action="store_true", help="Create git branch for task")
    
    s = sub.add_parser("status")
    
    u = sub.add_parser("update")
    u.add_argument("--task-id", required=True)
    u.add_argument("--status", required=True, choices=["running", "completed", "failed", "cancelled", "merged"])
    u.add_argument("--result", default=None)
    
    sub.add_parser("list")
    sub.add_parser("blackboard")
    
    args = parser.parse_args()
    
    if args.command == "dispatch":
        dispatch(args)
    elif args.command == "status":
        status(args)
    elif args.command == "update":
        update_task(args)
    elif args.command == "list":
        list_tasks(args)
    elif args.command == "blackboard":
        blackboard(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
