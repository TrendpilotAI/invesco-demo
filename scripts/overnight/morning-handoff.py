#!/usr/bin/env python3
"""
6. Morning Handoff Document Generator
Generates structured handoff artifacts per repo after overnight work.
Each repo gets: progress notes, next actions, risks, and recommended agent/model.

9. Per-Repo Recommendations Section
Generates what should be done next, deferred, dangerous, and highest leverage.

10. Results → Ranked Execution Queue Converter
Converts overnight results into a prioritized execution queue for the morning.
"""

import json
import os
import sys
from datetime import datetime, timezone

HANDOFF_DIR = "/data/workspace/scripts/overnight/handoffs"
STATE_DIR = "/data/workspace/scripts/overnight/state"
SCOREBOARD_FILE = f"{STATE_DIR}/coverage-scoreboard.json"
STOPLOSS_FILE = f"{STATE_DIR}/stop-loss-state.json"
FAILURE_FILE = f"{STATE_DIR}/failure-state.json"
PRIORITY_FILE = "/data/workspace/scripts/overnight/module-priority.json"

os.makedirs(HANDOFF_DIR, exist_ok=True)


def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def generate_repo_handoff(repo_name, summary, next_actions=None, risks=None,
                          recommended_model=None, deferred=None, dangerous=None,
                          highest_leverage=None, coverage_before=None, coverage_after=None):
    """Generate a handoff document for a single repo."""
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"{HANDOFF_DIR}/{date}-{repo_name}.md"
    
    doc = f"""# Overnight Handoff: {repo_name}
_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_

## Summary
{summary}

## Coverage
- Before: {coverage_before or 'N/A'}%
- After: {coverage_after or 'N/A'}%
- Delta: {f'+{coverage_after - coverage_before:.1f}%' if coverage_before and coverage_after else 'N/A'}

## Next Actions
{_format_list(next_actions or ['No specific next actions identified'])}

## Risks
{_format_list(risks or ['None identified'])}

## Recommendations

### What should be done next
{_format_list(next_actions or ['Continue coverage work on critical modules'])}

### What should be deferred
{_format_list(deferred or ['Nothing flagged for deferral'])}

### What's dangerous
{_format_list(dangerous or ['Nothing flagged as dangerous'])}

### Highest leverage
{_format_list(highest_leverage or ['Not assessed'])}

## Recommended Agent/Model for Continuation
- **Model:** {recommended_model or 'anthropic/claude-sonnet-4-6'}
- **Why:** {'Heavy coverage + architecture work' if not recommended_model else 'Based on task complexity'}

---
"""
    with open(filename, "w") as f:
        f.write(doc)
    print(f"📋 Handoff written: {filename}")
    return filename


def _format_list(items):
    return "\n".join(f"- {item}" for item in items)


def generate_morning_summary():
    """Generate the consolidated morning summary from all overnight data."""
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Gather all data
    scoreboard = load_json(SCOREBOARD_FILE)
    stoploss = load_json(STOPLOSS_FILE)
    failures = load_json(FAILURE_FILE)
    priorities = load_json(PRIORITY_FILE)
    
    # Collect handoff files from today
    handoff_files = [f for f in os.listdir(HANDOFF_DIR) if f.startswith(date)] if os.path.exists(HANDOFF_DIR) else []
    
    summary = f"""# 🌅 Morning Handoff — {date}
_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_

## Overnight Batch Results

### Coverage Scoreboard
"""
    
    if scoreboard.get("repos"):
        summary += "| Repo | Start | Current | Delta | Status |\n"
        summary += "|------|-------|---------|-------|--------|\n"
        for name, data in sorted(scoreboard["repos"].items(), key=lambda x: x[1].get("delta", 0), reverse=True):
            start = data.get("starting_coverage", 0)
            current = data.get("current_coverage", 0)
            delta = data.get("delta", 0)
            status = "🟢" if delta > 5 else "🟡" if delta > 0 else "🔴" if delta < 0 else "⚪"
            summary += f"| {name} | {start:.1f}% | {current:.1f}% | {delta:+.1f}% | {status} |\n"
    else:
        summary += "_No coverage data recorded._\n"
    
    # Stop-loss events
    summary += "\n### Stop-Loss Events\n"
    stopped = {n: r for n, r in stoploss.get("repos", {}).items() if r.get("stopped")}
    if stopped:
        for name, data in stopped.items():
            summary += f"- 🛑 **{name}**: {data.get('stop_reason', 'unknown')}\n"
    else:
        summary += "_No repos hit stop-loss._\n"
    
    # Failures
    summary += "\n### Failure Summary\n"
    total_failures = failures.get("total_failures", 0)
    total_successes = failures.get("total_successes", 0)
    if total_failures > 0:
        summary += f"- Total failures: {total_failures}\n"
        summary += f"- Total successes: {total_successes}\n"
        last = failures.get("last_failure")
        if last:
            summary += f"- Last failure: {last.get('repo', '?')} — {last.get('error', '?')}\n"
    else:
        summary += "_No failures recorded._\n"
    
    # Per-repo handoffs
    summary += f"\n### Detailed Handoffs\n"
    if handoff_files:
        for hf in sorted(handoff_files):
            summary += f"- [{hf}]({HANDOFF_DIR}/{hf})\n"
    else:
        summary += "_No per-repo handoffs generated._\n"
    
    # Ranked execution queue (item 10)
    summary += "\n## 🎯 Ranked Execution Queue\n"
    summary += "_Priority order for today's work:_\n\n"
    
    queue = build_execution_queue(scoreboard, stoploss, priorities)
    for i, item in enumerate(queue, 1):
        summary += f"### {i}. {item['repo']} — {item['action']}\n"
        summary += f"- **Priority:** {item['priority']}\n"
        summary += f"- **Category:** {item['category']}\n"
        summary += f"- **Recommended model:** {item['model']}\n"
        if item.get('notes'):
            summary += f"- **Notes:** {item['notes']}\n"
        summary += "\n"
    
    output_file = f"{HANDOFF_DIR}/{date}-MORNING-SUMMARY.md"
    with open(output_file, "w") as f:
        f.write(summary)
    
    print(f"🌅 Morning summary written: {output_file}")
    print(summary)
    return output_file


def build_execution_queue(scoreboard, stoploss, priorities):
    """10. Convert overnight results into a ranked execution queue."""
    queue = []
    
    sf_paths = priorities.get("salesforce_tagged_paths", {})
    critical_modules = priorities.get("priority_tiers", {}).get("critical", {}).get("modules", [])
    
    # Repos that hit stop-loss → investigate architecture issues
    for name, data in stoploss.get("repos", {}).items():
        if data.get("stopped"):
            queue.append({
                "repo": name,
                "action": f"Investigate stop-loss: {data.get('stop_reason', 'unknown')}",
                "priority": "P1",
                "category": "🔍 Investigation",
                "model": "anthropic/claude-opus-4-6",
                "notes": "Overnight agent couldn't make progress — may need architecture work"
            })
    
    # Repos with coverage regressions
    for name, data in scoreboard.get("repos", {}).items():
        if data.get("delta", 0) < 0:
            queue.append({
                "repo": name,
                "action": f"Fix coverage regression ({data['delta']:+.1f}%)",
                "priority": "P0",
                "category": "🔴 Regression",
                "model": "anthropic/claude-sonnet-4-6",
                "notes": "Coverage went backwards — likely broken tests"
            })
    
    # Repos below critical coverage threshold
    for name, data in scoreboard.get("repos", {}).items():
        current = data.get("current_coverage", 0)
        # Check if repo has critical modules
        has_critical = any(name in m.get("repos", []) for m in critical_modules)
        if has_critical and current < 90:
            queue.append({
                "repo": name,
                "action": f"Raise critical module coverage ({current:.1f}% → 90%)",
                "priority": "P0",
                "category": "🛡️ Security/Critical Coverage",
                "model": "anthropic/claude-sonnet-4-6",
                "notes": "Has critical modules (auth, tenant isolation, etc.) below threshold"
            })
    
    # Salesforce-facing repos → integration coverage
    sf_repos = set()
    for endpoint_data in sf_paths.values():
        if isinstance(endpoint_data, dict) and "repos" in endpoint_data:
            sf_repos.update(endpoint_data["repos"])
    
    for repo in sf_repos:
        queue.append({
            "repo": repo,
            "action": "Add Salesforce integration endpoint coverage",
            "priority": "P1",
            "category": "🔗 Salesforce Integration",
            "model": "anthropic/claude-sonnet-4-6",
            "notes": "Endpoints that the Apex/LWC wrapper will call"
        })
    
    # Sort by priority
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    queue.sort(key=lambda x: priority_order.get(x["priority"], 99))
    
    return queue


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} repo <name> --summary '...' [--next 'a1,a2'] [--risks 'r1,r2'] [--model 'x'] [--deferred 'd1,d2'] [--dangerous 'x'] [--leverage 'x'] [--before N] [--after N]")
        print(f"  {sys.argv[0]} morning    — Generate consolidated morning summary + execution queue")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "morning":
        generate_morning_summary()
    
    elif cmd == "repo":
        if len(sys.argv) < 3:
            print("Need repo name")
            sys.exit(1)
        
        repo_name = sys.argv[2]
        kwargs = {"repo_name": repo_name, "summary": "Overnight batch work completed"}
        
        i = 3
        while i < len(sys.argv):
            arg = sys.argv[i]
            val = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
            
            if arg == "--summary":
                kwargs["summary"] = val
            elif arg == "--next":
                kwargs["next_actions"] = val.split(",")
            elif arg == "--risks":
                kwargs["risks"] = val.split(",")
            elif arg == "--model":
                kwargs["recommended_model"] = val
            elif arg == "--deferred":
                kwargs["deferred"] = val.split(",")
            elif arg == "--dangerous":
                kwargs["dangerous"] = val.split(",")
            elif arg == "--leverage":
                kwargs["highest_leverage"] = val.split(",")
            elif arg == "--before":
                kwargs["coverage_before"] = float(val)
            elif arg == "--after":
                kwargs["coverage_after"] = float(val)
            i += 2
        
        generate_repo_handoff(**kwargs)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
