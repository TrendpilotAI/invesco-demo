"""
Temporal Activities for Railway Resource Management.
Each activity wraps a Railway GraphQL API operation.
"""

import asyncio
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx
from temporalio import activity

RAILWAY_TOKEN = os.environ.get("RAILWAY_API_TOKEN", "d51e4138-dca9-4bfd-b093-93f599681c63")
RAILWAY_API = "https://backboard.railway.com/graphql/v2"
HEADERS = {"Authorization": f"Bearer {RAILWAY_TOKEN}", "Content-Type": "application/json"}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ProjectInfo:
    id: str
    name: str
    services: List[Dict[str, Any]]


@dataclass
class ServiceInfo:
    id: str
    name: str
    project_id: str
    project_name: str
    status: Optional[str] = None
    last_deploy: Optional[str] = None
    days_since_deploy: Optional[int] = None


@dataclass
class DeploymentStatus:
    service_id: str
    status: str
    created_at: str
    deployment_id: Optional[str] = None


@dataclass
class ServiceActionInput:
    service_id: str
    environment_id: Optional[str] = None


@dataclass
class RedeployInput:
    service_id: str
    environment_id: str


@dataclass
class ServiceConfigInput:
    service_id: str
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CreateServiceInput:
    project_id: str
    name: str
    source: Optional[Dict[str, str]] = None  # {"image": "...", "repo": "..."}


@dataclass
class AuditResult:
    total_projects: int
    total_services: int
    crashed_or_failed: List[Dict[str, Any]]
    stale_services: List[Dict[str, Any]]
    redundant_databases: List[Dict[str, Any]]
    recommendations: List[str]
    generated_at: str


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

async def _gql(query: str, variables: Optional[Dict] = None) -> Dict:
    async with httpx.AsyncClient(timeout=30) as client:
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        resp = await client.post(RAILWAY_API, json=payload, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")
        return data["data"]


# ---------------------------------------------------------------------------
# Activities
# ---------------------------------------------------------------------------

@activity.defn
async def list_projects() -> List[Dict[str, Any]]:
    """List all Railway projects with their services."""
    activity.logger.info("Listing all Railway projects")
    data = await _gql("""
    {
        projects {
            edges {
                node {
                    id
                    name
                    services {
                        edges {
                            node {
                                id
                                name
                                deployments(first: 1) {
                                    edges {
                                        node { id status createdAt }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """)
    results = []
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
                "status": latest["status"] if latest else "NO_DEPLOYMENTS",
                "last_deploy": latest["createdAt"] if latest else None,
            })
        results.append({"id": node["id"], "name": node["name"], "services": services})
    return results


@activity.defn
async def list_services(project_id: str) -> List[Dict[str, Any]]:
    """List services for a specific project."""
    activity.logger.info(f"Listing services for project {project_id}")
    data = await _gql("""
    query($projectId: String!) {
        project(id: $projectId) {
            services {
                edges {
                    node {
                        id
                        name
                        deployments(first: 1) {
                            edges {
                                node { id status createdAt }
                            }
                        }
                    }
                }
            }
        }
    }
    """, {"projectId": project_id})
    services = []
    for edge in data["project"]["services"]["edges"]:
        svc = edge["node"]
        deploys = svc.get("deployments", {}).get("edges", [])
        latest = deploys[0]["node"] if deploys else None
        services.append({
            "id": svc["id"],
            "name": svc["name"].strip(),
            "status": latest["status"] if latest else "NO_DEPLOYMENTS",
            "last_deploy": latest["createdAt"] if latest else None,
        })
    return services


@activity.defn
async def get_deployment_status(service_id: str) -> Dict[str, Any]:
    """Get latest deployment status for a service."""
    activity.logger.info(f"Getting deployment status for {service_id}")
    data = await _gql("""
    query($serviceId: String!) {
        deployments(first: 1, input: { serviceId: $serviceId }) {
            edges {
                node {
                    id
                    status
                    createdAt
                }
            }
        }
    }
    """, {"serviceId": service_id})
    edges = data["deployments"]["edges"]
    if not edges:
        return {"service_id": service_id, "status": "NO_DEPLOYMENTS"}
    node = edges[0]["node"]
    return {
        "service_id": service_id,
        "deployment_id": node["id"],
        "status": node["status"],
        "created_at": node["createdAt"],
    }


@activity.defn
async def redeploy_service(input: RedeployInput) -> Dict[str, Any]:
    """Trigger a redeployment of a service."""
    activity.logger.info(f"Redeploying service {input.service_id}")
    data = await _gql("""
    mutation($serviceId: String!, $environmentId: String!) {
        serviceInstanceRedeploy(serviceId: $serviceId, environmentId: $environmentId)
    }
    """, {"serviceId": input.service_id, "environmentId": input.environment_id})
    return {"service_id": input.service_id, "success": True, "result": data}


@activity.defn
async def restart_service(input: ServiceActionInput) -> Dict[str, Any]:
    """Restart a service."""
    activity.logger.info(f"Restarting service {input.service_id}")
    data = await _gql("""
    mutation($serviceId: String!, $environmentId: String!) {
        serviceInstanceRedeploy(serviceId: $serviceId, environmentId: $environmentId)
    }
    """, {"serviceId": input.service_id, "environmentId": input.environment_id or ""})
    return {"service_id": input.service_id, "success": True}


@activity.defn
async def delete_service(service_id: str) -> Dict[str, Any]:
    """Delete a service (use with caution!)."""
    activity.logger.info(f"DELETING service {service_id}")
    data = await _gql("""
    mutation($serviceId: String!) {
        serviceDelete(id: $serviceId)
    }
    """, {"serviceId": service_id})
    return {"service_id": service_id, "deleted": True}


@activity.defn
async def run_resource_audit() -> Dict[str, Any]:
    """Run a full resource audit across all projects."""
    activity.logger.info("Running full resource audit")
    now = datetime.now(timezone.utc)
    projects = await list_projects()

    crashed_or_failed = []
    stale_services = []
    redundant_databases = []
    recommendations = []

    for project in projects:
        redis_count = 0
        postgres_count = 0

        for svc in project["services"]:
            status = svc["status"]
            name = svc["name"].lower()

            if status in ("CRASHED", "FAILED"):
                crashed_or_failed.append({
                    "project": project["name"],
                    "service": svc["name"],
                    "service_id": svc["id"],
                    "status": status,
                })

            if svc["last_deploy"]:
                deployed_at = datetime.fromisoformat(svc["last_deploy"].replace("Z", "+00:00"))
                days = (now - deployed_at).days
                if days > 30:
                    stale_services.append({
                        "project": project["name"],
                        "service": svc["name"],
                        "service_id": svc["id"],
                        "days_stale": days,
                    })

            if "redis" in name:
                redis_count += 1
            if "postgres" in name:
                postgres_count += 1

        if redis_count > 1:
            redundant_databases.append({
                "project": project["name"],
                "type": "Redis",
                "count": redis_count,
            })
            recommendations.append(f"Consolidate {redis_count} Redis in {project['name']} → 1")
        if postgres_count > 2:
            redundant_databases.append({
                "project": project["name"],
                "type": "Postgres",
                "count": postgres_count,
            })
            recommendations.append(f"Consolidate {postgres_count} Postgres in {project['name']} → 1-2")

    if crashed_or_failed:
        recommendations.append(f"Fix or remove {len(crashed_or_failed)} crashed/failed services")
    if stale_services:
        recommendations.append(f"Review {len(stale_services)} stale services (>30 days)")

    return {
        "total_projects": len(projects),
        "total_services": sum(len(p["services"]) for p in projects),
        "crashed_or_failed": crashed_or_failed,
        "stale_services": stale_services,
        "redundant_databases": redundant_databases,
        "recommendations": recommendations,
        "generated_at": now.isoformat(),
    }


# All activities for registration
ALL_RAILWAY_ACTIVITIES = [
    list_projects,
    list_services,
    get_deployment_status,
    redeploy_service,
    restart_service,
    delete_service,
    run_resource_audit,
]
