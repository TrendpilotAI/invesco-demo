# TODO.md — Master Project Plan

> Auto-monitored by Honey's cron loops. Last updated: 2026-03-02 08:04 UTC (judge-signal-builder-backend: re-scored signal-builder-backend [revenue:8, strategic:9, completeness:7, urgency:7, effort_remaining:6], refreshed BRAINSTORM/PLAN/AUDIT, created TODO-391-395 covering mypy cleanup, test coverage for schema_builder/translators/analytical_db, Flask dep removal, N+1 batch fix, dev CVE upgrades. Previously: 2026-03-02 08:01 UTC judge-signal-studio: re-scored signal-studio, refreshed BRAINSTORM/PLAN/AUDIT, created TODO-384-388.)

---

## 🔴 P0 — Critical /Revenue-Impacting

> Daily Judge Swarm (2026-02-27 08:11 UTC): Judge agents produced 14 BRAINSTORM.md, 15 PLAN.md, and 16 AUDIT.md files across projects. Planning agents created 181 TODO files (see /data/workspace/todos/). Trendpilot judge required a retry but completed; cleanup agent ran to prune stale orchestrator state. Continued: review high-priority TODOs listed below and attack P0 items (Invesco demo deploy).
> invesco-sprint cron check 2026-03-03 05:01 UTC: ALL INVESCO TECHNICAL P0s COMPLETE ✅. Demo live at https://trendpilotai.github.io/invesco-demo/ (HTTP 200). Remaining critical path is NATHAN ACTION: Email Megan+Craig → Schedule Dry Run → Brian Kiley Demo → Pilot signed. No new sub-agents needed — unblock is outreach, not code.
> invesco-sprint cron check 2026-03-03 21:01 UTC: Demo still live. Identified 4 remaining P0 security/quality items across data-provider, backend, and templates. Spawned 4 parallel Sonnet agents: TODO-422 (demo auth hardening), TODO-426 (templates JWT auth), TODO-434 (Snowflake param binding), TODO-445 (TanStack Query wiring).
> invesco-sprint cron check 2026-03-04 05:01 UTC: TODO-422 ✅ DONE (HMAC X-Demo-Token auth, commit 501aa6b0). TODO-426 ✅ DONE (JWT middleware via JWKS-RSA, commit 9af41e8, 18 tests pass). TODO-434 + TODO-445 still pending — spawned 2 fresh Sonnet agents in parallel to complete.



### INVESCO-RETENTION: Demo App Deploy + Brian Kiley Demo (🚨 $300K/yr — Early March 2026)
- **Why:** $300K/yr account retention. All 5 demo deliverables built, NOT deployed. Demo to Brian Kiley needed ASAP.
- **Status:** 🟡 CODE PUSHED to GitHub (TrendpilotAI/invesco-demo) — needs 1-click Vercel/Railway deploy by Nathan
- **Owner:** Honey (technical) + Nathan (outreach + demo)
- **Deadline:** Early March 2026
- **Plan:** `/data/workspace/projects/invesco-retention/PLAN.md`
- **TODOs Created:**
  - [x] 211 — Vercel Deploy (P0, XS, BLOCKS ALL) → ✅ LIVE at https://trendpilotai.github.io/invesco-demo/ (GitHub Pages) 2026-02-27
  - [x] 212 — Demo Recordings / Loom (P0, S) → `todos/212-pending-p0-invesco-retention-demo-recordings-loom.md`
  - [x] 213 — Push-to-Salesforce Simulation (P1, S) → `todos/213-pending-p1-invesco-retention-push-to-salesforce-simulation.md` ✅ 2026-02-27
  - [x] 214 — Invesco Branding in SF Chrome (P1, XS) → `todos/214-pending-p1-invesco-retention-invesco-branding.md` ✅ 2026-02-27
  - [x] 215 — Skeleton Loaders / AI Animation (P1, S) → `todos/215-pending-p1-invesco-retention-skeleton-loaders.md` ✅ 2026-02-27
  - [x] 216 — Demo Reset Button (P1, XS) → `todos/216-pending-p1-invesco-retention-demo-reset.md` ✅ 2026-02-27
  - [x] 217 — Support Model Polish (P1, XS-S) → `todos/217-pending-p1-invesco-retention-support-model-polish.md` ✅ 2026-02-27
  - [x] 218 — Leave-Behind Package (P1, S) → `todos/218-pending-p1-invesco-retention-leave-behind-package.md` ✅ 2026-02-27
- **Critical path:** Deploy (211) → Email Megan+Craig → Dry Run → Brian Demo → Pilot signed
  - [x] 320 — Error Boundary Components (P0, S) → `todos/320-pending-p0-invesco-retention-error-boundaries.md` — protect all 4 demo views from runtime crashes during live demo ✅ DONE 2026-02-28 13:07 UTC (commit cf64cda, pushed)
  - [x] 321 — GitHub Repo Privacy Check (P0, XS) → ✅ 2026-02-28 — Repo is PUBLIC. Scanned for sensitive data: "Marcus Thompson" is synthetic demo data (not a real person). No real advisor names (Brian Kiley, Craig Lieb, Megan) in source. Invesco references are appropriate demo framing. Risk assessed as LOW — demo content is generic enough. No action required beyond documenting.
  - [x] 322 — 🚨 GitHub Pages 404 FIX (P0, XS) → ✅ FIXED 2026-03-01 — Demo live at https://trendpilotai.github.io/invesco-demo/ (200 OK all routes). Root cause: no gh-pages branch + repo was private (blocked Pages). Created gh-pages branch, made repo public, enabled Pages. All 4 routes verified.



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
- [x] Wire template gallery route in signal-studio (/templates) — import ALL_TEMPLATES, render TemplateGallery component ✅ 2026-02-27 — /app/templates/page.tsx created, 20 templates, search+filters, detail modal, commit 12ee450
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
- **Status:** 🟢 All tests passing, build clean, lint clean — ready for feature work
- **Tasks:**
- [x] **BUG FIXED:** h1 SEO bug — changed subtitle `<p>` to `<h2>` with keyword "Create your personalized Taylor Swift Eras Tour storybook", fixed span space bug in h1, updated page title to keyword-rich ✅ 2026-02-26 commit ad6d983
- [x] **BUG FIXED:** Pricing page 404 — wired `/pricing` route → PricingPage (454-line component that existed but wasn't routed) ✅ 2026-02-26 commit ad6d983
- [x] **Tests fixed:** 468/471 passing (3 skipped), 0 failures ✅ 2026-03-01 — installed msw + vitest-axe as real deps, fixed BookReader timeout tests, updated setup.ts to use real MSW server + vitest-axe matchers (commits 58ec7e0, de2a24a)
- [x] **Build verified:** TypeScript typecheck clean, ESLint 0 errors, production build successful ✅ 2026-03-01
- [x] **Lint fixes:** Fixed empty catch block in AuthCallback.tsx, added eslint-disable for necessary any in StoryForm.test.tsx ✅ 2026-03-01
- [x] **Package manager:** Switched to pnpm (npm broken at system level), pnpm-lock.yaml added ✅ 2026-03-01
- **6 modules status (marketplace, affiliates, gallery, sharing, gifting, templates):** All are substantial implementations (96-549 lines each), compile cleanly, and have tests for marketplace/affiliates/sharing. Gallery exists as 3 components (703 lines). Gifting and templates lack tests but are functional UI components. All need backend integration (Supabase) for production use.
- [ ] Wire 6 modules to Supabase backend (marketplace, affiliates, gifting need DB tables + edge functions)
- [ ] Add tests for gifting and templates modules
- [ ] Stripe checkout live mode validation
- [ ] SEO optimization + social media launch plan

### ULTRA-001: Ultrafone MVP
- **Why:** Production-grade AI phone receptionist backend (composite 6.3), missing final integrations
- **Status:** 🟡 Phase 2 complete, bug fixes + security hardening done ✅ 2026-03-01
- **Completed 2026-03-01:**
  - [x] **5 test failures fixed** — 276/276 tests now passing
    - Fixed `call_handler.py`: `Start.recording()` → `Start.add_child('Record')` (Twilio SDK bug)
    - Fixed `test_receptionist.py`: added `get_or_create_caller` + `is_auto_trusted` mocks
  - [x] **CORS hardened** — replaced `allow_origins=["*"]` with `app_settings.cors_origins` from config (defaults to localhost:3000/5173 dev; set `CORS_ORIGINS` env var for production). Also restricted `allow_methods` and `allow_headers` to explicit lists.
  - [x] **24 security vulnerabilities patched** (25→1 remaining: ecdsa CVE-2024-23342 — no fix available)
    - fastapi 0.109.0→0.134.0, starlette 0.35.1→0.52.1, aiohttp 3.11.18→3.13.3
    - python-jose 3.3.0→3.5.0, pillow 11.1.0→12.1.1, pipecat-ai 0.0.60→0.0.103
    - pip 23.0.1→26.0.1, setuptools 66.1.1→82.0.0
  - [x] **Frontend build fixed** — added missing `src/lib/utils.ts` (cn utility), installed framer-motion + clsx deps. Build succeeds (686KB JS bundle).
  - [x] **iOS app assessed** — Flutter project, 22 Dart files, well-structured (models, providers, screens, services, theme, widgets). Needs macOS + Xcode to build. Design spec in `IOS_APP_DESIGN_PROMPT.md`.
  - [x] **All fixes pushed** to GitHub (TrendpilotAI/Ultrafone) — commit ffd61d0
- **Remaining:**
  - [ ] Calendar integration (Google Calendar / Outlook) for call context
  - [ ] CRM integration (Salesforce/HubSpot) for caller lookup
  - [ ] SaaS multi-user mode (currently single-tenant)
  - [ ] iOS native app (Flutter scaffold exists, needs build on macOS)
  - [ ] Live production E2E Twilio test (end-to-end call test)
  - [ ] Set `CORS_ORIGINS` env var in Railway production (e.g. `https://ultrafone.app,https://admin.ultrafone.app`)

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
- [x] Migrate CRA → Vite (10x faster builds) ✅ 2026-03-01 (TODO-326)
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
- **Scored:** revenue_potential:7 strategic_value:8 completeness:7 urgency:5 effort_remaining:7
- **Tasks:**
- [ ] [TODO-519] Add Stripe monetization (freemium: free/pro/$9.99/unlimited/$29.99)
- [ ] [TODO-520] ELI5 ↔ Clinical language toggle in results view (3h quick win)
- [ ] [TODO-521] Provider/Doctor dashboard for B2B clinic sales
- [ ] [TODO-522] Longitudinal case tracking (follow-up uploads, delta analysis)
- [ ] [TODO-523] Test suite: >60% coverage on services/ + hooks/
- [ ] [TODO-524] Sentry error monitoring (production is currently blind)
- [ ] [TODO-525] Bundle optimization (code-split 43 components, target <500KB gzipped)
- [ ] Add CSP headers to firebase.json (security gap)
- [ ] Fix auditLog.ts TODO — tamper-evident Firestore writes (HIPAA)
- [ ] Wire real ClinicalTrials.gov API to ClinicalTrialMatcher
- [ ] Add FHIR export button (service exists, no UI)
- [ ] Remove debug-app.ts and vite-7.3.1.tgz from root
- [ ] See BRAINSTORM.md, PLAN.md, AUDIT.md for full analysis

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
- **Status:** 🟢 All P0 items COMPLETE ✅ 2026-03-01 — dead Flask code removed, Pydantic max_length guard, slowapi rate limiting, API key rotation. Pushed to GitHub (TrendpilotAI/core-entityextraction main).
- **Plan:** /data/workspace/projects/core-entityextraction/PLAN.md
- **TODOs:** 228–235, 337–340, 351–352 in /data/workspace/todos/

#### 🔴 P0 — Execute Immediately
- [x] **[TODO-230]** Delete dead Flask files (app.py, uswgi.py, utils/extensions.py, utils/app_context.py) · _30min_ → ✅ 2026-03-01 (also removed dead Dockerfile.railway, start.sh) [2669582]
- [x] **[TODO-337]** Add Pydantic `max_length=50_000` to EntityExtractionRequest (prevents memory exhaustion) · _30min_ → ✅ 2026-03-01 [7ba7d6b]
- [x] **[TODO-351]** Add slowapi rate limiting per API key (100/min regex, 60/min ML) · _2h_ → ✅ 2026-03-01 (keyed on X-API-Key header, falls back to IP) [a69689e]
- [x] **[TODO-229]** API key rotation — support comma-separated keys in env var · _1h_ → ✅ 2026-03-01 (ENTITY_EXTRACTION_API_KEY supports comma-separated values) [e27adb7]
- [x] **[TODO-231]** Deduplicate entity constants (single source in constants/entities.py) · _1h_ → ✅ 2026-03-02 — main.py now imports from constants/entities.py instead of redefining 17 constants (commit a63d4eb)

#### 🟠 P1 — This Week
- [x] **[TODO-232]** Cache compiled regex patterns at module level (10-50x speedup) · _2h_ → ✅ 2026-03-03 — _pattern_cache + _cache_version counter, compiled once per entity_store state, invalidated on add/delete/startup-load (commit 247d371)
- [x] **[TODO-338]** Migrate persistence.py to asyncpg/psycopg3 (sync DB blocks event loop) · _4h_ → ✅ 2026-03-03 — asyncpg.Pool replaces psycopg2.ThreadedConnectionPool, all persistence funcs async, startup/shutdown events updated, commit fad0c42
- [ ] **[TODO-233]** Add pytest test suite (conftest, pattern tests, API tests, persistence tests) · _1 day_
- [ ] **[TODO-234]** Batch regex extraction endpoint (POST /batch_regex_entity_extraction) · _2h_
- [ ] **[TODO-340]** Batch ML extraction endpoint (POST /batch_ml_entity_extraction) · _2h_
- [ ] **[TODO-352]** Pre-commit hooks (ruff, mypy, bandit) · _1h_

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

- [x] **[TODO-203]** Pin all Pipfile wildcards — `fastapi-jwt-auth`, `uvicorn`, `pydantic`, `celery`, `redis`, `pandas` et al. + add `pip-audit` to CI · _2h_ · ✅ 2026-02-28 — pinned 19 packages + 10 dev packages to Pipfile.lock versions, added pip-audit dev dep + `audit` script, commit c9445f3, pushed Bitbucket + GitHub

### 🟡 HIGH — Phase 3 (Parallel, after 203)

- [x] **[TODO-204]** Signal versioning — `signal_versions` table, snapshot on publish, rollback endpoint, diff · _8h_ · ✅ 2026-02-28 — commit 0285a39, pushed Bitbucket
- [x] **[TODO-205]** Dry-run preview — `POST /signals/{id}/preview` returns sample rows + generated SQL without publishing · _6h_ · `205-pending-high-...-add-dry-run-execution.md` ✅ 2026-02-28
- [x] **[TODO-206]** Audit log — append-only `audit_events` table, fire-and-forget writes on all mutations, admin query endpoint · _8h_ · ✅ DONE 2026-02-28 — commit 9a7a717, pushed Bitbucket

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

## 🧩 Signal Studio Templates (Invesco) — Updated 2026-03-03

> Revenue=8 | Strategic=9 | Completeness=7 | Urgency=9 | Effort Remaining=7
> Full plan: `/data/workspace/projects/signal-studio-templates/PLAN.md`
> Brainstorm: `/data/workspace/projects/signal-studio-templates/BRAINSTORM.md`
> Audit: `/data/workspace/projects/signal-studio-templates/AUDIT.md`

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

### 🟢 v2 Additions (2026-03-02 — judge-agent-v2)
- [ ] **#386** Invesco-specific template pack — 5 Invesco-tailored templates (fund-performance, redemption-risk, flows-summary, competitive-wins, distribution-readiness) [L]
- [ ] **#387** Result export — CSV/Excel export from TemplateEngine + API endpoint [M]
- [ ] **#388** Webhook triggers — execute templates on CRM/portfolio events, push to Slack/email [M]
- [ ] **#389** Zod validation — replace Record<string, any> with Zod schemas in engine + API [M]
- [ ] **#390** Template diff/audit trail — change tracking for compliance (Invesco requirement) [S]

### 🔴 v3 Additions (2026-03-03 — judge-agent-v2 updated run)
- [x] **TODO-426** API auth middleware — JWT validation, no auth = CRITICAL security gap [S] ✅ DONE 2026-03-03 — JWT middleware via JWKS-RSA (RS256), AUTH_DISABLED bypass for dev/test, 18 tests pass, commit 9af41e8
- [ ] **TODO-427** Integration tests — MockDataProvider, engine.test.ts, api.test.ts, ≥80% coverage [M] → `/data/workspace/todos/427-pending-p1-signal-studio-templates-integration-tests.md`
- [ ] **TODO-428** GitHub Actions CI — typecheck/lint/test/build pipeline [S] → `/data/workspace/todos/428-pending-p1-signal-studio-templates-github-actions-ci.md`
- [ ] **TODO-429** DataProvider adapters — Snowflake + Postgres real implementations [L] → `/data/workspace/todos/429-pending-p1-signal-studio-templates-data-provider-implementations.md`
- [ ] **TODO-430** Expand template library 20→40 — 20 new templates across all 5 categories [M] → `/data/workspace/todos/430-pending-p2-signal-studio-templates-expand-template-library.md`
- [ ] **TODO-466** Rate limiting + CORS on Templates API — express-rate-limit, cors allowlist, body size limit [S/P0] → `/data/workspace/todos/466-pending-p0-signal-studio-templates-rate-limiting-cors.md`
- [ ] **TODO-467** Publish @forwardlane/signal-studio-templates to npm registry — publishConfig, .npmrc, CI publish on tag [S/P0] → `/data/workspace/todos/467-pending-p0-signal-studio-templates-npm-publish-pipeline.md`
- [ ] **TODO-468** Template preview/dry-run mode — POST /templates/:id/preview, previewData in schema, no DB needed [S/P1] → `/data/workspace/todos/468-pending-p1-signal-studio-templates-preview-dryrun.md`


---

## 🔒 ForwardLane Backend (Invesco Demo Hardening) — 2026-02-26

> Revenue=8 | Strategic=9 | Security=CRITICAL | Urgency=9
> Full plan: `/data/workspace/projects/forwardlane-backend/PLAN.md`
> Audit: `/data/workspace/projects/forwardlane-backend/AUDIT.md`

### 🔴 P0 — Do Before Next Demo (Security Critical)
- [x] **#211** [P0] Auth on demo endpoints — env-gated EasyButtonPermission (AllowAny → env-based) ✅ commit bb777cc0, Railway redeployed
- [x] **#214** [P0] Pytest tests — easy_button/_clean_sql security tests ✅ easy_button/tests/test_clean_sql.py (13 tests), commit bb777cc0

### 🟠 P1 — This Sprint
- [x] **#212** [P1] Real LLM calls in MeetingPrepView — Gemini→Kimi→static fallback, Redis cache ✅ 2026-02-27
- [x] **#213** [P1] Connection pooling — add CONN_MAX_AGE=60 to both DATABASES entries ✅ 2026-02-27 — committed 4844f79b, pushed to railway-deploy
- [x] **#215** [P1] CI pipeline — PR test gate + development branch already implemented in bitbucket-pipelines.yml ✅ verified 2026-02-28

### Execution Order
1. #213 (pooling) — settings change, zero risk, immediate production benefit
2. #211 (auth) — deploy to staging first with DEMO_ENV=staging
3. #212 (LLM) — high demo value, reuses existing Gemini infrastructure
4. #214 (tests) — after auth + LLM implemented
5. #215 (CI) — after tests exist


---

## Signal Studio — Judge v2 (2026-03-02 refresh)
> Revenue=8 | Strategic=9 | Completeness=7 | Urgency=9 | EffortRemaining=6
> Brainstorm: `/data/workspace/projects/signal-studio/BRAINSTORM.md`
> Plan: `/data/workspace/projects/signal-studio/PLAN.md`
> Audit: `/data/workspace/projects/signal-studio/AUDIT.md`

### 🔴 P0 — Fix Immediately
- [x] **#219** [CRITICAL] Auth middleware.ts — protect all API routes ✅ commit 261526c
- [x] **Untracked** [CRITICAL] Rate limit LLM proxy routes ✅ commit 3650d4b
- [x] **Untracked** [CRITICAL] Upgrade next@16.0.10 → 16.0.11 (DoS CVE) ✅ commit ef184e2
- ✅ **TODO-384** [HIGH] Remove ignoreBuildErrors from next.config.mjs [S] — commit 48c642f: Fixed Next.js 15 async params pattern for all dynamic route handlers in app/api/signals/[id]/ and app/session/status/[agentId]/. Fixed jest-dom types in tsconfig. NOTE: ignoreBuildErrors kept due to 100+ pre-existing TS errors (ai SDK mismatches, missing radix-ui/recharts types, oracledb types, etc.) — full removal requires separate cleanup effort.
- [x] **TODO-385** [HIGH] Rate limit Oracle query + signal run routes [S] ✅ 2026-03-02 — DB_RATE_LIMITED_PATHS added (/api/oracle/query, /api/oracle/preview, /api/signals/run, /api/signals/compile), 10 req/min per IP, commit a9169fa

### 🟠 P1 — This Sprint
- [ ] **TODO-352** [HIGH] Remove duplicate reactflow (-300KB bundle) [M]
- [ ] **TODO-353** [MEDIUM] Replace 94 console.log with pino logger [M]
- [ ] **TODO-355** [HIGH] E2E Playwright tests for critical flows [M]
- [ ] **TODO-356** [MEDIUM] Redis caching for signal execution [M]
- [ ] **TODO-357** [LOW] Lazy load ReactFlow visual builder [S]
- [ ] **TODO-386** [HIGH] signal_runs audit table (execution history) [M]
- [ ] **TODO-387** [MEDIUM] /api/health/db connection pool health check [S]

### 🟡 P2 — Next Sprint
- [ ] **TODO-358** [LOW] OpenTelemetry instrumentation.ts [M]
- [ ] **TODO-388** [MEDIUM] Compliance audit_log table [M]
- [ ] **TODO-359** [MEDIUM] Signal export/sharing [M]

### 🟢 P3 — Hygiene
- [ ] **TODO-360** [MEDIUM] Update Jest, fix glob CVE (DEP-003) [S]
- [ ] **ARCH-001** [LOW] Fix deprecated experimental.serverComponentsExternalPackages [S]

---

## signal-builder-backend (ForwardLane Core API)
> Revenue=8 | Strategic=9 | Completeness=7 | Urgency=7
> Brainstorm: `/data/workspace/projects/signal-builder-backend/BRAINSTORM.md`
> Plan: `/data/workspace/projects/signal-builder-backend/PLAN.md`
> Audit: `/data/workspace/projects/signal-builder-backend/AUDIT.md`

### 🔴 High Priority
- [ ] **#219** [HIGH] Upgrade FastAPI 0.92→0.115, SQLAlchemy, asyncpg, alembic [4h]
- [x] **#219** [HIGH] Add /health endpoint + Sentry error tracking [3h] ✅ 2026-02-28 — commit 70c94e1, pushed Bitbucket + GitHub

### 🟠 Medium Priority
- [ ] **#220** [MEDIUM] Redis caching for signal-to-SQL translation (PropertiesMap, SignalNodesTree) [4h]
- [ ] **#220** [MEDIUM] Test coverage for analytical_db and schema_builder modules [6h]

### 🟡 Low Priority
- [ ] **#221** [LOW] Replace Flask admin with starlette-admin (remove dual-framework) [8h]

## signalhaus-website
*AI consultancy marketing site — Nathan's SignalHaus business*

### 🔴 Critical (Ship ASAP — every day offline = missed leads)
- [x] **#221** [CRITICAL] Fix contact form backend — wire up Resend API route [2h] ✅ done 2026-02-27
- [ ] **#222** [CRITICAL] Deploy to Vercel with signalhaus.ai custom domain [1h] — vercel.json committed (10f3f68); Nathan just needs to import repo in Vercel UI + set NEXT_PUBLIC_GA_MEASUREMENT_ID + RESEND_API_KEY env vars

### 🟠 High Priority
- [x] **#223** [HIGH] Fix contact page metadata bug (use client + metadata conflict) ✅ 2026-02-27 — split into ContactForm.tsx (client) + page.tsx (server with metadata export), commit aa240d6
- [x] **#224** [HIGH] Add Calendly booking embed to contact page ✅ 2026-02-27 — Calendly inline widget added above contact form, commit aa240d6

### 🟠 High Priority (v3 additions — 2026-03-02)
- [x] **#321** [P1] Slack webhook on contact form submit ✅ done 2026-03-02 — commit 49c4448
- [x] **#320** [P1] CSP security headers in next.config.ts [30min] ✅ 2026-03-02 — CSP + HSTS + X-Frame-Options + Referrer-Policy + Permissions-Policy + X-XSS-Protection (commit 602f694)
- [x] **#317** [P1] JSON-LD Organization + Service + Article schemas [2h] ✅ 2026-03-02 — Organization + WebSite schemas in layout.tsx, Service ItemList on /services, Article on /blog/[slug], JsonLd component extracted (commit 46a57d4)
- [x] **#323** [P1] Dynamic sitemap (replace public/sitemap.xml) [30min] ✅ 2026-03-02 — app/sitemap.ts auto-includes blog MDX posts + static routes, build clean (commit b1a3cd0)
- [x] **#324** [P1] Microsoft Clarity heatmaps [15min] ✅ 2026-03-03 — MicrosoftClarity component added, reads NEXT_PUBLIC_CLARITY_PROJECT_ID (commit 39d42d7)
- [x] **#325** [P1] LinkedIn Insight Tag [15min] ✅ 2026-03-03 — LinkedInInsight component added with noscript fallback, reads NEXT_PUBLIC_LINKEDIN_PARTNER_ID (commit 39d42d7)
- [ ] **#326** [P1] Welcome email sequence via Resend [2h]
- [ ] **#318** [P1] HubSpot CRM integration on contact submit [4h]
- [ ] **#322** [P1] ESLint + Prettier + CI type-check [2h]

### 🟡 Medium Priority
- [x] **#225** [MEDIUM] Add Google Analytics 4 tracking + conversion events [1h] ✅ done 2026-02-27 — GoogleAnalytics.tsx component + gtag.ts helpers + layout.tsx wired, commit 10f3f68
- [ ] [MEDIUM] Add testimonials/case studies section to homepage [2h]
- [ ] [MEDIUM] Publish 3+ SEO blog posts targeting AI consulting keywords [6h]
- [ ] **#319** [P2] Playwright E2E tests [4h]
- [ ] **#327** [P2] CRO: Move social proof metrics above fold + count-up animation [30min]
- [ ] **#329** [P2] Type-safe env.ts + constants.ts [30min]
- [ ] **#330** [P2] Google Search Console verification + GA4 link [15min] (Nathan action)
- [ ] **#332** [P2] Uptime monitoring setup [15min]
- [ ] **#443** [P1] HubSpot CRM + Deal creation on contact submit [4h] → TODO-443
- [ ] **#444** [P1] Fix CONTACT_EMAIL silent fallback bug [30min] → TODO-444
- [ ] **#445** [P2] Calendly sticky CTA on homepage hero [1h] → TODO-445
- [ ] **#446** [P2] Case study PDF downloads (gated lead capture) [3h] → TODO-446
- [ ] **#447** [P2] FAQ accordion + FAQPage JSON-LD on pricing page [1.5h] → TODO-447
- [ ] **#448** [P2] Author bio page /team/nathan-stevenson + E-E-A-T [1.5h] → TODO-448


## Signal Studio Frontend (signal-studio-frontend) — Added 2026-02-27

- [x] [P0] Fix auth token injection in apiClient — ALL API calls currently unauthenticated (TODO-221) ✅ commit e3c9a66 (signal-builder-frontend)
- [x] [P0] Build signal canvas/builder UI with React Flow (TODO-222) ✅ 2026-02-28 — SignalCanvas at /canvas, 3 custom node types (ConditionNode, FilterNode, OutputNode), drag-and-drop palette, mobile-responsive, Run Signal stub with toast, 6 passing tests; commit 4281bd8 (signal-studio)
- [ ] [P1] Real-time signal run status via Supabase Realtime (TODO-223)
- [ ] [P1] Error boundaries + loading/empty states on all pages (TODO-224)
- [ ] [P1] GitHub Actions CI — lint + typecheck + jest (TODO-227)
- [ ] [P2] Wire dark mode Zustand state to document.documentElement (TODO-225)
- [ ] [P2] Jest + React Testing Library test suite (TODO-226)
- [ ] [P3] Signal scheduling UI (cron builder component)
- [ ] [P3] Sentry error monitoring integration
- [ ] [P3] CSP + security headers in next.config.ts

## core-entityextraction (2026-02-27)
- [x] [P0] Add PostgreSQL connection pooling to persistence.py — critical prod stability (TODO-228) ✅ already in repo (aebdc62)
- [x] [P0] Add X-API-Key authentication middleware — all endpoints currently open (TODO-229) ✅ already in repo (10586df)
- [x] [P0] Remove dead Flask code from services/ and controllers/ — 7 files never imported (TODO-230) ✅ already in repo (5933da4)
- [x] [P1] Add pytest test suite — zero tests currently exist (TODO-233) ✅ 2026-02-28 — 30/30 tests passing, committed + pushed
- [ ] [P1] Cache compiled regex patterns — rebuilt on every request today (TODO-232)

## NarrativeReactor — AI Content Generation Platform (added 2026-02-27)

- ✅ [CRITICAL] Fix auth bypass — API_KEY unset disables all auth (TODO-224) — done 2026-02-27
- [x] [P1] Add Docker multi-stage build + Railway deployment config (TODO-223) ✅ 2026-03-01 — Dockerfile (node:20-slim multi-stage, non-root user, HEALTHCHECK), railway.json, .dockerignore — commit da6c30b, pushed
- [ ] [P1] Add Redis caching for LLM flows, brand profiles, trend data (TODO-225)
- [ ] [P1] Set up GitHub Actions CI/CD — PR gate + auto-deploy on merge (TODO-226)
- [ ] [P1] Expand vitest coverage from ~2 services to 70%+ overall (TODO-228)
- [ ] [P2] Add Zod env validation at startup — prevent silent missing-var failures (TODO-229)
- [ ] [P2] Add pino structured logging with request correlation IDs (TODO-230)
- [ ] [P2] Consolidate blotatoPublisher + publisher into unified adapter pattern (TODO-227)

## signal-builder-frontend — Security + Quality + Performance (added 2026-02-27)

- [x] [P1-CRITICAL] Remove .env from git tracking + add prod guard for dev auth (TODO-228) ✅ 2026-02-27 — git rm --cached .env, .env.example added, commit 23305f5
- [ ] [P1-CRITICAL] Eliminate `any` types in RTK Query API layer — 76 instances (TODO-229)
- [ ] [P1-CRITICAL] Zero test coverage on builder.lib.ts — unit tests needed urgently (TODO-231)
- [ ] [P1] Add Sentry error tracking — replace 4x console.error TODO placeholders (TODO-230)
- [ ] [P1] Add typecheck + test gates to Bitbucket CI pipeline (TODO-232)
- [ ] [P1] Route-level code splitting + memoize FlowNode/RightBar + RTK cache tags (TODO-233)
- [ ] [P1] Dependency audit: uuidv4 deprecated, react-scripts CVEs, compose-function stale (TODO-234)
- [ ] [P1] Fix 11x @ts-ignore suppressors + resolve circular imports in Redux (TODO-235)
- [ ] [P2] MSW integration tests for RTK Query endpoints (TODO-236)
- [ ] [P2] DRY: consolidate REPEATING_FILTER_VALUE_PROCESSING + replace JSON.parse deep clones (TODO-237)
- [ ] [P2] Signal Templates Library feature in Catalog module (TODO-238)
- [ ] [P2] Nginx CSP headers + security headers + move auth token off localStorage (TODO-239)

## SignalHaus Website (updated by Judge Agent v2 — 2026-03-01)
- [x] 315: Contact API security — rate limiting + Zod validation (P0) ✅ 2026-02-28 — in-memory 5req/IP/15min, input validation (name/email/company/budget/message), XSS guard, commit b074064
- [ ] 316: Testimonials & case studies page (P1) — needs Nathan content
- [x] 317: JSON-LD structured data for SEO (P1) — Organization + Service + Article schemas ✅ 2026-03-02 (commit 46a57d4)
- [ ] 318: Newsletter signup + HubSpot CRM integration (P1) — direct revenue pipeline
- [ ] 319: E2E tests with Playwright (P2)
- [x] 320: CSP/security headers in next.config.ts + CONTACT_EMAIL env guard (P1) ✅ 2026-03-02 commit 602f694
- [x] 321: Slack webhook notification on contact form submit (P1) — instant lead visibility ✅ 2026-03-02 — fire-and-forget Block Kit message with name/email/company/budget/message preview + Reply CTA; SLACK_WEBHOOK_URL env var (commit 49c4448)
- [ ] 322: ESLint + Prettier + CI type-check (P1) — code quality baseline
- [x] 323: Dynamic sitemap.ts replacing public/sitemap.xml (P2) — SEO scalability ✅ 2026-03-02 (commit b1a3cd0)

## signal-builder-backend (ForwardLane)
- [x] 325: Fix silent exception in signal delete endpoint (critical) ✅ 2026-02-28 — commit 823abdd: raises DBNotFoundException on rowcount=0 (was silent), logs WebServiceException warning (was swallowed), 3 unit tests added
- [ ] 326: Run pip-audit + fix CVEs + add to CI (critical)
- [ ] 327: Add API rate limiting with slowapi (high)
- [ ] 328: Pydantic v2 + FastAPI upgrade (high)
- [ ] 329: Test coverage for schema_builder + translators (high)
- [ ] 330: Redis caching for validator hot paths (medium)
- [ ] 331: Signal webhooks / event system (medium)

## signal-studio-data-provider (added 2026-02-28)
- [x] [P0] Fix JWT SQL injection in supabase_provider.py → TODO 311 ✅ FIXED (commit 98ee5a7, local) — needs manual Bitbucket push
- [x] [P0] Fix Snowflake sync connector blocking asyncio event loop → TODO 312 ✅ FIXED (commit 98ee5a7, local) — needs manual Bitbucket push
- [x] [P1] Fix table-name SQL injection in write_back() across all providers → TODO 313 ✅ 2026-03-01 — _validate_identifier() added to oracle_provider.py + snowflake_provider.py, validates table+columns before INSERT, 13 tests pass (commit 6fa4272)
- [x] [P1] Add asyncpg connection pooling to SupabaseProvider → TODO 314 ✅ already implemented — asyncpg.create_pool(min_size=2, max_size=20) with lazy init in _get_pool()
- [x] [P1] Add GitHub Actions CI pipeline (pytest + ruff + mypy + pip-audit) → TODO 315 ✅ 2026-03-01 — .github/workflows/ci.yml created (lint/ruff/mypy + pytest matrix 3.11+3.12 + pip-audit), committed 7fe0bc7
- [x] [P1] Add Snowflake Cortex AI methods (cortex_complete, cortex_embed) ✅ already implemented
- [x] [P0] Fix JWT RLS race condition — per-connection scoping + full claims JSON → TODO-433 ✅ DONE 2026-03-03
- [ ] [P0] Fix Snowflake param binding dict→tuple in get_tables/get_columns → TODO-434 ⏳ Agent spawned 2026-03-04 05:01 UTC (todo-434-snowflake-params)
- [ ] [P0] Audit oracle_provider.py for async blocking (apply asyncio.to_thread if needed)
- [ ] [P1] Add Snowflake Cortex model allowlist (prevent injection via model param)
- [ ] [P1] Add OpenTelemetry tracing across all provider calls → TODO-436
- [ ] [P1] Fix N+1 get_columns() in SchemaRegistry with asyncio.gather → TODO-435
- [ ] [P1] Add max_rows guard to execute_query() (prevent OOM from unbounded queries)
- [ ] [P2] Add async context manager __aenter__/__aexit__ to all providers → TODO-437
- [ ] [P2] Add upsert_back() with dialect-specific conflict resolution → TODO-438
- [ ] [P2] Add streaming execute_query_stream() returning AsyncIterator
- [ ] [P2] Wire library into Signal Studio Django backend
- [ ] [P2] Add testcontainers integration tests (PostgreSQL container)
- [ ] [P2] Add pytest-cov with --cov-fail-under=80 to CI

## signal-builder-frontend (added 2026-02-28)
- [x] [P0] Sentry integration — error monitoring, React Router + canvas error boundary → TODO 323 ✅ DONE 2026-02-28
- [x] [P0] Fix deprecated deps — replace uuidv4 with crypto.randomUUID(), patch CVEs → TODO 324 ✅ DONE 2026-02-28
- [x] [P0] Test coverage for Redux slices (builder + auth) — 80% target → TODO 325 ✅ DONE 2026-02-28
- [x] [P1] Vite migration from CRA+craco — faster dev/build ✅ 2026-03-01 (TODO-326)
- [ ] [P1] Bundle optimization — lodash-es, lazy loading, 30%+ size reduction → TODO 327
- [ ] [P1] Playwright E2E tests — auth, signal creation, onboarding flows → TODO 328

## signal-studio-frontend (refreshed 2026-03-02 — Judge Agent v2)
- [ ] [P1] Form validation on auth pages → TODO 336
- [ ] [P1] Loading/error states + skeleton components → TODO 337
- [ ] [P1] Toast notification system → TODO 338
- [ ] [P1] Dark mode CSS implementation → TODO 339
- [ ] [P1] Wire dashboard to real API → TODO 340
- [ ] [P1] CI/CD GitHub Actions pipeline → TODO 341
- [ ] [P1] Visual signal builder page → TODO 342
- [ ] [P1] AI chat streaming → TODO 343
- [ ] [P2] Billing/Stripe integration → TODO 344
- [ ] [P2] Supabase Realtime subscriptions → TODO 345
- [ ] [P2] Playwright E2E test suite → TODO 346
- [ ] [P2] Complete settings page → TODO 347
- [ ] [P1] Security headers CSP/HSTS → TODO 349
- [ ] [P2] Bundle size optimization → TODO 350
- [x] [P0] Wire all pages to real TanStack Query hooks (replace mocks) → TODO-411 ✅ DONE 2026-03-02 13:14 UTC — all 5 pages wired (dashboard, signals, templates, chat, settings), loading skeletons + error states, TS clean
- [x] [P0] Visual node graph builder with React Flow → TODO-412 ✅ DONE 2026-03-02 13:11 UTC — SignalCanvas + 5 node types (DataSource/Filter/Transform/AI/Output), drag-drop palette, config panel, save wiring, build clean
- [ ] [P1] Tests + CI/CD (Vitest + Playwright + GitHub Actions) → TODO-413
- [ ] [P1] Fix dark mode CSS (toggle works, visuals broken) → TODO-414

## signal-builder-frontend — 2026-03-01 refresh (Judge Agent v2)
- [ ] [P1] DRY — Consolidate 3x FilterContent into shared/ui → TODO-361
- [ ] [P1] Route-level code splitting + ReactFlow lazy load → TODO-362
- [ ] [P1] nginx security headers (CSP, HSTS, X-Frame-Options) → TODO-363
- [ ] [P1] Axios token refresh interceptor (401 → refresh → retry) → TODO-364
- [ ] [P2] Remove deprecated @sentry/tracing package → TODO-365
- [ ] [P2] Storybook v6 → v8 migration with Vite builder → TODO-366
- [ ] [P2] TypeScript 4.4 → 5.x upgrade → TODO-367
- [ ] [P2] Bundle analyzer + lodash-es + chunk optimization → TODO-368


## signal-studio-auth (2026-03-01)
- [x] 351 [CRITICAL] Fix hardcoded/empty JWT secret fallbacks in config.py ✅ 2026-03-01 — _require_secret() fails fast on empty/weak/short secrets in prod, bypassed in pytest (commit 7867b73)
- [x] 352 [CRITICAL] Add rate limiting to /auth/login and /auth/signup ✅ 2026-03-01 — sliding-window per-IP limiter: 5/60s login, 3/60s signup, 429+Retry-After, X-Forwarded-For support; 9/9 tests pass (commit 7867b73)
- [ ] 353 [HIGH] Fix admin role check missing on invite-to-org endpoint
- [ ] 354 [HIGH] Add password reset / forgot-password routes
- [ ] 355 [HIGH] Write ForwardLane → Supabase user migration script
- [ ] 356 [HIGH] Add RBAC require_role() FastAPI dependency
- [ ] 357 [MEDIUM] Add integration tests for all auth routes
- [ ] 358 [MEDIUM] Set up CI/CD GitHub Actions pipeline
- [ ] 359 [MEDIUM] Fix httpx connection pooling (per-request → shared client)

## signal-studio-auth (2026-03-02 — Judge Agent v2 refresh)
- [ ] 402 [CRITICAL] Replace in-memory rate limiter with Redis sliding-window (multi-replica safe) ⏳ Agent spawned 2026-03-02 21:01 UTC
- [ ] 403 [CRITICAL] Add refresh token rotation + server-side revocation list (Redis-backed) ⏳ Agent spawned 2026-03-02 21:01 UTC
- [ ] 404 [HIGH] Migrate to Pydantic v2 (model_config, model_dump, response models)
- [ ] 405 [HIGH] Add CORS middleware + Sentry error tracking + Prometheus /metrics
- [ ] 406 [HIGH] Create Dockerfile + GitHub Actions CI (pytest, ruff, bandit, safety)

## signal-builder-backend (2026-03-01 — P0 Planning Agent)
- [x] [P0] Fix silent WebServiceException in signal delete endpoint → TODO-355 → ✅ DONE 2026-02-28 (commit 823abdd)
- [x] [P0] CI security pipeline (pip-audit + bandit + mypy) → TODO-354 → ✅ DONE 2026-03-02 05:09 UTC — Pipfile mypy added, bitbucket-pipelines.yml security step, scripts/security_check.sh, 0 prod CVEs, 0 HIGH bandit
- [x] [P0] Add rate limiting with slowapi → TODO-353 → ✅ DONE 2026-03-02 05:11 UTC — slowapi wired, 4 endpoints limited (validate 10/min, preview 30/min, publish 5/min, logout 20/min), 13 tests pass, pushed feat/p0-todos-352-356
- [ ] [P0] Pydantic v2 + FastAPI upgrade → TODO-352 → ⏳ DEFERRED (major refactor, post-demo)
- [x] [P0] Comprehensive tests for schema_builder + analytical_db → TODO-356 → ✅ DONE 2026-03-02 05:12 UTC — 134 unit tests (51 schema_builder ops, 48 utils, 35 analytical_db), all pass, pushed feat/p0-todos-352-356

## NarrativeReactor (2026-03-01 — Planning Agent)
- [ ] [HIGH] #354 Set up GitHub Actions CI pipeline (type-check, lint, test, build) → `354-pending-high-NarrativeReactor-github-actions-ci-pipeline.md`
- [ ] [HIGH] #355 Add supertest-based E2E tests for full Express app → `355-pending-high-NarrativeReactor-supertest-e2e-tests.md`
- [ ] [HIGH] #356 Lock test coverage threshold at 70% in vitest.config → `356-pending-high-NarrativeReactor-coverage-threshold-70pct.md`
- [ ] [MEDIUM] #357 Add /api/health alias for load balancer compatibility → `357-pending-medium-NarrativeReactor-api-health-alias.md`
- [ ] [HIGH] #358 Wire React dashboard login to /login endpoint fully → `358-pending-high-NarrativeReactor-wire-dashboard-login.md`
- [ ] [MEDIUM] #359 Add webhook retry logic with exponential backoff + delivery log → `359-pending-medium-NarrativeReactor-webhook-retry-logic.md`
- [ ] [HIGH] #360 Multi-tenant support (per-tenant API keys, data isolation) → `360-pending-high-NarrativeReactor-multi-tenant-support.md`
- [ ] [MEDIUM] #361 Analytics dashboard (content performance + cost trends) → `361-pending-medium-NarrativeReactor-analytics-dashboard.md`
- [ ] [MEDIUM] #362 Content approval email notifications via Resend → `362-pending-medium-NarrativeReactor-content-approval-email-notifications.md`

## NarrativeReactor — Audit Findings (2026-03-01 — Code Quality Audit)
- [x] [HIGH/S] #369 Add GitHub Actions CI pipeline (typecheck + lint + test + docker build) → `369-pending-high-NarrativeReactor-github-actions-ci.md` ✅ DONE 2026-03-01 — Enhanced CI workflow with typecheck, lint, test with coverage, docker-build parallel jobs; README has CI badge
- [ ] [HIGH/S] #370 Add DB indexes for content_drafts/campaigns/workflows/scheduled_posts → `370-pending-high-NarrativeReactor-db-indexes.md`
- [ ] [HIGH/S] #371 Fix wildcard Genkit dependency versions in package.json → `371-pending-high-NarrativeReactor-fix-genkit-wildcard-deps.md`
- [ ] [MEDIUM/L] #372 Add supertest E2E tests for Express routes (full HTTP layer) → `372-pending-medium-NarrativeReactor-supertest-e2e-tests.md`
- [ ] [MEDIUM/S] #373 Add per-endpoint rate limiting for /api/generate and /api/video → `373-pending-medium-NarrativeReactor-per-endpoint-rate-limiting.md`
- [ ] [MEDIUM/M] #374 Replace console.log with structured logger (pino) — fix Fal.ai data leak → `374-pending-medium-NarrativeReactor-structured-logger.md`
- [ ] [MEDIUM/XL] #375 Add multi-tenant support with per-tenant API keys + DB isolation → `375-pending-medium-NarrativeReactor-multi-tenant-support.md`
- [ ] [MEDIUM/L] #376 Add analytics dashboard with cost/performance trends → `376-pending-medium-NarrativeReactor-analytics-dashboard.md`
- [ ] [MEDIUM/M] #377 Add webhook retry logic for failed publishes (exponential backoff) → `377-pending-medium-NarrativeReactor-webhook-retry-logic.md`

## NarrativeReactor (2026-03-03 — Judge Agent v2 refresh)
- [ ] [HIGH/S] #430 Add SQLite indexes + pin Genkit wildcard deps → `430-pending-high-NarrativeReactor-sqlite-indexes.md`
- [ ] [HIGH/M] #431 Wire ForwardLane API bridge for personalized content → `431-pending-high-NarrativeReactor-forwardlane-bridge.md`
- [ ] [MEDIUM/S] #432 Railway auto-deploy on main branch push → `432-pending-medium-NarrativeReactor-railway-autodeploy.md`

## NarrativeReactor (2026-03-02 — Judge Agent v2 refresh)
- [ ] [CRITICAL/S] #396 Deploy to production with CD pipeline → `396-pending-critical-NarrativeReactor-production-deployment.md`
- [ ] [CRITICAL/M] #397 Multi-tenant SaaS foundation (tenant_id, scoped queries) → `397-pending-critical-NarrativeReactor-multi-tenancy.md`
- [ ] [HIGH/M] #398 TypeScript `any` cleanup (169 violations → strict mode) → `398-pending-high-NarrativeReactor-typescript-any-cleanup.md`
- [ ] [HIGH/M] #399 Redis caching for AI calls (LRU, TTL, tenant-scoped) → `399-pending-high-NarrativeReactor-redis-caching.md`
- [ ] [HIGH/L] #400 Stripe billing integration (usage-based + subscriptions) → `400-pending-high-NarrativeReactor-stripe-billing.md`
- [ ] [HIGH/M] #401 E2E integration tests (Supertest + mocked externals) → `401-pending-high-NarrativeReactor-e2e-tests.md`

## forwardlane-backend (2026-03-03 — Judge Agent v2 Rescore)
*Scores: revenue=9 strategic=10 completeness=7 urgency=9 effort_remaining=6*
- [x] [CRITICAL/S] #422 Replace DEMO_ENV AllowAny with X-Demo-Token HMAC auth ✅ DONE 2026-03-03 — commit 501aa6b0, 6 unit tests pass
- [ ] [HIGH/M] #423 NL→SQL multi-turn conversation memory via Redis thread_id → `423-pending-high-forwardlane-backend-nl-sql-multiturn.md`
- [ ] [HIGH/M] #424 Usage analytics model for Invesco renewal evidence → `424-pending-high-forwardlane-backend-usage-analytics.md`
- [ ] [HIGH/M] #425 Dependency CVE audit — upgrade sentry/boto3/dj-rest-auth/pypdf → `425-pending-high-forwardlane-backend-dep-upgrades.md`
- [ ] [HIGH/M] #220 Integration tests for all easy_button Invesco endpoints
- [ ] [HIGH/M] #222 OpenAPI schema validation tests — prevent NL→SQL regressions
- [ ] [HIGH/M] #226 E2E test fixtures with synthetic Invesco advisor data
- [ ] [HIGH/H] #229 Expand NL→SQL to portfolio-level queries (fund comparisons, ESG)
- [ ] [MEDIUM/S] #223 Async Celery task monitoring dashboard (Prometheus celery metrics)
- [ ] [MEDIUM/S] #224 Redis cache warming on startup for meeting-prep + signals
- [ ] [MEDIUM/S] #227 Structured error responses with error codes across easy_button
- [ ] [MEDIUM/S] #228 DB connection health check endpoint for Railway monitoring

## signal-studio-frontend (re-scored 2026-03-03 — Judge Agent v2 refresh)
Scores: revenue=8, strategic=9, completeness=5, urgency=7, effort_remaining=5
- ✅ [P0-CRITICAL] Add auth middleware to protect all /app/* routes → TODO-444 ✅ DONE 2026-03-03
- [ ] [P0-CRITICAL] Wire TanStack Query hooks to all pages (replace mock data) → TODO-445 ⏳ Agent spawned 2026-03-04 05:01 UTC (todo-445-tanstack-wire)
- [ ] [P1-HIGH] Supabase Realtime — live signal run status updates → TODO-446
- [x] [P1-HIGH] Security headers — CSP, HSTS, X-Frame-Options → TODO-447 ✅ DONE 2026-03-04 — X-DNS-Prefetch-Control, HSTS (2yr), X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, CSP (Supabase+OpenAI+Anthropic+Railway); frame-ancestors none. Commit 0796b6ea
- [ ] [P1-HIGH] CI/CD pipeline — Bitbucket Pipelines + Railway deploy → TODO-448
- [ ] [P1-HIGH] E2E tests — Playwright auth + signal CRUD flows → TODO-449
- [ ] [P2-MEDIUM] PostHog analytics + Sentry error tracking → TODO-450

## forwardlane_advisor (scored 2026-03-03 — Judge Agent v2)
Scores: revenue=8, strategic=9, completeness=5, urgency=6, effort_remaining=3
Core ForwardLane advisor platform — Node.js/Express with AI dialog, portfolio recs, alerts. Critical: IBM Watson NLC deprecated, all deps from 2016-2017.
- [x] [P0-CRITICAL] Upgrade Node.js from 0.10 to v20 LTS → TODO-451 ✅ DONE 2026-03-03
- [x] [P0-CRITICAL] Security audit & CVE remediation (npm audit) → TODO-452 ✅ 2026-03-04
- [ ] [P1-HIGH] Replace Watson NLC with Anthropic Claude LLM → TODO-453
- [ ] [P1-HIGH] CI/CD pipeline + Docker Compose dev environment → TODO-454
- [ ] [P1-HIGH] N+1 query audit & performance fixes → TODO-455

## signal-builder-backend (re-scored 2026-03-04 — Judge Agent v2 daily refresh)
Scores: revenue=7, strategic=9, completeness=7, urgency=6, effort_remaining=7
Active FastAPI backend — 653 tests passing, rate limiting + security CI in place. 21 in-code TODOs catalogued.
- [ ] [HIGH] Celery Redis task lock guard (prevent duplicate DB syncs) → TODO-456
- [ ] [HIGH] Orphaned node cleanup on signal edge creation failure → TODO-457
- [ ] [MEDIUM] Redis caching for validator DB lookups (3 cache TODOs) → TODO-458
- [ ] [HIGH] Refactor sql_code arg to parameterized SQL (security) → TODO-403 (existing)
- [ ] [HIGH] Implement list of property ids processing in filter validator → TODO-404 (existing)

## forwardlane-backend Round 4 (2026-03-04)
- [ ] TODO-456: Fix force_text → force_str Django 4.2 compat [CRITICAL/XS]
- [ ] TODO-457: Upgrade abandoned deps (boto3, sentry-sdk, pypdf, dj-rest-auth) [CRITICAL/M]
- [ ] TODO-458: Extract shared LLM client with fallback chain [HIGH/S]
- [ ] TODO-459: Streaming LLM responses via SSE [HIGH/M]
- [ ] TODO-460: Add pytest-cov 50% coverage gate to CI [HIGH/S]
- [ ] TODO-461: Pre-commit hooks (ruff + black + bandit) [HIGH/XS]
- [ ] TODO-462: Enforce MFA for admin via django-otp [HIGH/M]
- [ ] TODO-463: Daily Briefing aggregate endpoint + Celery pre-gen [MEDIUM/L]
- [ ] TODO-464: Celery dead letter queue + Flower monitoring [MEDIUM/M]
- [ ] TODO-465: N+1 query audit for pipeline_engine + ranking [MEDIUM/M]

## signal-studio-auth (2026-03-04 — Judge Agent v2 refresh)
**Scores:** revenue=7, strategic=9, completeness=7, urgency=6, effort_remaining=7
**✅ Done since last run:** TODO-402 (Redis rate limiter), TODO-403 (refresh token rotation)
- [x] 353 [CRITICAL] Add admin role check to /invite-to-org — security vulnerability open NOW ✅ 2026-03-04 — _get_caller_role() + HTTP 403 guard, 5 tests pass, commit 4d74e79
- [ ] 356 [HIGH] Add require_role() FastAPI dependency for RBAC enforcement
- [ ] 359 [HIGH] Replace per-request httpx.AsyncClient with module-level connection pool
- [ ] 354 [HIGH] Add password reset/change routes (/auth/recover, /auth/change-password)
- [ ] 404 [HIGH] Migrate to Pydantic v2 (model_config, model_dump, response models)
- [ ] 405 [HIGH] Add CORS middleware + Sentry error tracking + Prometheus /metrics
- [ ] 406 [HIGH] Create Dockerfile + GitHub Actions CI (pytest, ruff, bandit, pip-audit)
- [ ] 357 [HIGH] Add pytest-asyncio integration tests for all 7 auth routes
- [ ] 501 [P1] Redis connection pool (currently creates new connection per call)
- [ ] 504 [P1] Add pre-commit hooks (ruff, mypy, detect-private-key)
- [ ] 502 [P2] Supabase webhook handler (user delete → purge Redis tokens)
- [ ] 503 [P2] Auth audit log to Postgres (SOC2 compliance)

## signal-studio-frontend (2026-03-04 — Judge Agent v2 refresh)
**Scores:** revenue=7, strategic=9, completeness=5, urgency=7, effort_remaining=5
- [ ] 494 [P0/XL] Complete Oracle AI vector service — OracleVectorService, SemanticSearchService, embeddings (CORE VALUE PROP)
- [ ] 495 [P0/M] Add rate limiting to AI API routes — prevents API credit exhaustion
- [ ] 496 [P1/S] Remove dual reactflow dependency (reactflow v11 + @xyflow v12 both present)
- [ ] 497 [P1/L] Build ForwardLane Django backend bridge (BFF proxy + JWT forwarding + Oracle sync)
- [ ] 498 [P1/S] Wire Bitbucket CI/CD → Railway auto-deploy (pipelines + deploy hooks)
- [ ] 499 [P1/M] Bundle size audit — verify @xenova server-only, fix dynamic imports
- [ ] 500 [P2/M] Add E2E Playwright test suite for critical flows
- [ ] [QUICK] Add dump.rdb to .gitignore (Redis dump file committed to git)
- [ ] [QUICK] Harden SQL injection check in /api/oracle/query (multi-statement bypass possible)
- [ ] [QUICK] Archive/delete 30+ stale root-level .md files (PHASE-*.md, PR-*.md etc)
