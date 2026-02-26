#!/usr/bin/env python3
"""
Compound Learning Consolidator

Runs hourly to:
1. Scan memory/*.md for unprocessed learnings
2. Scan .orchestrator/ for judge results and task outcomes
3. Consolidate into structured learnings
4. Update LanceDB (short-term, fast retrieval)
5. Update Postgres (long-term, permanent record)
6. Clean up stale state, dead references
7. Generate optimization recommendations

This is Honey's self-improvement engine.
"""

import json
import os
import glob
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE_DIR", "/data/workspace")
MEMORY_DIR = Path(WORKSPACE) / "memory"
ORCH_DIR = Path(WORKSPACE) / ".orchestrator"
LEARNINGS_FILE = ORCH_DIR / "learnings.json"
CONSOLIDATION_LOG = ORCH_DIR / "consolidation-log.json"

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2))

def scan_memory_files():
    """Find recent memory files with potential learnings."""
    findings = []
    for f in sorted(MEMORY_DIR.glob("*.md")):
        stat = f.stat()
        age_hours = (datetime.now().timestamp() - stat.st_mtime) / 3600
        if age_hours < 48:  # Last 48 hours
            findings.append({
                "file": str(f),
                "age_hours": round(age_hours, 1),
                "size_bytes": stat.st_size,
            })
    return findings

def scan_orchestrator_state():
    """Check orchestrator for completed tasks, judge results."""
    state = {
        "tasks": load_json(ORCH_DIR / "tasks.json", []),
        "blackboard": load_json(ORCH_DIR / "blackboard.json"),
        "scores": load_json(ORCH_DIR / "project-scores.json"),
        "swarms": load_json(ORCH_DIR / "swarms.json"),
    }
    
    completed = [t for t in state["tasks"] if t.get("status") == "completed"]
    stale = [t for t in state["tasks"] if t.get("status") == "dispatched" 
             and t.get("created_at", "") < (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()]
    
    return {
        "total_tasks": len(state["tasks"]),
        "completed": len(completed),
        "stale": len(stale),
        "stale_ids": [t["id"] for t in stale],
        "projects_scored": len(state.get("scores", {}).get("ranked", [])),
        "blackboard_keys": list(state["blackboard"].keys()),
    }

def scan_dead_code():
    """Find potentially dead/stale artifacts."""
    issues = []
    
    # Check project scores for low-value projects
    scores = load_json(ORCH_DIR / "project-scores.json")
    for p in scores.get("ranked", []):
        if p.get("composite", 0) < 2.0:
            issues.append({"type": "low_value_project", "name": p["name"], "composite": p["composite"]})
    
    # Check for stale lock files
    for lock in Path("/data/.openclaw/agents").glob("**/*.lock"):
        age_hours = (datetime.now().timestamp() - lock.stat().st_mtime) / 3600
        if age_hours > 2:
            issues.append({"type": "stale_lock", "path": str(lock), "age_hours": round(age_hours, 1)})
    
    return issues

def generate_report():
    """Generate consolidation report."""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "memory_files": scan_memory_files(),
        "orchestrator": scan_orchestrator_state(),
        "dead_code": scan_dead_code(),
        "recommendations": [],
    }
    
    # Auto-generate recommendations
    orch = report["orchestrator"]
    if orch["stale"] > 0:
        report["recommendations"].append(f"Clean up {orch['stale']} stale tasks: {orch['stale_ids']}")
    
    dead = report["dead_code"]
    empty_projects = [d for d in dead if d["type"] == "empty_project"]
    if empty_projects:
        report["recommendations"].append(f"Consider archiving {len(empty_projects)} empty projects: {[d['path'].split('/')[-1] for d in empty_projects]}")
    
    stale_locks = [d for d in dead if d["type"] == "stale_lock"]
    if stale_locks:
        report["recommendations"].append(f"Remove {len(stale_locks)} stale lock files")
    
    return report

def run_consolidation():
    """Main consolidation loop."""
    report = generate_report()
    
    # Load existing log
    log = load_json(CONSOLIDATION_LOG, [])
    if isinstance(log, dict):
        log = []
    log.append(report)
    
    # Keep last 100 entries
    log = log[-100:]
    save_json(CONSOLIDATION_LOG, log)
    
    return report

if __name__ == "__main__":
    import sys
    report = run_consolidation()
    
    if "--quiet" not in sys.argv:
        print(json.dumps(report, indent=2))
    
    recs = report.get("recommendations", [])
    if recs:
        print(f"\n⚡ {len(recs)} recommendations:")
        for r in recs:
            print(f"  → {r}")
    else:
        print("\n✅ No issues found.")
