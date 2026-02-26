#!/usr/bin/env python3
"""
Health Publisher Daemon — checks services every 60s, publishes on state CHANGES only.

Tracks last-known state per service. Only emits honey.service.health events
when a service transitions between up/down.
"""

import asyncio
import json
import logging
import os
import signal
import sys
from pathlib import Path

# Add parent for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from event_bus import AsyncEventBus

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("health_publisher")

CHECK_INTERVAL = int(os.environ.get("HEALTH_CHECK_INTERVAL", "60"))
STATE_FILE = Path(__file__).resolve().parents[2] / "config" / "health-state.json"

# Services to monitor: name → check config
SERVICES = {
    "redis": {
        "type": "redis",
        "url": os.environ.get("REDIS_URL", "redis://default:n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E@trolley.proxy.rlwy.net:11973"),
    },
    "gateway": {
        "type": "command",
        "command": "openclaw gateway status",
        "timeout": 10,
    },
    "n8n": {
        "type": "http",
        "url": os.environ.get("N8N_URL", "https://primary-production-4244.up.railway.app/healthz"),
        "timeout": 10,
    },
}


async def check_redis(config: dict) -> bool:
    import redis.asyncio as aioredis
    try:
        r = aioredis.from_url(config["url"])
        await r.ping()
        await r.close()
        return True
    except Exception:
        return False


async def check_http(config: dict) -> bool:
    try:
        proc = await asyncio.create_subprocess_exec(
            "curl", "-sf", "-o", "/dev/null", "-w", "%{http_code}",
            "--max-time", str(config.get("timeout", 10)), config["url"],
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        code = stdout.decode().strip()
        return code.startswith("2") or code.startswith("3")
    except Exception:
        return False


async def check_command(config: dict) -> bool:
    try:
        proc = await asyncio.create_subprocess_shell(
            config["command"],
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        await asyncio.wait_for(proc.communicate(), timeout=config.get("timeout", 10))
        return proc.returncode == 0
    except Exception:
        return False


CHECKERS = {
    "redis": check_redis,
    "http": check_http,
    "command": check_command,
}


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


async def run(bus: AsyncEventBus):
    state = load_state()
    logger.info("Health publisher started (interval=%ds, services=%d)", CHECK_INTERVAL, len(SERVICES))

    while True:
        for name, config in SERVICES.items():
            checker = CHECKERS.get(config["type"])
            if not checker:
                continue

            try:
                is_up = await checker(config)
            except Exception:
                is_up = False

            status = "up" if is_up else "down"
            prev = state.get(name)

            if prev != status:
                event_name = "service_up" if is_up else "service_down"
                await bus.publish(
                    "honey.service.health",
                    event_name,
                    data={"service": name, "status": status, "previous": prev or "unknown"},
                    source="health_publisher",
                )
                logger.info("State change: %s %s → %s", name, prev, status)
                state[name] = status
                save_state(state)
            else:
                logger.debug("%s: %s (unchanged)", name, status)

        await asyncio.sleep(CHECK_INTERVAL)


async def main():
    bus = AsyncEventBus()
    assert await bus.ping(), "Redis connection failed"
    logger.info("Redis connected ✓")

    loop = asyncio.get_event_loop()
    stop = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    task = asyncio.create_task(run(bus))

    await stop.wait()
    logger.info("Shutting down...")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    await bus.close()


if __name__ == "__main__":
    asyncio.run(main())
