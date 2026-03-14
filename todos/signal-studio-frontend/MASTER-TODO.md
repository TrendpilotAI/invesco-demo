# MASTER-TODO: signal-studio-frontend
**Scored:** 2026-03-14 | **Composite:** 6.2/10 | **Tier:** 2 (Growth)

## Score Breakdown
| Dimension       | Score | Delta | Notes |
|----------------|-------|-------|-------|
| code_quality   | 6.5   | ↑0.5  | `strict: true` confirmed in tsconfig; `any` usage remains in oracle-service; DRY violations persist |
| test_coverage  | 4.5   | ↑0.5  | 32 test files exist; GH Actions runs tests; coverage thresholds too low (10% global); many API routes untested |
| security       | 4.0   | →     | **32/44 API routes still have ZERO auth** — critical blocker; no rate limiting; no CORS |
| documentation  | 7.0   | →     | README comprehensive; BRAINSTORM/PLAN/AUDIT thorough; 20+ stale planning docs clutter root |
| architecture   | 7.0   | ↑0.5  | Clean Next.js app router; ReactFlow v12 done; service layer well-separated; Oracle DRY issues remain |
| business_value | 8.0   | ↑0.5  | Strong fintech signal platform; Oracle 23ai + multi-model AI; high revenue potential once deployed |
| **COMPOSITE**  | **6.2** | ↓0.15 | Security drag keeps composite down despite improvements elsewhere |

## 🚨 CRITICAL FLAGS
1. **🔴 32/44 API routes have NO authentication** — middleware.ts explicitly passes ALL `/api/` as public. Oracle query, AI chat, vectorization endpoints all wide open. Cost DoS + data exposure risk.
2. **🔴 No rate limiting on AI chat routes** — unauthenticated users can burn OpenAI/Anthropic credits.
3. **🟠 CI runs tests but no coverage enforcement** — global threshold 10% is meaningless; no `pnpm audit` step.
4. **🟠 No production deployment** — platform complete but unreachable; zero revenue possible.

---

## P0 — Fix Now (Blockers)
- [ ] **AUTH CRITICAL:** Create `lib/auth/require-auth.ts` helper; apply to all 32 unprotected API routes in `app/api/` (est: 2-4h)
- [ ] **AUTH CRITICAL:** Remove `pathname.startsWith('/api/')` from middleware.ts public whitelist, OR enforce per-route auth
- [ ] **DEPLOY:** Set up production deployment (Vercel/GCP) with proper env secrets, domain, health endpoint
- [ ] **CI:** Add `pnpm audit` step to GitHub Actions (fail on HIGH severity)
- [ ] **CI:** Raise Jest coverage thresholds from 10% to at least 50% global

## P1 — This Sprint
- [ ] Add Zod schema validation to all POST/PUT API routes (security + reliability)
- [ ] Add rate limiting (`@upstash/ratelimit`) to AI chat routes — 10 req/min/user
- [ ] Configure CORS headers in `next.config.mjs` restricting origins
- [ ] Archive 20+ stale root markdown docs → `docs/archive/`
- [ ] Move debug/setup scripts from root → `scripts/debug/`
- [ ] Delete duplicate `src/middleware.ts` (Next.js ignores it; only root loaded)
- [ ] Centralize AI client init into `lib/ai/clients.ts` (DRY fix)
- [ ] Consolidate Oracle connection logic — single `getOracleConnection()` factory

## P2 — Next Sprint
- [ ] Add API route auth tests — verify 401 on unauthenticated requests (would catch the 32-route gap)
- [ ] Add component tests for Signal Library, AI Chat panel, Visual Builder
- [ ] Add Playwright E2E for auth flow + signal CRUD
- [ ] Sentry error tracking post-deploy
- [ ] PostHog product analytics post-deploy
- [ ] Remove redundant `@anthropic-ai/sdk` if `@ai-sdk/anthropic` covers all cases
- [ ] Add health check endpoint `app/api/health/route.ts`

## P3 — Backlog
- [ ] Signal Sharing & Collaboration (enterprise sales unlock)
- [ ] Signal Backtesting Engine (quant team value prop)
- [ ] Dashboard/PDF Report Export
- [ ] Signal Alerts & Webhooks (Slack/email)
- [ ] LRU cache for Oracle queries (5-min TTL)
- [ ] Redis caching layer for semantic search
- [ ] React.memo optimization on Signal Library list items
- [ ] Multi-tenant / White-label architecture

## Corrections from Prior Audit
- **tsconfig.json `strict: true`** — AUDIT.md incorrectly stated this was missing. It IS enabled. ✅
- **CI runs tests** — GitHub Actions workflow includes test job (Jest with `--passWithNoTests`). Bitbucket still lint+build only.
- **Some signal routes forward auth headers** — `app/api/signals/route.ts` forwards Authorization/Cookie headers to backend, but does NOT validate them server-side.
