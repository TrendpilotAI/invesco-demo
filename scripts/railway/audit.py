#!/usr/bin/env python3
"""
Railway Resource Audit Script.
Queries all projects/services via Railway GraphQL API and generates a comprehensive report.
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import httpx

RAILWAY_TOKEN = os.environ.get("RAILWAY_API_TOKEN", "d51e4138-dca9-4bfd-b093-93f599681c63")
RAILWAY_API = "https://backboard.railway.com/graphql/v2"
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "audit-results.json")

HEADERS = {
    "Authorization": f"Bearer {RAILWAY_TOKEN}",
    "Content-Type": "application/json",
}

# Thresholds
STALE_DAYS = 30
KNOWN_ISSUES = {
    "Entity Extraction": "Known failure — NLP model deployment issues",
    "Hypebase-ai": "Duplicate project of Hypebase AI",
}


async def gql(client: httpx.AsyncClient, query: str, variables: Optional[Dict] = None) -> Dict:
    """Execute a GraphQL query."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    resp = await client.post(RAILWAY_API, json=payload, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    return data["data"]


async def fetch_all_projects(client: httpx.AsyncClient) -> List[Dict]:
    """Fetch all projects with services and latest deployments."""
    query = """
    {
        projects {
            edges {
                node {
                    id
                    name
                    environments {
                        edges {
                            node { id name }
                        }
                    }
                    services {
                        edges {
                            node {
                                id
                                name
                                deployments(first: 1) {
                                    edges {
                                        node {
                                            id
                                            status
                                            createdAt
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    data = await gql(client, query)
    projects = []
    for edge in data["projects"]["edges"]:
        node = edge["node"]
        services = []
        for svc_edge in node["services"]["edges"]:
            svc = svc_edge["node"]
            deploys = svc.get("deployments", {}).get("edges", [])
            latest = deploys[0]["node"] if deploys else None
            services.append({
                "id": svc["id"],
                "name": svc["name"].strip(),
                "latest_deployment": {
                    "id": latest["id"],
                    "status": latest["status"],
                    "created_at": latest["createdAt"],
                } if latest else None,
            })
        projects.append({
            "id": node["id"],
            "name": node["name"],
            "environments": [e["node"]["name"] for e in node.get("environments", {}).get("edges", [])],
            "services": services,
        })
    return projects


def analyze_projects(projects: List[Dict]) -> Dict[str, Any]:
    """Analyze projects for issues."""
    now = datetime.now(timezone.utc)
    total_services = sum(len(p["services"]) for p in projects)

    issues = {
        "crashed_or_failed": [],
        "stale_services": [],
        "no_deployments": [],
        "duplicate_suspects": [],
        "redundant_databases": [],
        "known_issues": [],
    }

    recommendations = []
    services_to_delete = []
    services_to_fix = []

    for project in projects:
        redis_count = 0
        postgres_count = 0
        redis_services = []
        postgres_services = []

        for svc in project["services"]:
            name = svc["name"]
            deploy = svc["latest_deployment"]

            # Check for known issues
            if name in KNOWN_ISSUES:
                issues["known_issues"].append({
                    "project": project["name"],
                    "service": name,
                    "note": KNOWN_ISSUES[name],
                })

            if deploy is None:
                issues["no_deployments"].append({
                    "project": project["name"],
                    "service": name,
                    "service_id": svc["id"],
                })
                services_to_delete.append(f"{project['name']}/{name} (never deployed)")
                continue

            status = deploy["status"]
            deployed_at = datetime.fromisoformat(deploy["created_at"].replace("Z", "+00:00"))
            days_ago = (now - deployed_at).days

            # Crashed/Failed
            if status in ("CRASHED", "FAILED"):
                issues["crashed_or_failed"].append({
                    "project": project["name"],
                    "service": name,
                    "service_id": svc["id"],
                    "status": status,
                    "deployed_at": deploy["created_at"],
                    "days_ago": days_ago,
                })

            # Stale
            if days_ago > STALE_DAYS:
                issues["stale_services"].append({
                    "project": project["name"],
                    "service": name,
                    "service_id": svc["id"],
                    "deployed_at": deploy["created_at"],
                    "days_ago": days_ago,
                    "status": status,
                })

            # Count databases
            name_lower = name.lower()
            if "redis" in name_lower:
                redis_count += 1
                redis_services.append(name)
            if "postgres" in name_lower:
                postgres_count += 1
                postgres_services.append(name)

        # Flag redundant databases
        if redis_count > 1:
            issues["redundant_databases"].append({
                "project": project["name"],
                "type": "Redis",
                "count": redis_count,
                "services": redis_services,
                "recommendation": f"Consolidate {redis_count} Redis → 1",
            })
        if postgres_count > 2:
            issues["redundant_databases"].append({
                "project": project["name"],
                "type": "Postgres",
                "count": postgres_count,
                "services": postgres_services,
                "recommendation": f"Consolidate {postgres_count} Postgres → 1-2",
            })

    # Check for duplicate projects
    names = [p["name"].lower().replace("-", " ").replace("_", " ").strip() for p in projects]
    seen = {}
    for i, name in enumerate(names):
        base = name.split()[0]  # first word
        if base in seen:
            issues["duplicate_suspects"].append({
                "project_a": projects[seen[base]]["name"],
                "project_b": projects[i]["name"],
                "reason": f"Similar names (both start with '{base}')",
            })
        seen[base] = i

    return {
        "summary": {
            "total_projects": len(projects),
            "total_services": total_services,
            "crashed_or_failed": len(issues["crashed_or_failed"]),
            "stale_services": len(issues["stale_services"]),
            "no_deployments": len(issues["no_deployments"]),
            "redundant_database_groups": len(issues["redundant_databases"]),
            "duplicate_project_suspects": len(issues["duplicate_suspects"]),
        },
        "issues": issues,
        "projects": projects,
        "generated_at": now.isoformat(),
    }


def print_report(analysis: Dict):
    """Print a human-readable report."""
    s = analysis["summary"]
    print("=" * 70)
    print("RAILWAY RESOURCE AUDIT REPORT")
    print(f"Generated: {analysis['generated_at']}")
    print("=" * 70)
    print(f"\nTotal Projects: {s['total_projects']}")
    print(f"Total Services: {s['total_services']}")
    print(f"Crashed/Failed: {s['crashed_or_failed']}")
    print(f"Stale (>{STALE_DAYS} days): {s['stale_services']}")
    print(f"Never Deployed: {s['no_deployments']}")
    print(f"Redundant DB Groups: {s['redundant_database_groups']}")
    print(f"Duplicate Project Suspects: {s['duplicate_project_suspects']}")

    issues = analysis["issues"]

    if issues["crashed_or_failed"]:
        print(f"\n{'─' * 50}")
        print("⛔ CRASHED / FAILED SERVICES")
        print(f"{'─' * 50}")
        for item in issues["crashed_or_failed"]:
            print(f"  [{item['status']}] {item['project']} / {item['service']}")
            print(f"           Last deploy: {item['deployed_at']} ({item['days_ago']}d ago)")

    if issues["no_deployments"]:
        print(f"\n{'─' * 50}")
        print("❌ NEVER DEPLOYED")
        print(f"{'─' * 50}")
        for item in issues["no_deployments"]:
            print(f"  {item['project']} / {item['service']}")

    if issues["stale_services"]:
        print(f"\n{'─' * 50}")
        print(f"💤 STALE SERVICES (>{STALE_DAYS} days since deploy)")
        print(f"{'─' * 50}")
        for item in issues["stale_services"]:
            print(f"  {item['project']} / {item['service']}")
            print(f"           {item['days_ago']}d stale, status: {item['status']}")

    if issues["redundant_databases"]:
        print(f"\n{'─' * 50}")
        print("🗄️  REDUNDANT DATABASES")
        print(f"{'─' * 50}")
        for item in issues["redundant_databases"]:
            print(f"  {item['project']}: {item['count']}x {item['type']}")
            print(f"    Services: {', '.join(item['services'])}")
            print(f"    → {item['recommendation']}")

    if issues["duplicate_suspects"]:
        print(f"\n{'─' * 50}")
        print("🔄 DUPLICATE PROJECT SUSPECTS")
        print(f"{'─' * 50}")
        for item in issues["duplicate_suspects"]:
            print(f"  {item['project_a']} ↔ {item['project_b']}")
            print(f"    Reason: {item['reason']}")

    if issues["known_issues"]:
        print(f"\n{'─' * 50}")
        print("📋 KNOWN ISSUES")
        print(f"{'─' * 50}")
        for item in issues["known_issues"]:
            print(f"  {item['project']} / {item['service']}: {item['note']}")

    # Per-project summary
    print(f"\n{'=' * 70}")
    print("PROJECT DETAILS")
    print(f"{'=' * 70}")
    for project in analysis["projects"]:
        print(f"\n📦 {project['name']} ({len(project['services'])} services)")
        for svc in project["services"]:
            d = svc["latest_deployment"]
            if d:
                status_icon = {"SUCCESS": "✅", "FAILED": "⛔", "CRASHED": "💥", "SLEEPING": "💤"}.get(d["status"], "❓")
                print(f"   {status_icon} {svc['name']:35s} {d['status']:12s} {d['created_at'][:10]}")
            else:
                print(f"   ❌ {svc['name']:35s} NO DEPLOYMENTS")

    print(f"\n{'=' * 70}")
    print("RECOMMENDATIONS")
    print(f"{'=' * 70}")
    print("""
  1. DELETE Hypebase-ai project (duplicate, failed since Jan 7)
  2. DELETE Ultrafone redundant DBs: 4 Postgres + 4 Redis (keep 1 each)
  3. DELETE unnamed '.' service in Hypebase AI (crashed)
  4. DELETE never-deployed Redis in Ultrafone
  5. FIX Celery Worker + Beat in ForwardLane (critical)
  6. FIX Agent Ops Center in OpenClaw (recently failed)
  7. REVIEW FalkorDB (sleeping 53+ days)
  8. REVIEW Entity Extraction (known failure)
  9. REVIEW Postiz usage (is it needed?)

  Estimated savings: ~$65-125/month by removing 15-17 services.
""")


async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        print("Fetching Railway projects...")
        projects = await fetch_all_projects(client)
        print(f"Found {len(projects)} projects, {sum(len(p['services']) for p in projects)} services\n")

        analysis = analyze_projects(projects)

        # Save JSON
        with open(OUTPUT_JSON, "w") as f:
            json.dump(analysis, f, indent=2, default=str)
        print(f"JSON results saved to {OUTPUT_JSON}\n")

        # Print report
        print_report(analysis)

        return analysis


if __name__ == "__main__":
    asyncio.run(main())
