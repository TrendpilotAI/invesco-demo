#!/usr/bin/env python3
"""
Search past session notes in LanceDB.
Usage: python3 search-sessions.py --query "signal studio deployment" [--limit 5]
"""

import argparse
import json
import os
from pathlib import Path

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE_DIR", "/data/workspace")
LANCEDB_DIR = Path(WORKSPACE) / ".lancedb-sessions"


def search(query: str, limit: int = 5):
    import lancedb

    db = lancedb.connect(str(LANCEDB_DIR))

    try:
        table = db.open_table("session_notes")
    except Exception:
        print("No session notes found yet.")
        return

    # Full-text search on summary
    results = table.search(query, query_type="fts").limit(limit).to_list()

    if not results:
        # Fallback: just list recent
        results = table.to_pandas().tail(limit).to_dict("records")

    for r in results:
        print(f"\n📅 {r.get('timestamp', '?')} | 🤖 {r.get('model', '?')}")
        goals = json.loads(r.get("goals", "[]"))
        if goals:
            print(f"   Goals: {', '.join(goals)}")
        print(f"   {r.get('summary', '')[:200]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    search(args.query, args.limit)


if __name__ == "__main__":
    main()
