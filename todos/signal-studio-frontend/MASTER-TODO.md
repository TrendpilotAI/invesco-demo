# MASTER-TODO: signal-studio-frontend
**Scored:** 2026-03-15T16:21Z | **Composite:** 5.8/10 | **Tier:** 2 (Growth) | **Priority:** 7.7

## Score Breakdown
| Dimension       | Score | Delta   | Notes |
|----------------|-------|---------|-------|
| code_quality   | 6.0   | →       | `any` usage persists in oracle-service (10 instances); 20+ stale planning docs in root; DRY violations in Oracle connection + AI client init; debug scripts still in root |
| test_coverage  | 5.0   | →       | 28 test files; GH Actions CI runs typecheck + lint + Jest + build; `--passWithNoTests` hides real failures; 10% global threshold meaningless; no auth/security tests; no `pnpm audit` step |
| security       | 3.0   | →       | **🔴 CRITICAL: middleware.ts line 14 `pathname.startsWith('/api/')` marks ALL 45 API routes as public** — zero auth on any API endpoint. No `withAuth`, no RBAC, no rate-limit, no CSRF, no CORS. Bitbucket repo has all fixes but they haven't been ported. |
| documentation  | 7.0   | →       | README solid; BRAINSTORM/PLAN/AUDIT thorough; root cluttered with 20+ stale planning docs |
| architecture   | 7.0   | →       | Clean Next.js 15 app router; @xyflow/react v12; TanStack Query + Supabase Realtime wired; Visual Node Graph Builder; service layer separated |
| business_value | 8.0   | →       | Strong fintech signal platform; Oracle 23ai + multi-model AI; Vercel deploy pipeline exists; high revenue potential for ForwardLane |
| **COMPOSITE**  | **5.8** | →     | Security is the primary anchor — all fixes exist in Bitbucket but are NOT in this repo. No changes since last scoring. |

## 🚨 CRITICAL FLAGS
1. **🔴 CRITICAL: ALL 45 API routes have NO authentication** — `middleware.ts` line 14 `pathname.startsWith('/api/')` explicitly marks ALL API routes as public. No `requireAuth`/`withAuth` helper exists. Oracle query, AI chat, vectorization, signal generation endpoints all wide open.
2. **🔴 CRITICAL: Fixes exist in Bitbucket repo but NOT ported** — `repos/signal-studio` (Bitbucket) has: `lib/with-auth.ts`, `lib/rbac.ts`, `lib/rate-limit.ts`, `lib/api-audit-logger.ts`, `lib/audit.ts`, secured middleware, CSRF protection, health endpoint. NONE of these exist in `projects/signal-studio-frontend` (GitHub).
3. **🟠 HIGH: No rate limiting on AI/DB routes** — unauthenticated users can burn OpenAI/Anthropic/Google credits via `/api/chat/*` and hit Oracle DB via `/api/oracle/query`.
4. **🟠 HIGH: CI has `--passWithNoTests`** — Jest runs with `--passWithNoTests` which silently succeeds if no tests match. No `pnpm audit` step. Global coverage threshold is 10% (meaningless).
5. **🟠 HIGH: Build broken** — `npx next build` fails with `Class extends value undefined is not a constructor or null`. Needs investigation.
6. **🟡 MEDIUM: 38K LOC codebase** — substantial app with 45 API routes, ~28 test files, but security gap negates production readiness.

---

## P0 — Fix Now (Blockers)

### Security (CRITICAL — blocks any client demo or production use)
- [ ] **PORT SECURITY FROM BITBUCKET:** Copy `lib/with-auth.ts`, `lib/rbac.ts`, `lib/rate-limit.ts`, `lib/api-audit-logger.ts`, `lib/audit.ts`, `lib/logger.ts` from `repos/signal-studio` → adapt to this repo's structure
- [ ] **FIX MIDDLEWARE:** Replace current middleware.ts — remove blanket `/api/` public whitelist, add per-route auth, CSRF, rate limiting
- [ ] **APPLY AUTH TO ALL 45 API ROUTES:** Either via middleware enforcement (preferred) or per-route `withAuth` wrapper
- [ ] **ADD HEALTH ENDPOINT:** Create `app/api/health/route.ts` — required for Vercel/GCP healthchecks and uptime monitoring

### Build (blocks deploy)
- [ ] **FIX BUILD ERROR:** `Class extends value undefined is not a constructor or null` — investigate dependency/import issue preventing `next build`

### CI Pipeline (blocks regression prevention)
- [ ] **REMOVE `--passWithNoTests`** from Jest CI step — replace with explicit test paths
- [ ] **ADD `pnpm audit`** step to GH Actions — fail on HIGH severity CVEs
- [ ] **RAISE COVERAGE THRESHOLDS** from 10% global to at least 40%
- [ ] **ADD AUTH TESTS:** Create `__tests__/lib/with-auth.test.ts` and `__tests__/middleware.test.ts`

## P1 — This Sprint
- [ ] Add Zod schema validation to all POST/PUT API routes (only ~4/45 currently have it)
- [ ] Configure CORS headers in `next.config.mjs` restricting origins
- [ ] Archive 20+ stale root markdown docs → `docs/archive/` (AI-CHAT-FINAL.md, IMPLEMENTATION-*.md, MVP-*.md, PHASE3-*.md, etc.)
- [ ] Move debug/setup scripts from root → `scripts/debug/` (test-*.js, check-*.js, show-*.js, setup-ords.js)
- [ ] Remove stale shell scripts from root (customize-workspace.sh, practical-repo-setup.sh, setup-forwardlane-workspace.sh, workspace-commands.sh)
- [ ] Centralize AI client initialization into `lib/ai/clients.ts` (DRY fix — currently scattered across API routes)
- [ ] Consolidate Oracle connection logic — ensure all services use single `getOracleConnection()` factory
- [ ] Replace `any` types in `lib/oracle-service.ts` (10 instances)

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
| Health endpoint | ❌ Missing | ✅ `app/api/health/route.ts` |
| Error boundaries | ❌ Missing | ✅ Added |

**Recommendation:** Cherry-pick or merge the security/infra commits from Bitbucket into this repo ASAP.

## Change Log
- **2026-03-15T16:21Z** — Re-scored. No changes since last scoring. Added P0 item for broken build (`next build` fails). All scores hold steady. Security remains the critical blocker.
- **2026-03-15 (prior)** — Initial deep audit. Security score lowered to 3.0 after confirming 45 unprotected API routes.
