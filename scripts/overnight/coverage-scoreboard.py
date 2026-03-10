#!/usr/bin/env python3
"""
3. Coverage Scoreboard
Tracks test coverage across repos with starting/current/delta metrics.
Persists to /data/workspace/scripts/overnight/state/coverage-scoreboard.json
"""

import json
import os
import sys
from datetime import datetime, timezone

SCOREBOARD_FILE = "/data/workspace/scripts/overnight/state/coverage-scoreboard.json"
os.makedirs(os.path.dirname(SCOREBOARD_FILE), exist_ok=True)


def load_scoreboard():
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE) as f:
            return json.load(f)
    return {"repos": {}, "last_updated": None}


def save_scoreboard(data):
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_repo(repo_name, current_coverage, key_modules=None, blockers=None, framework=None):
    """Update coverage for a repo. First call sets the starting baseline."""
    sb = load_scoreboard()
    
    if repo_name not in sb["repos"]:
        sb["repos"][repo_name] = {
            "starting_coverage": current_coverage,
            "current_coverage": current_coverage,
            "delta": 0.0,
            "key_modules_covered": key_modules or [],
            "blockers": blockers or [],
            "framework": framework or "unknown",
            "history": [],
            "first_seen": datetime.now(timezone.utc).isoformat()
        }
    else:
        entry = sb["repos"][repo_name]
        old_coverage = entry["current_coverage"]
        entry["current_coverage"] = current_coverage
        entry["delta"] = round(current_coverage - entry["starting_coverage"], 2)
        if key_modules:
            entry["key_modules_covered"] = list(set(entry.get("key_modules_covered", []) + key_modules))
        if blockers:
            entry["blockers"] = blockers
        entry["history"].append({
            "coverage": current_coverage,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "change": round(current_coverage - old_coverage, 2)
        })
        # Keep last 100 history entries
        entry["history"] = entry["history"][-100:]
    
    save_scoreboard(sb)
    print(f"📊 {repo_name}: {current_coverage}% (Δ {sb['repos'][repo_name]['delta']:+.1f}%)")


def show_scoreboard():
    """Print the full scoreboard in a readable format."""
    sb = load_scoreboard()
    
    if not sb["repos"]:
        print("📊 Coverage Scoreboard: Empty (no repos tracked yet)")
        return
    
    print("=" * 80)
    print("📊 COVERAGE SCOREBOARD")
    print(f"   Last updated: {sb.get('last_updated', 'never')}")
    print("=" * 80)
    
    # Sort by delta descending (biggest gains first)
    sorted_repos = sorted(sb["repos"].items(), key=lambda x: x[1].get("delta", 0), reverse=True)
    
    print(f"\n{'Repo':<35} {'Start':>7} {'Current':>8} {'Delta':>7} {'Status'}")
    print("-" * 80)
    
    for name, data in sorted_repos:
        start = data.get("starting_coverage", 0)
        current = data.get("current_coverage", 0)
        delta = data.get("delta", 0)
        
        if delta > 5:
            status = "🟢 Great progress"
        elif delta > 0:
            status = "🟡 Moving"
        elif delta == 0:
            status = "⚪ No change"
        else:
            status = "🔴 Regression!"
        
        print(f"{name:<35} {start:>6.1f}% {current:>7.1f}% {delta:>+6.1f}% {status}")
    
    # Show blockers
    blocked = [(name, data["blockers"]) for name, data in sb["repos"].items() if data.get("blockers")]
    if blocked:
        print(f"\n⚠️ Blockers:")
        for name, blockers in blocked:
            for b in blockers:
                print(f"   • {name}: {b}")
    
    # Show key modules covered
    print(f"\n🎯 Key Modules Covered:")
    for name, data in sorted_repos:
        modules = data.get("key_modules_covered", [])
        if modules:
            print(f"   {name}: {', '.join(modules)}")


def export_markdown():
    """Export scoreboard as markdown for handoff docs."""
    sb = load_scoreboard()
    
    if not sb["repos"]:
        print("No repos tracked.")
        return
    
    sorted_repos = sorted(sb["repos"].items(), key=lambda x: x[1].get("delta", 0), reverse=True)
    
    print("## Coverage Scoreboard\n")
    print(f"_Updated: {sb.get('last_updated', 'unknown')}_\n")
    print("| Repo | Start | Current | Delta | Key Modules | Blockers |")
    print("|------|-------|---------|-------|-------------|----------|")
    
    for name, data in sorted_repos:
        start = data.get("starting_coverage", 0)
        current = data.get("current_coverage", 0)
        delta = data.get("delta", 0)
        modules = ", ".join(data.get("key_modules_covered", [])[:5]) or "—"
        blockers = ", ".join(data.get("blockers", [])[:3]) or "—"
        print(f"| {name} | {start:.1f}% | {current:.1f}% | {delta:+.1f}% | {modules} | {blockers} |")


def reset():
    """Reset the scoreboard."""
    save_scoreboard({"repos": {}, "last_updated": None})
    print("🔄 Scoreboard reset.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} update <repo> <coverage%> [--modules m1,m2] [--blockers b1,b2] [--framework pytest|jest]")
        print(f"  {sys.argv[0]} show")
        print(f"  {sys.argv[0]} markdown")
        print(f"  {sys.argv[0]} reset")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "show":
        show_scoreboard()
    elif cmd == "markdown":
        export_markdown()
    elif cmd == "reset":
        reset()
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Usage: update <repo> <coverage%> [--modules m1,m2] [--blockers b1,b2]")
            sys.exit(1)
        repo = sys.argv[2]
        coverage = float(sys.argv[3])
        
        modules = None
        blockers = None
        framework = None
        
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--modules" and i + 1 < len(sys.argv):
                modules = sys.argv[i + 1].split(",")
                i += 2
            elif sys.argv[i] == "--blockers" and i + 1 < len(sys.argv):
                blockers = sys.argv[i + 1].split(",")
                i += 2
            elif sys.argv[i] == "--framework" and i + 1 < len(sys.argv):
                framework = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        update_repo(repo, coverage, modules, blockers, framework)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
