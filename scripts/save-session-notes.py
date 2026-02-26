#!/usr/bin/env python3
"""
Save session notes to both Markdown files and LanceDB.
Usage: python3 save-session-notes.py --summary "..." --goals "goal1,goal2" --model "anthropic/claude-sonnet-4-5" [--tags "tag1,tag2"]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE_DIR", "/data/workspace")
MEMORY_DIR = Path(WORKSPACE) / "memory"
LANCEDB_DIR = Path(WORKSPACE) / ".lancedb-sessions"
STATE_FILE = MEMORY_DIR / "session-state.json"


def save_to_markdown(notes: dict):
    """Append session notes to today's memory file."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    md_path = MEMORY_DIR / f"{today}.md"

    entry = f"\n\n## Session — {notes['timestamp']}\n"
    entry += f"**Model:** {notes['model']}\n"
    if notes.get("goals"):
        entry += f"**Goals:** {', '.join(notes['goals'])}\n"
    if notes.get("tags"):
        entry += f"**Tags:** {', '.join(notes['tags'])}\n"
    entry += f"\n{notes['summary']}\n"

    if md_path.exists():
        with open(md_path, "a") as f:
            f.write(entry)
    else:
        header = f"# Memory — {today}\n"
        with open(md_path, "w") as f:
            f.write(header + entry)

    print(f"✅ Saved to {md_path}")


def save_to_lancedb(notes: dict):
    """Save session notes to LanceDB for vector search."""
    try:
        import lancedb
        import pyarrow as pa

        db = lancedb.connect(str(LANCEDB_DIR))

        # Create record
        record = {
            "id": notes["timestamp"].replace(":", "-").replace(" ", "_"),
            "timestamp": notes["timestamp"],
            "model": notes["model"],
            "goals": json.dumps(notes.get("goals", [])),
            "tags": json.dumps(notes.get("tags", [])),
            "summary": notes["summary"],
        }

        table_name = "session_notes"

        try:
            table = db.open_table(table_name)
            table.add([record])
        except Exception:
            # Table doesn't exist, create it
            schema = pa.schema([
                pa.field("id", pa.string()),
                pa.field("timestamp", pa.string()),
                pa.field("model", pa.string()),
                pa.field("goals", pa.string()),
                pa.field("tags", pa.string()),
                pa.field("summary", pa.string()),
            ])
            db.create_table(table_name, [record], schema=schema)

        print(f"✅ Saved to LanceDB ({LANCEDB_DIR})")

    except Exception as e:
        print(f"⚠️ LanceDB save failed: {e}", file=sys.stderr)


def update_state(notes: dict):
    """Update session state with last model used."""
    state = {}
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            state = json.load(f)

    state["lastModel"] = notes["model"]
    state["lastSessionGoals"] = notes.get("goals", [])
    state["lastSessionEnd"] = notes["timestamp"]

    # Keep last 20 sessions in history
    history = state.get("sessionHistory", [])
    history.append({
        "timestamp": notes["timestamp"],
        "model": notes["model"],
        "goals": notes.get("goals", []),
        "summary": notes["summary"][:200],
    })
    state["sessionHistory"] = history[-20:]

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print(f"✅ Updated session state (lastModel: {notes['model']})")


def main():
    parser = argparse.ArgumentParser(description="Save session notes")
    parser.add_argument("--summary", required=True, help="Session summary")
    parser.add_argument("--goals", default="", help="Comma-separated goals")
    parser.add_argument("--model", required=True, help="Model used")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    args = parser.parse_args()

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    notes = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "model": args.model,
        "goals": [g.strip() for g in args.goals.split(",") if g.strip()],
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
        "summary": args.summary,
    }

    save_to_markdown(notes)
    save_to_lancedb(notes)
    update_state(notes)


if __name__ == "__main__":
    main()
