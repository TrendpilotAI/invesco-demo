# Temporal Integration for Honey AI

## Architecture

```
┌─────────────────────────────────────┐
│     Temporal Server (Railway)       │
│  temporal.railway.internal:7233     │
│  Postgres-backed durability         │
└──────────┬──────────────────────────┘
           │ gRPC
┌──────────▼──────────────────────────┐
│     Honey Worker (worker.py)        │
│  Task Queue: "honey-main"          │
│                                     │
│  Workflows:                         │
│  ├─ SelfHealingWorkflow            │
│  ├─ JudgeSwarmWorkflow             │
│  ├─ OrchestratorWorkflow           │
│  └─ HealthMonitorWorkflow          │
│                                     │
│  Activities:                        │
│  ├─ spawn_agent      (OpenClaw)    │
│  ├─ check_service_health (HTTP)    │
│  ├─ run_shell        (subprocess)  │
│  ├─ score_project    (scoring)     │
│  ├─ publish_event    (Redis)       │
│  ├─ send_notification (Telegram)   │
│  ├─ steer_agent      (drift fix)  │
│  ├─ git_push         (git ops)    │
│  └─ wait_for_agent   (polling)    │
└─────────────────────────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `activities.py` | 9 activity definitions wrapping Honey operations |
| `workflows.py` | 4 workflow definitions (self-heal, judge, orchestrate, health) |
| `worker.py` | Worker process — registers everything, connects to Temporal |
| `schedules.py` | Creates Temporal Schedules replacing cron jobs |

## Quick Start

```bash
# Start the worker
python3 /data/workspace/scripts/temporal/worker.py

# Set up schedules (run once)
python3 /data/workspace/scripts/temporal/schedules.py
```

## Workflows

### SelfHealingWorkflow
**Trigger:** Scheduled every 12h + on-demand
**Flow:** Monitor services → detect failure → spawn debug agent → verify fix → retry or escalate
**Signals:** `stop` to gracefully terminate

### JudgeSwarmWorkflow
**Trigger:** Daily schedule + on-demand
**Flow:** Fan-out judge per repo → fan-out brainstorm+plan+optimize per repo → consolidate results
**Pattern:** Parallel fan-out with dependency chains

### OrchestratorWorkflow
**Trigger:** On-demand (via API or CLI)
**Flow:** Decompose goal → parse task graph → execute respecting dependencies → publish results
**Pattern:** DAG execution with configurable parallelism

### HealthMonitorWorkflow
**Trigger:** Continuous (restarts daily via schedule)
**Flow:** Check all services every N seconds → track failure counts → alert after threshold → publish metrics
**Signals:** `stop`, `update_services` (dynamic reconfiguration)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TEMPORAL_HOST` | `temporal.railway.internal:7233` | Temporal server address |
| `TEMPORAL_NAMESPACE` | `default` | Temporal namespace |
| `TEMPORAL_TASK_QUEUE` | `honey-main` | Worker task queue name |
| `REDIS_URL` | Railway internal URL | Redis for event publishing |

## Starting a Workflow Manually

```python
from temporalio.client import Client
from workflows import OrchestratorInput

client = await Client.connect("temporal.railway.internal:7233")
result = await client.execute_workflow(
    "OrchestratorWorkflow",
    OrchestratorInput(goal="Build feature X"),
    id="my-workflow-run",
    task_queue="honey-main",
)
```

## Key Design Decisions

1. **Activities are thin wrappers** — each does one thing (spawn, check, shell, etc.)
2. **Workflows never do I/O directly** — all side effects go through activities
3. **Heartbeats on long-polling activities** — `wait_for_agent` heartbeats so Temporal can detect stuck workers
4. **Retry policies per-concern** — agent spawns get fewer retries with longer backoff; health checks retry fast
5. **Signals for control** — workflows can be stopped/reconfigured without redeployment
6. **Output capped** — shell output truncated to prevent workflow history bloat
