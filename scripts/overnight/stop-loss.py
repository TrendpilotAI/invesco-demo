#!/usr/bin/env python3
"""
5. Stop-Loss Rules
Determines when to abandon a repo and move on during overnight batch work.
Tracks time spent, coverage gains, and blockers per repo.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

STATE_FILE = "/data/workspace/scripts/overnight/state/stop-loss-state.json"
os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

# Stop-loss thresholds
MAX_MINUTES_PER_REPO = 45          # Max time on a single repo
MIN_COVERAGE_GAIN_PER_15MIN = 1.0  # Must gain at least 1% per 15 min window
MAX_STALL_WINDOWS = 2              # After 2 stalled windows, stop
MAX_HARNESS_FAILURES = 3           # If test harness fails 3 times, stop


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"repos": {}}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def start_repo(repo_name, initial_coverage):
    """Start tracking a repo for stop-loss."""
    state = load_state()
    state["repos"][repo_name] = {
        "start_time": time.time(),
        "initial_coverage": initial_coverage,
        "checkpoints": [{"coverage": initial_coverage, "time": time.time()}],
        "harness_failures": 0,
        "stall_count": 0,
        "stopped": False,
        "stop_reason": None
    }
    save_state(state)
    print(f"⏱️ Started tracking {repo_name} at {initial_coverage}% coverage")


def checkpoint(repo_name, current_coverage):
    """Record a coverage checkpoint and check stop-loss conditions."""
    state = load_state()
    
    if repo_name not in state["repos"]:
        print(f"⚠️ {repo_name} not tracked. Call start_repo first.")
        return {"should_stop": False}
    
    repo = state["repos"][repo_name]
    now = time.time()
    elapsed_min = (now - repo["start_time"]) / 60
    
    repo["checkpoints"].append({"coverage": current_coverage, "time": now})
    
    # Check 1: Time limit
    if elapsed_min > MAX_MINUTES_PER_REPO:
        repo["stopped"] = True
        repo["stop_reason"] = f"Time limit exceeded ({elapsed_min:.0f}m > {MAX_MINUTES_PER_REPO}m)"
        save_state(state)
        return _stop_result(repo_name, repo)
    
    # Check 2: Coverage stall (check last 15min window)
    recent = [cp for cp in repo["checkpoints"] if now - cp["time"] < 900]  # last 15min
    if len(recent) >= 2:
        window_gain = recent[-1]["coverage"] - recent[0]["coverage"]
        if window_gain < MIN_COVERAGE_GAIN_PER_15MIN:
            repo["stall_count"] = repo.get("stall_count", 0) + 1
            if repo["stall_count"] >= MAX_STALL_WINDOWS:
                repo["stopped"] = True
                repo["stop_reason"] = f"Coverage stalled ({repo['stall_count']} windows with <{MIN_COVERAGE_GAIN_PER_15MIN}% gain)"
                save_state(state)
                return _stop_result(repo_name, repo)
    
    # Check 3: Harness failures
    if repo.get("harness_failures", 0) >= MAX_HARNESS_FAILURES:
        repo["stopped"] = True
        repo["stop_reason"] = f"Test harness broken ({repo['harness_failures']} failures)"
        save_state(state)
        return _stop_result(repo_name, repo)
    
    total_gain = current_coverage - repo["initial_coverage"]
    save_state(state)
    print(f"📊 {repo_name}: {current_coverage}% (+{total_gain:.1f}%) — {elapsed_min:.0f}m elapsed — continue ✅")
    return {"should_stop": False, "elapsed_min": elapsed_min, "total_gain": total_gain}


def record_harness_failure(repo_name):
    """Record a test harness failure (broken fixture, missing dep, etc)."""
    state = load_state()
    if repo_name in state["repos"]:
        state["repos"][repo_name]["harness_failures"] = state["repos"][repo_name].get("harness_failures", 0) + 1
        save_state(state)
        failures = state["repos"][repo_name]["harness_failures"]
        print(f"⚠️ {repo_name}: harness failure #{failures}/{MAX_HARNESS_FAILURES}")


def _stop_result(repo_name, repo):
    total_gain = repo["checkpoints"][-1]["coverage"] - repo["initial_coverage"]
    elapsed = (time.time() - repo["start_time"]) / 60
    print(f"🛑 STOP-LOSS: {repo_name}")
    print(f"   Reason: {repo['stop_reason']}")
    print(f"   Coverage: {repo['initial_coverage']}% → {repo['checkpoints'][-1]['coverage']}% (+{total_gain:.1f}%)")
    print(f"   Time spent: {elapsed:.0f}m")
    return {
        "should_stop": True,
        "reason": repo["stop_reason"],
        "total_gain": total_gain,
        "elapsed_min": elapsed
    }


def show_status():
    """Show current stop-loss state for all repos."""
    state = load_state()
    if not state["repos"]:
        print("No repos being tracked.")
        return
    
    for name, repo in state["repos"].items():
        elapsed = (time.time() - repo["start_time"]) / 60
        gain = repo["checkpoints"][-1]["coverage"] - repo["initial_coverage"] if repo["checkpoints"] else 0
        status = f"🛑 STOPPED ({repo['stop_reason']})" if repo.get("stopped") else "🟢 Active"
        print(f"  {name}: {repo['initial_coverage']}% → {repo['checkpoints'][-1]['coverage']}% (+{gain:.1f}%) | {elapsed:.0f}m | {status}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} start <repo> <initial_coverage>")
        print(f"  {sys.argv[0]} check <repo> <current_coverage>")
        print(f"  {sys.argv[0]} harness-fail <repo>")
        print(f"  {sys.argv[0]} status")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "start" and len(sys.argv) >= 4:
        start_repo(sys.argv[2], float(sys.argv[3]))
    elif cmd == "check" and len(sys.argv) >= 4:
        result = checkpoint(sys.argv[2], float(sys.argv[3]))
        if result.get("should_stop"):
            sys.exit(1)  # Non-zero exit = agent should move on
    elif cmd == "harness-fail" and len(sys.argv) >= 3:
        record_harness_failure(sys.argv[2])
    elif cmd == "status":
        show_status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
