#!/usr/bin/env python3
"""
Event Bus Listener — subscribes to honey.* channels, matches against reactions, executes actions.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from event_bus import AsyncEventBus
from reactions import load_reactions, process_event

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("listener")


async def main():
    bus = AsyncEventBus()
    assert await bus.ping(), "Redis connection failed"
    logger.info("Redis connected ✓")

    reactions = load_reactions()
    logger.info("Loaded %d reactions", len(reactions))

    loop = asyncio.get_event_loop()
    stop = asyncio.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    async def handle(event: dict):
        process_event(reactions, event)

    # Run listener in background, wait for stop signal
    listen_task = asyncio.create_task(
        bus.psubscribe("honey.*", callback=handle)
    )

    await stop.wait()
    logger.info("Shutting down...")
    listen_task.cancel()
    try:
        await listen_task
    except asyncio.CancelledError:
        pass
    await bus.close()


if __name__ == "__main__":
    asyncio.run(main())
