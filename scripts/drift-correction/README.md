# Mid-Session Drift Correction

Detects and corrects AI agent drift during long-running sessions.

## Architecture

```
┌───────────────┐     ┌──────────────┐     ┌─────────────────┐
│ Drift Detector │────→│ Drift Score  │────→│ Corrector       │
│ (60s polling)  │     │ 0-10 scale   │     │                 │
│                │     │              │     │ Score < 6: OK   │
│ Checks:        │     │ Heuristic +  │     │ Score 6-8: Steer│
│ - runtime      │     │ model eval   │     │ Score 8+: Kill  │
│ - progress     │     │              │     │ & respawn       │
│ - alignment    │     └──────────────┘     └─────────────────┘
└───────────────┘
        │
        ▼
┌───────────────┐     ┌──────────────┐
│ Intent Tracker │     │ Strategies   │
│                │     │              │
│ Stores:        │     │ Drift types: │
│ - original task│     │ - scope_creep│
│ - checkpoints  │     │ - rabbit_hole│
│ - drift scores │     │ - over_eng.  │
│ - corrections  │     │ - wrong_path │
└───────────────┘     │ - stalled    │
                      └──────────────┘
```

## Components

| File | Purpose |
|------|---------|
| `drift_detector.py` | Main daemon — monitors agents, scores drift, triggers corrections |
| `corrector.py` | Applies corrections via `openclaw subagents steer` or kill/respawn |
| `intent_tracker.py` | Persists original task intent and checkpoints to JSON |
| `strategies.py` | Drift type definitions, detection heuristics, correction templates |

## Usage

```bash
# Run as daemon (polls every 60s)
python drift_detector.py run

# One-shot check of all running agents
python drift_detector.py check

# Show current status
python drift_detector.py status

# Custom poll interval
DRIFT_POLL_INTERVAL=30 python drift_detector.py run
```

## Drift Types

| Type | Signal | Default Action |
|------|--------|---------------|
| **Scope creep** | Adding unasked features | Steer (≥6.0) |
| **Rabbit hole** | Deep in tangent | Steer (≥6.0) |
| **Over-engineering** | Unnecessary abstractions | Steer (≥6.0) |
| **Wrong approach** | Bad path chosen | Steer (≥7.0) |
| **Stalled** | Loop/no progress | Kill & respawn (≥8.0) |

Severity ≥8.5 on any type escalates to kill/respawn.

## State Files

- `/data/workspace/.orchestrator/intents.json` — Agent intents and checkpoints
- `/data/workspace/.orchestrator/drift-corrections.json` — Correction history log

## Event Bus Integration

Publishes `honey.agent.drift` events when drift is detected. Requires the event bus at `../event-bus/event_bus.py`. Falls back gracefully if unavailable.

## Integration with Orchestrator

- **Intent registration**: Call `IntentTracker.register()` when spawning agents
- **Drift monitoring**: Run `drift_detector.py run` as a background daemon
- **Correction feedback**: Check `Corrector.success_rate()` for learning loop
