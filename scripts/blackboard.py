"""
Blackboard v2 — Agent-to-Agent Shared Memory
=============================================
Agents read/write named keys with optional TTL and metadata.
Backed by Convex (real-time) with local JSON fallback.

Usage:
  # Write a value
  python3 blackboard.py write judge-results/invesco '{"score": 9.1, "todos": [...]}' --agent honey --project invesco-retention

  # Read a value
  python3 blackboard.py read judge-results/invesco

  # List all keys (optionally filtered)
  python3 blackboard.py list --prefix judge-results/

  # Post a message to another agent
  python3 blackboard.py post --to "j-backend" --from "honey" --message "P0: add integration tests to easy_button" --priority urgent

  # Read messages addressed to this agent
  python3 blackboard.py messages --for honey

  # Clear expired keys
  python3 blackboard.py gc
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
CONVEX_URL = os.environ.get("CONVEX_URL", "https://warmhearted-goldfish-440.convex.cloud")
STATE_DIR = Path(os.environ.get("WORKSPACE", "/data/workspace")) / ".agent-state"
BB_FILE = STATE_DIR / "blackboard.json"
MSG_FILE = STATE_DIR / "agent-messages.json"

# ── Local fallback storage ────────────────────────────────────────────────────
def _load(path: Path, default):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(default, indent=2))
    return json.loads(path.read_text())

def _save(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))

# ── Blackboard ops ────────────────────────────────────────────────────────────
def bb_write(key: str, value, agent: str = "honey", project: str = None, ttl_seconds: int = None):
    """Write a value to the blackboard."""
    bb = _load(BB_FILE, {})
    entry = {
        "value": value,
        "agent": agent,
        "project": project,
        "written_at": int(time.time()),
        "expires_at": int(time.time()) + ttl_seconds if ttl_seconds else None,
    }
    bb[key] = entry
    _save(BB_FILE, bb)
    print(json.dumps({"ok": True, "key": key, "agent": agent}))

def bb_read(key: str):
    """Read a value from the blackboard."""
    bb = _load(BB_FILE, {})
    if key not in bb:
        print(json.dumps({"error": f"Key '{key}' not found"}))
        return
    entry = bb[key]
    # Check TTL
    if entry.get("expires_at") and time.time() > entry["expires_at"]:
        print(json.dumps({"error": f"Key '{key}' has expired"}))
        return
    print(json.dumps(entry, indent=2))

def bb_list(prefix: str = None, project: str = None):
    """List all blackboard keys."""
    bb = _load(BB_FILE, {})
    now = time.time()
    results = []
    for key, entry in bb.items():
        if prefix and not key.startswith(prefix):
            continue
        if project and entry.get("project") != project:
            continue
        if entry.get("expires_at") and now > entry["expires_at"]:
            continue
        age = int(now - entry.get("written_at", now))
        results.append({
            "key": key,
            "agent": entry.get("agent"),
            "project": entry.get("project"),
            "age_seconds": age,
            "has_value": entry.get("value") is not None,
        })
    print(json.dumps(results, indent=2))

def bb_gc():
    """Remove expired keys."""
    bb = _load(BB_FILE, {})
    now = time.time()
    expired = [k for k, v in bb.items() if v.get("expires_at") and now > v["expires_at"]]
    for k in expired:
        del bb[k]
    _save(BB_FILE, bb)
    print(json.dumps({"removed": expired, "remaining": len(bb)}))

# ── Agent messaging ───────────────────────────────────────────────────────────
def post_message(to: str, from_agent: str, message: str, priority: str = "info", context: dict = None):
    """Post a message from one agent to another."""
    msgs = _load(MSG_FILE, [])
    msg = {
        "id": f"msg-{int(time.time() * 1000)}",
        "to": to,
        "from": from_agent,
        "message": message,
        "priority": priority,  # urgent / attention / info
        "context": context or {},
        "sent_at": int(time.time()),
        "read": False,
    }
    msgs.append(msg)
    # Keep last 500 messages
    if len(msgs) > 500:
        msgs = msgs[-500:]
    _save(MSG_FILE, msgs)
    print(json.dumps({"ok": True, "id": msg["id"]}))

def read_messages(for_agent: str, mark_read: bool = True):
    """Read messages addressed to an agent."""
    msgs = _load(MSG_FILE, [])
    unread = [m for m in msgs if m.get("to") == for_agent and not m.get("read")]
    if mark_read:
        for m in msgs:
            if m.get("to") == for_agent:
                m["read"] = True
        _save(MSG_FILE, msgs)
    print(json.dumps(unread, indent=2))
    return unread

def list_messages(for_agent: str = None, limit: int = 20):
    """List recent messages."""
    msgs = _load(MSG_FILE, [])
    if for_agent:
        msgs = [m for m in msgs if m.get("to") == for_agent]
    print(json.dumps(msgs[-limit:], indent=2))

# ── Shared context (for judge results, scores, etc.) ─────────────────────────
def share_judge_result(project: str, scores: dict, todos: list, agent: str = "honey"):
    """Write judge results to blackboard in standardized format."""
    key = f"judge/{project}"
    value = {
        "scores": scores,
        "todos": todos,
        "judged_at": int(time.time()),
    }
    bb_write(key, value, agent=agent, project=project, ttl_seconds=86400)  # 24h TTL

def get_judge_result(project: str):
    """Read judge results for a project."""
    bb_read(f"judge/{project}")

# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Blackboard v2 — Agent shared memory")
    sub = parser.add_subparsers(dest="cmd")

    # write
    w = sub.add_parser("write", help="Write a value")
    w.add_argument("key"); w.add_argument("value"); w.add_argument("--agent", default="honey")
    w.add_argument("--project"); w.add_argument("--ttl", type=int, help="TTL in seconds")

    # read
    r = sub.add_parser("read", help="Read a value")
    r.add_argument("key")

    # list
    l = sub.add_parser("list", help="List keys")
    l.add_argument("--prefix"); l.add_argument("--project")

    # gc
    sub.add_parser("gc", help="Remove expired keys")

    # post (agent→agent message)
    p = sub.add_parser("post", help="Send a message to an agent")
    p.add_argument("--to", required=True); p.add_argument("--from", dest="from_agent", default="honey")
    p.add_argument("--message", required=True); p.add_argument("--priority", default="info")

    # messages (read inbox)
    m = sub.add_parser("messages", help="Read messages")
    m.add_argument("--for", dest="for_agent", required=True)
    m.add_argument("--no-mark-read", action="store_true")
    m.add_argument("--all", action="store_true")

    args = parser.parse_args()

    if args.cmd == "write":
        try:
            val = json.loads(args.value)
        except json.JSONDecodeError:
            val = args.value
        bb_write(args.key, val, args.agent, args.project, args.ttl)
    elif args.cmd == "read":
        bb_read(args.key)
    elif args.cmd == "list":
        bb_list(getattr(args, "prefix", None), getattr(args, "project", None))
    elif args.cmd == "gc":
        bb_gc()
    elif args.cmd == "post":
        post_message(args.to, args.from_agent, args.message, args.priority)
    elif args.cmd == "messages":
        if getattr(args, "all", False):
            list_messages(args.for_agent)
        else:
            read_messages(args.for_agent, not args.no_mark_read)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
