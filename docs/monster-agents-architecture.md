# Monster Agents Architecture — Multi-Model Autonomous Agent Fleet

## Executive Summary

Build a fleet of fully autonomous "monster agents" — each with independent capabilities equivalent to Honey — that benchmark against each other, communicate via ACP + email, present results via A2UI, and run on ephemeral compute. All intelligence feeds back to Honey as the central orchestrator.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    HONEY (Central Brain — Opus 4)                │
│              Orchestrator · Judge · Memory Owner                 │
│              Compound Learning DB (Convex + Postgres)            │
└────────┬──────────┬──────────┬──────────┬──────────┬───────────┘
         │          │          │          │          │
    ┌────▼───┐ ┌───▼────┐ ┌──▼───┐ ┌───▼────┐ ┌──▼─────┐
    │MONSTER │ │MONSTER │ │MONST │ │MONSTER │ │MONSTER │
    │Sonnet  │ │GPT5.4  │ │Kimi  │ │Opus4   │ │DeepSk  │
    │4.6     │ │        │ │K2.5  │ │(clone) │ │        │
    └────┬───┘ └───┬────┘ └──┬───┘ └───┬────┘ └──┬─────┘
         │         │         │         │         │
    ┌────▼─────────▼─────────▼─────────▼─────────▼──────┐
    │              SHARED INFRASTRUCTURE                  │
    │  ┌──────────┐ ┌──────────┐ ┌───────────────────┐  │
    │  │Blackboard│ │AgentMail │ │ A2UI Canvas       │  │
    │  │(Convex)  │ │(inboxes) │ │ (Results UI)      │  │
    │  └──────────┘ └──────────┘ └───────────────────┘  │
    │  ┌──────────┐ ┌──────────┐ ┌───────────────────┐  │
    │  │ACP Comms │ │Browser   │ │ Ephemeral Compute │  │
    │  │(sessions)│ │(BrowserU)│ │ (Fly/Daytona)     │  │
    │  └──────────┘ └──────────┘ └───────────────────┘  │
    └───────────────────────────────────────────────────┘
```

## 1. GPT 5.4 Investigation Results

### Finding: GPT 5.4 Works Fine — OpenClaw Harness Issue

**Direct API test (March 10):**
- Model: `gpt-5.4-2026-03-05`
- Task: Merge sort with tests
- Output: 1,099 tokens, 164 lines, quality code
- Time: 15.9 seconds
- **Verdict: The model works perfectly.**

**The problem:** When spawned as an OpenClaw sub-agent, GPT 5.4 completes in 1-6 seconds with minimal output. This is likely because:
1. OpenClaw uses `max_tokens` (deprecated for GPT 5.x) — needs `max_completion_tokens`
2. The system prompt + tool definitions consume most of the context, and GPT 5.4 may be hitting a completion limit
3. GPT 5.4's "reasoning" mode may conflict with OpenClaw's tool-use harness

**Fix needed:** Update OpenClaw's model adapter for GPT 5.x family to:
- Use `max_completion_tokens` instead of `max_tokens`
- Potentially adjust system prompt format for GPT 5.x reasoning
- Test with explicit `temperature: 0.7` (GPT 5.4 may default to 0)

## 2. Model Benchmark Framework

### Models to Benchmark

| Model | Provider | ID | Cost Tier |
|-------|----------|-----|-----------|
| Claude Sonnet 4.6 | Anthropic | claude-sonnet-4-6 | Mid |
| Claude Opus 4.6 | Anthropic | claude-opus-4-6 | Premium |
| GPT 5.4 | OpenAI | gpt-5.4 | Mid-High |
| GPT 5.4 Pro | OpenAI | gpt-5.4-pro | Premium |
| Kimi K2.5 | Moonshot | kimi-k2.5 | Budget |
| DeepSeek Chat | DeepSeek | deepseek-chat | Budget |

### Benchmark Tasks

1. **Coding** — Build a FastAPI CRUD app with tests (measures: code quality, completeness, correctness)
2. **Strategic** — Write a GTM plan for a fintech product (measures: depth, actionability, insight)
3. **Debugging** — Find and fix bugs in a provided codebase (measures: accuracy, speed)
4. **Architecture** — Design a microservices system (measures: quality of design decisions)
5. **Analysis** — Analyze a financial dataset and produce insights (measures: depth, accuracy)

### Metrics Per Task

- Wall clock time (seconds)
- Tokens in / out
- Tokens per second (output)
- Cost (USD)
- Quality score (1-10, judged by Honey or another model)
- Completion rate (did it finish the task?)
- Error rate

## 3. Monster Agent Architecture

### What Makes a "Monster Agent"

Each monster agent is a fully autonomous entity with:

| Capability | Implementation |
|------------|----------------|
| Own identity | Unique name, model, personality |
| Own memory | Dedicated Convex namespace |
| Own email | AgentMail inbox (agent-name@forwardlane.agentmail.to) |
| Own browser | BrowserUse session for web tasks |
| Own compute | Ephemeral Fly.io/Daytona instance |
| Own blackboard | Read/write to shared Convex blackboard |
| ACP communication | Can message other agents via OpenClaw ACP |
| A2UI presentation | Can present findings via canvas UI |
| Reports to Honey | All learnings flow back to central compound DB |

### Agent Fleet (Initial)

| Agent Name | Model | Specialty | Email |
|------------|-------|-----------|-------|
| Athena | claude-sonnet-4-6 | Coding, architecture, refactoring | athena@forwardlane.agentmail.to |
| Apollo | gpt-5.4 | Analysis, strategy, planning | apollo@forwardlane.agentmail.to |
| Hermes | kimi-k2.5 | Quick tasks, judging, scoring | hermes@forwardlane.agentmail.to |
| Hephaestus | claude-opus-4-6 | Complex builds, deep reasoning | hephaestus@forwardlane.agentmail.to |
| Mercury | deepseek-chat | Background ops, maintenance | mercury@forwardlane.agentmail.to |

## 4. Blackboard Architecture (Convex)

The blackboard is a shared state store in Convex that all agents can read/write:

```typescript
// convex/blackboard.ts
blackboard: defineTable({
  key: v.string(),           // Namespaced key: "benchmark:sonnet:coding:result"
  value: v.any(),            // Flexible JSON value
  author: v.string(),        // Agent name
  visibility: v.union(v.literal("public"), v.literal("private"), v.literal("team")),
  expiresAt: v.optional(v.string()),
  tags: v.array(v.string()),
  createdAt: v.string(),
  updatedAt: v.string(),
})
```

## 5. ACP (Agent Communication Protocol)

OpenClaw's built-in `sessions_send` and `sessions_spawn` provide the ACP layer:
- Agents spawn as persistent sessions (`mode: "session"`)
- Can send messages to each other via `sessions_send`
- Honey can steer any agent via `subagents steer`
- All completions auto-announce back to Honey

## 6. A2UI (Agent-to-User Interface)

Use OpenClaw's canvas system to present results:
- Agents generate HTML/React dashboards
- `canvas.present` shows them to Nathan
- Real-time updates via Convex subscriptions
- Benchmark results, code diffs, strategy docs all rendered visually

## 7. Ephemeral Compute

### Fly.io Machines (Primary)
- REST API: `https://api.machines.dev/v1/apps/{app}/machines`
- Sub-second boot times
- Global distribution
- Auto-stop on idle
- Cost: ~$0.0000021/s (shared-cpu-1x)

### Daytona (Alternative)
- Workspace API for full dev environments
- Git integration, file system, process management
- Stateful snapshots across sessions
- Better for long-running dev tasks

### Usage Pattern
1. Monster agent needs compute → Honey creates Fly Machine
2. Agent runs task in isolated environment
3. Results written to Convex blackboard
4. Machine auto-destroyed after task

## 8. AgentMail Integration

```python
from agentmail import AgentMail
client = AgentMail(api_key=AGENTMAIL_API_KEY)

# Create inbox for each monster agent
inbox = client.inboxes.create(username="athena", domain="agentmail.to")
# athena@agentmail.to

# Agent can receive tasks via email
messages = client.messages.list(inbox_id=inbox.id)

# Agent can send results via email
client.messages.send(
    inbox_id=inbox.id,
    to="nathan@forwardlane.com",
    subject="Benchmark Results: Coding Task",
    body=results_html
)
```

## 9. BrowserUse Integration

For debugging, logging into services, and web verification:
- Each monster agent gets a browser session via OpenClaw's browser tool
- Used for: verifying deployments, debugging UI issues, checking external services
- NOT for general browsing — focused on authenticated debugging tasks

## 10. Implementation Phases

### Phase 1: Benchmark Framework (Today)
- [ ] Build benchmark runner script
- [ ] Run same 5 tasks across all models
- [ ] Record metrics to compound learning DB
- [ ] Present results via A2UI canvas

### Phase 2: Monster Agent Spawning (Day 2)
- [ ] Create persistent agent sessions for each model
- [ ] Set up Convex blackboard
- [ ] Wire ACP communication
- [ ] Build A2UI dashboard for agent status

### Phase 3: External Services (Day 3)
- [ ] Set up AgentMail accounts
- [ ] Install Fly.io CLI + configure
- [ ] Install Daytona CLI + configure
- [ ] Build ephemeral compute manager

### Phase 4: Full Integration (Day 4)
- [ ] Monster agents running autonomously
- [ ] Benchmark results flowing to compound learning
- [ ] A2UI dashboard live
- [ ] Email communication working
- [ ] Browser debugging functional
