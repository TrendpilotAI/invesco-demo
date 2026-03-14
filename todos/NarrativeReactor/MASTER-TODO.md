# MASTER TODO - NarrativeReactor
> Last judged: 2026-03-14 | Composite: 7.8/10 | Category: PRODUCT

## 🚨 Critical Flags
- **SHA-256 API key hashing** — `tenants.ts:131` uses `crypto.createHash('sha256')`, vulnerable to GPU brute-force if DB leaked. Needs scrypt migration.
- **Dual SQLite connections** — `tenants.ts` imports `better-sqlite3` directly, bypassing the WAL singleton in `db.ts`. Lock contention risk on every auth call.
- **Wildcard genkit deps** — 6 packages at `*` version in package.json. Any `npm install` could pull breaking changes.

## P0 - Critical (Do Immediately)
- [ ] Replace SHA-256 API key hashing with `crypto.scrypt()` + salt; implement rehash-on-login migration (`tenants.ts`)
- [ ] Migrate `tenants.ts` to use `getDb()` from `db.ts` singleton; remove `better-sqlite3` dependency
- [ ] Add `helmet` middleware to Express app (already imported in index.ts but verify CSP config)
- [ ] Pin wildcard genkit dependencies to current installed versions (`npm ls genkit` → pin)
- [ ] Add SQLite index on `tenants(api_key_hash)` — queried on EVERY API request

## P1 - High Priority (This Sprint)
- [ ] Implement true HTTP E2E tests using `supertest` (current e2e/ tests use `vi.mock` — not real integration)
- [ ] Add SQLite indexes on `content_drafts(brand_id)`, `schedules(scheduled_at, status)`, `campaigns(brand_id, phase)`
- [ ] Replace `console.log` (18+ instances in services) with `pino` structured logger
- [ ] Add ESLint configuration in project root (currently only in `/dashboard`)
- [ ] Move `@types/better-sqlite3` from `dependencies` to `devDependencies`
- [ ] Replace full `lodash` import with modular `lodash/merge` in `contentPipeline.ts`

## P2 - Medium Priority (Next Sprint)
- [ ] Implement LRU cache for AI content generation flows (hash of prompt+brandId, 5min TTL) — est. 30-50% API cost savings
- [ ] Build async video job queue (`videoQueue.ts`) — current sync video gen blocks HTTP thread for 30-120s
- [ ] Add pagination middleware for list endpoints (`/api/content`, `/api/campaigns`, `/api/schedules`)
- [ ] Add request audit logging middleware (tenant_id, endpoint, timestamp, response_code)
- [ ] Wire `trendpilotBridge.ts` to a route or remove it (currently unreachable dead code)
- [ ] Add Stripe webhook signature verification tests (valid/invalid/replayed payloads)
- [ ] Add rate limiting enforcement tests (fire 101 requests, verify 429)

## P3 - Future / Nice-to-Have
- [ ] Content repurposing pipeline (blog → Twitter thread → LinkedIn → newsletter) — revenue upsell
- [ ] API key rotation UI with 24h grace period for old key
- [ ] Slack notifications for content approval/rejection events
- [ ] Set up Renovate bot for automated dependency updates
- [ ] Pre-commit hooks via husky + lint-staged
- [ ] Content A/B testing framework

## Completed ✅
- [x] Multi-tenant Stripe billing (checkout/portal/webhooks/quota)
- [x] SQLite WAL singleton (`db.ts`)
- [x] JWT sessions with `exp` claim (24h default)
- [x] React dashboard auth (login/logout/session)
- [x] GitHub Actions CI (typecheck + test + docker-build)
- [x] Docker + Railway deployment
- [x] OpenAPI/Swagger docs at `/docs`
- [x] Sentry error monitoring
- [x] Rate limiting (express-rate-limit, 100 req/15min/IP)
- [x] AES-256-GCM token encryption
- [x] 287 tests passing across 26 files
- [x] Helmet middleware imported (verify active)
