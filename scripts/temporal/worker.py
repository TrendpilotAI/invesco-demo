#!/usr/bin/env python3
"""
Temporal Worker for Honey AI.
Connects to Temporal server, registers all workflows and activities,
and processes tasks from the "honey-main" queue.
"""

import asyncio
import logging
import os
import signal
import sys

from temporalio.client import Client
from temporalio.worker import Worker

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from activities import ALL_ACTIVITIES
from workflows import ALL_WORKFLOWS

# Railway resource management
try:
    from railway_activities import ALL_RAILWAY_ACTIVITIES
    from railway_workflows import ALL_RAILWAY_WORKFLOWS
except ImportError:
    ALL_RAILWAY_ACTIVITIES = []
    ALL_RAILWAY_WORKFLOWS = []

TEMPORAL_HOST = os.environ.get("TEMPORAL_HOST", "temporal.railway.internal:7233")
TEMPORAL_NAMESPACE = os.environ.get("TEMPORAL_NAMESPACE", "honey-agents")
TASK_QUEUE = os.environ.get("TEMPORAL_TASK_QUEUE", "honey-main")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("honey-worker")


async def run_worker():
    logger.info(f"Connecting to Temporal at {TEMPORAL_HOST}...")
    client = await Client.connect(TEMPORAL_HOST, namespace=TEMPORAL_NAMESPACE)
    logger.info(f"Connected. Starting worker on queue '{TASK_QUEUE}'...")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=ALL_WORKFLOWS + ALL_RAILWAY_WORKFLOWS,
        activities=ALL_ACTIVITIES + ALL_RAILWAY_ACTIVITIES,
    )

    # Graceful shutdown
    shutdown_event = asyncio.Event()

    def _signal_handler():
        logger.info("Shutdown signal received")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)

    logger.info(f"Worker running. Workflows: {[w.__name__ for w in ALL_WORKFLOWS]}")
    logger.info(f"Activities: {[a.__name__ for a in ALL_ACTIVITIES]}")

    # Run worker until shutdown
    async with worker:
        await shutdown_event.wait()

    logger.info("Worker shut down gracefully.")


def main():
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
