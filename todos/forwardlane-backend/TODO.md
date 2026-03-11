# TODO — forwardlane-backend
> Judge Swarm Tier 1 | Updated: 2026-03-11 | Score: 7.4/10
> Business Priority: 🔴 HIGH — Core Django backend, all clients depend on it

## ⚠️ CRITICAL FLAGS

### 🔴 SECURITY — API Audit Logging Missing
- No audit trail of who accessed what data when
- Required for SOC2 and Invesco financial compliance
- **File:** New middleware needed
- **Status:** TODO #868

### 🔴 QUALITY — Test Coverage at 50% (Target: 75%)
- 50% test coverage leaves half the codebase unverified
- No CI gate enforcing coverage threshold
- **Status:** TODO #871

### 🟡 SECURITY — Demo API Key Auth Not Enforced
- Demo endpoints accessible without proper API key validation
- **Status:** TODO #422

---

## P0 — Critical / Immediate

- [ ] **#581** Fix analytical psycopg2 connection pooling (prod blocking issue)
- [ ] **#582** Analytical endpoint integration tests (blocking prod confidence)
- [ ] **#336** Fix analytical psycopg2 connection pool leak
- [ ] **#337** Railway prod env vars — ensure all secrets set correctly
- [ ] **#338** Analytical endpoint tests
- [ ] **#867** Migration CI check (`manage.py migrate --check` in CI)
- [ ] **#868** API audit logging middleware (SOC2/compliance)
- [ ] **#869** LLM cost dashboard/tracking endpoint
- [ ] **#870** LLM flow integration tests (Gemini→Kimi fallback chain)
- [ ] **#422** Demo API key authentication on demo endpoints

## P1 — High Priority

- [ ] **#871** Coverage gate to 75% — enforce in CI
- [ ] **#353** Fix easy_button models (stale data shapes)
- [ ] **#354** Dependency security upgrades (scheduled pip-audit run)
- [ ] **#355** Shared LLM client consolidation
- [ ] **#378** Django 4.2 compatibility check (verify no 3.x-isms)
- [ ] **#379** Railway prod env vars complete audit
- [ ] **#380** NL-SQL multi-turn conversation support
- [ ] **#381** Upgrade stale/pinned dependencies
- [ ] **#456** Force-text Django 4.2 migration (deprecation cleanup)
- [ ] **#457** Dep security upgrades (pip-audit results)
- [ ] **#458** Shared LLM module extract
- [ ] **#462** MFA enforcement for enterprise clients
- [ ] **#583** Extract LLM module (critical for maintainability)
- [ ] **#584** CI test gate on development branch
- [ ] **#585** urllib → requests migration (deprecated stdlib usage)
- [ ] **#586** Extract LLM module from monolith views
- [ ] **#587** Easy button rate throttling
- [ ] **#588** LLM fallback integration tests

## P1 — New (2026-03-11)

- [ ] **#872** Celery queue routing (separate high/low priority queues)
- [ ] **#873** DB index audit (analytical queries missing indexes)
- [ ] **#874** Webhook event system (outbound events for integrations)
- [ ] **#875** Tenant API keys (per-client API key management)

## P2 — Medium Priority

- [ ] **#361** OpenAPI schema generation (drf-yasg → drf-spectacular)
- [ ] **#363** Expand NL-SQL template library (more financial query types)
- [ ] **#463** Daily briefing endpoint (scheduled digest generation)
- [ ] **#464** Celery dead-letter queue (failed task recovery)
- [ ] **#465** N+1 query audit (Django ORM select_related audit)
- [ ] **#590** Pin wildcard deps (remove unpinned `>=` constraints)
- [ ] **#311** Django 4.2 migration verification (full compat pass)
- [ ] **#312** Easy button integration tests
- [ ] **#313** Railway prod environment activation
- [ ] **#314** Sentry integration (error tracking)
- [ ] **#339** NL-SQL Redis cache (expensive query caching)
- [ ] **#340** Demo token auth (lightweight token for demo environments)

## Done (Recent — Round 5)

- [x] `six` dependency fully removed ✅
- [x] pysaml2 >= 6.5.0 pinned (XML signature CVE) ✅
- [x] 10 circular dependencies broken ✅
- [x] Major deps upgraded (django-filter, storages, environ, celery-beat) ✅
- [x] Sentry SDK integrated ✅
- [x] pip-audit in CI ✅
- [x] Pre-commit hooks configured ✅
- [x] SSE streaming for LLM responses ✅
- [x] SAML2 auth upgrade ✅
- [x] psycopg2 raw connection fix ✅
