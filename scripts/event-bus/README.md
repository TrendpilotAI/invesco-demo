# Honey AI — Redis Event Bus

Real-time event-driven infrastructure for Honey AI. Replaces polling with instant pub/sub.

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│ Health Publisher  │────→│  Redis Pub/  │────→│ Listener +      │
│ (60s checks)     │     │  Sub Bus     │     │ Reactions Engine │
├─────────────────┤     │              │     ├─────────────────┤
│ Cron Jobs        │────→│ Channels:    │────→│ Actions:        │
│ publish_event.py │     │ honey.*      │     │ - log           │
├─────────────────┤     │              │     │ - notify_human  │
│ Subagents        │────→│              │     │ - run_command   │
│ (on complete)    │     └──────────────┘     │ - publish_event │
└─────────────────┘                           └─────────────────┘
```

## Components

| File | Purpose |
|------|---------|
| `event_bus.py` | Core EventBus (sync) + AsyncEventBus classes |
| `reactions.py` | YAML-driven reaction engine with action executors |
| `health_publisher.py` | Async daemon — monitors services, publishes state changes |
| `listener.py` | Async daemon — subscribes to `honey.*`, executes reactions |
| `publish_event.py` | CLI tool for emitting events from scripts/cron |
| `config/reactions.yaml` | Reaction definitions (channel/event matching + actions) |

## Event Channels

- `honey.service.health` — service up/down transitions
- `honey.agent.completed` — subagent finished
- `honey.agent.failed` — subagent failed
- `honey.cron.completed` — cron job finished
- `honey.cron.failed` — cron job errored

## Quick Start

```bash
# Test Redis connection
python3 -c "from event_bus import EventBus; print(EventBus().ping())"

# Publish an event
python3 publish_event.py honey.cron.failed cron_failed \
  --data '{"job":"backup","error":"timeout"}' --source mycron

# Run the listener daemon
python3 listener.py

# Run the health publisher daemon
python3 health_publisher.py
```

## Reactions Config

Edit `config/reactions.yaml` to define reactions:

```yaml
reactions:
  - name: my_reaction
    match:
      channel: "honey.service.health"
      event: "service_down"
    cooldown: 300
    actions:
      - type: notify_human
        params:
          channel: telegram
          message: "🔴 {service} is down!"
```

**Action types:** `log`, `notify_human`, `run_command`, `publish_event`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | Railway external URL | Redis connection string |
| `REACTIONS_YAML` | `config/reactions.yaml` | Path to reactions config |
| `HEALTH_CHECK_INTERVAL` | `60` | Seconds between health checks |

## Integration

From any script, emit events:
```python
from event_bus import EventBus
bus = EventBus()
bus.publish("honey.cron.failed", "backup_failed", data={"error": "timeout"}, source="backup-cron")
bus.close()
```
