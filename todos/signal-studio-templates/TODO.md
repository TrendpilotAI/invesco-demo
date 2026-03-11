# TODO — signal-studio-templates
> Judge Swarm Tier 1 | Updated: 2026-03-11 | Score: 6.8/10
> Business Priority: 🟡 HIGH — Template system for Signal Studio, Invesco integration

## ⚠️ CRITICAL FLAGS

### 🔴 P0 — PostgreSQL DataProvider Not Implemented
- Templates library ships without a real database provider
- Blocks production deployment and Invesco demo
- Mock provider is the only option currently
- **Status:** TODO #700

### 🟡 P1 — Template Engine Core Path Untested
- Zero unit tests on the engine itself
- SQL injection hardening relies on untested path
- **Status:** TODO #701

### 🟡 SECURITY — No Zod Validation on POST Bodies
- Execute endpoint accepts arbitrary `parameters` object
- No schema validation — type confusion, injection risk
- **Status:** TODO #702

---

## P0 — Critical / Blocking

- [ ] **#700** PostgreSQL DataProvider implementation (BLOCKS PRODUCTION)
  - Implement `PostgresDataProvider` class
  - Connection pool with `pg` driver
  - Query timeout enforcement (default 30s)
  - Credential management via env vars
  - **Effort:** Large (~2 days)

- [ ] **#701** Template engine unit tests
  - Test `executeTemplate()` with each template type
  - Test parameter substitution edge cases
  - Test SQL injection resistance
  - Mock DataProvider and AI provider
  - Target: 80% engine coverage
  - **Effort:** Medium (~1 day)

## P1 — High Priority

- [ ] **#702** Zod validation + JWT audience + query timeouts
  - Add Zod schema for `/execute` request body
  - Validate `parameters` against template's expected schema
  - Add JWT `aud` claim validation (reject tokens from wrong service)
  - Enforce 30s query execution timeout
  - **Effort:** Small (~4h)

- [ ] **#703** Redis caching layer
  - Cache template execution results (TTL: 5 min)
  - Cache key: `template_id + parameters hash + org_id`
  - Invalidation on template update
  - **Effort:** Medium (~1 day)

- [ ] **#427** Integration tests
  - Test full execute flow with real PostgreSQL (testcontainers)
  - Test auth middleware rejects invalid tokens
  - Test rate limiting enforced
  - **Effort:** Medium

- [ ] **#389** Zod validation on all parameter inputs
- [ ] **#390** Template diff/audit trail (track template changes)
- [ ] **#353** Execution telemetry (timing, row count, provider used)
- [ ] **#583** Rate limit by JWT sub (per-user execution limits)

## P2 — Medium Priority

- [ ] **#704** ESLint config + OpenAPI docs
  - Add ESLint + Prettier config
  - Generate OpenAPI spec from Express routes
  - Publish to docs site
  - **Effort:** Small

- [ ] **#430** Expand template library
  - Add compliance/risk templates
  - Add portfolio attribution templates
  - Invesco-specific templates pack
  - **Effort:** Large

- [ ] **#582** Mock DataProvider for demo/seed data
- [ ] **#321** Redis caching for template versioning
- [ ] **#320** npm publish pipeline for OpenAI + PostgreSQL providers

## P3 — Low Priority

- [ ] **#386** Invesco template pack (specialized for retention use case)
- [ ] **#387** CSV/Excel result export
- [ ] **#388** Webhook triggers on template execution

## Code Debt (No TODO# yet)

- [ ] Migrate all 20 templates from `{{param}}` to `buildQuery` tagged literals
  - `parameterizeLegacyTemplate` is marked transitional — must remove eventually
  - Start with `sales-intelligence` category (highest value)
  - **Effort:** 3-4h for full migration

- [ ] Create `sql-fragments.ts` for shared SQL patterns
  - advisor/territory JOIN pattern repeated in 15+ templates
  - Schema change to `advisors` table requires 15+ edits currently

- [ ] Convert 5 identical category index files to dynamic registry
  - `templates/registry.ts` with `registerTemplate()` pattern

- [ ] Remove `corsOptions`/`globalLimiter` named exports from `api/templates.ts`
  - Internal middleware leaking to public package API

## Done (Recent)

- [x] SQL injection parameterized queries ✅
- [x] JWT auth REST router ✅
- [x] CI ESLint/Prettier/Husky ✅
- [x] GitHub Actions CI ✅
- [x] Fix ESM build ✅
- [x] API auth middleware ✅
- [x] Rate limiting + CORS ✅
- [x] npm publish pipeline ✅
- [x] OpenAI AI provider ✅
- [x] Mock data provider ✅
- [x] Strip SQL from API response ✅
