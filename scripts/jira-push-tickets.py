#!/usr/bin/env python3
"""Push Signal Studio tickets to Jira SS project."""
import json
import requests
import time
import os

JIRA_URL = "https://forwardlane.atlassian.net"
JIRA_AUTH = (os.environ.get("JIRA_EMAIL", ""), os.environ.get("JIRA_API_TOKEN", ""))
PROJECT = "SS"

# Issue type IDs
EPIC = "10000"
STORY = "10001"
TASK = "10002"
BUG = "10004"

# Priority IDs
BLOCKER = "10000"
HIGHEST = "1"
HIGH = "2"
MEDIUM = "3"
LOW = "4"

def create_issue(summary, description, issue_type=TASK, priority=MEDIUM, labels=None, epic_key=None):
    """Create a Jira issue."""
    fields = {
        "project": {"key": PROJECT},
        "summary": summary,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
        },
        "issuetype": {"id": issue_type},
        "priority": {"id": priority},
    }
    if labels:
        fields["labels"] = labels
    if epic_key:
        fields["parent"] = {"key": epic_key}

    resp = requests.post(
        f"{JIRA_URL}/rest/api/3/issue",
        auth=JIRA_AUTH,
        json={"fields": fields},
        headers={"Content-Type": "application/json"}
    )
    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"  ✅ {data['key']}: {summary}")
        return data["key"]
    else:
        print(f"  ❌ FAILED ({resp.status_code}): {summary}")
        print(f"     {resp.text[:200]}")
        return None


def main():
    created = []

    # ═══════════════════════════════════════════════════════════════
    # EPIC 1: Security — P0 Critical Issues
    # ═══════════════════════════════════════════════════════════════
    print("\n🔴 Creating Epic: Security Critical Issues")
    epic_security = create_issue(
        "SECURITY: Critical vulnerabilities across Signal Studio repos",
        "Three P0 security issues found during March 2026 judge swarm audit. All require immediate attention.",
        issue_type=EPIC, priority=BLOCKER, labels=["security", "p0"]
    )

    if epic_security:
        create_issue(
            "BUG: NEXT_PUBLIC_SKIP_AUTH=true in signal-studio .env.production",
            "Signal Studio has NEXT_PUBLIC_SKIP_AUTH=true in .env.production which DISABLES ALL AUTH IN PRODUCTION. "
            "Any user can access any endpoint without authentication. Remove this flag immediately and verify "
            "all protected routes require valid session tokens.",
            issue_type=BUG, priority=BLOCKER, labels=["security", "signal-studio", "p0"],
            epic_key=epic_security
        )
        create_issue(
            "BUG: SQL injection risk in signal-studio-data-provider",
            "cortex_complete() and cortex_embed() in signal-studio-data-provider pass model name directly into SQL "
            "without parameterization or allowlist validation. An attacker could inject arbitrary SQL via the model "
            "parameter. Fix: add model name allowlist validation before SQL execution.",
            issue_type=BUG, priority=BLOCKER, labels=["security", "sql-injection", "data-provider", "p0"],
            epic_key=epic_security
        )
        create_issue(
            "BUG: signal-builder-frontend uses REACT_APP_* env vars after Vite migration",
            "The Bitbucket pipeline for signal-builder-frontend still uses REACT_APP_* environment variables "
            "but the project was migrated to Vite which uses VITE_* prefixes. Deployed environments likely have "
            "broken/missing configuration. Update pipeline and .env files to use VITE_ prefix.",
            issue_type=BUG, priority=HIGH, labels=["devops", "signal-builder", "broken-deploy"],
            epic_key=epic_security
        )

    # ═══════════════════════════════════════════════════════════════
    # EPIC 2: Invesco Demo Preparation
    # ═══════════════════════════════════════════════════════════════
    print("\n🎯 Creating Epic: Invesco Demo Preparation")
    epic_invesco = create_issue(
        "Invesco Demo: Salesforce-embedded meeting prep + easy buttons",
        "Craig Lieb meeting (Feb 17) requirements: Salesforce-embedded easy buttons, meeting prep briefs, "
        "mobile-first. Brian Kiley is key user. 2-3 week demo window. NOT chat interfaces or complex dashboards.",
        issue_type=EPIC, priority=HIGHEST, labels=["invesco", "demo", "salesforce"]
    )

    if epic_invesco:
        create_issue(
            "Build Salesforce Apex wrapper for meeting prep endpoints",
            "Create MeetingPrepController.cls + meetingPrepBrief.lwc that calls ForwardLane meeting_prep API. "
            "Uses Named Credential for auth. Must work in Salesforce mobile app.",
            issue_type=STORY, priority=HIGHEST, labels=["invesco", "salesforce", "apex"],
            epic_key=epic_invesco
        )
        create_issue(
            "Build Salesforce easy button LWC component",
            "Create ActionController.cls + easyButton.lwc for one-click advisor actions. "
            "Craig Lieb's primary UX requirement — simple buttons, not complex dashboards.",
            issue_type=STORY, priority=HIGHEST, labels=["invesco", "salesforce", "lwc"],
            epic_key=epic_invesco
        )
        create_issue(
            "Build Salesforce advisor dashboard LWC",
            "Create AdvisorDetailController.cls + advisorDashboard.lwc showing advisor details, "
            "client holdings, and signal recommendations from ForwardLane API.",
            issue_type=STORY, priority=HIGH, labels=["invesco", "salesforce", "lwc"],
            epic_key=epic_invesco
        )
        create_issue(
            "Build Salesforce signal explorer LWC",
            "Create SignalController.cls + signalExplorer.lwc for browsing/filtering signals. "
            "Calls signal-builder-backend and forwardlane-backend signal endpoints.",
            issue_type=STORY, priority=HIGH, labels=["invesco", "salesforce", "lwc"],
            epic_key=epic_invesco
        )
        create_issue(
            "Configure Salesforce Named Credential for ForwardLane API auth",
            "Set up Named Credential pointing to ForwardLane API with proper OAuth/token auth. "
            "All Apex callouts must use this credential, never hardcoded tokens.",
            issue_type=TASK, priority=HIGH, labels=["invesco", "salesforce", "auth"],
            epic_key=epic_invesco
        )

    # ═══════════════════════════════════════════════════════════════
    # EPIC 3: Test Coverage — Critical Modules
    # ═══════════════════════════════════════════════════════════════
    print("\n🧪 Creating Epic: Test Coverage for Critical Modules")
    epic_coverage = create_issue(
        "Test Coverage: Auth, tenant isolation, API contracts, signal validation",
        "Raise test coverage on critical modules identified in module-priority.json. "
        "Target: 90% on critical tier (auth, tenant isolation, meeting prep, API contracts, "
        "signal validation, injection security). 75% on high tier.",
        issue_type=EPIC, priority=HIGH, labels=["testing", "coverage"]
    )

    if epic_coverage:
        create_issue(
            "Add auth module tests — forwardlane-backend",
            "Test authentication flows: login, session management, JWT validation, SAML/SSO, "
            "token refresh, permission checks. Target: 90% coverage on auth/**",
            issue_type=STORY, priority=HIGH, labels=["testing", "auth", "forwardlane-backend"],
            epic_key=epic_coverage
        )
        create_issue(
            "Add tenant isolation tests — forwardlane-backend",
            "Test that users cannot access data from other organizations. Cover tenant/**, "
            "org_id filtering, permission checks. Cross-tenant data leak = catastrophic.",
            issue_type=STORY, priority=BLOCKER, labels=["testing", "tenant-isolation", "security"],
            epic_key=epic_coverage
        )
        create_issue(
            "Add API contract tests — forwardlane-backend",
            "Test all public API endpoints for correct request/response schemas, status codes, "
            "error handling, and backward compatibility. Focus on endpoints called by Salesforce.",
            issue_type=STORY, priority=HIGH, labels=["testing", "api", "forwardlane-backend"],
            epic_key=epic_coverage
        )
        create_issue(
            "Add NL→SQL injection prevention tests — signal-builder-backend",
            "Test the NL→SQL engine (translators, schema_builder) for SQL injection vectors. "
            "The NL→SQL engine is core IP — wrong signals = wrong financial advice.",
            issue_type=STORY, priority=BLOCKER, labels=["testing", "security", "signal-builder"],
            epic_key=epic_coverage
        )
        create_issue(
            "Add meeting prep endpoint tests — forwardlane-backend",
            "Test meeting_prep/** and easy_button/** endpoints. Core Invesco demo deliverable.",
            issue_type=STORY, priority=HIGH, labels=["testing", "invesco", "meeting-prep"],
            epic_key=epic_coverage
        )

    # ═══════════════════════════════════════════════════════════════
    # EPIC 4: Data Waterfall Pipeline
    # ═══════════════════════════════════════════════════════════════
    print("\n📊 Creating Epic: Data Waterfall Pipeline")
    epic_enrichment = create_issue(
        "Data Waterfall: Multi-provider lead enrichment pipeline",
        "Complete the lead enrichment system at signal-studio-backend/enrichment/. "
        "7 providers (Hunter → FindyMail → Icypeas → QuickEnrich → Forager → Wiza → LeadIQ). "
        "Code complete, needs API keys configured in ProviderConfig admin.",
        issue_type=EPIC, priority=MEDIUM, labels=["enrichment", "data-pipeline"]
    )

    if epic_enrichment:
        create_issue(
            "Configure enrichment provider API keys in admin",
            "Set up API keys for all 7 enrichment providers in the ProviderConfig admin panel. "
            "Enable providers in priority order: Hunter first (cheapest), then FindyMail, etc.",
            issue_type=TASK, priority=MEDIUM, labels=["enrichment", "configuration"],
            epic_key=epic_enrichment
        )
        create_issue(
            "Test enrichment pipeline end-to-end with real data",
            "Run single + batch enrichment with real contacts. Verify waterfall logic, "
            "caching (Redis + DB), short-circuit behavior, and audit logging.",
            issue_type=STORY, priority=MEDIUM, labels=["enrichment", "testing"],
            epic_key=epic_enrichment
        )

    # ═══════════════════════════════════════════════════════════════
    # EPIC 5: Repo Sync & DevOps
    # ═══════════════════════════════════════════════════════════════
    print("\n🔄 Creating Epic: Repo Sync & DevOps")
    epic_devops = create_issue(
        "DevOps: GitHub ↔ Bitbucket repo sync + CI/CD",
        "3 core repos are out of sync between GitHub (TrendpilotAI) and Bitbucket (forwardlane). "
        "Victor pushes to BB, agents push to GH. Need mirroring or single source of truth.",
        issue_type=EPIC, priority=HIGH, labels=["devops", "git-sync"]
    )

    if epic_devops:
        create_issue(
            "Sync forwardlane-backend: BB is 1 day ahead of GH",
            "Bitbucket forwardlane/forwardlane-backend has newer commits than GitHub TrendpilotAI/signal-studio-backend. "
            "Pull BB latest, merge with GH branches, set up mirroring.",
            issue_type=TASK, priority=HIGH, labels=["devops", "git-sync", "forwardlane-backend"],
            epic_key=epic_devops
        )
        create_issue(
            "Sync signal-builder-backend: BB is 3 days ahead of GH",
            "Bitbucket is 3 days ahead of GitHub. Biggest divergence risk.",
            issue_type=TASK, priority=HIGH, labels=["devops", "git-sync", "signal-builder"],
            epic_key=epic_devops
        )
        create_issue(
            "Sync forwardlane_advisor: BB is 1 day ahead of GH",
            "Pull latest from Bitbucket and sync to GitHub.",
            issue_type=TASK, priority=MEDIUM, labels=["devops", "git-sync"],
            epic_key=epic_devops
        )
        create_issue(
            "Set up automatic BB→GH mirroring for core repos",
            "Configure Bitbucket Pipelines or GitHub Actions to auto-mirror commits between "
            "Bitbucket (forwardlane) and GitHub (TrendpilotAI) for the 5 core repos.",
            issue_type=STORY, priority=HIGH, labels=["devops", "automation", "git-sync"],
            epic_key=epic_devops
        )

    # ═══════════════════════════════════════════════════════════════
    # EPIC 6: Infrastructure & Monitoring
    # ═══════════════════════════════════════════════════════════════
    print("\n🏗️ Creating Epic: Infrastructure")
    epic_infra = create_issue(
        "Infrastructure: Railway services, Temporal workflows, monitoring",
        "39 Railway services across 5 projects. Temporal connected but not primary executor. "
        "Need to migrate critical cron jobs to Temporal for durable execution.",
        issue_type=EPIC, priority=MEDIUM, labels=["infrastructure", "railway", "temporal"]
    )

    if epic_infra:
        create_issue(
            "Migrate self-healing cron to Temporal workflow",
            "Move the service-health cron job (every 2h) to a Temporal SelfHealingWorkflow "
            "for retry semantics, visibility, and durable execution.",
            issue_type=STORY, priority=MEDIUM, labels=["temporal", "self-healing"],
            epic_key=epic_infra
        )
        create_issue(
            "Migrate judge swarm cron to Temporal workflow",
            "Move daily-judge-swarm (3AM ET) to Temporal JudgeSwarmWorkflow. "
            "Currently errors occasionally — Temporal retries would fix.",
            issue_type=STORY, priority=MEDIUM, labels=["temporal", "judge-swarm"],
            epic_key=epic_infra
        )
        create_issue(
            "Clean up Ultrafone redundant Railway services",
            "Flagged during audit: Ultrafone has redundant services on Railway. "
            "Consolidate or remove duplicates to reduce cost.",
            issue_type=TASK, priority=LOW, labels=["railway", "cleanup", "ultrafone"],
            epic_key=epic_infra
        )
        create_issue(
            "Archive signal-studio-frontend (scored 0.0)",
            "Judge swarm scored signal-studio-frontend at 0.0 — possible dead project. "
            "Verify it's superseded by Signal-Studio (Next.js 15) and archive if so.",
            issue_type=TASK, priority=LOW, labels=["cleanup", "archive"],
            epic_key=epic_infra
        )

    print(f"\n{'='*50}")
    print(f"Done! All tickets pushed to Jira project SS")


if __name__ == "__main__":
    main()
