#!/usr/bin/env python3
"""
CLI tool for publishing events to the Honey AI event bus.

Usage:
  python publish_event.py <channel> <event> [--data '{"key":"val"}'] [--source mysvc]

Examples:
  python publish_event.py honey.cron.failed cron_failed --data '{"job":"backup","error":"timeout"}'
  python publish_event.py honey.service.health service_down --data '{"service":"n8n"}'
  python publish_event.py honey.agent.completed agent_done --data '{"agent":"research","result":"ok"}'
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from event_bus import EventBus


def main():
    parser = argparse.ArgumentParser(description="Publish an event to the Honey AI event bus")
    parser.add_argument("channel", help="Event channel (e.g. honey.cron.failed)")
    parser.add_argument("event", help="Event name (e.g. cron_failed)")
    parser.add_argument("--data", "-d", default="{}", help="JSON data payload")
    parser.add_argument("--source", "-s", default="cli", help="Event source identifier")
    parser.add_argument("--redis-url", help="Override Redis URL")
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON data: {e}", file=sys.stderr)
        sys.exit(1)

    kwargs = {}
    if args.redis_url:
        kwargs["redis_url"] = args.redis_url

    bus = EventBus(**kwargs)
    try:
        receivers = bus.publish(args.channel, args.event, data=data, source=args.source)
        print(f"✓ Published {args.event} → {args.channel} ({receivers} subscriber(s))")
    finally:
        bus.close()


if __name__ == "__main__":
    main()
