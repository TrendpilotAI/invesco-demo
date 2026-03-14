# TODO — signal-studio-templates
> Judge Swarm Tier 1 | Updated: 2026-03-14 | Score: 7.5/10
> Business Priority: 🟡 HIGH — Template system for Signal Studio + Invesco demo

## 📊 Score Card (2026-03-14)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7.0/10 | DRY violations (5 identical index files, 20 {{param}} templates); otherwise clean TypeScript |
| Test Coverage | 5.0/10 | 4 test suites, 35 tests all passing; engine core path + React component untested (~35-40% coverage) |
| Security | 7.5/10 | SQL parameterized ✅, JWT auth w/ audience+issuer ✅, rate limiting ✅, CORS ✅; missing Zod validation on POST bodies |
| Documentation | 7.5/10 | AUDIT.md, PLAN.md, BRAINSTORM.md, README all present and thorough; OpenAPI spec missing |
| Architecture | 7.0/10 | Clean Express + TypeScript; ESM/CJS dual build; Mock + OpenAI providers; DataProvider/AIProvider interfaces well-designed |
| Business Value | 8.5/10 | Invesco demo + production template system for all Signal Studio clients; 20 templates across 5 categories |
| **Composite** | **7.5/10** | Stable from 7.7 — JWT audience now validated, but PostgresDataProvider still missing (the big blocker) |

---

## ⚠️ CRITICAL FLAGS

### 🔴 P0 BLOCKER — PostgreSQL DataProvider Not Implemented
- Templates library ships without a real database provider
- MockDataProvider is the only option — **blocks production deployment and live Invesco demo**
- No `pg` or `postgres.js` dependency yet
- **Impact:** Cannot demo with real data. Revenue blocked.
- **Status:** TODO #700 — URGENT

### 🟡 P1 — Template Engine Core Path Untested
- Zero unit tests on `TemplateEngine.execute()`, `validate()`, `customize()`, `getTemplates()` with filters
- SQL injection hardening relies on `parameterizeLegacyTemplate` which IS tested, but the engine calling it is NOT
- **Status:** TODO #701

### 🟡 SECURITY — No Zod Validation on POST Bodies
- `POST /templates/:id/execute` destructures `req.body` directly without schema validation
- `POST /templates/:id/customize` accepts arbitrary body as `Partial<SignalTemplate>` — could inject malicious sqlTemplate
- Type confusion and prototype pollution risk from malformed inputs
- **Status:** TODO #702

### 🟡 SECURITY — Customize Endpoint Accepts Arbitrary SQL
- `POST /templates/:id/customize` allows overriding `sqlTemplate` field with arbitrary SQL
- Combined with lack of Zod validation, this is a SQL injection vector via the customize→execute path
- **Mitigation needed:** Whitelist which fields can be customized, or validate sqlTemplate

---

## P0 — Critical / Blocking

- [ ] **#700** PostgreSQL DataProvider implementation (BLOCKS PRODUCTION)
  - `PostgresDataProvider` class implementing `DataProvider` interface
  - Use `pg` or `postgres.js` with connection pooling (min 2, max 10)
  - Query timeout enforcement (30s default via `statement_timeout`)
  - Credential management via `POSTGRES_CONNECTION_STRING` env var
  - `availableDataSources()` maps to configured table/view registry
  - **Effort:** Large (~2 days) — **START IMMEDIATELY**

- [ ] **#701** Template engine unit tests
  - Test `TemplateEngine.execute()` end-to-end with MockDataProvider
  - Test `getTemplates()` with all filter combos (category, tags, complexity, search)
  - Test `validateParameters()` edge cases (missing required, type mismatch, min/max)
  - Test `validateDataSources()` with missing sources
  - Test `customize()` returns properly forked template
  - Test error cases (missing template, validation failures)
  - Target: 70%+ engine coverage
  - **Effort:** Medium (~1 day)

## P1 — High Priority

- [ ] **#702** Zod validation + query timeouts
  - Add `zod` dependency
  - Zod schema for `/execute` request body (`parameters: z.record()`, `includeTalkingPoints: z.boolean().optional()`)
  - Zod schema for `/customize` — whitelist allowed override fields (block `sqlTemplate` override)
  - `parameters` validated against template's `ParameterDef[]` schema at API layer
  - 30s query execution timeout via `Promise.race()` in `TemplateEngine.execute()`
  - Return 408 on timeout, 400 on validation failure with structured errors
  - **Effort:** Small (~4h)

- [ ] **#703** Redis caching layer
  - `CacheProvider` interface with `get/set/invalidate`
  - `RedisCacheProvider` using `ioredis`
  - Cache key: `sha256(templateId + JSON.stringify(sortedParams) + orgId)`
  - Default TTL: 5 min (configurable per template)
  - Wire as optional in `TemplateEngine.execute()`
  - No-op fallback when Redis unavailable
  - **Effort:** Medium (~1 day)

- [ ] **#427** Integration tests with testcontainers
  - Real PostgreSQL via testcontainers or docker-compose
  - Run all 20 template SQL queries against real DB with seed data
  - Validate output shape matches `outputSchema` definitions
  - Auth middleware rejects invalid tokens
  - **Effort:** Medium — depends on #700

- [ ] **#389** Zod validation on all parameter inputs (covered by #702)
- [ ] **#353** Execution telemetry (timing, row count, provider used)
- [ ] **#583** Rate limit by JWT `sub` (per-user execution limits, not just per-IP)

## P2 — Medium Priority

- [ ] **#704** ESLint config + OpenAPI docs
  - `.eslintrc.json` with `@typescript-eslint/recommended`
  - Pre-commit hooks via `husky` + `lint-staged`
  - OpenAPI spec auto-generated from Express routes
  - **Effort:** Small

- [ ] **#705** Snowflake DataProvider
  - `SnowflakeDataProvider` using `snowflake-sdk`
  - Required for Invesco production deployment
  - **Effort:** Large (~2 days, after #700 pattern established)

- [ ] **#390** Template diff/audit trail
- [ ] **#430** Expand template library to 30+
  - ESG drift, client lifecycle, retention risk, whitespace analysis templates
  - **Effort:** Large

- [ ] React component (TemplateGallery) tests with @testing-library/react

## Code Debt (No TODO# Yet)

- [ ] Migrate all 20 templates from `{{param}}` to `buildQuery` tagged literals
  - `parameterizeLegacyTemplate` is marked transitional — must remove eventually
  - Start with `sales-intelligence` category (highest value, well-tested)
  - **Effort:** 3-4h for full migration

- [ ] Create `sql-fragments.ts` for shared SQL patterns
  - advisor/territory JOIN pattern repeated in 15+ templates
  - Schema change to `advisors` table currently requires 15+ edits

- [ ] Convert 5 identical category index files to dynamic registry
  - `templates/registry.ts` with `registerTemplate()` pattern

- [ ] Remove `corsOptions`/`globalLimiter`/`executeLimiter` named exports from `api/templates.ts`
  - Internal middleware leaking to public package API

- [ ] Change `includeTalkingPoints` default from `true` to `false`
  - Currently every execute call triggers an OpenAI API call unless explicitly disabled
  - Adds ~1-2s latency and cost per request

- [ ] Empty `jest.setup.js` — remove or fill with actual setup

- [ ] Add `coverageThreshold` to jest config (target: lines 70%, branches 60%)

## Done (Recent)

- [x] SQL injection parameterized queries ✅
- [x] JWT auth with audience + issuer validation ✅
- [x] CI ESLint/Prettier/Husky ✅
- [x] GitHub Actions CI (typecheck → lint → test → build → publish on tag) ✅
- [x] Fix ESM/CJS dual build ✅
- [x] API auth middleware ✅
- [x] Rate limiting (100/15min global, 20/60s execute) + CORS ✅
- [x] npm publish pipeline ✅
- [x] OpenAI AI provider ✅
- [x] Mock data provider (50 advisors, 500 accounts, 200 interactions, 1000 holdings) ✅
- [x] Strip SQL from API response ✅
- [x] 35 tests across 4 suites all passing ✅

---
*Scored by Judge Swarm v2 | 2026-03-14 16:01 UTC | Tier 1*
