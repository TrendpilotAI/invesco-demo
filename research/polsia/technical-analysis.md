# Polsia — Technical Analysis
**Research Date:** March 10, 2026

---

## Tech Stack (Confirmed via Public Repos & Privacy Policy)

| Layer | Technology | Source |
|-------|-----------|--------|
| Backend framework | Express.js / Node.js | r/AgentsOfAI technical analysis |
| Database | PostgreSQL (via Neon) | Privacy policy + AgentsOfAI |
| Hosting | Render | Privacy policy mentions Render |
| Code versioning | GitHub | Privacy policy + podcast |
| Primary LLM | Anthropic Claude (Opus 4.5/4.6) | Podcast transcript |
| Secondary LLM | OpenAI (Codex/GPT-4) | Podcast transcript |
| Additional LLMs | Google (mentioned) | Tech stack search |
| Browser automation | Puppeteer / Chromium | AgentsOfAI analysis |
| Billing | Stripe Connect | Podcast + privacy policy |
| Ads integration | Meta CAPI | Privacy policy |
| Context protocol | MCP (Model Context Protocol) | Tech stack search |
| Frontend | SPA (React likely) | Cannot crawl — JS-rendered |

---

## Agent Architecture (Detailed)

### Company Instance Structure
Each user-registered "company" gets provisioned with:
- Dedicated web app (deployed on Render)
- PostgreSQL database (Neon instance)
- GitHub repository (code lives here)
- Email address (for company communications)
- Stripe account (via Stripe Connect — enables the 20% revenue share)
- Meta Ads account (for autonomous ad campaigns)

### Orchestration Model
- **Not a single agent** — an orchestration layer running specialized agents in parallel
- Each agent has a **role/mission + tools**
- Agents can **request features from each other** (not just humans)

### Confirmed Agent Types
1. **PM Agent** — Prioritizes feature requests, analyzes what's most requested, creates development tickets
2. **Engineer Agent (Builder)** — Writes code, fixes bugs, implements features
3. **QA Agent** — Runs unit tests + integration tests, makes push-to-production recommendations
4. **Cold Reach Agent** — Handles B2B outreach (uses Hunter.io-style email database for addresses)
5. **Meta Ads Agent** — Creates UGC-style video ads (uses Subtitle API), launches campaigns, monitors performance daily, creates new ads based on results
6. **Support Agent** — Responds to user emails, escalates complex issues
7. **Investor/Fundraising Agent** — Handles investor inquiries via email (new, experimental)
8. **Planning/Strategy Agent** — Wakes daily, assesses state, determines "best next step"

### Daily Cycle Logic
```
Every day (or more frequently):
1. Strategy agent wakes, assesses: bugs? marketing? feature requests?
2. If production bug → prioritize fix before marketing
3. If product is stable → allocate to marketing/outreach/ads
4. Cold reach agent: checks memory for company-specific preferences, runs outreach
5. Ads agent: checks performance metrics, creates new ad content if needed
6. Engineer agent: handles feature queue, builds, QA tests
7. All agents: report status → user receives daily email summary
```

### Memory Architecture
**Two-tier memory system:**

1. **Company-specific memory files** — per-company context stored as markdown files in the codebase
   - Company background, preferences, tone
   - What outreach has been done
   - What customers said
   - Learned constraints (e.g., "don't reach out to famous people")

2. **Shared cross-company memory files** — global best practices learned from all companies
   - "Emojis in email subject lines improve response rates"
   - Any pattern that holds across multiple companies
   - This is the network effect — more companies = smarter shared memory

**Implementation:** Markdown files in the repository. Simple but effective. Could be a liability at scale (not a proper vector DB, but pragmatic for where they are).

---

## MCP Integration Strategy

Polsia uses the Model Context Protocol for "live data integrations." Specifically:
- MCP provides standardized tool interfaces for LLMs
- Allows agents to access real-time data without custom integration code per service
- Described as "USB-C for AI" — plug-and-play external tool connections

This means Polsia agents can access current data from any MCP-compatible service — which as of 2026 includes a rapidly growing ecosystem of enterprise tools.

---

## Claude Code / Agent SDK Usage

Ben's development workflow relies heavily on Claude Code:
- Uses the **Anthropic Agents SDK** (not just the API)
- **Skills system** in Claude Code — creates reusable skill files for testing, deployment verification, monitoring
- **Workflow:** Build feature with Opus → create "verification skill" → call skill post-deploy to test → iterate

**Quote from Ben:**
> "When it's done building a feature, I say 'create a new skill called check-that-the-improvement-worked-in-production.' It knows all the context of what it changed. Then after I push to production, I call that skill from the CLI and it gives me a report."

This is sophisticated use of the Claude Code skills system. We should replicate this in our development workflow immediately.

---

## Polsia's Own Platform Is Self-Healing (Partially)

The platform itself follows the same pattern as the companies it builds:
- **User feedback → PM Agent → Engineer Agent → QA Agent → Production**
- Currently: Ben reviews before final prod push ("conservative mode")
- Ben's goal: full autonomy where the platform builds itself without him

**This is eating the dogfood at maximum intensity** — building the product with the product. Smart.

---

## Known Technical Issues / Vulnerabilities (Found in Research)

1. **Google OAuth consent screen in "Testing" mode** — blocking most users who try to authenticate via Google. This would significantly limit sign-ups. Critical bug.

2. **Internal platform references exposed to customers** — the payment method update modal was showing internal Polsia platform references that customers shouldn't see. Data hygiene issue.

3. **"Made with 5 Dollar Website" branding** — references found suggesting Polsia may be using a template called "5 Dollar Website" for company frontends. This is the template that appears as the company websites — explains why they look like empty templates. The "Made with 5 Dollar Website" branding being visible is a credibility problem.

4. **Hallucination in investor agent** — Ben confirmed his fundraising agent scheduled a meeting (with calendar invite) without confirming with him first. Trust/safety issue with autonomous agents taking actions.

5. **Black box agent behavior** — No audit trail for why agents made specific decisions. Makes it hard to debug or build trust.

---

## Comparison to Our Architecture (Honey/Odin)

| Aspect | Polsia | Honey/Odin (Our Approach) |
|--------|--------|--------------------------|
| Primary LLM | Claude Opus (Anthropic) | Claude Opus (Anthropic) |
| Memory system | Markdown files in repo | LanceDB + Postgres (richer) |
| Agent framework | Custom orchestration | Custom orchestration |
| Company instances | One per user | TBD — per project/division |
| Revenue model | $50/mo + 20% rev share | TBD |
| Auditability | None (black box) | **Opportunity: build this** |
| Code transparency | Public repos (GitHub) | Private/internal |
| Scale | 3,300+ companies | Starting |
| Enterprise-readiness | Low | High (target) |
| Self-healing | Partial, needs Ben | Target: full autonomy |

---

## What We Can Learn From Their Tech Stack

1. **Simplicity wins at speed** — Express/Node + Postgres is basic. They moved fast because of it. We should not over-engineer our initial stack.
2. **Markdown files as agent memory** — simple, works, can be upgraded later
3. **Skills in Claude Code** — this is underrated. Build skills for everything. Reusable automation compounds.
4. **Cross-company learning** — the shared memory pattern is genuinely valuable. Implement from Day 1.
5. **Stripe Connect from the start** — enables the revenue share model. Even if we don't take a rev share, the integration is table stakes.
6. **Daily agent cycles** — scheduled wakeups to assess and execute. Don't just respond to user commands.
7. **The "tell Ben" conservative mode** — smart default. Let humans approve until you trust the agent fully.

---

## What We Should Do Differently

1. **Vector DB for memory** — Polsia uses markdown files. We already have LanceDB. This is a real competitive advantage in memory quality.
2. **Audit trail** — Every agent action should be logged with rationale. This is the feature that unlocks enterprise trust.
3. **Structured agent outputs** — Don't just have agents write free-form notes; use typed schemas so outputs are machine-parseable.
4. **Multi-model routing** — Polsia uses Opus for product + Codex for engineering review. We should build this into our architecture formally.
5. **Real company provisioning** — Don't just spin up frontend templates. Ensure companies have working backends and real transaction capability from day 1.
6. **Google OAuth fix** — If we ever build OAuth, test it outside "testing mode" before launch. This is an embarrassing bug.
