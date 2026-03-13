# TODO — forwardlane-backend
> Judge Swarm Tier 1 | Updated: 2026-03-13 | Score: 7.7/10
> Business Priority: 🔴 HIGH — Core Django backend, all clients depend on it

## 📊 Score Card (2026-03-13)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7.5/10 | Good Django structure; circular deps fixed, SSE streaming added |
| Test Coverage | 5.5/10 | ~50% coverage — no CI gate, analytical endpoints poorly tested |
| Security | 7.0/10 | pysaml2 CVE fixed, pip-audit in CI, pre-commit; conn leak + no audit log |
| Documentation | 7.0/10 | No OpenAPI spec, but internal docs adequate |
| Architecture | 8.0/10 | Solid Django + Celery; SSE streaming added; LLM module needs extraction |
| Business Value | 8.5/10 | Revenue-critical — all ForwardLane clients depend on this |
| **Composite** | **7.7/10** | Up from 7.4 — good recent hardening sprint |

---

## ⚠️ CRITICAL FLAGS

### 🔴 PRODUCTION — Analytical psycopg2 Connection Pool Leak
- Blocking production confidence on analytical endpoints
- **File:** `forwardlane/adapters/analytical.py` (psycopg2 raw conn management)
- **Risk:** Connection exhaustion under load → 500 errors for all analytical queries
- **Status:** TODO #581, #336, #582

### 🔴 COMPLIANCE — API Audit Logging Missing
- No audit trail of who accessed what data when
- Required for SOC2 and Invesco financial data compliance
- **Fix:** Middleware to log user + endpoint + timestamp + response code
- **Status:** TODO #868

### 🟡 QUALITY — Test Coverage at 50% (Target: 75%)
- No CI gate enforcing coverage threshold
- Analytical endpoints and LLM flows under-tested
- **Status:** TODO #871

### 🟡 SECURITY — Demo Endpoints Without Proper Auth
- Demo API key not enforced on demo-flagged endpoints
- **Status:** TODO #422

---

## P0 — Critical / Immediate

- [ ] **#581** Fix analytical psycopg2 connection pooling (PRODUCTION BLOCKER)
- [ ] **#582** Analytical endpoint integration tests (blocking prod confidence)
- [ ] **#336** Fix analytical psycopg2 connection pool leak
- [ ] **#337** Railway prod env vars — full secrets audit
- [ ] **#867** Migration CI check (`manage.py migrate --check` in CI pipeline)
- [ ] **#868** API audit logging middleware (SOC2/Invesco compliance)
- [ ] **#869** LLM cost dashboard/tracking endpoint
- [ ] **#870** LLM flow integration tests (Gemini→Kimi fallback chain)
- [ ] **#422** Demo API key authentication enforcement

## P1 — High Priority

- [ ] **#871** Coverage gate to 75% — enforce in CI
- [ ] **#353** Fix easy_button models (stale data shapes causing runtime errors)
- [ ] **#354** Dependency security upgrades (pip-audit results action items)
- [ ] **#355** Shared LLM client consolidation (3 separate implementations → 1)
- [ ] **#378** Django 4.2 full compatibility pass
- [ ] **#380** NL-SQL multi-turn conversation support
- [ ] **#381** Upgrade stale/pinned dependencies (review pip-audit report)
- [ ] **#456** Force-text Django 4.2 migration (deprecation cleanup)
- [ ] **#462** MFA enforcement for enterprise clients
- [ ] **#583** Extract LLM module from monolith views (maintainability)
- [ ] **#584** CI test gate on development branch (block merges without tests)
- [ ] **#585** urllib → requests/httpx migration (deprecated stdlib, done FL-007 — verify complete)
- [ ] **#587** Easy button rate throttling
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
- [ ] **#590** Pin wildcard deps (remove unpinned `>=` constraints)
- [ ] **#314** Sentry integration (error tracking)
- [ ] **#339** NL-SQL Redis cache (expensive query caching)

## Done (Recent)

- [x] `six` dependency fully removed ✅
- [x] pysaml2 >= 6.5.0 pinned (XML signature CVE) ✅
- [x] 10 circular dependencies broken ✅
- [x] Major deps upgraded (django-filter, storages, environ, celery-beat) ✅
- [x] Sentry SDK integrated ✅
- [x] pip-audit in CI ✅
- [x] Pre-commit hooks configured ✅
- [x] SSE streaming for LLM responses (FL-007) ✅
- [x] SAML2 auth upgrade (FL-004) ✅
- [x] psycopg2 raw connection fix (partial) ✅
- [x] httpx migration for LLM client timeout/pooling ✅

---
*Scored by Judge Swarm v2 | 2026-03-13 16:00 UTC | Tier 1*
