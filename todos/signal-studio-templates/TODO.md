# TODO — signal-studio-templates
> Judge Swarm Tier 1 | Updated: 2026-03-13 | Score: 7.7/10
> Business Priority: 🟡 HIGH — Template system for Signal Studio + Invesco demo

## 📊 Score Card (2026-03-13)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7.0/10 | DRY violations (5 identical index files, 20 {{param}} templates); otherwise clean |
| Test Coverage | 5.0/10 | API/SQL safety tests pass; template engine and data providers untested |
| Security | 7.0/10 | SQL parameterized ✅, JWT auth ✅, rate limiting ✅; no Zod validation, no JWT aud check |
| Documentation | 7.0/10 | AUDIT.md, PLAN.md, README present; OpenAPI spec missing |
| Architecture | 7.0/10 | Express + TypeScript; ESM/CJS dual build fixed; Mock + OpenAI providers added |
| Business Value | 8.0/10 | Invesco demo + production template system for all Signal Studio clients |
| **Composite** | **7.7/10** | Up from 6.8 — ESM fix, rate limiting, auth, mock + OpenAI providers shipped |

---

## ⚠️ CRITICAL FLAGS

### 🔴 P0 BLOCKER — PostgreSQL DataProvider Not Implemented
- Templates library ships without a real database provider
- Mock provider is the only option — **blocks production deployment and live Invesco demo**
- **Status:** TODO #700 — URGENT

### 🟡 P1 — Template Engine Core Path Untested
- Zero unit tests on the engine execution path
- SQL injection hardening relies on untested code
- **Status:** TODO #701

### 🟡 SECURITY — No Zod Validation on POST Bodies
- Execute endpoint accepts arbitrary `parameters` object
- Type confusion and injection risk from malformed inputs
- **Status:** TODO #702

---

## P0 — Critical / Blocking

- [ ] **#700** PostgreSQL DataProvider implementation (BLOCKS PRODUCTION)
  - `PostgresDataProvider` class with `pg` driver
  - Connection pool (min 2, max 10)
  - Query timeout enforcement (30s default)
  - Credential management via env vars
  - **Effort:** Large (~2 days) — **START IMMEDIATELY**

- [ ] **#701** Template engine unit tests
  - Test `executeTemplate()` with each provider type
  - Test parameter substitution edge cases
  - Test SQL injection resistance on parameterized path
  - Mock DataProvider and AIProvider
  - Target: 80% engine coverage
  - **Effort:** Medium (~1 day)

## P1 — High Priority

- [ ] **#702** Zod validation + JWT audience + query timeouts
  - Zod schema for `/execute` request body
  - `parameters` validated against template's expected schema
  - JWT `aud` claim validation
  - 30s query execution timeout enforcement
  - **Effort:** Small (~4h)

- [ ] **#703** Redis caching layer
  - Cache template execution results (TTL: 5 min)
  - Cache key: `template_id + parameters hash + org_id`
  - Invalidation on template update
  - **Effort:** Medium (~1 day)

- [ ] **#427** Integration tests with testcontainers
  - Real PostgreSQL via testcontainers
  - Auth middleware rejects invalid tokens
  - Rate limiting enforced
  - **Effort:** Medium

- [ ] **#389** Zod validation on all parameter inputs
- [ ] **#390** Template diff/audit trail
- [ ] **#353** Execution telemetry (timing, row count, provider used)
- [ ] **#583** Rate limit by JWT sub (per-user execution limits)

## P2 — Medium Priority

- [ ] **#704** ESLint config + OpenAPI docs
  - ESLint + Prettier config
  - OpenAPI spec from Express routes
  - **Effort:** Small

- [ ] **#430** Expand template library
  - Compliance/risk templates
  - Portfolio attribution templates
  - Invesco-specific templates pack
  - **Effort:** Large

- [ ] **#582** Mock DataProvider for demo/seed data (already done — verify)
- [ ] **#321** Redis caching for template versioning

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

- [ ] Remove `corsOptions`/`globalLimiter` named exports from `api/templates.ts`
  - Internal middleware leaking to public package API

## Done (Recent)

- [x] SQL injection parameterized queries ✅
- [x] JWT auth REST router ✅
- [x] CI ESLint/Prettier/Husky ✅
- [x] GitHub Actions CI ✅
- [x] Fix ESM/CJS dual build ✅
- [x] API auth middleware ✅
- [x] Rate limiting + CORS ✅
- [x] npm publish pipeline ✅
- [x] OpenAI AI provider ✅
- [x] Mock data provider ✅
- [x] Strip SQL from API response ✅

---
*Scored by Judge Swarm v2 | 2026-03-13 16:00 UTC | Tier 1*
