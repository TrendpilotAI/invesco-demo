# Implementation Plan: Honey AI Next-Gen Architecture

> **Date:** 2026-02-24  
> **Author:** Honey 🍯  
> **Status:** ACTIVE  
> **North Star:** Max tokens/sec × min cost × max uptime × perfect fault tolerance

---

## Executive Summary

Three major upgrades transform Honey from a cron-driven polling system to an event-driven, self-correcting, durable multi-agent orchestration platform:

1. **P0:** Redis Event Bus → instant failure reactions (replaces 15-min polling)
2. **P1:** Mid-session drift correction → agents stay on track
3. **P2:** Agentic Orchestrator v2 → intelligent task decomposition & model routing
4. **P3:** Temporal.io Integration → 100X more durable, long-running, fault-tolerant workflows

Each builds on the previous. Temporal (P3) is the game-changer that ties everything together.

---

## Phase 0: Redis Event Bus (2-3 days)

### Why
Currently: cron polls every 15 min → failure sits undetected for up to 14 min 59 sec.  
After: event fires instantly → reaction triggers in < 1 second.

### Architecture
```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│ Health Monitor   │────→│  Redis Pub/  │────→│ Reactions Engine │
│ (60s checks)     │     │  Sub Bus     │     │ (YAML config)   │
├─────────────────┤     │              │     ├─────────────────┤
│ Cron Jobs        │────→│ Channels:    │────→│ Actions:        │
│ (on fail/success)│     │ honey.*      │     │ - spawn_agent   │
├─────────────────┤     │              │     │ - notify_human  │
│ Subagents        │────→│              │     │ - retry_task    │
│ (on complete)    │     └──────────────┘     │ - escalate      │
└─────────────────┘                           └─────────────────┘
```

### Components
| File | Purpose |
|------|---------|
| `scripts/event-bus/event_bus.py` | Core pub/sub client, event schema |
| `scripts/event-bus/reactions.py` | YAML-driven reaction engine |
| `scripts/event-bus/health_publisher.py` | Persistent daemon, state-change detection |
| `scripts/event-bus/listener.py` | Subscribes to all channels, executes reactions |
| `scripts/event-bus/publish_event.py` | CLI tool for manual/script event emission |
| `config/reactions.yaml` | Reaction definitions |

### Event Channels
- `honey.service.health` — service up/down transitions
- `honey.agent.completed` — subagent finished successfully
- `honey.agent.failed` — subagent failed
- `honey.cron.completed` — cron job finished
- `honey.cron.failed` — cron job errored
- `honey.deploy.status` — Railway deploy events
- `honey.agent.drift` — drift detected in running agent

### Redis
- Internal: `redis://default:n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E@redis.railway.internal:6379`
- External: `redis://default:n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E@trolley.proxy.rlwy.net:11973`

### Deliverables
- [ ] Event bus core with pub/sub
- [ ] Reactions engine with YAML config
- [ ] Health monitor daemon (replaces rapid-health cron)
- [ ] Listener daemon with action execution
- [ ] CLI publish tool
- [ ] Integration with existing cron jobs (emit events on fail)

---

## Phase 1: Mid-Session Drift Correction (2 days)

### Why
Agents running 20-40+ minutes can go off-track — scope creep, rabbit holes, over-engineering. No current mechanism to detect or correct this.

### Architecture
```
┌───────────────┐     ┌──────────────┐     ┌─────────────────┐
│ Drift Detector │────→│ Drift Score  │────→│ Corrector       │
│ (60s polling)  │     │ 0-10 scale   │     │                 │
│                │     │              │     │ Score < 6: OK   │
│ Checks:        │     │ Lightweight  │     │ Score 6-8: Steer│
│ - runtime      │     │ model eval   │     │ Score 8+: Kill  │
│ - progress     │     │              │     │ & respawn       │
│ - alignment    │     └──────────────┘     └─────────────────┘
└───────────────┘
```

### Components
| File | Purpose |
|------|---------|
| `scripts/drift-correction/drift_detector.py` | Monitors running agents, scores drift |
| `scripts/drift-correction/corrector.py` | Sends steer commands or kills/respawns |
| `scripts/drift-correction/intent_tracker.py` | Stores original intent + checkpoints |
| `scripts/drift-correction/strategies.py` | Drift type detection + correction templates |

### Drift Types & Corrections
| Type | Signal | Correction |
|------|--------|------------|
| Scope creep | Adding unasked features | "Focus only on {original_scope}" |
| Rabbit hole | Deep in tangent | "Skip {tangent}, priority is {goal}" |
| Over-engineering | Building abstractions | "Keep it simple. MVP approach." |
| Wrong approach | Bad path chosen | "Stop. Try {alternative} instead." |
| Stalled | Loop/no progress | Kill & respawn with hints |

### Integration
- Publishes `honey.agent.drift` events to event bus
- Uses `subagents steer` for mid-session corrections
- Tracks correction success rates for learning

### Deliverables
- [ ] Drift detector daemon
- [ ] Correction engine with strategy selection
- [ ] Intent tracker (auto-registers on spawn)
- [ ] Learning feedback loop
- [ ] CLI: `drift_detector.py status` and `drift_detector.py correct`

---

## Phase 2: Agentic Orchestrator v2 (1 week)

### Why
Current orchestrator is a dispatch script. It does what it's told.  
New orchestrator REASONS about what to do — decomposes goals, picks models, manages dependencies, learns from outcomes.

### Architecture
```
┌──────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR v2 (Opus 4-6)                 │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │ Decomposer   │  │ Model Router │  │ Execution Engine   │  │
│  │              │  │              │  │                    │  │
│  │ Goal → Tasks │  │ Task → Model │  │ Tasks → Subagents  │  │
│  │ + Dependencies│  │ + History   │  │ + Monitoring       │  │
│  └──────────────┘  └──────────────┘  └────────────────────┘  │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │ Learning     │  │ Event Bus    │  │ Drift Correction   │  │
│  │ Engine       │  │ Integration  │  │ Integration        │  │
│  │              │  │              │  │                    │  │
│  │ Outcomes →   │  │ Reacts to    │  │ Steers agents      │  │
│  │ Better routing│  │ failures    │  │ mid-session        │  │
│  └──────────────┘  └──────────────┘  └────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Model Routing Table
| Task Type | Complexity | Context | Model |
|-----------|-----------|---------|-------|
| Heavy coding | High | Any | `openai-codex/gpt-5.3-codex` |
| Small coding | Low | Small | `x-ai/grok-code-fast-1` |
| Analysis | Any | >100K tokens | `google/gemini-3-flash-preview` |
| Orchestration | High | Any | `anthropic/claude-opus-4-6` |
| Swarms/bulk | Any | Any | `kimi/kimi-k2.5` |
| Lightweight | Low | Small | `deepseek/deepseek-chat` |

### Components
| File | Purpose |
|------|---------|
| `scripts/orchestrator-v2/orchestrator.py` | Main agentic loop |
| `scripts/orchestrator-v2/decomposer.py` | Goal → task graph |
| `scripts/orchestrator-v2/model_router.py` | Intelligent model selection |
| `scripts/orchestrator-v2/executor.py` | Task graph execution engine |
| `scripts/orchestrator-v2/learner.py` | Outcome tracking + learning |

### Deliverables
- [ ] Agentic orchestrator with goal decomposition
- [ ] Model router with historical learning
- [ ] Execution engine with dependency management
- [ ] Learning engine with Postgres persistence
- [ ] CLI interface
- [ ] Integration with event bus and drift correction

---

## Phase 3: Temporal.io Integration — The Game Changer (1-2 weeks)

### Why Temporal Changes Everything

Temporal.io is a **durable execution engine**. It makes workflows survive crashes, restarts, and failures automatically. Here's why this is a 100X improvement for our multi-agent system:

### Current Problems Temporal Solves

| Problem | Current | With Temporal |
|---------|---------|---------------|
| **Agent crashes mid-task** | Lost. Have to restart from scratch. | Automatically resumes from exact point of failure. |
| **Server restarts** | All running agents die. Cron restarts from scratch. | Workflows survive restarts. Resume exactly where they left off. |
| **Long-running tasks (hours/days)** | Timeout after 15-60 min. State lost. | Runs for days/weeks. State persisted durably. |
| **Complex dependencies** | Manual tracking via blackboard JSON | Native workflow DAG with automatic dependency resolution. |
| **Retry logic** | Hand-coded retry 3x in prompts | Configurable retry policies per activity (exponential backoff, max attempts, timeouts). |
| **Parallel execution** | `sessions_spawn` with 5/5 limit | Native parallel execution with configurable concurrency. |
| **Observability** | Black box until done | Temporal Web UI shows every step, every retry, every timer, every signal. |
| **Agent coordination** | Blackboard JSON files | Temporal signals and queries — type-safe inter-workflow communication. |
| **Scheduling** | Cron jobs via OpenClaw CLI | Temporal Schedules — same cron expressions but with full durability. |
| **Failure cascades** | One failure can orphan child agents | Child workflows automatically cancelled or compensated. |

### Architecture with Temporal

```
┌─────────────────────────────────────────────────────────────────┐
│                      TEMPORAL SERVER                              │
│                 temporal.railway.internal:7233                     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    WORKFLOW DEFINITIONS                       │  │
│  │                                                               │  │
│  │  ┌──────────────────┐  ┌──────────────────────────────────┐  │  │
│  │  │ JudgeSwarmWF     │  │ SelfHealingWF                    │  │  │
│  │  │                  │  │                                  │  │  │
│  │  │ for each repo:   │  │ monitor health                   │  │  │
│  │  │   judge()        │  │ on failure:                      │  │  │
│  │  │   brainstorm()   │  │   debug_agent()                  │  │  │
│  │  │   plan()         │  │   ops_agent()                    │  │  │
│  │  │   optimize()     │  │   qa_verify()                    │  │  │
│  │  │   consolidate()  │  │   if still_broken: escalate()    │  │  │
│  │  └──────────────────┘  └──────────────────────────────────┘  │  │
│  │                                                               │  │
│  │  ┌──────────────────┐  ┌──────────────────────────────────┐  │  │
│  │  │ InvescoSprintWF  │  │ OrchestratorWF                   │  │  │
│  │  │                  │  │                                  │  │  │
│  │  │ seed_data()      │  │ decompose_goal()                 │  │  │
│  │  │ wire_frontend()  │  │ for task in tasks:               │  │  │
│  │  │ build_demo()     │  │   route_model()                  │  │  │
│  │  │ test_e2e()       │  │   execute_with_retry()           │  │  │
│  │  │ report()         │  │   learn_from_outcome()           │  │  │
│  │  └──────────────────┘  └──────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    ACTIVITY DEFINITIONS                       │  │
│  │                                                               │  │
│  │  spawn_agent()      — OpenClaw sessions_spawn wrapper        │  │
│  │  check_service()    — HTTP health check                      │  │
│  │  run_shell()        — Execute shell command                  │  │
│  │  score_project()    — Run scoring script                     │  │
│  │  publish_event()    — Redis event bus publish                │  │
│  │  send_notification()— Telegram/Slack alert                   │  │
│  │  query_postgres()   — DB operations                          │  │
│  │  steer_agent()      — Mid-session drift correction           │  │
│  │  git_push()         — Commit and push changes                │  │
│  │  wait_for_agent()   — Poll/wait for subagent completion      │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      TEMPORAL WORKER                              │
│                 (Python, runs alongside OpenClaw)                  │
│                                                                   │
│  Registers all workflows + activities                             │
│  Connects to temporal.railway.internal:7233                       │
│  Task queue: "honey-main"                                         │
│  Scales horizontally (can run multiple workers)                   │
└─────────────────────────────────────────────────────────────────┘
```

### Key Temporal Patterns for Honey

#### 1. Judge Swarm as Temporal Workflow
```python
@workflow.defn
class JudgeSwarmWorkflow:
    @workflow.run
    async def run(self, repos: list[str]):
        # Fan-out: judge all repos in parallel
        results = await asyncio.gather(*[
            workflow.execute_activity(
                judge_repo, repo,
                start_to_close_timeout=timedelta(minutes=30),
                retry_policy=RetryPolicy(maximum_attempts=3)
            )
            for repo in repos
        ])
        
        # For each judged repo, fan-out brainstorm + plan + optimize
        for result in results:
            await asyncio.gather(
                workflow.execute_activity(brainstorm_repo, result),
                workflow.execute_activity(plan_repo, result),
                workflow.execute_activity(optimize_repo, result),
            )
        
        # Consolidate all learnings
        await workflow.execute_activity(consolidate_learnings)
```

**Why this is better:** If the server crashes after judging 10 of 15 repos, Temporal resumes from repo 11 — doesn't redo the first 10.

#### 2. Self-Healing as Temporal Workflow
```python
@workflow.defn
class SelfHealingWorkflow:
    @workflow.run
    async def run(self, service_name: str, failure_details: dict):
        for attempt in range(3):
            # Run debug + ops agents in parallel
            debug_result, ops_result = await asyncio.gather(
                workflow.execute_activity(run_debug_agent, service_name, failure_details),
                workflow.execute_activity(run_ops_agent, service_name, failure_details),
            )
            
            # Wait, then verify
            await workflow.sleep(timedelta(minutes=2))
            health = await workflow.execute_activity(check_service_health, service_name)
            
            if health.status == "healthy":
                await workflow.execute_activity(run_qa_verification, service_name)
                await workflow.execute_activity(log_learning, "fixed", attempt)
                return "resolved"
        
        # All retries failed — escalate
        await workflow.execute_activity(escalate_to_human, service_name, failure_details)
        return "escalated"
```

**Why this is better:** The retry loop, the wait, the escalation — all durable. Server can crash and restart at any point and the workflow continues.

#### 3. Orchestrator Goal as Temporal Workflow
```python
@workflow.defn  
class OrchestratorWorkflow:
    @workflow.run
    async def run(self, goal: str):
        # Decompose goal into tasks (uses Opus)
        task_graph = await workflow.execute_activity(decompose_goal, goal)
        
        # Execute tasks respecting dependencies
        completed = set()
        while not all_done(task_graph, completed):
            ready = get_ready_tasks(task_graph, completed)
            results = await asyncio.gather(*[
                workflow.execute_activity(
                    execute_task, task,
                    start_to_close_timeout=timedelta(minutes=task.estimated_minutes * 2),
                    retry_policy=RetryPolicy(maximum_attempts=3)
                )
                for task in ready
            ])
            for task, result in zip(ready, results):
                completed.add(task.id)
                await workflow.execute_activity(learn_from_outcome, task, result)
```

**Why this is better:** Complex multi-step goals with dependencies survive any failure. Temporal tracks exactly which steps completed.

#### 4. Cron Jobs as Temporal Schedules
```python
# Replace OpenClaw cron with Temporal Schedules
await client.create_schedule(
    "judge-swarm-daily",
    Schedule(
        action=ScheduleActionStartWorkflow(JudgeSwarmWorkflow.run, repos),
        spec=ScheduleSpec(cron_expressions=["0 3 * * *"]),
    ),
)
```

**Why this is better:** If the workflow takes 2 hours, Temporal handles overlap policies, catch-up runs, and pause/resume.

### Temporal Superpowers We'd Gain

| Superpower | Impact |
|------------|--------|
| **Durable timers** | `workflow.sleep(hours=8)` survives restarts. No need for cron. |
| **Signals** | Send real-time commands to running workflows (like drift correction). |
| **Queries** | Ask running workflows their status without interrupting. |
| **Child workflows** | Each agent is a child workflow — automatic lifecycle management. |
| **Continue-as-new** | Long-running workflows reset their history to avoid memory bloat. |
| **Search attributes** | Tag workflows with metadata — query by project, priority, model. |
| **Versioning** | Deploy new workflow code without breaking running workflows. |
| **Temporal Web UI** | Built-in dashboard showing all workflows, their status, history. |

### Implementation Plan

#### Week 1: Foundation
- [ ] Create `/data/workspace/scripts/temporal/` directory
- [ ] Define activity functions wrapping OpenClaw operations
- [ ] Build worker that connects to `temporal.railway.internal:7233`
- [ ] Convert `self-healing` flow to Temporal workflow (simplest, highest value)
- [ ] Convert `health-monitor` to Temporal workflow with durable timer
- [ ] Test: kill worker mid-workflow, restart, verify it resumes

#### Week 2: Full Migration
- [ ] Convert judge swarm to Temporal workflow with parallel fan-out
- [ ] Convert orchestrator v2 goal execution to Temporal workflow
- [ ] Convert all 9 cron jobs to Temporal Schedules
- [ ] Add drift correction as Temporal signals to agent workflows
- [ ] Add event bus publishing from Temporal activities
- [ ] Build Temporal Web UI access (port forward or expose on Railway)
- [ ] Integrate with Postgres learning engine

### Deliverables
- [ ] Temporal worker process (runs alongside OpenClaw)
- [ ] 4+ workflow definitions (self-heal, judge-swarm, orchestrator, health-monitor)
- [ ] 10+ activity definitions (spawn_agent, check_health, git_push, etc.)
- [ ] Temporal Schedules replacing all 9 cron jobs
- [ ] Documentation + architecture diagram

---

## Implementation Timeline

```
Week 1 (Feb 24-28):
├── Day 1-2: P0 — Redis Event Bus (core + reactions + health daemon)
├── Day 3-4: P1 — Drift Correction (detector + corrector + strategies)
└── Day 5:   P3 — Temporal foundation (worker + self-healing workflow)

Week 2 (Mar 1-5):
├── Day 1-2: P2 — Agentic Orchestrator v2 (decomposer + router + executor)
├── Day 3-4: P3 — Temporal full migration (judge swarm + crons → schedules)
└── Day 5:   P3 — Integration testing + Temporal Web UI + docs

Week 3 (Mar 6-7):
├── Day 1:   Integration — Wire event bus + drift + orchestrator + Temporal
└── Day 2:   Production hardening + monitoring + cost analysis
```

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Failure detection time | Up to 15 min | < 5 seconds |
| Agent drift rate | Unknown (no tracking) | < 10% of sessions |
| Workflow survival on crash | 0% (all lost) | 100% (Temporal durable) |
| Model routing accuracy | Manual/static | 90%+ automated |
| Max sustained workflow duration | ~60 min (timeout) | Days/weeks (Temporal) |
| Parallel agent capacity | 5 (hardcoded) | 50+ (Temporal workers) |
| Learning from outcomes | Manual memory files | Automated Postgres + feedback |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Temporal adds complexity | Start with one workflow (self-healing), expand gradually |
| Redis event bus reliability | Redis already running; pub/sub is battle-tested |
| Drift correction false positives | Start with conservative thresholds (score > 8 only) |
| Orchestrator v2 cost (Opus for decomposition) | Cache decomposition results; use for complex goals only |
| Migration disruption | Run Temporal and cron in parallel during transition |

---

*This plan transforms Honey from a cron-driven polling system into a durable, event-driven, self-correcting AI mesh. Temporal is the backbone that makes everything 100X more resilient.*
