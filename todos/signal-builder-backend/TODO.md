# TODO — signal-builder-backend
> Judge Swarm Tier 1 | Updated: 2026-03-13 | Score: 8.0/10
> Business Priority: 🔴 HIGH — Signal generation engine, core product feature

## 📊 Score Card (2026-03-13)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 8.0/10 | Clean FastAPI + DI architecture; HMAC signing, JWT revocation added |
| Test Coverage | 7.0/10 | 170 test files, multi-tenant isolation tests; schema translators under-covered |
| Security | 7.0/10 | JWT revocation ✅, HMAC ✅; CRITICAL: webhook secrets plaintext, CORS wildcard, SQL injection in EXPLAIN |
| Documentation | 7.0/10 | AUDIT.md, BRAINSTORM.md, PLAN.md present; OpenAPI missing |
| Architecture | 8.5/10 | FastAPI + Celery + DI container — solid, scalable design |
| Business Value | 8.5/10 | Signal generation powers the primary product |
| **Composite** | **8.0/10** | Up from 7.5 — strong hardening sprint |

---

## ⚠️ CRITICAL FLAGS

### 🔴 SECURITY — Webhook Secrets Stored in Plaintext
- **File:** `apps/webhooks/models/webhook.py:16`
- `secret: Mapped[str | None] = mapped_column(String(255))` — plaintext in database
- If DB is breached, all webhook consumer secrets exposed
- **Fix:** AES-256-GCM encryption via `cryptography` lib + env-sourced key
- Requires migration script for existing secrets
- **Status:** TODO #832 — HIGH URGENCY

### 🔴 SECURITY — SQL Injection in EXPLAIN Endpoint
- Raw SQL passed to EXPLAIN without proper parameterization
- **Status:** TODO #219, #202 — CRITICAL

### 🔴 SECURITY — CORS Wildcard (`*`)
- **File:** CORS middleware config
- All origins accepted — must lock to known frontend domains
- **Status:** TODO #200 — CRITICAL

### 🟡 SECURITY — Hardcoded JWT Secrets
- JWT signing secrets committed in codebase (not env-only)
- **Status:** TODO #201 — HIGH

### 🟡 HIGH — Optional Storage Params Mask DI Failures
- `signal_version_storage=None` and `signal_run_storage=None` fail silently
- Runtime `AttributeError` instead of loud startup failure
- **Status:** TODO #826

---

## P0 — Critical

- [ ] **#832** Encrypt webhook secrets (AES-256-GCM, migration script required)
- [ ] **#202/219** SQL injection in EXPLAIN endpoint — parameterize immediately
- [ ] **#200** CORS wildcard — lock to allowed frontend origins
- [ ] **#201** Remove hardcoded JWT secrets (env-only)
- [ ] **#822** Celery task idempotency (duplicate task execution risk)
- [ ] **#325/355** Fix silent exception swallowing on signal delete
- [ ] **#354** CI security pipeline (pip-audit, bandit, mypy gates)

## P1 — High Priority

- [ ] **#826** Fix optional storage params → required (startup failure instead of silent None)
- [ ] **#827** Signal scheduling via Celery Beat
- [ ] **#831** Alembic check in CI (detect unapplied migrations)
- [ ] **#833** JWT key rotation implementation
- [ ] **#834** Production Dockerfile — audit for dev dependencies leaking into prod image
- [ ] **#823** Pagination on signal list endpoints (unbounded queries → OOM risk)
- [ ] **#824** Webhook delivery reliability (retry + dead-letter queue)
- [ ] **#825** Translator unit tests (schema builder coverage)
- [ ] **#204** Signal versioning (track changes over time)
- [ ] **#205** Dry-run execution mode (validate signal before running)
- [ ] **#206** Audit log for signal operations (SOC2)
- [ ] **#219** IDOR: signal access authorization check
- [ ] **#327/353** Rate limiting middleware
- [ ] **#328/352** Pydantic v2 + FastAPI upgrade
- [ ] **#329/392** Test coverage for schema builder + schema translators
- [ ] **#391** Mypy type error reduction (currently many errors, blocking strict mode)
- [ ] **#456** Celery task lock (prevent concurrent execution of same signal)
- [ ] **#457** Orphaned node cleanup (dangling nodes after edge failures)
- [ ] **#458** Validator caching optimization (hot path)

## P2 — Medium Priority

- [ ] **#330** Redis caching for signal trees (expensive graph computation)
- [ ] **#331** Signal webhooks (outbound event notifications)
- [ ] **#393** Remove Flask admin (still in codebase, dead dependency)
- [ ] **#394** Fix N+1 batch create queries
- [ ] **#203/830** Pin Pipfile dependencies (no wildcard versions)
- [ ] **#829** OpenTelemetry tracing
- [ ] **#835** selectinload for signal list (N+1 fix)

## Done (Recent Sprint)

- [x] jsonpickle removed (SBB-002) ✅
- [x] JWT refresh revocation with Redis JTI blacklist (TODO-582) ✅
- [x] PyJWT + argon2-cffi — python-jose CVE fixed (TODO-583) ✅
- [x] HMAC-SHA256 webhook signing (TODO-581) ✅
- [x] organization_id non-nullable (TODO-580) ✅
- [x] Validator instance caching (TODO-396) ✅
- [x] Celery deduplication lock (TODO-397) ✅
- [x] Multi-tenant isolation tests (SBB-003) ✅
- [x] Signal run history (TODO-584) ✅

---
*Scored by Judge Swarm v2 | 2026-03-13 16:00 UTC | Tier 1*
