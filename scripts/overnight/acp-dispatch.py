#!/usr/bin/env python3
"""
8. ACP Dispatch for Heavy Repos
Generates the sessions_spawn configuration for overnight ACP work.
The heaviest repos get full ACP coding harness treatment.

Usage: python3 acp-dispatch.py generate <repo_name>
       python3 acp-dispatch.py list
"""

import json
import os
import sys
from datetime import datetime, timezone

# Repos best suited for ACP (full coding harness)
ACP_REPOS = {
    "forwardlane-backend": {
        "description": "Django backend with 150+ models, complex test infrastructure",
        "model": "anthropic/claude-sonnet-4-6",
        "task_template": """You are working on the ForwardLane Django backend.
Repository: /data/workspace/repos/forwardlane-backend

CRITICAL RULES:
1. Work ONLY on the overnight branch (never commit to main/master)
2. Run tests after every change
3. Focus on HIGH-VALUE coverage: auth, tenant isolation, API contracts, meeting prep
4. If test harness breaks 3 times, STOP and document the issue
5. Commit incrementally with descriptive messages prefixed with [overnight]

PRIORITY MODULES (from module-priority.json):
- CRITICAL: auth, tenant-isolation, meeting-prep, api-contracts, signal-validation, injection-security
- HIGH: easy-button, data-pipeline, salesforce-endpoints

SALESFORCE LENS: Tag any endpoint that will be called by the Apex/LWC wrapper:
- meeting_prep endpoints → MeetingPrepController.cls
- advisor/client endpoints → AdvisorDetailController.cls
- signal endpoints → SignalController.cls
- action endpoints → ActionController.cls

Your goal: Raise test coverage to {target}% focusing on critical modules first.
Current coverage: {current_coverage}%

After completing work:
1. Run full test suite and record final coverage
2. Write a summary to /data/workspace/scripts/overnight/handoffs/{date}-forwardlane-backend.md
3. Include: what was done, next actions, risks, recommendations
""",
        "timeout_seconds": 2700  # 45 min
    },
    "signal-builder-backend": {
        "description": "FastAPI signal builder with graph→SQL compiler, core IP",
        "model": "anthropic/claude-sonnet-4-6",
        "task_template": """You are working on the Signal Builder Backend (FastAPI).
Repository: /data/workspace/repos/signal-builder-backend

CRITICAL RULES:
1. Work ONLY on the overnight branch
2. Run tests after every change
3. Focus on: schema_builder, translators, analytical_db, signal validation
4. If test harness breaks 3 times, STOP and document
5. Commit incrementally with [overnight] prefix

PRIORITY: This repo contains the NL→SQL engine — the company's core IP.
SQL injection prevention in translators is the #1 coverage priority.

SALESFORCE: Signal CRUD and validation endpoints feed the signalExplorer.lwc component.

Goal: Raise coverage to {target}% on critical paths.
Current: {current_coverage}%
""",
        "timeout_seconds": 2700
    },
    "signal-studio": {
        "description": "Next.js 15 platform frontend + API routes",
        "model": "anthropic/claude-sonnet-4-6",
        "task_template": """You are working on Signal Studio (Next.js 15).
Repository: /data/workspace/repos/signal-studio

CRITICAL RULES:
1. Work ONLY on the overnight branch
2. Run tests after every change (vitest or jest)
3. Focus on: API routes (auth, signals, meeting-prep), middleware, tenant isolation
4. If test harness breaks 3 times, STOP and document
5. Commit incrementally with [overnight] prefix

SALESFORCE: The BFF proxy routes are what Salesforce Named Credentials will call.
Ensure all proxy endpoints have proper auth validation and error handling tests.

Goal: Raise coverage to {target}% on API routes and middleware.
Current: {current_coverage}%
""",
        "timeout_seconds": 2700
    }
}

# Non-ACP repos get lighter treatment
STANDARD_REPOS = {
    "signal-studio-auth": "anthropic/claude-sonnet-4-6",
    "forwardlane_advisor": "anthropic/claude-sonnet-4-6",
    "invesco-demo": "deepseek/deepseek-chat",
}


def generate_task(repo_name, target_coverage=80, current_coverage=0):
    """Generate the ACP task string for a repo."""
    if repo_name not in ACP_REPOS:
        print(f"⚠️ {repo_name} is not an ACP-preferred repo. Use standard agent instead.")
        return None
    
    config = ACP_REPOS[repo_name]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    task = config["task_template"].format(
        target=target_coverage,
        current_coverage=current_coverage,
        date=date
    )
    
    result = {
        "repo": repo_name,
        "runtime": "acp",
        "model": config["model"],
        "task": task,
        "timeout_seconds": config["timeout_seconds"],
        "mode": "run",
        "label": f"overnight-{repo_name}-{date}"
    }
    
    print(json.dumps(result, indent=2))
    return result


def list_repos():
    """List all configured repos with their dispatch type."""
    print("🔬 ACP-Preferred Repos (full coding harness):")
    for name, config in ACP_REPOS.items():
        print(f"  • {name}: {config['description']} ({config['model']})")
    
    print("\n📦 Standard Repos (lighter agent):")
    for name, model in STANDARD_REPOS.items():
        print(f"  • {name}: {model}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} generate <repo_name> [target_coverage] [current_coverage]")
        print(f"  {sys.argv[0]} list")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "list":
        list_repos()
    elif cmd == "generate":
        repo = sys.argv[2] if len(sys.argv) > 2 else ""
        target = int(sys.argv[3]) if len(sys.argv) > 3 else 80
        current = float(sys.argv[4]) if len(sys.argv) > 4 else 0
        generate_task(repo, target, current)
    else:
        print(f"Unknown command: {cmd}")
