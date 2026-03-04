# Project Intelligence OS — Architecture Spec
## Nathan Stevenson × Honey — March 4, 2026

## Vision
A living, self-updating intelligence platform that tracks every project across its full lifecycle 
(SDLC → GTM → Revenue) with compound learning built in. Not a dashboard — an operating system 
for decision-making and project velocity.

---

## Core Concepts

### 1. Project Dossier
Standardized situational intelligence report per project. Always current. Always structured the same way.

**Sections:**
- Executive Summary (2-sentence AI-generated status)
- SDLC Progress (where in the pipeline: Idea → Dev → Testing → Staging → Production → Scale)
- GTM Planning (ICP, positioning, messaging, channels, launch readiness)
- GTM Architecture (tech stack for distribution: CRM, analytics, automation)
- Sales Pipeline (leads, stages, deal value, velocity)
- Insight Cards: What's Working | What's Not | Production Readiness | SWOT
- Playbooks (per-section checklists with completion tracking)
- Streaming project updates (live feed of agent actions on this project)

### 2. Global Scoring Rubric (GSR)
Applied consistently across ALL projects. 12 dimensions, each scored 0-10.

**Dimensions:**
- `sdlc_completeness` — % of SDLC stages complete
- `code_quality` — tests, type coverage, lint, complexity
- `security_posture` — vulns, auth, secrets hygiene, OWASP
- `qa_quality` — test coverage %, integration tests, E2E
- `deployment_health` — uptime, build success rate, latency
- `gtm_readiness` — ICP defined, messaging done, channels ready
- `sales_pipeline` — leads qualified, demos scheduled, ARR potential
- `revenue_proximity` — how many steps to first dollar
- `strategic_value` — alignment with ForwardLane/SignalHaus north star
- `velocity` — tasks completed per day (trailing 7d)
- `tech_debt` — mypy errors, deprecated deps, TODOs in code
- `market_timing` — urgency of the opportunity (competitor moves, deadlines)

**Composite score** = weighted average (weights configurable per project type)

### 3. Agentic Trajectory Store
Every single agent action is logged as a trajectory event:

```typescript
interface AgentTrajectory {
  id: string
  timestamp: Date
  projectName: string
  sessionKey: string
  agentModel: string
  
  // State before
  stateBefore: {
    scores: Record<string, number>  // GSR snapshot
    openTasks: number
    lastCommit: string
  }
  
  // Action
  action: {
    type: 'code_change' | 'deploy' | 'research' | 'plan' | 'communicate'
    description: string
    filesChanged: string[]
    toolsUsed: string[]
    reasoning: string  // agent's chain of thought
    tokensUsed: number
    costUsd: number
  }
  
  // State after
  stateAfter: {
    scores: Record<string, number>
    openTasks: number
    lastCommit: string
  }
  
  // Delta
  scoreDelta: Record<string, number>  // what changed
  
  // Human feedback (RLHF)
  humanFeedback?: {
    rating: 1 | 2 | 3 | 4 | 5
    comment?: string
    correctedAction?: string
    timestamp: Date
  }
  
  // Outcome (measured 24h later)
  outcome?: {
    measuredAt: Date
    velocityImpact: number  // tasks/day change
    qualityImpact: number   // GSR delta
    wasCorrect: boolean     // did the action achieve intended result
  }
}
```

### 4. Reinforcement Learning Loop
1. Agent takes action → logs trajectory
2. Human sees result → rates it (thumbs up/down, or ignores = neutral)
3. 24h later: measure outcome metrics (did velocity go up? did tests pass?)
4. Store (state, action, reward) triplet
5. Daily: export trajectory dataset → fine-tune on ForwardLane-specific patterns
6. Over time: agents learn which actions maximize velocity on THIS codebase

---

## Database Schema (Convex)

```
projects: { name, color, type, sdlcStage, scores: GSR, updatedAt }
dossiers: { projectName, sections: {}, lastGeneratedAt, streamingUpdate }
trajectories: { ...AgentTrajectory }
playbooks: { projectName, section, steps: [{id, text, done, doneAt, doneBy}] }
scoringHistory: { projectName, timestamp, scores: GSR, composite }
kanban: { taskId, projectName, column, order, priority }
conversations: { sessionKey, projectName, messages, model, tokens, startedAt }
gtmPipeline: { projectName, leads: [], stages: [], arrPotential }
```

---

## UI Structure

```
/                    → Command Center (service health + active agents + today's velocity)
/projects            → Project grid (all projects, GSR score cards)
/projects/[name]     → Project Dossier (full situational intelligence report)
/kanban              → Global Kanban (all projects, filterable)
/kanban/[project]    → Per-project Kanban
/conversations       → Conversation log (grouped by project)
/agents              → Agent Orchestrator (dispatch, timeline, decision feed)
/trajectories        → Agentic trajectory log + RLHF feedback UI
/scoring             → GSR rubric manager + score history charts
/railway             → Railway Command Center (service cards + incident board)
/light               → Light theme version of command center
```

---

## Build Phases

### Phase 1 (Now): Foundation + Railway Command Center
- Railway service cards with inline logs + redeploy buttons
- Incident intelligence board (status.railway.com + builder health)
- Convex schema setup
- Sessions API route

### Phase 2: Project Dossier
- GSR scoring engine
- Dossier template + section rendering
- SWOT insight cards (AI-generated, cached)
- Playbooks with checklists

### Phase 3: Trajectory Store + RLHF
- Log every agent action to Convex
- Human feedback UI (rate this action)
- Outcome measurement (24h delta)
- Export pipeline for fine-tuning

### Phase 4: GTM + Sales Pipeline
- Lead tracking per project
- GTM readiness checklist
- Revenue proximity scoring

---

## Key Design Principles
- **Consistency over completeness** — every project scored the same way, always
- **Trace everything** — no action is lost, every state is saved
- **Human in the loop** — feedback UI on every trajectory event
- **Compound learning** — yesterday's data trains tomorrow's agents
- **Streaming-first** — never stale, always live

