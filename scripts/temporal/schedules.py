#!/usr/bin/env python3
"""
Create Temporal Schedules to replace cron jobs.
Run once to set up, idempotent (updates existing schedules).
"""

import asyncio
import logging
import os
import sys

from temporalio.client import Client, Schedule, ScheduleActionStartWorkflow, ScheduleSpec, ScheduleIntervalSpec
from datetime import timedelta

sys.path.insert(0, os.path.dirname(__file__))

from workflows import (
    SelfHealingInput, HealthMonitorInput, JudgeSwarmInput, OrchestratorInput,
)

try:
    from railway_workflows import ResourceOptimizationWorkflow
    HAS_RAILWAY = True
except ImportError:
    HAS_RAILWAY = False

TEMPORAL_HOST = os.environ.get("TEMPORAL_HOST", "temporal.railway.internal:7233")
TEMPORAL_NAMESPACE = os.environ.get("TEMPORAL_NAMESPACE", "honey-agents")
TASK_QUEUE = "honey-main"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("honey-schedules")

# Default services to monitor
MONITORED_SERVICES = [
    {"name": "openclaw-gateway", "url": "http://localhost:3000/health"},
    {"name": "temporal", "url": "http://temporal.railway.internal:7233"},
    {"name": "redis", "url": "http://redis.railway.internal:6379"},
]

# Schedule definitions
SCHEDULES = [
    {
        "id": "health-monitor-continuous",
        "workflow": "HealthMonitorWorkflow",
        "input": HealthMonitorInput(
            services=MONITORED_SERVICES,
            interval_seconds=60,
            alert_after_failures=3,
        ),
        "interval": timedelta(hours=24),  # Restart daily (workflow runs continuously inside)
        "memo": "Continuous health monitoring with alerting",
    },
    {
        "id": "self-healing-loop",
        "workflow": "SelfHealingWorkflow",
        "input": SelfHealingInput(
            services=MONITORED_SERVICES,
            check_interval_seconds=300,
            max_retries=3,
        ),
        "interval": timedelta(hours=12),
        "memo": "Self-healing monitor — detects and fixes failures",
    },
    {
        "id": "judge-swarm-daily",
        "workflow": "JudgeSwarmWorkflow",
        "input": JudgeSwarmInput(repos=["honey-ai"]),
        "interval": timedelta(hours=24),
        "memo": "Daily code quality judging",
    },
]

# Add Railway resource audit schedule
if HAS_RAILWAY:
    SCHEDULES.append({
        "id": "railway-resource-audit-weekly",
        "workflow": "ResourceOptimizationWorkflow",
        "input": {},  # No input needed, uses defaults
        "interval": timedelta(days=7),
        "memo": "Weekly Railway resource audit and optimization",
    })


async def create_schedules():
    logger.info(f"Connecting to Temporal at {TEMPORAL_HOST}...")
    client = await Client.connect(TEMPORAL_HOST, namespace=TEMPORAL_NAMESPACE)

    for sched_def in SCHEDULES:
        schedule_id = sched_def["id"]
        try:
            # Try to delete existing
            handle = client.get_schedule_handle(schedule_id)
            await handle.delete()
            logger.info(f"Deleted existing schedule: {schedule_id}")
        except Exception:
            pass

        try:
            await client.create_schedule(
                schedule_id,
                Schedule(
                    action=ScheduleActionStartWorkflow(
                        sched_def["workflow"],
                        sched_def["input"],
                        id=f"{schedule_id}-run",
                        task_queue=TASK_QUEUE,
                    ),
                    spec=ScheduleSpec(
                        intervals=[ScheduleIntervalSpec(every=sched_def["interval"])],
                    ),
                ),
            )
            logger.info(f"✅ Created schedule: {schedule_id} (every {sched_def['interval']})")
        except Exception as e:
            logger.error(f"❌ Failed to create {schedule_id}: {e}")

    logger.info("All schedules configured.")


if __name__ == "__main__":
    asyncio.run(create_schedules())
