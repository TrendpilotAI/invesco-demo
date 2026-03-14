#!/usr/bin/env python3
"""
Project Scorer — evaluates all repos and writes results to the orchestrator blackboard.
Run by judge agents or directly.

Scoring dimensions:
  - Revenue Potential (0-10): How close to generating money?
  - Strategic Value (0-10): How important to Nathan's businesses?
  - Completeness (0-10): How finished is the code?
  - Urgency (0-10): Time-sensitive deadlines?
  - Effort Remaining (0-10): How much work left? (10 = almost done, 1 = massive)

Categories:
  - CORE: ForwardLane/SignalHaus core business
  - PRODUCT: Standalone products that can generate revenue
  - INFRA: Infrastructure, tooling, internal ops
  - TEMPLATE: Starter templates, boilerplate
  - LEGACY: Old/deprecated, kept for reference
  - MARKETING: Websites, landing pages, content
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE_DIR", "/data/workspace")
STATE_DIR = Path(WORKSPACE) / ".orchestrator"
BLACKBOARD_FILE = STATE_DIR / "blackboard.json"
SCORES_FILE = STATE_DIR / "project-scores.json"

def load_blackboard():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if BLACKBOARD_FILE.exists():
        return json.loads(BLACKBOARD_FILE.read_text())
    return {}

def save_blackboard(bb):
    BLACKBOARD_FILE.write_text(json.dumps(bb, indent=2))

def save_scores(scores):
    SCORES_FILE.write_text(json.dumps(scores, indent=2))

def update_project_score(project_name, scores_dict):
    """Update a single project's score on the blackboard."""
    bb = load_blackboard()
    if "project_scores" not in bb:
        bb["project_scores"] = {}
    
    bb["project_scores"][project_name] = {
        **scores_dict,
        "scored_at": datetime.now(timezone.utc).isoformat(),
    }
    bb["last_scoring_run"] = datetime.now(timezone.utc).isoformat()
    save_blackboard(bb)
    return bb

def get_all_scores():
    bb = load_blackboard()
    return bb.get("project_scores", {})

def generate_summary():
    """Generate a ranked summary of all scored projects."""
    scores = get_all_scores()
    if not scores:
        return "No projects scored yet."
    
    # Calculate composite score
    ranked = []
    for name, data in scores.items():
        composite = (
            data.get("revenue_potential", 0) * 2 +
            data.get("strategic_value", 0) * 2 +
            data.get("completeness", 0) * 1.5 +
            data.get("urgency", 0) * 2.5 +
            data.get("effort_remaining", 0) * 1
        ) / 9  # weighted average
        ranked.append({
            "name": name,
            "category": data.get("category", "UNKNOWN"),
            "composite": round(composite, 1),
            "revenue_potential": data.get("revenue_potential", 0),
            "strategic_value": data.get("strategic_value", 0),
            "completeness": data.get("completeness", 0),
            "urgency": data.get("urgency", 0),
            "effort_remaining": data.get("effort_remaining", 0),
            "summary": data.get("summary", ""),
        })
    
    ranked.sort(key=lambda x: x["composite"], reverse=True)
    
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_projects": len(ranked),
        "by_category": {},
        "ranked": ranked,
        "top_5_priority": ranked[:5],
    }
    
    for p in ranked:
        cat = p["category"]
        if cat not in output["by_category"]:
            output["by_category"][cat] = []
        output["by_category"][cat].append(p["name"])
    
    save_scores(output)
    return output

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        result = generate_summary()
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "update":
        # Usage: score-projects.py update <name> <json_scores>
        if len(sys.argv) < 4:
            print("Error: Missing arguments for update command.")
            print("Usage: score-projects.py update <name> <json_scores>")
            sys.exit(1)
        name = sys.argv[2]
        scores = json.loads(sys.argv[3])
        update_project_score(name, scores)
        print(f"Updated {name}")
    else:
        print("Usage: score-projects.py [summary|update <name> <json>]")
