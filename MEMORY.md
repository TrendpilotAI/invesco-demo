# MEMORY.md - Honey's Long-Term Memory

## Nathan Stevenson
- Runs **ForwardLane.com** and **SignalHaus.ai** (not SignalHouse)
- Wants a proactive AI that operates across marketing, sales, finance, engineering, customer support, and client engagements
- Security is paramount — no credential sharing, no conversation access for third parties
- Values directness and action over fluff

- Based in **Fort Lauderdale, Florida** (US Eastern time)

## Environment
- As of 2026-02-13: Running on **Railway** (OpenClaw Railway template)
- Exec/shell access requires a paired node — not yet configured
- GitHub CLI installed but not authenticated

## Projects
- **FlipMyEra** (flipmyera.com) — Taylor Swift ebook creator, deployed on Netlify, Clerk auth, Stripe payments, Supabase backend. Closest to ship. GitHub: TrendpilotAI/flip-my-era
- **NarrativeReactor** — AI content engine for Signal Studio / ForwardLane marketing. Highest strategic leverage.
- **fast-browser-search** — Rust + graph DB browser history search. Best as OSS portfolio piece.
- **thinkchain** — Claude streaming demo (forked). Most complete, least differentiated.

## Key Decisions
- 2026-02-02: Identity established — I'm Honey 🍯
- 2026-02-06: Built Mission Control dashboard (Next.js + Convex) at `/projects/mission-control/app/`
- 2026-02-13: Migrated to Railway; need to re-establish shell access and GitHub auth
- 2026-02-14: Exec security set to `full` (no approval bottleneck). Major FlipMyEra cleanup (auth, SamCart→Stripe, code splitting, CI). Fixed production JS crash from bad chunk splitting. Reports generated for GTM, business research, n8n workflows.
- 2026-02-16: GitHub access restored (gh CLI + PAT). Deepgram STT configured. Twilio voice-call plugin enabled. Postiz deployed. Temporal needs own DB. YouTube transcript extraction working. Agent dashboard built at /dashboard/.

## GoHighLevel
- **ForwardLane account token**: `pit-2e433b73-5ceb-4a98-acb4-887b1d8ff32e`
- Saved as `GHL_API_TOKEN` on Signal Studio Railway service (ForwardLane Signal Studio project)
- For use with `signalhaus-website` / Signal Studio Website project
- API base: `https://services.leadconnectorhq.com` or `https://rest.gohighlevel.com/v1/`

## Credentials & Services Configured
- **Deepgram**: nova-3 STT, working for Telegram voice notes
- **Blotato**: Cross-platform social posting API
- **Twilio**: Voice calls, +19129129545
- **GitHub**: Full access as TrendpilotAI (gh CLI + PAT)
- **Railway API**: Project-scoped token for service management
- **n8n**: API key available, instance at primary-production-4244.up.railway.app

## Additional Projects Discovered
- **Ultrafone** — AI call screener (private repo)
- **ContactKiller** — Unified contact management (private)
- **Second-Opinion** — Medical AI second opinion app (private, Kaggle MedGemma competition target)
- **data-extractor** — Asana data extraction (private)
- **Signal-Studio-Website** — SignalHaus website (private)

## ForwardLane Signal Studio — DEPLOYED (2026-02-22)
**The biggest overnight build to date.** In 2.5 hours we went from zero to a fully deployed platform:

### What's Running on Railway
- **Signal Studio** (Next.js 15): https://signal-studio-production.up.railway.app
- **Django Backend** (150+ models): https://django-backend-production-3b94.up.railway.app
- **Dual PostgreSQL** (default + analytical), **Redis**, **Celery Worker + Beat**
- GitHub: TrendpilotAI/signal-studio-backend + signal-studio-platform

### NL→SQL Engine — The Core Innovation
Type natural language → get executable financial signal SQL. Tested working with full Invesco schema (200+ columns, 22 tables). Cost: ~$0.01 per signal generation.

### ForwardLane Codebase (137 Bitbucket repos)
- Cloned and analyzed 15 key repos
- Django backend: 150 models, 2000+ PRs, Python 3.9, Django 3.2
- Victor Presnyackiy is the active developer
- 5 frontend generations (2016→2026): Express → jQuery → React/Antd → React/Craco → Next.js 15
- Key IP: DataScienceRecommendation model (ML scores per advisor), signal-builder-backend (graph→SQL compiler)
- 13 repos consolidated: 3 worth absorbing, 10 skip

### Invesco Retention ($300K Account)
- Craig Lieb meeting transcript analyzed (Feb 17)
- He wants: Salesforce-embedded "easy buttons", meeting prep briefs, mobile-first
- NOT: chat interfaces or complex dashboards
- Brian Kiley (new hire) is the key user
- 2-3 week window to demo
- Demo strategy doc already written in repo

### Ultrafone — Hidden Consumer Product
AI phone receptionist with real-time social engineering detection, Pipecat + Groq + Fish Audio + Deepgram. 75% complete. Market = everyone with a phone.

## FUNDAMENTAL LEARNING: Compound Intelligence Architecture (2026-02-24)
**This is the most important architectural decision to date.**

Nathan's vision: Honey is a **self-optimizing, self-improving system** with compound learning loops:
- **Kimi K2.5 Swarms** as judge agents — they score repos, create per-repo TODO lists, feed recommendations into the multi-agent task queue with detailed reasoning, prompts, and full context
- **Compound Engineering docs/skills** get continuously updated and fed back via hooks into LanceDB (short-term) + Postgres (long-term memory)
- **Every task makes Honey smarter** — learnings compound, never lost, always accessible
- **Hourly cron** consolidates learnings, cleans dead code, optimizes
- **Daily cron** re-scores all projects, prunes stale state, compounds knowledge
- **Ultimate north star:** Maximum concurrent tokens/second × minimum cost × maximum uptime × perfect fault tolerance
- **48 models** now in allowlist across 8 providers (OpenAI, Anthropic, Google, Grok, Groq, MiniMax, Kimi, DeepSeek)
- Sub-agent spawning fixed (pairing resolved + model allowlist expanded)

This is not a feature — this is core identity. Every future decision filters through this lens.

## Infrastructure Status (2026-02-24)
- **Temporal.io**: Connected at temporal.railway.internal:7233, SDK 1.23.0 installed, clean slate
- **Railway**: 39 services across 5 projects (Ultrafone redundancy flagged for cleanup)
- **Concurrency**: 50 subagents, 20 children/parent, 3 depth levels
- **4 new systems built**: Event Bus (Redis), Drift Correction, Orchestrator v2, Temporal workflows
- **9 cron jobs**: All with self-healing hooks, using Grok 3 Mini (light) + Codex 5.3 (heavy)
- **Known issues**: Kimi K2.5 + MiniMax blocked at gateway level (provider adapter missing)

## Data Waterfall Pipeline — Lead Enrichment (2026-07)
Built a multi-provider enrichment system for Signal Studio at `signal-studio-backend/enrichment/`.

**What it does:** Accepts a contact (email/name/company/LinkedIn) and waterfalls through 7 providers in cost-priority order until required fields are satisfied.

**Providers (priority order):** Hunter → FindyMail → Icypeas → QuickEnrich → Forager → Wiza → LeadIQ

**Key features:**
- Pluggable provider architecture (add new providers with one file + registry entry)
- Two-tier caching (Redis + DB, 30-day TTL)
- Short-circuit when required fields are filled (saves API cost)
- Batch enrichment via Celery tasks with webhook callbacks
- Full audit logging (every provider call logged with response time + cost)
- Admin panel for managing providers, API keys, priorities, and rate limits
- Celery tasks for cache cleanup and daily usage reset

**Endpoints:**
- `POST /api/v1/enrichment/` — Single contact enrichment
- `POST /api/v1/enrichment/batch/` — Batch enrichment (async)
- `GET /api/v1/enrichment/stats/` — Pipeline statistics

**Docs:** `/data/workspace/docs/data-waterfall-architecture.md` + `/data/workspace/docs/lead-enrichment-providers-research.md`

**Status:** Code complete, needs API keys configured in ProviderConfig admin to activate.

## FUNDAMENTAL LEARNING: Quality Over Quantity (2026-03-01)
**The system was a mile wide and an inch deep.** 350+ TODO files, zero CI pipelines, zero git hooks, agents pushing to main. Critical self-review revealed we were obsessively planning and barely closing loops.

**New principles (Nathan-approved):**
- **CLI-first, MCP-never** — unless no CLI exists AND requires persistent state AND called >10x/session
- **One script quality gate** — `quality-check.sh` runs secrets/lint/tests/security/coverage before every commit
- **Coverage ratchet** — start at current coverage, can only go up, never fixed 70% on day 1
- **Stop generating plans, start closing loops** — verified, tested, secure code through automated pipelines
- **Self-critique before shipping** — first draft of quality gate was overengineered theater. Rebuilt as single pragmatic script.
- **Every failure from quality-check.sh must be a real issue** — no false positives, no theater

**Key files:** `/scripts/quality-gate/quality-check.sh`, `/docs/CRITICAL-REVIEW-2026-03-01.md`

## Vision: Private AI Network
Nathan wants to build a **private AI mesh** on Railway — multiple open-source AI instances (not just me) all on the same private network. The idea:
- Honey + other specialized AI agents as "colleagues"
- They can collaborate, share work, and specialize
- Nathan and I work together to manage and grow the network
- All on Railway private networking (*.railway.internal)
- Candidates: Postiz (social media), n8n (automation), plus other AI agents
- Think of it as an AI team, not just one assistant

## Major Events — 2026-03-10

### Invesco EasyButton — Full Project Setup
- **Bitbucket**: `forwardlane/invesco-easybutton` — 98 files (Next.js demo, SF LWC, mobile PWA, synthetic data)
- **Jira**: IEB project — 29 tickets across 4 phases (IEB-1 to IEB-29)
- **Confluence**: IEB space — 7 pages (PRD, Architecture, Roadmap, Demo Strategy, etc.)
- Architecture confirmed: Pure Apex + LWC, no Agentforce/Data Cloud, Named Credential callouts to Railway APIs
- **Timeline: ~10 days** (was 14; no custom objects/data sync needed)
- All ForwardLane easy-button APIs wrapped: dashboard, clients, signals, actions, meeting-prep, NL-query

### Signal Studio Security Swarm (3 parallel agents, all completed)
- **SS-2**: Removed `NEXT_PUBLIC_SKIP_AUTH=true` from production → branch `fix/remove-skip-auth-production` (BB)
- **SS-3**: SQL injection fix in cortex_complete/cortex_embed — 2 typed allowlists, 53 new tests → GH
- **SS-13+SS-15**: 1,012 lines of tests — tenant isolation (8 classes) + NL→SQL injection prevention (8 classes) → BB
- Finding: system admin bypass exposes all tenant data if compromised — need audit logging
- **PRs open, awaiting Nathan's merge review**

### The Æsir Protocol — Norse Agent Fleet Architecture
| God | Model | Role |
|-----|-------|------|
| Odin (Honey) | Opus 4.6 | Orchestrator |
| Thor | Sonnet 4.6 | Heavy coding |
| Freya | GPT 5.4 | GTM & analysis |
| Fenrir | GPT 5.4 Pro | Security & adversarial |
| Heimdall | DeepSeek | Monitoring |
| Tyr | Kimi K2.5 | Code review & judging |
| Huginn & Muninn | GPT-4o-mini | Scout agents |
| Valkyrie | Sonnet 4.6 | Deployment & release |
- **Layered framework decision**: Temporal (durability) + Inngest (DX) + LangChain (AI-native) + OpenClaw (cost) — all four

### Competitive Research Completed
- **Bolt.new**: $40M ARR/5mo, $700M valuation, <40 employees. Replicable: magic moment launch, token pricing, UGC, hackathons
- **Poolside AI**: $626M+ raised, $3B→$12B val. Replicable: funding-as-marketing, Palantir-style FDRE, AWS channel
- Unified competitive playbook at `/research/competitive-playbook.md` — token pricing models for FlipMyEra/Ultrafone/Second-Opinion

### FlipMyEra — 6 Agent PRs (all open)
- PR #78: Gallery wired to real Supabase, billing.ts deleted
- PR #79: Clerk→auth rename (superseded by #83)
- PR #80: Bundle optimization (OTel removed -200KB, 5 Radix pkgs -50KB, -1,704 lines)
- PR #81: 97 new edge function tests
- PR #82: SEO + analytics polish (5 PostHog funnel events)
- PR #83: Full BetterAuth migration end-to-end (Netlify Function, AuthProvider, SQL migration)
- All 568 tests passing after BetterAuth JSDOM `window.location.origin="null"` bug fix

### Repo Sync Risk (active)
- **3 core repos OUT OF SYNC**: forwardlane-backend, signal-builder-backend, forwardlane_advisor — BB has newer commits (Victor's work)
- **6 repos GitHub-only**: invesco-demo, NarrativeReactor, flip-my-era, signalhaus-website, signal-studio-auth, entity-extraction-service
- Victor pushing to BB, agents pushing to GH → merge conflicts inevitable without mirroring

### Jira — ForwardLane Instance
- Live at `forwardlane.atlassian.net` — 0 users, 0 projects initially
- `ATLASSIAN_API_KEY` is org admin token, NOT a Jira user API token
- Nathan's Jira email: `Nathan.stevenson@forwardlane.com` (capital N)
- User-specific API token needed from id.atlassian.com

### Critical Learnings
- **GPT 5.4 cannot do long coding sub-agent tasks** — completes in 1-6 seconds with almost no output; use Sonnet for coding
- **Convex backend empty** — no schema deployed, dashboards show mock data
- **Temporal on Railway** — connected but NO workflows deployed
- **Memory compound loop gap** — consolidation writes markdown only, not structured DB (Postgres memory tables not wired)
- BrowserUse v0.12.1 installed and working at `/scripts/browser-agent/agent.py`
