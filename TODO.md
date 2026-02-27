# TODO.md — Master Project Plan

> Auto-monitored by Honey's cron loops. Last updated: 2026-02-27 05:01 UTC (invesco-sprint cron: spawned 3 Sonnet agents for TODO-213 Push-to-SF, TODO-214 Branding, TODO-215 Skeletons, TODO-216 Demo Reset)

---

## 🔴 P0 — Critical / Revenue-Impacting

### INVESCO-RETENTION: Demo App Deploy + Brian Kiley Demo (🚨 $300K/yr — Early March 2026)
- **Why:** $300K/yr account retention. All 5 demo deliverables built, NOT deployed. Demo to Brian Kiley needed ASAP.
- **Status:** 🟡 CODE PUSHED to GitHub (TrendpilotAI/invesco-demo) — needs 1-click Vercel/Railway deploy by Nathan
- **Owner:** Honey (technical) + Nathan (outreach + demo)
- **Deadline:** Early March 2026
- **Plan:** `/data/workspace/projects/invesco-retention/PLAN.md`
- **TODOs Created:**
  - [x] 211 — Vercel Deploy (P0, XS, BLOCKS ALL) → `todos/211-pending-p0-invesco-retention-vercel-deploy.md`
  - [x] 212 — Demo Recordings / Loom (P0, S) → `todos/212-pending-p0-invesco-retention-demo-recordings-loom.md`
  - [ ] 213 — Push-to-Salesforce Simulation (P1, S) → `todos/213-pending-p1-invesco-retention-push-to-salesforce-simulation.md`
  - [x] 214 — Invesco Branding in SF Chrome (P1, XS) → `todos/214-pending-p1-invesco-retention-invesco-branding.md` ✅ 2026-02-27
  - [x] 215 — Skeleton Loaders / AI Animation (P1, S) → `todos/215-pending-p1-invesco-retention-skeleton-loaders.md` ✅ 2026-02-27
  - [x] 216 — Demo Reset Button (P1, XS) → `todos/216-pending-p1-invesco-retention-demo-reset.md` ✅ 2026-02-27
  - [ ] 217 — Support Model Polish (P1, XS-S) → `todos/217-pending-p1-invesco-retention-support-model-polish.md`
  - [ ] 218 — Leave-Behind Package (P1, S) → `todos/218-pending-p1-invesco-retention-leave-behind-package.md`
- **Critical path:** Deploy (211) → Email Megan+Craig → Dry Run → Brian Demo → Pilot signed



### INVESCO-001: Easy Button Demo for Craig Lieb
- **Why:** $300K account retention, 2-3 week demo window
- **Status:** ✅ COMPLETE — 51/51 E2E tests pass, mobile layout done, all endpoints live
- **Owner:** Honey
- **Tasks:**
- [x] Build Easy Button page with Ant Design (`/easy-button`)
- [x] Stats row, Priorities table, Active Signals, Action Items
- [x] Wire to Django API — all 6 endpoints live at /api/v1/easy-button/ ✅ 2026-02-26
- [x] Signal templates (5): aum-decline-alert, cross-sell-etf, revenue-defense, dormant-reactivation, growing-fast ✅
- [x] Meeting prep brief generator (MeetingPrepView) — GET /api/v1/easy-button/meeting-prep/{id}/ ✅
- [x] Salesforce embed wrapper (iframe-ready, postMessage API) ✅ 2026-02-26
- [x] End-to-end test: API verified live (/dashboard $156B, /clients 500 advisors, /signals, /meeting-prep) ✅
- [x] NL→SQL "Ask the Data" panel ✅ 2026-02-26 — POST /api/v1/easy-button/nl-query/ w/ Gemini→Kimi→fallback chain
- [x] NL→SQL quick prompts: 5 one-click examples (at-risk, top AUM, Invesco holdings, fastest-growing, RIA West) ✅
- [x] Mobile-responsive NL query panel (100% width on mobile) ✅
- [x] Seed analytical DB with demo data ✅ (INVESCO-002 complete)
- [x] GEMINI_API_KEY + KIMI_API_KEY set on Django Railway via API ✅ 2026-02-26 05:45 UTC
- [x] Django redeployed to pick up new LLM API keys ✅ 2026-02-26 05:45 UTC
- [x] Mobile-responsive layout — committed by sub-agent ✅ 2026-02-26 (xs/sm/md breakpoints, stacking cols, scrollable tables)
- [x] End-to-end test: 51/51 tests PASS ✅ 2026-02-26 — script at /data/workspace/scripts/test-invesco-e2e.py
- [x] NL→SQL security hardening — SQL injection block + rate throttle committed ✅ 2026-02-26
- **Depends on:** INVESCO-002 ✅ complete
- **Deadline:** ~March 7, 2026 — **COMPLETE AHEAD OF SCHEDULE** 🎉

### INVESCO-002: Demo Data Seeding
- **Why:** Can't demo without realistic data
- **Status:** 🟢 SEEDED AND LIVE ✅ 2026-02-26
- **Tasks:**
- [x] Create proper multi-table schema (advisors, holdings, flows, signals)
- [x] Generate 500 synthetic advisors with realistic AUM ($50M-$2B)
- [x] Generate holdings data — 2775 holdings (30% Invesco, 70% competitors)
- [x] Generate flow/transaction history — 33300 monthly flow records (12 months)
- [x] Create 10 "interesting" advisors with clear signal patterns (CHAMPION, AUM_DECLINE, CROSS_SELL_ETF, etc.)
- [x] Django management commands: seed_analytical_db + seed_analytical (auto-runs on deploy)
- [x] Django API endpoints: /api/analytics/ + /api/v1/easy-button/ (884-line views.py)
- [x] pushed to Bitbucket railway-deploy branch — Railway rebuild triggered
- [x] Analytical DB env vars set on Django (ANALYTICAL_POSTGRES_HOST/USER/PASS/DB/PORT)
- [x] Railway deployed + DB seeded ✅ — 500 advisors, $156B AUM, 88 at-risk, 489 competitor-heavy
- [x] Schema consistent — views.py uses correct column names (advisor_id, full_name, aum_current, etc.) ✅
- [x] NL→SQL validated live ✅ — keyword fallback chain working (Gemini/Kimi will activate after redeploy)
- [x] Signal templates validated — all 6 run successfully: 88 AUM decline, 50 cross-sell ETF, 135 revenue defense, 489 competitor-heavy, 45 growing-fast ✅ 2026-02-26

---

## 🟠 P1 — Infrastructure & Integration

### INFRA-001: Entity Extraction Service
- **Why:** Django depends on it for NLP features
- **Status:** 🟢 DONE — FastAPI + spaCy 3.7 live ✅ 2026-02-26
- **Tasks:**
- [x] Rewrite as FastAPI + spacy 3.7+ on Python 3.11
- [x] Port all original endpoints (regex, ml, spacy, fixed_lists, version)
- [x] Add /health endpoint — returns {"status": "ok"}
- [x] Push to TrendpilotAI/core-entityextraction (GitHub)
- [x] Deploy to Railway — SUCCESS (deployment 43aaaaaf)
- [x] Verified: GET /health → 200, POST /ml_entity_extraction → detects QQQ as Ticker
- [ ] Wire ENTITY_EXTRACTION_SERVICE_URL on Django (optional — not blocking demo)

### INFRA-002: Wire Frontend → Backend
- **Why:** Signal Studio UI is disconnected from Django API
- **Status:** 🟢 Demo auth fully working ✅
- **Tasks:**
- [x] Set NEXT_PUBLIC_CORE_API on Signal Studio service ✅ → https://django-backend-production-3b94.up.railway.app
- [x] NEXT_PUBLIC_SKIP_AUTH=true — bypasses login for demo, no JWT required ✅ (already set)
- [x] Django login confirmed: POST /api/v1/users/login/ → JWT token ✅ (demo@forwardlane.com / Demo2026!)
- [x] Django easy_button views patched with AllowAny — no auth required for demo ✅
- [x] auth-context.tsx + auth-layout.tsx correctly bypass auth when skipAuth=true ✅
- [x] api-client.ts uses NEXT_PUBLIC_CORE_API for all API calls ✅
- [ ] Wire dashboard data fetches to Django endpoints (depends on INVESCO-002 deploy)
- [ ] Wire NL→SQL to Signal Builder API
- [ ] Test demo user login flow end-to-end (manual QA needed)

### INFRA-003: Agent Ops Center Fix
- **Why:** Dashboard deployed but broken (JSX syntax error on agents page)
- **Status:** ✅ FULLY COMPLETE (2026-02-26)
- **Tasks:**
- [x] Fix JSX syntax in agents/page.tsx — remote already had fix (aafe7605)
- [x] Push to GitHub — pushed clean:main → TrendpilotAI/agent-ops-center ✅
- [x] Railway build triggered via new push
- [x] Real telemetry polling CONFIRMED: /api/telemetry polls Railway GraphQL + HTTP health + reads orchestrator JSON files + memory state — verified 15s auto-refresh cycle ✅ 2026-02-26
- **Estimate:** 30 min

### INFRA-004: Django Security Hardening
- **Why:** 70 Dependabot vulns, hardcoded SECRET_KEY + SQL injection risk on easy_button endpoints
- **Status:** 🟡 Partially done
- **Tasks:**
- [x] Generate and set SECRET_KEY as Railway env var ✅ (y32acblzz...P7xbwk, 70-char random) 2026-02-26
- [x] Set ANALYTICAL_DATABASE_URL env var on Django ✅
- [x] Fixed CORS_ALLOWED_ORIGINS to include both Signal Studio URLs ✅
- [x] **FIXED:** ORDER BY was already whitelisted via ordering_map dict — verified safe ✅
- [x] **FIXED:** NL→SQL _clean_sql hardened — blocks pg_read_file/pg_exec/pg_sleep/dblink/etc., strips multi-statement, auto-adds LIMIT ✅ 2026-02-26
- [x] NLQueryView rate throttled: 10 req/min per IP via DRF AnonRateThrottle ✅
- [ ] **CRITICAL:** Remove AllowAny from all easy_button endpoints post-demo (add JWT auth)
- [ ] Review and merge critical Dependabot PRs (boto3==1.23, sentry 1.5, PyPDF2 deprecated)
- [ ] Upgrade Django 3.2 → 4.2 LTS (3.2 is EOL)
- [ ] Add rate limiting on NL→SQL endpoints (no throttling = abuse risk)
- [ ] Add Redis caching on hot NL→SQL paths
- [ ] Audit CORS/ALLOWED_HOSTS settings
- [ ] Enable HTTPS redirect

### INFRA-005: Signal Studio Templates Integration
- **Why:** 20 pre-built signal templates built but not wired into Signal Studio UI (composite 7.9, urgency 8)
- **Status:** 🟡 Phase 1 done — package scaffolded, tests written, pushed to GitHub
- **Tasks:**
- [x] Add package.json + tsconfig to signal-studio-templates ✅ 2026-02-26 — repo: TrendpilotAI/signal-studio-templates commit 26eed90
- [x] Create index.ts entry point (re-exports schema, engine, templates, API router) ✅
- [x] Add Jest test suite — 6 tests: count=20, unique IDs, all 5 categories=4 templates each ✅
- [ ] Wire template gallery route in signal-studio (/templates) — import ALL_TEMPLATES, render TemplateGallery component
- [ ] Harden SQL generation — parameterized queries, injection protection
- [ ] Custom template persistence (save user-defined templates to DB)
- [ ] CI/CD pipeline for template package

### INFRA-006: Entity Extraction Persistence Fix
- **Why:** In-memory entity store loses all data on pod restart — psycopg2 is in requirements but unused
- **Status:** 🟢 Persistence fixed ✅ 2026-02-26
- **Tasks:**
- [x] Wire psycopg2 to Railway Postgres for entity persistence ✅ 2026-02-26 — `persistence.py` created, write-through cache, startup load, graceful fallback (commit fa05da9)
- [ ] Remove dead Flask codebase (app.py, controllers/, old services/ — duplicate dead code)
- [ ] Add test suite (currently zero tests)
- [ ] Add ENTITY_EXTRACTION_SERVICE_URL to Django env vars

---

## 🟡 P2 — Product Features

### PRODUCT-001: Signal Agent Framework
- **Why:** AI-powered signal creation and research
- **Status:** 🟡 Deployed, needs credentials
- **Tasks:**
- [ ] Add Resend API key for email tools
- [ ] Wire Twilio for voice/SMS tools
- [ ] Add Django auth to agent endpoint
- [ ] Build agent memory (conversation history per user)
- [ ] Add "research advisor" tool (pull from analytical DB)
- [ ] Add "create signal" tool (call Signal Builder API)
- [ ] Test full flow: ask question → agent researches → creates signal

### PRODUCT-002: Client Research Widget
- **Why:** Craig wants meeting prep briefs
- **Status:** 🔴 Not started
- **Tasks:**
- [ ] Build /api/research/advisor endpoint on Django
- [ ] Pull advisor AUM, top holdings, recent flows, signals triggered
- [ ] Generate 1-page meeting prep brief (PDF or HTML)
- [ ] Add to Easy Button page as "Prep for Meeting" button
- [ ] Wire to Salesforce contact/account lookup

### PRODUCT-003: Signal Templates Library
- **Why:** Pre-built signals = instant value for Invesco demo
- **Status:** 🔴 Not started  
- **Tasks:**
- [ ] Define 10 signal templates with SQL + display config
- [ ] AUM Decline Alert (>10% drop in 90 days)
- [ ] Cross-Sell ETF Opportunity (concentrated in MF, no ETF)
- [ ] Revenue Defense (advisor AUM declining + competitor flows)
- [ ] RIA Conversion Ready (breakaway signals)
- [ ] Dormant Account Reactivation
- [ ] Build template picker UI
- [ ] One-click deploy: select template → populate params → run

---

## 🔵 P3 — Other Projects

### FLIP-001: FlipMyEra Ship
- **Why:** Live at flipmyera.com, Taylor Swift ebook creator (composite 6.2, Stripe wired)
- **Status:** 🟡 Live, 2 SEO/revenue bugs fixed, needs remaining polish
- **Tasks:**
- [x] **BUG FIXED:** h1 SEO bug — changed subtitle `<p>` to `<h2>` with keyword "Create your personalized Taylor Swift Eras Tour storybook", fixed span space bug in h1, updated page title to keyword-rich ✅ 2026-02-26 commit ad6d983
- [x] **BUG FIXED:** Pricing page 404 — wired `/pricing` route → PricingPage (454-line component that existed but wasn't routed) ✅ 2026-02-26 commit ad6d983
- [ ] Complete 6 incomplete modules: marketplace, affiliates, gallery, sharing, gifting, templates
- [ ] E2E test pass — 66% passing currently (get to 90%+)
- [ ] Stripe checkout live mode validation
- [ ] SEO optimization + social media launch plan

### ULTRA-001: Ultrafone MVP
- **Why:** Production-grade AI phone receptionist backend (composite 6.3), missing final integrations
- **Status:** 🟡 Phase 2 complete, needs phase 3
- **Tasks:**
- [ ] Calendar integration (Google Calendar / Outlook) for call context
- [ ] CRM integration (Salesforce/HubSpot) for caller lookup
- [ ] CORS hardening (currently permissive)
- [ ] SaaS multi-user mode (currently single-tenant)
- [ ] iOS native app (design prompt exists, needs build)
- [ ] Live production E2E Twilio test (end-to-end call test)

### SIGBUILD-001: Signal Builder Backend Hardening
- **Why:** Production FastAPI NL→SQL engine (composite 7.7), deployed, needs reliability work
- **Status:** 🟡 Deployed, missing observability + type safety
- **Tasks:**
- [ ] Remove hardcoded fallback secrets — move to environment config
- [ ] Add Redis caching on hot graph→SQL compilation paths
- [ ] Add Prometheus metrics + alert rules
- [ ] Pin dependency versions (currently unpinned — deployment risk)
- [ ] Add mypy + type checking to CI pipeline

### SIGBUILD-002: Signal Builder Frontend Modernization
- **Why:** React SPA on Create React App (aging/slow), near-zero test coverage (composite 6.4)
- **Status:** 🟡 Deployed to QA+Demo, no production pipeline
- **Tasks:**
- [ ] Migrate CRA → Vite (10x faster builds)
- [ ] Add E2E Playwright tests for core visual builder flow
- [ ] Expand unit tests from 5 → 50+ (targeting 80% coverage)
- [ ] Resolve dual state management (Redux vs React Query — pick one)
- [ ] Create production deployment pipeline (currently only demo+QA)

### ADVISOR-001: Modernize forwardlane_advisor
- **Why:** Critical advisor portal (composite 5.9) with severe security issues blocking enterprise use
- **Status:** 🟡 Critical security fixed
- **Tasks:**
- [x] **CRITICAL FIXED:** Removed Dockerfile fetching SSH private keys from http://158.85.245.10:4006 (plain HTTP + hardcoded bearer token) ✅ 2026-02-26 (commit 308f960)
- [x] Upgraded base image: node:argon (Node 0.10 EOL 2016) → node:20-slim ✅
- [x] Checked config files — no hardcoded app credentials (models/index.js uses process.env) ✅
- [ ] Replace deprecated IBM Watson Dialog API with modern LLM
- [ ] Add test coverage (currently near zero)

### OPS-001: Agent Mesh / Private AI Network
- **Why:** Nathan's vision for multi-agent collaboration
- **Status:** 🟡 Orchestrator script exists, not operational
- **Tasks:**
- [ ] Finalize orchestrator dispatch → subagent flow
- [ ] Build agent-to-agent communication protocol
- [ ] Add cost tracking per agent/task
- [ ] Dashboard integration (Agent Ops Center)

### NARRATIVE-001: NarrativeReactor
- **Why:** Content engine for SignalHaus/ForwardLane (composite 5.8, 30+ services built)
- **Status:** 🟡 Partially built — TypeScript/Express + Google Genkit, blocked on broken tests
- **Tasks:**
- [ ] Fix broken tests (currently blocking CI) — top priority
- [ ] Wire real DB persistence for content store (currently in-memory)
- [ ] Configure deployment (Railway or Vercel)
- [ ] Wire social OAuth flows (scaffolded but not connected to real providers)
- [ ] Wire real LLM calls for content generation (Genkit + Claude/Gemini configured but stubs remain)

### SECOND-OPP-001: Second-Opinion Post-Competition Hardening
- **Why:** Submitted to Kaggle MedGemma challenge (Feb 24), now needs productionization (composite 5.1)
- **Status:** 🟡 Live at gen-lang-client-0003791133.web.app, ~40 stub components
- **Tasks:**
- [ ] Complete ~40 stubbed UI components
- [ ] Increase test coverage from ~18 to 60+ test files
- [ ] Add real HIPAA compliance layer (auth, audit trail, data encryption)
- [ ] Add monitoring (Sentry/Datadog)
- [ ] Define SaaS pricing + billing model
- [ ] Launch marketing page for second-opinion product

### TRENDPILOT-001: Trendpilot Real Data Layer
- **Why:** 423 tests + enterprise architecture exist but ALL services use in-memory storage (composite 6.0)
- **Status:** 🔴 Architecture complete, no real integrations
- **Tasks:**
- [ ] Replace in-memory stores with real Supabase DB (project: ycisqlzzsimtlqfabmns)
- [ ] Wire real news API (NewsAPI / RSS) for trend ingestion
- [ ] Wire real LLM pipeline for newsletter generation
- [ ] Wire real email delivery (Resend or SendGrid)
- [ ] Deploy frontend with auth to production
- [ ] Launch beta to first 10 users

### SIGNALHAUS-001: Fix SignalHaus Contact Form
- **Why:** Marketing website cannot convert any leads — contact form is fake (composite 7.1, urgency 8)
- **Status:** 🔴 CRITICAL — form submits nothing
- **Tasks:**
- [ ] Wire contact form to real email (Resend API) or CRM
- [ ] Add Google Analytics / Plausible analytics
- [ ] Add Calendly embed for demo booking
- [ ] Write 5+ more blog posts for SEO content velocity
- [ ] Add CI/CD pipeline

### ENTITYEXT-001: Entity Extraction Cleanup
- **Why:** Dead legacy Flask code still in repo, zero tests (composite 7.1)
- **Status:** 🟡 FastAPI + spaCy live, but legacy dead code present
- **Tasks:**
- [ ] Remove dead Flask codebase (app.py, controllers/, old services/)
- [ ] Add test suite (currently zero tests)
- [ ] Add connection pooling (currently new DB conn per request)
- [ ] Add rate limiting + auth
- [ ] Fix uswgi.py typo → uwsgi.py
- [ ] Update README to reflect FastAPI architecture

---

## signal-builder-backend

> FastAPI backend for ForwardLane signal builder. Security hardening + feature additions.  
> Plan: /data/workspace/projects/signal-builder-backend/PLAN.md  
> TODOs: 200–206 in /data/workspace/todos/

### 🔴 CRITICAL — Execute Immediately (Phase 1, ~4h parallelizable)

- [x] **[TODO-200]** Fix CORS wildcard — replace `allow_origins=["*"]` with `settings.CORS_ALLOWED_ORIGINS` env var · _1h_ · `200-pending-critical-...-fix-cors-wildcard.md`
- [x] **[TODO-201]** Remove hardcoded JWT secrets — `AUTH_SECRET_KEY` defaults to `"very_secure_secret"` · _1h_ · ✅ 2026-02-26 — `_require_secret()` validator, fails fast if missing/weak, test suite added, committed e50ece6
- [x] **[TODO-202]** Fix EXPLAIN SQL injection in `is_sql_code_correct()` — add `sqlglot` validation + read-only transaction + statement_timeout · _2h_ · ✅ 2026-02-27 — sql_validator.py + read-only txn + 15 tests, commit 141c1b1

### 🟠 HIGH — Phase 2 (After security fixes)

- [ ] **[TODO-203]** Pin all Pipfile wildcards — `fastapi-jwt-auth`, `uvicorn`, `pydantic`, `celery`, `redis`, `pandas` et al. + add `pip-audit` to CI · _2h_ · `203-pending-high-...-pin-pipfile-dependencies.md`

### 🟡 HIGH — Phase 3 (Parallel, after 203)

- [ ] **[TODO-204]** Signal versioning — `signal_versions` table, snapshot on publish, rollback endpoint, diff · _8h_ · `204-pending-high-...-add-signal-versioning.md`
- [ ] **[TODO-205]** Dry-run preview — `POST /signals/{id}/preview` returns sample rows + generated SQL without publishing · _6h_ · `205-pending-high-...-add-dry-run-execution.md`
- [ ] **[TODO-206]** Audit log — append-only `audit_events` table, fire-and-forget writes on all mutations, admin query endpoint · _8h_ · `206-pending-high-...-add-audit-log.md`

---

## 📊 Service Health Dashboard

| Service | URL | Status |
|---------|-----|--------|
| Signal Studio (new) | signal-studio-production-a258.up.railway.app | ✅ 200 |
| Signal Studio (old) | signal-studio-production.up.railway.app | ✅ 200 |
| Django Backend | django-backend-production-3b94.up.railway.app | ✅ 200 |
| Signal Builder API | signal-builder-api-production.up.railway.app | ✅ 200 |
| Agent Ops Center | agent-ops-center-production.up.railway.app | ✅ 200 |
| Entity Extraction | entity-extraction-production.up.railway.app | ✅ 200 |

---

## 🕐 Cron Schedule

| Job | Frequency | What it does |
|-----|-----------|-------------|
| `service-health` | Every 2h | DeepSeek — checks all Railway service URLs, alerts on failures |
| `todo-progress` | Every 4h | **Codex 5.3** — picks next task, spawns **Sonnet 4-6** sub-agents for parallel coding |
| `git-sync` | Every 6h | DeepSeek — commits and pushes workspace changes (silent) |
| `invesco-sprint` | Every 8h | **Codex 5.3** — P0 Invesco work, spawns **Sonnet 4-6** agents for speed |

---

*This file is the source of truth. Cron jobs read it, update it, and work from it.*

---

## 🧩 Signal Studio Templates (Invesco) — 2026-02-26

> Revenue=8 | Strategic=9 | Completeness=5 | Urgency=8
> Full plan: `/data/workspace/projects/signal-studio-templates/PLAN.md`

### 🔴 Critical (run first, unblock everything)
- [x] **#211** Fix build system — install deps, fix tsconfig, generate dist/ [2h] ✅ 2026-02-26 — pnpm, tsconfig fixed, dist/ generated clean
- [ ] **#212** Add ESLint — @typescript-eslint, .eslintrc.js, lint script [1.5h]
- [x] **#213** SQL injection hardening — rewrite generateSQL() with parameterized queries [3h] ⚠️ SECURITY ✅ 2026-02-26 — utils/sql-safety.ts, parameterized queries, 12 tests pass

### 🟠 High (after critical)
- [ ] **#214** Integration tests — mock DataProvider, execute() E2E, ≥80% coverage [4h]
- [ ] **#215** Custom template persistence — Django model + CRUD API + TypeScript client [5h]
- [ ] **#216** Signal Studio Next.js integration — TemplateBrowser + TemplateConfigForm + /templates route [5h]

### 🟡 Medium (stabilization)
- [ ] **#217** Pre-commit hooks — husky + lint-staged + prettier [1h]
- [ ] **#218** GitHub Actions CI — typecheck + test + lint on push [1.5h]


---

## 🔒 ForwardLane Backend (Invesco Demo Hardening) — 2026-02-26

> Revenue=8 | Strategic=9 | Security=CRITICAL | Urgency=9
> Full plan: `/data/workspace/projects/forwardlane-backend/PLAN.md`
> Audit: `/data/workspace/projects/forwardlane-backend/AUDIT.md`

### 🔴 P0 — Do Before Next Demo (Security Critical)
- [x] **#211** [P0] Auth on demo endpoints — env-gated EasyButtonPermission (AllowAny → env-based) ✅ commit bb777cc0, Railway redeployed
- [x] **#214** [P0] Pytest tests — easy_button/_clean_sql security tests ✅ easy_button/tests/test_clean_sql.py (13 tests), commit bb777cc0

### 🟠 P1 — This Sprint
- [ ] **#212** [P1] Real LLM calls in MeetingPrepView — Gemini → Kimi → static fallback, Redis cache [4–6h]
- [x] **#213** [P1] Connection pooling — add CONN_MAX_AGE=60 to both DATABASES entries ✅ 2026-02-27 — committed 4844f79b, pushed to railway-deploy
- [ ] **#215** [P1] CI pipeline — add PR test gate + development branch test step [1–2h]

### Execution Order
1. #213 (pooling) — settings change, zero risk, immediate production benefit
2. #211 (auth) — deploy to staging first with DEMO_ENV=staging
3. #212 (LLM) — high demo value, reuses existing Gemini infrastructure
4. #214 (tests) — after auth + LLM implemented
5. #215 (CI) — after tests exist

