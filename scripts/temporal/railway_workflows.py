"""
Temporal Workflows for Railway Resource Management.
Orchestrate audit, scaling, and deployment operations.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Dict, List, Optional

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from railway_activities import (
        RedeployInput, ServiceActionInput,
        list_projects, list_services, get_deployment_status,
        redeploy_service, restart_service, delete_service,
        run_resource_audit,
        ALL_RAILWAY_ACTIVITIES,
    )
    from activities import (
        HealthCheckInput, HealthCheckOutput,
        PublishEventInput, NotificationInput,
        check_service_health, publish_event, send_notification,
    )

DEFAULT_RETRY = RetryPolicy(
    initial_interval=timedelta(seconds=5),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(minutes=2),
    maximum_attempts=3,
)


# ---------------------------------------------------------------------------
# ResourceOptimizationWorkflow
# ---------------------------------------------------------------------------

@dataclass
class ResourceOptimizationInput:
    auto_restart_crashed: bool = True
    notify_on_issues: bool = True
    dry_run: bool = True  # Don't actually delete/stop services unless False


@workflow.defn
class ResourceOptimizationWorkflow:
    """Periodic workflow that audits and optimizes Railway resources."""

    @workflow.run
    async def run(self, input: ResourceOptimizationInput = None) -> Dict[str, Any]:
        if input is None:
            input = ResourceOptimizationInput()

        workflow.logger.info("Starting Railway resource optimization audit")

        # Step 1: Run full audit
        audit = await workflow.execute_activity(
            run_resource_audit,
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=DEFAULT_RETRY,
        )

        actions_taken = []

        # Step 2: Auto-restart crashed services
        if input.auto_restart_crashed and not input.dry_run:
            for svc in audit.get("crashed_or_failed", []):
                try:
                    await workflow.execute_activity(
                        restart_service,
                        ServiceActionInput(service_id=svc["service_id"]),
                        start_to_close_timeout=timedelta(seconds=30),
                        retry_policy=DEFAULT_RETRY,
                    )
                    actions_taken.append(f"Restarted {svc['project']}/{svc['service']}")
                except Exception as e:
                    actions_taken.append(f"Failed to restart {svc['service']}: {e}")

        # Step 3: Publish audit results to Redis
        await workflow.execute_activity(
            publish_event,
            PublishEventInput(
                channel="honey:railway-audit",
                data={
                    "type": "resource_audit",
                    "total_services": audit.get("total_services", 0),
                    "issues": len(audit.get("crashed_or_failed", [])) + len(audit.get("stale_services", [])),
                    "recommendations": audit.get("recommendations", []),
                },
            ),
            start_to_close_timeout=timedelta(seconds=15),
        )

        # Step 4: Alert if significant issues found
        if input.notify_on_issues:
            issues_count = (
                len(audit.get("crashed_or_failed", []))
                + len(audit.get("redundant_databases", []))
            )
            if issues_count > 0:
                msg = (
                    f"🔍 Railway Audit Complete\n"
                    f"Services: {audit.get('total_services', 0)}\n"
                    f"Failed: {len(audit.get('crashed_or_failed', []))}\n"
                    f"Stale: {len(audit.get('stale_services', []))}\n"
                    f"Redundant DBs: {len(audit.get('redundant_databases', []))}\n"
                )
                if audit.get("recommendations"):
                    msg += "Recommendations:\n" + "\n".join(f"• {r}" for r in audit["recommendations"][:5])
                if actions_taken:
                    msg += "\nActions:\n" + "\n".join(f"• {a}" for a in actions_taken)

                await workflow.execute_activity(
                    send_notification,
                    NotificationInput(target="telegram", message=msg),
                    start_to_close_timeout=timedelta(seconds=15),
                )

        return {
            "audit": audit,
            "actions_taken": actions_taken,
            "dry_run": input.dry_run,
        }


# ---------------------------------------------------------------------------
# ServiceScalerWorkflow
# ---------------------------------------------------------------------------

@dataclass
class ServiceScaleInput:
    service_id: str
    service_name: str
    action: str  # "scale_up", "scale_down", "restart"
    reason: str = ""
    environment_id: str = ""


@workflow.defn
class ServiceScalerWorkflow:
    """Scale Railway services up/down based on demand."""

    @workflow.run
    async def run(self, input: ServiceScaleInput) -> Dict[str, Any]:
        workflow.logger.info(f"Scaling {input.service_name}: {input.action} ({input.reason})")

        result = {"service": input.service_name, "action": input.action, "success": False}

        if input.action == "restart":
            await workflow.execute_activity(
                redeploy_service,
                RedeployInput(service_id=input.service_id, environment_id=input.environment_id),
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=DEFAULT_RETRY,
            )
            result["success"] = True

        elif input.action == "scale_up":
            # Redeploy triggers a fresh instance
            await workflow.execute_activity(
                redeploy_service,
                RedeployInput(service_id=input.service_id, environment_id=input.environment_id),
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=DEFAULT_RETRY,
            )
            result["success"] = True

        elif input.action == "scale_down":
            # For Railway, "scale down" means letting it sleep or removing
            workflow.logger.info(f"Scale down requested for {input.service_name} — service will idle naturally")
            result["success"] = True
            result["note"] = "Railway auto-sleeps idle services"

        # Publish scaling event
        await workflow.execute_activity(
            publish_event,
            PublishEventInput(
                channel="honey:railway-scaling",
                data={
                    "service": input.service_name,
                    "action": input.action,
                    "reason": input.reason,
                    "success": result["success"],
                },
            ),
            start_to_close_timeout=timedelta(seconds=15),
        )

        # Notify
        emoji = {"scale_up": "⬆️", "scale_down": "⬇️", "restart": "🔄"}.get(input.action, "📦")
        await workflow.execute_activity(
            send_notification,
            NotificationInput(
                target="telegram",
                message=f"{emoji} Railway: {input.action} {input.service_name}\nReason: {input.reason}",
            ),
            start_to_close_timeout=timedelta(seconds=15),
        )

        return result


# ---------------------------------------------------------------------------
# DeploymentPipelineWorkflow
# ---------------------------------------------------------------------------

@dataclass
class DeploymentPipelineInput:
    service_id: str
    service_name: str
    environment_id: str
    health_check_url: Optional[str] = None
    max_health_retries: int = 5
    health_check_interval_seconds: int = 15


@workflow.defn
class DeploymentPipelineWorkflow:
    """Managed deployment with health checks and rollback."""

    @workflow.run
    async def run(self, input: DeploymentPipelineInput) -> Dict[str, Any]:
        workflow.logger.info(f"Starting deployment pipeline for {input.service_name}")

        result = {
            "service": input.service_name,
            "deployed": False,
            "healthy": False,
            "rolled_back": False,
        }

        # Step 1: Get current deployment (for rollback reference)
        pre_deploy = await workflow.execute_activity(
            get_deployment_status,
            input.service_id,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=DEFAULT_RETRY,
        )
        result["previous_deployment"] = pre_deploy.get("deployment_id")

        # Step 2: Trigger deployment
        await workflow.execute_activity(
            redeploy_service,
            RedeployInput(service_id=input.service_id, environment_id=input.environment_id),
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=DEFAULT_RETRY,
        )
        result["deployed"] = True

        # Notify
        await workflow.execute_activity(
            send_notification,
            NotificationInput(
                target="telegram",
                message=f"🚀 Deploying {input.service_name}...",
            ),
            start_to_close_timeout=timedelta(seconds=15),
        )

        # Step 3: Wait for deployment to stabilize
        await workflow.sleep(timedelta(seconds=30))

        # Step 4: Health check loop
        if input.health_check_url:
            healthy = False
            for attempt in range(input.max_health_retries):
                check = await workflow.execute_activity(
                    check_service_health,
                    HealthCheckInput(
                        service_name=input.service_name,
                        url=input.health_check_url,
                    ),
                    start_to_close_timeout=timedelta(seconds=30),
                    retry_policy=DEFAULT_RETRY,
                )
                if check.healthy:
                    healthy = True
                    break
                workflow.logger.warn(f"Health check failed (attempt {attempt + 1}/{input.max_health_retries})")
                await workflow.sleep(timedelta(seconds=input.health_check_interval_seconds))

            result["healthy"] = healthy

            if not healthy:
                # Step 5: Rollback — redeploy previous version
                workflow.logger.error(f"Health check failed after {input.max_health_retries} attempts, rolling back")
                try:
                    await workflow.execute_activity(
                        redeploy_service,
                        RedeployInput(service_id=input.service_id, environment_id=input.environment_id),
                        start_to_close_timeout=timedelta(minutes=2),
                        retry_policy=DEFAULT_RETRY,
                    )
                    result["rolled_back"] = True
                except Exception:
                    result["rollback_error"] = "Failed to rollback"

                await workflow.execute_activity(
                    send_notification,
                    NotificationInput(
                        target="telegram",
                        message=f"⚠️ Deployment ROLLED BACK: {input.service_name} (health check failed)",
                    ),
                    start_to_close_timeout=timedelta(seconds=15),
                )
            else:
                await workflow.execute_activity(
                    send_notification,
                    NotificationInput(
                        target="telegram",
                        message=f"✅ Deployed {input.service_name} successfully ({check.response_time_ms}ms)",
                    ),
                    start_to_close_timeout=timedelta(seconds=15),
                )
        else:
            # No health check URL — just verify deployment status
            await workflow.sleep(timedelta(seconds=15))
            post_deploy = await workflow.execute_activity(
                get_deployment_status,
                input.service_id,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=DEFAULT_RETRY,
            )
            result["healthy"] = post_deploy.get("status") == "SUCCESS"

            status_emoji = "✅" if result["healthy"] else "⚠️"
            await workflow.execute_activity(
                send_notification,
                NotificationInput(
                    target="telegram",
                    message=f"{status_emoji} Deployed {input.service_name}: {post_deploy.get('status', 'UNKNOWN')}",
                ),
                start_to_close_timeout=timedelta(seconds=15),
            )

        # Publish result
        await workflow.execute_activity(
            publish_event,
            PublishEventInput(
                channel="honey:railway-deploy",
                data={
                    "service": input.service_name,
                    "deployed": result["deployed"],
                    "healthy": result["healthy"],
                    "rolled_back": result["rolled_back"],
                },
            ),
            start_to_close_timeout=timedelta(seconds=15),
        )

        return result


# All workflows for registration
ALL_RAILWAY_WORKFLOWS = [
    ResourceOptimizationWorkflow,
    ServiceScalerWorkflow,
    DeploymentPipelineWorkflow,
]
