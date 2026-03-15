# TODO — signal-studio-templates
> Judge Agent | Updated: 2026-03-15 | Score: 7.4/10
> Business Priority: 🟡 HIGH — Template system for Signal Studio + Invesco

## 📊 Score Card (2026-03-15)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7.0/10 | DRY violations (5 identical index files, 20 {{param}} templates); otherwise clean TypeScript |
| Test Coverage | 5.0/10 | 4 test suites, 35 tests passing; engine core + React component untested (~35-40%) |
| Security | 7.5/10 | SQL parameterized ✅, JWT auth ✅, rate limiting ✅, CORS ✅; missing Zod validation on POST bodies |
| Documentation | 7.5/10 | README, BRAINSTORM, PLAN, AUDIT all thorough; OpenAPI spec missing |
| Architecture | 7.0/10 | Clean provider pattern; ESM/CJS dual build; DataProvider/AIProvider interfaces |
| Business Value | 8.5/10 | Core intelligence layer for Signal Studio + Invesco; 20 templates across 5 categories |
| **Composite** | **7.4/10** | No changes since 3/14 — P0 PostgreSQL blocker still unaddressed |

---

## ⚠️ CRITICAL FLAGS

### 🔴 P0 BLOCKER — PostgreSQL DataProvider Not Implemented
- Only MockDataProvider exists — **blocks production deployment and live Invesco demo**
- No `pg` or `postgres.js` dependency installed
- **Impact:** Cannot demo with real data. Revenue blocked.
- **Status:** TODO #700 — URGENT, UNSTARTED

### 🔴 P0 — Template Engine Core Path Untested
- Zero unit tests on `TemplateEngine.execute()`, `validate()`, `customize()`, `getTemplates()`
- Core orchestration untested despite SQL safety utils being well-tested
- **Status:** TODO #701

### 🟡 P1 SECURITY — No Zod Validation on POST Bodies
- `POST /templates/:id/execute` destructures `req.body` without schema validation
- `POST /templates/:id/customize` accepts arbitrary body including `sqlTemplate` override
- Prototype pollution + SQL injection via customize→execute path
- **Status:** TODO #702

### 🟡 P1 — No Query Execution Timeout
- `dataProvider.executeSQL()` has no timeout — slow query blocks worker indefinitely
- **Status:** Included in TODO #702

---

## P0 — Critical / Production Blockers

- [ ] **#700** PostgreSQL DataProvider implementation ⚡ BLOCKS PRODUCTION
  - Implement `PostgresDataProvider` with `DataProvider` interface
  - Use `pg` or `postgres.js` with connection pooling
  - Query timeout enforcement (30s default via `statement_timeout`)
  - `POSTGRES_CONNECTION_STRING` env var for credentials
  - `availableDataSources()` maps to configured table/view registry
  - **Effort:** Large (~2 days) — **START IMMEDIATELY**

- [ ] **#701** Template engine unit tests
  - Test `TemplateEngine.execute()` end-to-end with MockDataProvider
  - Test `getTemplates()` with all filter combos (category, tags, complexity, search)
  - Test `validateParameters()` edge cases
  - Test `customize()` returns properly forked template
  - Test error cases (missing template, validation failures, missing data sources)
  - Target: 70%+ engine coverage
  - **Effort:** Medium (~1 day)

## P1 — High Priority

- [ ] **#702** Zod validation + query timeouts + JWT audience hardening
  - Add `zod` dependency
  - Zod schemas for `/execute` and `/customize` request bodies
  - Whitelist allowed override fields in customize (block `sqlTemplate`)
  - 30s query execution timeout via `Promise.race()` in engine
  - Return 408 on timeout, 400 on validation failure
  - **Effort:** Small (~4h)

- [ ] **#703** Redis caching layer
  - `CacheProvider` interface with `get/set/invalidate`
  - `RedisCacheProvider` using `ioredis`
  - Cache key: `sha256(templateId + JSON.stringify(sortedParams))`
  - Default TTL: 5 min (configurable per template)
  - No-op fallback when Redis unavailable
  - **Effort:** Medium (~1 day)

- [ ] **#427** Integration tests with real PostgreSQL
  - Testcontainers or docker-compose with Postgres + seed data
  - Run all 20 template SQL queries against real DB
  - Validate output matches `outputSchema` definitions
  - Depends on #700
  - **Effort:** Medium

## P2 — Medium Priority

- [ ] **#704** ESLint config + OpenAPI docs
  - `.eslintrc.json` with `@typescript-eslint/recommended`
  - Pre-commit hooks via `husky` + `lint-staged`
  - OpenAPI spec for Express routes
  - **Effort:** Small

- [ ] **#705** Snowflake DataProvider
  - `SnowflakeDataProvider` using `snowflake-sdk`
  - Required for Invesco production (after Postgres pattern established)
  - **Effort:** Large (~2 days)

- [ ] **#430** Expand template library to 30+
  - ESG drift, client lifecycle, retention risk, whitespace analysis
  - **Effort:** Large

- [ ] React component (TemplateGallery) tests with `@testing-library/react`

## Code Debt

- [ ] Migrate 20 templates from `{{param}}` to `buildQuery` tagged literals (~3-4h)
- [ ] Create `sql-fragments.ts` for shared advisor/territory JOIN pattern (15+ templates)
- [ ] Convert 5 identical category index files to dynamic registry
- [ ] Remove leaked `corsOptions`/`globalLimiter`/`executeLimiter` exports
- [ ] Default `includeTalkingPoints` to `false` (saves ~1-2s latency + OpenAI cost per call)
- [ ] Remove empty `jest.setup.js` or add actual setup
- [ ] Add `coverageThreshold` to jest config (lines: 70%, branches: 60%)
- [ ] Replace `Record<string, any>` overuse with typed output schemas

## ✅ Done

- [x] SQL injection parameterized queries
- [x] JWT auth with audience + issuer validation
- [x] GitHub Actions CI (typecheck → lint → test → build → publish on tag)
- [x] ESM/CJS dual build
- [x] Rate limiting (100/15min global, 20/60s execute) + CORS
- [x] npm publish pipeline
- [x] OpenAI AI provider + Mock AI provider
- [x] Mock data provider (50 advisors, 500 accounts, 200 interactions, 1000 holdings)
- [x] Strip SQL from API response
- [x] 35 tests across 4 suites all passing

---
*Scored by Judge Agent | 2026-03-15 16:00 UTC*
