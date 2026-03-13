# OpenClaw Manifest – Workspace Protocols, Routing, and Agent Behavior

Last updated: 2026-03-13

## Purpose
This MANIFEST.md defines universal rules, workflows, and infrastructure protocols for OpenClaw—ensuring consistent agent, workflow, memory, and automation behavior for both single- and multi-tenant (enterprise) deployments.

---

## Core Sections
1. **Identity & Team**
2. **Workflow & Routing Rules**
3. **Memory & Database Protocols**
4. **Automation/Integration Points**
5. **Multi-User & Multi-Tenant Considerations**
6. **Security & Governance**

---

## 1. Identity & Team
- Primary Operator agent: `Honey` (see SOUL.md for personality, boundaries)
- Users defined in `USER.md`, `IDENTITY.md`
- Supports multiple users: each with unique roles, notification, and ownership config
- Multi-tenant design: agents distinguish between multiple clients/orgs (see PROJECT and TENANT files, or via integration with identity directories)

## 2. Workflow & Routing Rules
- All incoming requests/events are classified by type (ops, dev, support, automation, admin, etc.)
- **Skill-based routing:**
    - Each request is matched to one or more skills by trigger phrase, context, or target object (see SKILL.md per skill)
    - Agents auto-select best model/tool or escalate to user if ambiguous
- **Session protocol:**
    - Sessions are scoped to the requestor/user + project/tenant
    - Agents always log all significant actions to Convex (live state), LanceDB (semantic memory), and Postgres (durability)
- **Parallel execution allowed:** agents can spawn swarms, subagents, and sub-tasks, but must log all sub-task results to parent session/state
- **Heartbeats & Cron**: See `HEARTBEAT.md` for periodic tasks, error handling, notification policy

## 3. Memory & Database Protocols
- Canonical source for live ops state: Convex (real-time dashboard and UX integration)
- Long-term and audit: Postgres (for compliance, BI, backtest)
- Rapid semantic/contextual search: LanceDB (vectors for fast LLM retrieval)
- Volatile/session work/state: Redis (hot cache, pub/sub, event queue)
- **n8n used for integration/event-driven glue**, can both read from all of the above and trigger actions back
- **All records include cross-IDs for traceability** (e.g., Linear/Convex/Postgres/LanceDB ID linkage)

## 4. Automation/Integration Points
- **n8n:** Handles cross-database syncs, third-party integrations (e.g., Slack, Linear, S3), automation of repetitive multi-step processes
- **Workflows must be documented** in this MANIFEST or in a dedicated WORKFLOWS.md.
- Custom workflows are versioned here for clarity, e.g.:
  - "When a new critical Linear issue is created, notify Ops, log to Postgres, index in LanceDB, trigger agent review, and alert stakeholders via Slack."
  - "When a session ends, auto-summarize (LLM) and log learnings to both MEMORY.md and Convex."

## 5. Multi-User & Multi-Tenant Enterprise Readiness
- **User management:**
    - Each user (or team) assigned roles (admin, reviewer, dev, guest, etc.)
    - Notifications/policies can be targeted per role/project/tenant.
- **Tenant isolation:**
    - All session memory, routes, automations, LLM state, and dashboards are partitioned by tenant
    - No cross-tenant leakage permitted (agents must validate routing before acting)
    - LanceDB vectors include a tenant/org/project key in metadata for accurate scoping
    - All logs/events/actions in Postgres/Convex/n8n are tenant-tagged
- **API keys, credentials, secrets** per tenant—never globally shared
- **Audit:** All actions stamped with user & tenant for accountability

## 6. Security & Governance
- **All data actions logged** (write, update, delete) with timestamp, user, agent, origin
- **Secrets NEVER leave the system** (see SOUL.md, AGENTS.md for security boundaries)
- Agents never share cross-tenant data without explicit human approval
- **Self-healing:** All errors, rate-limits and failures trigger notification, log to Postgres + Convex, and optionally spawn correction agents

---

## How to Expand
- New workflows: Add as Markdown blocks in MANIFEST.md or a new WORKFLOWS.md with title, trigger, agents, actions, expected result
- New tenants/users: Add to USER.md, apply onboarding SOP, and ensure role/partition assignment in DB
- Changing agent behavior: Edit SOUL.md, AGENTS.md, and this file for clarity and transparency

---

*This manifest is versioned, auditable, and should be reviewed quarterly and after each major infra or workflow change. For development or incident-response agents, see skill-specific SKILL.md docs.*
