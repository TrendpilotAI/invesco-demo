# Agentic Orchestrator v2

> Intelligent task decomposition, model routing, and execution with learning feedback.

## Architecture

```
                         ┌─────────────────────────┐
                         │     orchestrator.py      │
                         │   Main Reasoning Loop    │
                         │                          │
                         │  goal → decompose →      │
                         │  route → execute → learn │
                         └────────┬────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                    │
     ┌────────▼──────┐  ┌────────▼──────┐  ┌─────────▼─────┐
     │ decomposer.py │  │ model_router  │  │  executor.py  │
     │               │  │     .py       │  │               │
     │ Goal → Task   │  │ Task → Model  │  │ Graph → Run   │
     │ Graph (DAG)   │  │ (+ history)   │  │ (parallel)    │
     └───────────────┘  └───────┬───────┘  └───────┬───────┘
                                │                   │
                         ┌──────▼───────┐           │
                         │ learner.py   │◄──────────┘
                         │              │  outcomes
                         │ Postgres DB  │
                         │ Analytics    │
                         └──────────────┘
```

## Components

| File | Role |
|------|------|
| `orchestrator.py` | CLI + main loop: goal → decompose → execute → learn |
| `decomposer.py` | LLM-powered goal → task DAG with deps, prompts, criteria |
| `model_router.py` | Route tasks to optimal models by type/complexity/history |
| `executor.py` | Parallel dispatch with dep resolution, retries, monitoring |
| `learner.py` | Postgres outcome tracking, analytics, recommendation engine |

## Model Routing Table

```
┌─────────────────┬────────────────────────────────────┐
│ Task Type       │ Model                              │
├─────────────────┼────────────────────────────────────┤
│ Heavy coding    │ openai-codex/gpt-5.3-codex         │
│ Small coding    │ x-ai/grok-code-fast-1              │
│ Analysis >100K  │ google/gemini-3-flash-preview       │
│ Orchestration   │ anthropic/claude-opus-4-6           │
│ Swarms/bulk     │ kimi/kimi-k2.5                     │
│ Lightweight     │ deepseek/deepseek-chat              │
└─────────────────┴────────────────────────────────────┘
```

Routing adapts over time via learner feedback.

## CLI Usage

```bash
# Execute a goal (decompose → route → dispatch → monitor → learn)
python3 orchestrator.py goal "Make Invesco demo work end-to-end"

# Preview decomposition without executing
python3 orchestrator.py decompose "Build authentication system"

# Dry run (shows what would happen)
python3 orchestrator.py goal "Refactor API" --dry-run --yes

# Check status of all goals
python3 orchestrator.py status

# Test model routing
python3 orchestrator.py route "Build a complex REST API with auth"

# Initialize learning DB
python3 orchestrator.py learn --init

# View learning report
python3 orchestrator.py learn --report

# Get model recommendations from history
python3 orchestrator.py learn --recommend
```

## Task Graph Lifecycle

```
  Goal Text
      │
      ▼
  ┌──────────┐     ┌──────────┐
  │ Decompose │────▶│ Task DAG │
  └──────────┘     └────┬─────┘
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                  ▼
  ┌────────┐      ┌────────┐        ┌────────┐
  │ Task A │      │ Task B │        │ Task C │
  │ (root) │      │ (root) │        │dep: A,B│
  └───┬────┘      └───┬────┘        └───┬────┘
      │ model_router   │                 │
      ▼                ▼                 ▼
  ┌────────┐      ┌────────┐        ┌────────┐
  │ codex  │      │ grok   │        │ opus   │
  │subagent│      │subagent│        │subagent│
  └───┬────┘      └───┬────┘        └───┬────┘
      │                │                 │
      ▼                ▼                 ▼
  ┌──────────────────────────────────────────┐
  │           learner.py → Postgres          │
  │    Record outcomes, update routing       │
  └──────────────────────────────────────────┘
```

## Database

Postgres tables:
- `orchestrator_outcomes` — per-task results (model, type, success, duration)
- `orchestrator_goals` — per-goal aggregates

Initialize: `python3 orchestrator.py learn --init`

## Integration Points

- **Orchestrator v1**: Uses v1's dispatch mechanism for subagent spawning
- **Event Bus (P0)**: Can publish/subscribe to `honey.agent.*` events
- **Drift Correction (P1)**: Executor can integrate drift detection on long tasks
- **Temporal (P3)**: Future: wrap task graph execution as Temporal workflows
