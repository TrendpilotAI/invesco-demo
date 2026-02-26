"""
Core Event Bus — Redis pub/sub wrapper for Honey AI.

Channels follow the pattern: honey.<domain>.<event>
  e.g. honey.service.health, honey.agent.failed, honey.cron.failed

Events are JSON payloads with a standard envelope:
  { "channel": "...", "event": "...", "ts": <epoch>, "data": {...} }
"""

import json
import time
import os
import logging
import asyncio
from typing import Callable, Optional, Any

import redis
import redis.asyncio as aioredis

logger = logging.getLogger("event_bus")

REDIS_URL = os.environ.get(
    "REDIS_URL",
    "redis://default:n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E@trolley.proxy.rlwy.net:11973",
)


def make_event(channel: str, event: str, data: dict | None = None, source: str = "unknown") -> dict:
    """Create a standard event envelope."""
    return {
        "channel": channel,
        "event": event,
        "ts": time.time(),
        "source": source,
        "data": data or {},
    }


# ── Synchronous client (for CLI / scripts) ──────────────────────────

class EventBus:
    """Synchronous Redis pub/sub event bus."""

    def __init__(self, redis_url: str = REDIS_URL):
        self._r = redis.from_url(redis_url, decode_responses=True)
        self._pubsub: Optional[redis.client.PubSub] = None

    # publish
    def publish(self, channel: str, event: str, data: dict | None = None, source: str = "unknown") -> int:
        payload = make_event(channel, event, data, source)
        logger.info("PUB %s → %s", channel, event)
        return self._r.publish(channel, json.dumps(payload))

    # subscribe to exact channels
    def subscribe(self, *channels: str, callback: Callable[[dict], None]):
        self._pubsub = self._r.pubsub()
        self._pubsub.subscribe(*channels)
        logger.info("SUB %s", channels)
        for msg in self._pubsub.listen():
            if msg["type"] == "message":
                try:
                    payload = json.loads(msg["data"])
                    callback(payload)
                except Exception:
                    logger.exception("Error handling message on %s", msg.get("channel"))

    # pattern subscribe
    def psubscribe(self, *patterns: str, callback: Callable[[dict], None]):
        self._pubsub = self._r.pubsub()
        self._pubsub.psubscribe(*patterns)
        logger.info("PSUB %s", patterns)
        for msg in self._pubsub.listen():
            if msg["type"] == "pmessage":
                try:
                    payload = json.loads(msg["data"])
                    callback(payload)
                except Exception:
                    logger.exception("Error handling message on %s", msg.get("channel"))

    def close(self):
        if self._pubsub:
            self._pubsub.close()
        self._r.close()

    def ping(self) -> bool:
        return self._r.ping()


# ── Async client (for daemons) ───────────────────────────────────────

class AsyncEventBus:
    """Asyncio Redis pub/sub event bus."""

    def __init__(self, redis_url: str = REDIS_URL):
        self._r = aioredis.from_url(redis_url, decode_responses=True)
        self._pubsub: Optional[aioredis.client.PubSub] = None

    async def publish(self, channel: str, event: str, data: dict | None = None, source: str = "unknown") -> int:
        payload = make_event(channel, event, data, source)
        logger.info("PUB %s → %s", channel, event)
        return await self._r.publish(channel, json.dumps(payload))

    async def subscribe(self, *channels: str, callback: Callable[[dict], Any]):
        self._pubsub = self._r.pubsub()
        await self._pubsub.subscribe(*channels)
        logger.info("SUB %s", channels)
        async for msg in self._pubsub.listen():
            if msg["type"] == "message":
                try:
                    payload = json.loads(msg["data"])
                    result = callback(payload)
                    if asyncio.iscoroutine(result):
                        await result
                except Exception:
                    logger.exception("Error handling message on %s", msg.get("channel"))

    async def psubscribe(self, *patterns: str, callback: Callable[[dict], Any]):
        self._pubsub = self._r.pubsub()
        await self._pubsub.psubscribe(*patterns)
        logger.info("PSUB %s", patterns)
        async for msg in self._pubsub.listen():
            if msg["type"] == "pmessage":
                try:
                    payload = json.loads(msg["data"])
                    result = callback(payload)
                    if asyncio.iscoroutine(result):
                        await result
                except Exception:
                    logger.exception("Error handling message on %s", msg.get("channel"))

    async def close(self):
        if self._pubsub:
            await self._pubsub.close()
        await self._r.close()

    async def ping(self) -> bool:
        return await self._r.ping()
