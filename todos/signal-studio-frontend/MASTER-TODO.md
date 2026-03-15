# MASTER-TODO: signal-studio-frontend
**Scored:** 2026-03-15 | **Composite:** 5.8/10 | **Tier:** 2 (Growth)

## Score Breakdown
| Dimension       | Score | Delta   | Notes |
|----------------|-------|---------|-------|
| code_quality   | 6.0   | ↓0.5    | `any` usage rampant in oracle-service (8+ instances); 20+ stale planning docs still in root; DRY violations in Oracle connection + AI client init; stale shell/debug scripts pollute root |
| test_coverage  | 5.0   | ↑0.5    | 32 test files exist; GH Actions CI runs typecheck + lint + Jest + build; but `--passWithNoTests` hides failures; 10% global threshold meaningless; no auth/security tests; no `pnpm audit` step |
| security       | 3.0   | ↓1.0    | **🔴 CRITICAL: middleware.ts still passes ALL `/api/` as public** — 45 API routes bypass auth; no `requireAuth` or `withAuth` helper exists; no rate limiting; no CSRF; no CORS config. Bitbucket repo has all these fixes but they haven't been ported. |
| documentation  | 7.0   | →       | README solid; BRAINSTORM/PLAN/AUDIT thorough; 20+ stale planning docs clutter root |
| architecture   | 7.0   | →       | Clean Next.js 15 app router; ReactFlow v12 done; service layer separated; TanStack Query + Supabase Realtime wired; Visual Node Graph Builder added |
| business_value | 8.0   | →       | Strong fintech signal platform; Oracle 23ai + multi-model AI; Vercel deploy pipeline exists; high revenue potential |
| **COMPOSITE**  | **5.8** | ↓0.4   | Security regression from deeper audit — middleware gap confirmed worse; critical fixes exist in Bitbucket repo but NOT ported to this GitHub repo |

## 🚨 CRITICAL FLAGS
1. **🔴 CRITICAL: ALL 45 API routes have NO authentication** — `middleware.ts` line `pathname.startsWith('/api/')` explicitly marks ALL API routes as public. No `requireAuth`/`withAuth` helper exists in this repo. Oracle query, AI chat, vectorization, signal generation endpoints all wide open.
2. **🔴 CRITICAL: Fixes exist in Bitbucket repo but NOT ported** — `repos/signal-studio` (Bitbucket) has: `lib/with-auth.ts`, `lib/rbac.ts`, `lib/rate-limit.ts`, `lib/api-audit-logger.ts`, `lib/audit.ts`, secured middleware, CSRF protection, health endpoint. NONE of these exist in `projects/signal-studio-frontend` (GitHub).
3. **🟠 HIGH: No rate limiting on AI/DB routes** — unauthenticated users can burn OpenAI/Anthropic/Google credits via `/api/chat/*` and hit Oracle DB via `/api/oracle/query`.
4. **🟠 HIGH: CI has `--passWithNoTests`** — Jest runs with `--passWithNoTests` which silently succeeds if no tests match. No `pnpm audit` step. No coverage enforcement.
5. **🟠 HIGH: No production deployment verified** — Vercel deploy workflow exists but no health check endpoint to confirm it's working.

---

## P0 — Fix Now (Blockers)

### Security (CRITICAL — blocks any client demo or production use)
- [ ] **PORT SECURITY FROM BITBUCKET:** Copy `lib/with-auth.ts`, `lib/rbac.ts`, `lib/rate-limit.ts`, `lib/api-audit-logger.ts`, `lib/audit.ts`, `lib/logger.ts` from `repos/signal-studio` → adapt to this repo's structure
- [ ] **FIX MIDDLEWARE:** Replace current middleware.ts with secured version from Bitbucket repo — removes blanket `/api/` public whitelist, adds per-route auth, CSRF, rate limiting
- [ ] **APPLY AUTH TO ALL 45 API ROUTES:** Either via middleware enforcement (preferred) or per-route `withAuth` wrapper
- [ ] **ADD HEALTH ENDPOINT:** Create `app/api/health/route.ts` — required for Vercel/GCP healthchecks and uptime monitoring

### CI Pipeline (blocks regression prevention)
- [ ] **REMOVE `--passWithNoTests`** from Jest CI step — replace with explicit test path
- [ ] **ADD `pnpm audit`** step to GH Actions — fail on HIGH severity CVEs
- [ ] **RAISE COVERAGE THRESHOLDS** from 10% global to at least 50%
- [ ] **ADD AUTH TESTS:** Create `__tests__/lib/with-auth.test.ts` and `__tests__/middleware.test.ts`

## P1 — This Sprint
- [ ] Add Zod schema validation to all POST/PUT API routes (only 4/45 currently have it)
- [ ] Configure CORS headers in `next.config.mjs` restricting origins
- [ ] Archive 20+ stale root markdown docs → `docs/archive/` (AI-CHAT-FINAL.md, IMPLEMENTATION-*.md, MVP-*.md, PHASE3-*.md, etc.)
- [ ] Move debug/setup scripts from root → `scripts/debug/` (test-*.js, check-*.js, show-*.js, setup-ords.js)
- [ ] Remove stale shell scripts from root (customize-workspace.sh, practical-repo-setup.sh, setup-forwardlane-workspace.sh, workspace-commands.sh)
- [ ] Centralize AI client initialization into `lib/ai/clients.ts` (DRY fix — currently scattered across API routes)
- [ ] Consolidate Oracle connection logic — ensure all services use single `getOracleConnection()` factory
- [ ] Replace `any` types in `lib/oracle-service.ts` (8+ instances at lines 55, 110, 146, 211, 335, 341, 345, 347)

## P2 — Next Sprint
- [ ] Add API route auth regression tests — verify 401 on unauthenticated requests
- [ ] Add Playwright E2E for auth flow + signal CRUD
- [ ] Port RBAC role-based access controls from Bitbucket repo (`lib/rbac.ts` with admin/editor/viewer roles)
- [ ] Port API audit logging from Bitbucket repo (`lib/api-audit-logger.ts`)
- [ ] Add Sentry error tracking post-deploy
- [ ] Add PostHog product analytics post-deploy
- [ ] Add component tests for Signal Library, AI Chat panel, Visual Builder
- [ ] Remove redundant `@anthropic-ai/sdk` if `@ai-sdk/anthropic` covers all cases

## P3 — Backlog
- [ ] Signal Sharing & Collaboration (enterprise sales unlock)
- [ ] Signal Backtesting Engine (quant team value prop)
- [ ] Dashboard/PDF Report Export
- [ ] Signal Alerts & Webhooks (Slack/email)
- [ ] LRU cache for Oracle queries (5-min TTL)
- [ ] Redis caching layer for semantic search
- [ ] React.memo optimization on Signal Library list items
- [ ] Multi-tenant / White-label architecture
- [ ] Mobile-responsive Signal Library
- [ ] LLM Model Selector UI (OpenRouter support exists but no UI)

## Repo Sync Issue ⚠️
The Bitbucket repo (`repos/signal-studio` — forwardlane/signal-studio) is **significantly ahead** of this GitHub repo (`projects/signal-studio-frontend` — TrendpilotAI/signal-studio-platform):

| Feature | GitHub (this repo) | Bitbucket |
|---------|-------------------|-----------|
| Middleware auth | ❌ All /api/ public | ✅ Per-route auth + CSRF |
| `withAuth` helper | ❌ Missing | ✅ `lib/with-auth.ts` |
| RBAC | ❌ Missing | ✅ `lib/rbac.ts` (admin/editor/viewer) |
| Rate limiting | ❌ Missing | ✅ `lib/rate-limit.ts` (LRU sliding window) |
| API audit logging | ❌ Missing | ✅ `lib/api-audit-logger.ts` + `lib/audit.ts` |
| Structured logger | ❌ Missing | ✅ `lib/logger.ts` (pino) |
| Health endpoint | ❌ Missing | ✅ `app/api/health/route.ts` (multi-service checks) |
| Error boundaries | ❌ Missing | ✅ Added in latest commit |
| Test count | 32 files | 34 files (incl. auth, rbac, audit tests) |

**Recommendation:** Cherry-pick or merge the security/infra commits from Bitbucket into this repo ASAP. The b058308 commit alone adds RBAC, audit logging, error boundaries, health endpoint, and bundle optimization.

## Corrections from Prior Scoring
- **Security score lowered 3→3.0** — prior score of 4.0 was overly generous; the middleware bypass is unchanged and deeper audit found 45 routes (not 32) unprotected in this repo
- **Code quality lowered 6.5→6.0** — stale docs and debug scripts still in root; `any` usage unchanged; DRY violations persist
- **Test coverage raised 4.5→5.0** — 32 test files is solid; CI pipeline does run tests now; but `--passWithNoTests` and low thresholds drag it down
- **Composite dropped 6.2→5.8** — security gap is the primary drag; the fixes exist but haven't been synced
