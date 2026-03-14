# TODO — forwardlane-backend
> Judge Swarm Tier 1 | Updated: 2026-03-14 | Score: 7.2/10
> Business Priority: 🔴 HIGH — Core Django backend, all clients depend on it

## 📊 Score Card (2026-03-14)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7.0/10 | Good Django structure; circular deps fixed, SSE streaming, but ~75 TODOs and wildcard deps |
| Test Coverage | 5.0/10 | 30.5% actual line coverage (22.7K/74K lines); 50% target unmet; analytical/LLM flows untested |
| Security | 6.5/10 | pysaml2 CVE fixed, pip-audit in CI; missing audit logging, rate limiting gaps, demo auth weakness |
| Documentation | 4.5/10 | Generic README, no OpenAPI spec (drf-yasg PR merged but incomplete), no deployment guide |
| Architecture | 7.5/10 | Solid Django + Celery + multi-tenant; LLM fallback chains; analytical psycopg2 leak unresolved |
| Business Value | 9.0/10 | Revenue-critical — all ForwardLane + Invesco clients depend on this |
| **Composite** | **7.2/10** | Slight dip from 7.7 — coverage measurement refined (30.5% actual vs claimed 50%) |

---

## ⚠️ CRITICAL FLAGS

### 🔴 PRODUCTION — Analytical psycopg2 Connection Pool Leak
- Raw `psycopg2.connect()` per request in `analytical/views.py` — never pooled, never closed
- Under load: connection exhaustion → 500 errors for all analytical queries
- `easy_button/views.py` correctly uses `connections['analytical']` — analytical must match
- **Status:** TODO #581, #336, #582 — NOT RESOLVED

### 🔴 COMPLIANCE — API Audit Logging Missing
- No audit trail of who accessed what data when
- Required for SOC2 and Invesco financial data compliance
- **Fix:** Middleware to log user + endpoint + timestamp + response code
- **Status:** TODO #868 — NOT STARTED

### 🔴 SECURITY — Demo Auth Still Weak
- `EasyButtonPermission` with `DEMO_ENV=demo` = fully public (no token check)
- `NLQueryView` executes LLM-generated SQL — publicly accessible in demo mode
- **Fix:** Add `EASY_BUTTON_DEMO_TOKEN` env var check
- **Status:** TODO #422 — NOT RESOLVED

### 🟡 QUALITY — Test Coverage at 30.5% (Target: 75%)
- `coverage.xml` shows 22,670 / 74,208 lines covered = 30.5%
- `easy_button/` and `analytical/` remain poorly tested
- LLM fallback chain (Gemini→Kimi) has zero integration tests
- **Status:** TODO #871

---

## P0 — Critical / Immediate

- [ ] **#581** Fix analytical psycopg2 connection pooling (PRODUCTION BLOCKER)
- [ ] **#336** Fix analytical psycopg2 connection pool leak (duplicate of #581)
- [ ] **#582** Analytical endpoint integration tests (blocking prod confidence)
- [ ] **#868** API audit logging middleware (SOC2/Invesco compliance)
- [ ] **#422** Demo API key authentication enforcement
- [ ] **#867** Migration CI check (`manage.py migrate --check` in CI pipeline)
- [ ] **#869** LLM cost dashboard/tracking endpoint
- [ ] **#870** LLM flow integration tests (Gemini→Kimi fallback chain)
- [ ] **#337** Railway prod env vars — full secrets audit

## P1 — High Priority

- [ ] **#871** Coverage gate to 75% — enforce in CI (currently 30.5%)
- [ ] **#353** Fix easy_button models (stale data shapes causing runtime errors)
- [ ] **#354** Dependency security upgrades (pip-audit results action items)
- [ ] **#355** Shared LLM client consolidation (3 separate implementations → 1)
- [ ] **#378** Django 4.2 full compatibility pass (force_text→force_str, etc.)
- [ ] **#456** Force-text Django 4.2 migration (deprecation cleanup)
- [ ] **#380** NL-SQL multi-turn conversation support
- [ ] **#381** Upgrade stale/pinned dependencies (boto3 1.23→1.35+, pypdf2→pypdf)
- [ ] **#462** MFA enforcement for enterprise clients
- [ ] **#583** Extract LLM module from monolith views (maintainability)
- [ ] **#584** CI test gate on development branch (block merges without tests)
- [ ] **#587** Easy button rate throttling (all endpoints, not just NL→SQL)
- [ ] **#588** LLM fallback integration tests
- [ ] **#872** Celery queue routing (separate high/low priority queues)
- [ ] **#873** DB index audit (analytical queries missing indexes)
- [ ] **#874** Webhook event system (outbound events for integrations)
- [ ] **#875** Tenant API keys (per-client API key management)

## P2 — Medium Priority

- [ ] **#361** OpenAPI schema generation (drf-yasg → drf-spectacular)
- [ ] **#363** Expand NL-SQL template library (more financial query types)
- [ ] **#463** Daily briefing endpoint (scheduled digest generation)
- [ ] **#464** Celery dead-letter queue (failed task recovery)
- [ ] **#465** N+1 query audit (Django ORM select_related review)
- [ ] **#590** Pin wildcard deps (numpy, pandas, scipy — remove unpinned `>=` constraints)
- [ ] **#314** Sentry integration improvements
- [ ] **#339** NL-SQL Redis cache (expensive query caching)

## Done (Recent)

- [x] OpenAPI schema docs via drf-yasg (FL-009) ✅
- [x] DashboardView/ClientsView/SignalsView/ActionsView tests (FL-008) ✅
- [x] httpx migration for LLM client (FL-007) ✅
- [x] pysaml2 >= 6.5.0 pinned — XML signature CVE (FL-004) ✅
- [x] easy_button, analytical, adapters added to pylint scope (FL-006) ✅
- [x] pip-audit security scan in all CI pipelines (FL-005) ✅
- [x] 10 circular dependencies broken (RI-001..RI-010) ✅
- [x] TODO triage report — 75 markers categorized (RI-027) ✅
- [x] Dead code radar — 123 findings (RI report) ✅
- [x] `six` dependency fully removed ✅
- [x] Major deps upgraded (django-filter, storages, environ, celery-beat) ✅
- [x] Sentry SDK integrated ✅
- [x] Pre-commit hooks configured ✅
- [x] SSE streaming for LLM responses (FL-007) ✅
- [x] SAML2 auth upgrade (FL-004) ✅

---
*Scored by Judge Swarm v2 | 2026-03-14 16:01 UTC | Tier 1*
