#!/usr/bin/env python3
"""Log agent swarm results to a JSON file for Convex import tomorrow."""
import json, sys, os, datetime

LOG_FILE = "/data/workspace/overnight-results-2026-03-11.json"

def log_result(agent_name, status, tasks_completed, tasks_total, details="", files_changed=0, tests_passed=0, tests_failed=0):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "agent": agent_name,
        "status": status,  # "success", "partial", "failed"
        "tasks_completed": tasks_completed,
        "tasks_total": tasks_total,
        "details": details,
        "files_changed": files_changed,
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "wave": os.environ.get("WAVE", "unknown")
    }
    
    results = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            results = json.load(f)
    
    results.append(entry)
    
    with open(LOG_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Logged: {agent_name} — {status} ({tasks_completed}/{tasks_total})")

if __name__ == "__main__":
    if len(sys.argv) >= 5:
        log_result(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]),
                   sys.argv[5] if len(sys.argv) > 5 else "")
    else:
        print("Usage: log-agent-result.py <agent_name> <status> <tasks_completed> <tasks_total> [details]")
