# Research: "The Self-Improving AI System That Built Itself" by @agent_wrapper

**Source:** https://x.com/agent_wrapper/status/2025986105485733945
**Author:** Prateek Karnal (@agent_wrapper), Composio — "Orchestrator of agent orchestrators"
**Date Published:** 2026-02-23 | **Date Analyzed:** 2026-02-24
**Engagement:** 649 likes, 1,898 bookmarks, 54 RTs, 110K views

---

## Article Summary

Prateek built **Agent Orchestrator** (github.com/ComposioHQ/agent-orchestrator) — a 40K-line TypeScript system built in 8 days, mostly by AI agents that the system itself orchestrates. Key thesis: **the bottleneck in AI-assisted coding isn't the agents — it's the human coordinating them.**

### Core Architecture (8 Plugin Slots)
1. **Tracker** — pulls issues (GitHub/Linear)
2. **Workspace** — creates isolated worktrees/clones
3. **Runtime** — starts tmux sessions or processes
4. **Agent** — Claude Code, Aider, etc. works autonomously
5. **Terminal** — observe live via iTerm2 or web dashboard
6. **SCM** — creates PRs, enriches with context
7. **Reactions** — auto-respawns agents on CI failures or review comments
8. **Notifier** — pings humans only when judgment is needed

### Key Patterns
- **Self-healing CI:** CI fails → agent reads logs → fixes → pushes. 41 failures across 9 branches self-corrected. 84.6% CI success rate. One PR went through 12 fix cycles with zero human intervention.
- **Automated code review loop:** Agent creates PR → Bugbot reviews → Agent fixes → Bugbot re-reviews. 700 automated comments, 1% human.
- **Self-improving loop:** Session outcomes tracked → retrospectives → adjusts future session management. The orchestrator learns which tasks need tighter guardrails.
- **Activity detection:** Reads Claude Code's JSONL event files to determine agent state (generating, waiting, idle, finished) — doesn't rely on self-reporting.
- **Git trailers for attribution:** Every commit tracks which AI model wrote it.
- **Attention zones:** Dashboard groups sessions by what needs attention (failing CI, awaiting review, running fine).
- **Mobile orchestration (planned):** Talk to orchestrator from Telegram/Slack while on a walk.
- **Mid-session drift correction (planned):** Check agent work against original intent, inject course corrections.
- **Automatic escalation (planned):** Agent can't solve → escalate to orchestrator → escalate to human.

---

## Comparison: Agent Orchestrator vs Honey AI

### ✅ What We're Doing RIGHT

| Pattern | Article Recommends | What Honey Has |
|---|---|---|
| **Self-healing** | CI fails → agent fixes automatically | ✅ On failure → Debug Agent + Ops Agent + QA Agent → retry 3x → escalate. We actually go further with multi-agent diagnosis. |
| **Escalation chain** | Agent → orchestrator → human | ✅ retry 3x → escalate to human via Telegram. Solid. |
| **Multi-model routing** | Opus for hard stuff, Sonnet for volume | ✅ 48 models across 8 providers with model-appropriate task routing (Codex 5.3 for debug/ops, Sonnet 4-6 for QA/brainstorm). |
| **Automated review** | Bugbot + agent fix cycle | ✅ Judge Swarm v2 scores repos and spawns improvement agents. Different mechanism, same intent. |
| **Learning loop** | Track session outcomes, run retrospectives | ✅ Compound learning: LanceDB (short-term) + Postgres (long-term). Daily consolidation via cron. |
| **Orchestrator is intelligent** | "Not a dashboard, not a cron job — an agent" | ⚠️ Partial. Our orchestrator has a blackboard and dispatches subagents, but the orchestration logic itself is more scripted than agentic. |
| **Notification discipline** | Only ping humans when judgment needed | ✅ Escalation only after 3 retries fail. Good. |
| **Multiple concurrent agents** | 30 agents working in parallel | ✅ Subagent spawning, parallel dispatch via orchestrator.py. |

### ❌ What We're MISSING

| Gap | What Article Has | Impact |
|---|---|---|
| **1. Plugin architecture** | 8 swappable slots (tracker, workspace, runtime, agent, terminal, SCM, reactions, notifier) | HIGH — Our integrations are hardcoded. Can't swap GitHub for Linear, or tmux for Docker, without code changes. |
| **2. Reactions system** | YAML-configured auto-responses to events (CI fail → spawn agent, changes_requested → spawn agent, approved → notify) | HIGH — We have self-healing but it's cron-based polling, not event-driven. Their reactions are immediate and configurable. |
| **3. Activity detection** | Reads agent JSONL event files to know state without asking | MEDIUM — We don't monitor subagent activity in real-time. We wait for completion or timeout. |
| **4. Git attribution** | Every commit has git trailer identifying which model wrote it | LOW — Nice for analytics but not critical for our north star. |
| **5. Live terminal observation** | xterm.js in browser showing agent terminal in real-time | MEDIUM — We have no live visibility into subagent work. Only see results after completion. |
| **6. Attention zones** | Sessions grouped by urgency (failing, awaiting review, running fine) | MEDIUM — Our dashboard (if any) doesn't prioritize what needs human attention. |
| **7. Drift correction** | Mid-session checks against original intent | HIGH — Our agents can go off-track. No mid-session correction mechanism exists. |
| **8. Isolated workspaces** | Each agent gets its own git worktree | MEDIUM — Our subagents share workspace. Risk of conflicts. |

### 🔧 What We Could IMPROVE

| Area | Current State | Improvement |
|---|---|---|
| **Orchestration intelligence** | Scripted dispatch + blackboard | Make the orchestrator itself an agent that reasons about task decomposition, priority, and resource allocation |
| **Event-driven reactions** | Cron-based polling (every 15m-8h) | Add webhook/event listeners for immediate response to failures, completions, external events |
| **Session observability** | Black box until complete | Add structured logging + activity detection for running subagents |
| **Self-improvement tracking** | Memory files + daily consolidation | Track per-session metrics: which prompts → clean completions, which → failure spirals |

---

## Actionable Recommendations (Prioritized by North Star Impact)

### P0: Event-Driven Reactions System (HIGH impact, MEDIUM effort — 2-3 days)

Our cron-based approach means a failure at minute 1 waits up to 15 minutes for detection. An event-driven system would catch it immediately.

**Implementation:**
```yaml
# /data/workspace/config/reactions.yaml
reactions:
  subagent_failed:
    action: spawn_debug_agent
    model: openai-codex/gpt-5.3-codex
    prompt: "Subagent failed. Diagnose from logs and retry."
    max_retries: 3
    
  cron_job_failed:
    action: spawn_ops_agent
    model: openai-codex/gpt-5.3-codex
    prompt: "Cron job {job_name} failed. Read logs, diagnose, fix."
    
  health_check_degraded:
    action: spawn_healing_agent
    escalate_after: 3
```

Add a lightweight event bus (Redis pub/sub, already have Redis) that cron jobs and subagents publish to. A listener process triggers reactions immediately.

### P1: Mid-Session Drift Correction (HIGH impact, MEDIUM effort — 2 days)

Subagents sometimes over-engineer or go off-track. Add periodic checkpoints.

**Implementation:**
- When spawning a subagent, include a `checkpoint_interval` (e.g., every 5 tool calls)
- At checkpoints, a lightweight evaluator (DeepSeek for cost) checks: "Is the agent's current work aligned with the original task?"
- If drift detected → inject course correction message
- This requires OpenClaw support for mid-session steering (may already exist via `subagents steer`)

### P2: Agentic Orchestrator Upgrade (HIGH impact, HIGH effort — 1 week)

Transform orchestrator from script-based dispatch to an actual reasoning agent.

**Current:** `orchestrator.py dispatch --task "Build X" --agent sonnet`
**Target:** Tell the orchestrator WHAT you want, it figures out HOW — decomposes into subtasks, picks models, manages dependencies, handles failures, learns from outcomes.

**Implementation:**
- Wrap orchestrator.py in an agent loop (Opus-level model)
- Give it access to: task history, success/failure rates per model per task type, current system load
- Let it make decisions: "This task is similar to task-47 which failed with Sonnet — route to Opus instead"
- Store decision outcomes in Postgres for learning

### P3: Structured Session Metrics (MEDIUM impact, LOW effort — 1 day)

Track what the article calls "signal" — which prompts/tasks succeed first-try vs spiral.

**Implementation:**
```sql
CREATE TABLE session_metrics (
  id SERIAL PRIMARY KEY,
  session_id TEXT,
  task_description TEXT,
  model_used TEXT,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  success BOOLEAN,
  retry_count INT,
  failure_reasons TEXT[],
  tokens_used INT,
  cost_estimate DECIMAL
);
```

Feed this into the agentic orchestrator (P2) for learning.

### P4: Workspace Isolation for Subagents (MEDIUM impact, LOW effort — 1 day)

Prevent subagent conflicts by giving each its own workspace.

**Implementation:**
- Use git worktrees or temp directories for subagent tasks that involve file editing
- Already have Orgo for heavy isolation; for light tasks, just `cp -r` the relevant subdirectory

### P5: Live Agent Observability (LOW impact on north star, MEDIUM effort — 3 days)

Nice-to-have: see what subagents are doing in real-time.

- Add structured JSONL logging for subagent actions
- Build a simple status endpoint or Telegram command: `/agents status` → shows all running agents, current activity, progress

---

## Key Insight

The article's deepest insight: **"The ceiling isn't 'how good is Claude Code at TypeScript.' It's 'how good can a system get at deploying, observing, and improving dozens of agents working in parallel.'"**

This perfectly aligns with our north star (max tokens/sec × min cost × max uptime × perfect fault tolerance). We're optimizing the right thing. But we're doing it with cron jobs and scripts where we should be doing it with an intelligent, event-driven, self-improving orchestration agent.

**The single highest-leverage change:** Make our orchestrator event-driven (P0) and then make it agentic (P2). Everything else follows.

---

## TL;DR for Nathan

We're ahead of this article on multi-model routing and escalation chains. We're behind on event-driven reactions (we poll, they react instantly) and mid-session agent oversight. The biggest gap is that our orchestrator is a script that dispatches tasks — theirs is an AI agent that reasons about orchestration. Fixing that is our highest-leverage improvement. Start with P0 (Redis event bus for reactions, 2-3 days) then P1 (drift correction via subagent steering).
