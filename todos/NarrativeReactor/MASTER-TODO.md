# MASTER TODO - NarrativeReactor
> Last judged: 2026-03-15 | Composite: 8.3/10 | Category: PRODUCT

## 📊 Judge Swarm Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Code Quality** | 8/10 | Well-structured 80+ TS files, 35 services. ESLint+Husky in place. 22 console.log/error still in services (no structured logger). Minor DRY violations in error handling. lodash full import. |
| **Test Coverage** | 7/10 | 29 test files, ~287 tests, ~83% statement coverage. No true HTTP E2E tests (supertest missing). E2E test file uses vi.mock — not real integration. No Stripe webhook sig tests. |
| **Security** | 8.5/10 | scrypt API key hashing ✅, helmet ✅, rate limiting ✅, AES-256-GCM token encryption ✅, CORS ✅, JWT with exp ✅, api_key_hash indexed ✅. Missing: request audit log, no pino (leaks internal paths via console.error in prod). |
| **Documentation** | 8/10 | Good README, OpenAPI/Swagger at /docs, MkDocs setup. Missing: runbook for incident response, API key rotation docs. |
| **Architecture** | 8.5/10 | Clean Express→Genkit→Services→SQLite architecture. WAL singleton DB, multi-tenant with quota enforcement, Docker multi-stage build, Railway deployment, GitHub Actions CI with typecheck+lint+test+docker-build. Synchronous video gen is a bottleneck. |
| **Business Value** | 8.5/10 | Full Stripe billing (checkout/portal/webhooks/quota), multi-tenant, content repurposing potential, 32+ services covering content gen, video, TTS, publishing, campaigns. Revenue-ready. |

**Composite: 8.3/10** (weighted: security×1.5, business×1.3, architecture×1.2)

## 📈 Progress Since Last Audit (2026-03-10 → 2026-03-15)

| Issue | Status | Notes |
|-------|--------|-------|
| SHA-256 → scrypt API key hashing | ✅ FIXED | scryptSync with migration path (SHA-256 fallback + rehash) |
| helmet middleware | ✅ FIXED | Active in index.ts with CSP disabled |
| tenants.ts bypasses DB singleton | ✅ FIXED | Now uses `getDb()` from db.ts; better-sqlite3 removed |
| Wildcard genkit deps | ✅ FIXED | All pinned to `^` semver ranges |
| No ESLint in root | ✅ FIXED | .eslintrc.json + lint script in package.json |
| No pre-commit hooks | ✅ FIXED | husky + lint-staged configured |
| Missing SQLite indexes | ✅ FIXED | Indexes on api_key_hash, brand_id, status, scheduled_at, tenant_id |
| @types/better-sqlite3 in prod deps | ✅ FIXED | Removed entirely |
| better-sqlite3 dependency | ✅ FIXED | Removed from package.json |
| trendpilotBridge unreachable | ✅ FIXED | Wired to routes/index.ts |

## 🚨 Critical Flags
- **No structured logger** — 22 console.log/error instances in production services. Risk: leaks internal paths, no log levels, no JSON for log aggregation.
- **No true HTTP E2E tests** — `e2e/integration.test.ts` mocks everything via vi.mock. No supertest in dependencies. Auth/billing flows untested at HTTP layer.
- **Test runner broken** — `npm run test:ci` fails with "Class extends value undefined is not a constructor or null" (likely vitest/dependency mismatch). CI may be green on different Node/lock state but local is broken.

## P0 - Critical (Do Immediately)
- [ ] **Fix test runner** — vitest fails locally with constructor error. Debug dependency resolution (vitest ^4.1.0 may conflict with coverage plugin). Blocking all test improvements.
- [ ] **Replace console.log/error with pino** — 22 instances across services. Create `src/lib/logger.ts`, structured JSON output for Railway log drain.

## P1 - High Priority (This Sprint)
- [ ] Implement true HTTP E2E tests using `supertest` — test auth flow, billing endpoints, content CRUD at HTTP layer
- [ ] Add Stripe webhook signature verification tests (valid/invalid/replayed payloads)
- [ ] Add rate limiting enforcement test (fire 101 requests → verify 429)
- [ ] Add quota enforcement test (tenant at limit → verify 429 with quota details)
- [ ] Replace full `lodash` import with `lodash/merge` in `contentPipeline.ts` (~70KB savings)
- [ ] Add request audit logging middleware (tenant_id, endpoint, timestamp, response_code)

## P2 - Medium Priority (Next Sprint)
- [ ] Implement LRU cache for AI content generation flows (hash of prompt+brandId, 5min TTL) — est. 30-50% API cost savings
- [ ] Build async video job queue (`videoQueue.ts`) — current sync video gen blocks HTTP thread for 30-120s
- [ ] Add pagination middleware for list endpoints (`/api/content`, `/api/campaigns`, `/api/schedules`)
- [ ] Content repurposing pipeline (blog → Twitter thread → LinkedIn → newsletter) — revenue upsell feature

## P3 - Future / Nice-to-Have
- [ ] API key rotation UI with 24h grace period
- [ ] Slack notifications for content approval/rejection events
- [ ] Renovate bot for automated dependency updates
- [ ] Content A/B testing framework
- [ ] Express 5 upgrade path evaluation

## Completed ✅
- [x] Multi-tenant Stripe billing (checkout/portal/webhooks/quota)
- [x] SQLite WAL singleton (`db.ts`) — tenants.ts migrated
- [x] scrypt API key hashing with SHA-256 migration path
- [x] JWT sessions with `exp` claim (24h default)
- [x] React dashboard auth (login/logout/session)
- [x] GitHub Actions CI (typecheck + lint + test + docker-build)
- [x] Docker multi-stage + Railway deployment
- [x] OpenAPI/Swagger docs at `/docs`
- [x] Sentry error monitoring
- [x] Rate limiting (express-rate-limit, 100 req/15min/IP)
- [x] AES-256-GCM token encryption
- [x] helmet security headers (CSP, HSTS, X-Frame-Options)
- [x] ESLint root config + husky pre-commit hooks
- [x] SQLite indexes on all hot columns
- [x] Pinned genkit dependencies (removed wildcards)
- [x] better-sqlite3 fully removed
- [x] trendpilotBridge wired to routes
- [x] 287+ tests across 29 files
