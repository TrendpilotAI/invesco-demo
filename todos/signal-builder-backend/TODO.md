# TODO — signal-builder-backend
> Judge Swarm Tier 1 | Updated: 2026-03-14 | Score: 8.1/10
> Business Priority: 🔴 HIGH — Signal generation engine, core product feature

## 📊 Score Card (2026-03-14)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 8.0/10 | Clean FastAPI + DI architecture; HMAC signing, JWT revocation added; optional storage params still an issue |
| Test Coverage | 7.0/10 | 107 test files across 590 source files; multi-tenant isolation tests present; schema translators under-covered |
| Security | 7.5/10 | JWT revocation ✅, HMAC ✅, sqlglot SQL validation ✅; CRITICAL: webhook secrets plaintext; CORS is properly configured (not wildcard) |
| Documentation | 7.0/10 | AUDIT.md, BRAINSTORM.md, PLAN.md comprehensive; OpenAPI docs auto-generated but not customized |
| Architecture | 8.5/10 | FastAPI + Celery + DI container + clean layering (routers→cases→storages→models) — solid, scalable |
| Business Value | 8.5/10 | Signal generation powers ForwardLane's primary product; Invesco integrations active |
| **Composite** | **8.1/10** | Up from 8.0 — security hardening sprint completed, CORS/SQL injection risks reassessed as mitigated |

### Score Changes vs Prior Assessment
- Security: 6.5 → 7.5 (CORS wildcard was FALSE POSITIVE — defaults to `https://app.forwardlane.com`; SQL injection in EXPLAIN mitigated by sqlglot `validate_select_only()` gate)
- Composite: 7.7 → 8.1 (corrected security scoring)

---

## ⚠️ CRITICAL FLAGS

### 🔴 SECURITY — Webhook Secrets Stored in Plaintext
- **File:** `apps/webhooks/models/webhook.py:16`
- `secret: Mapped[str | None] = mapped_column(String(255))` — plaintext in database
- If DB is breached, all webhook consumer secrets exposed
- **Fix:** AES-256-GCM encryption via `cryptography` lib + env-sourced key
- Requires migration script for existing secrets
- **Status:** TODO #832 — HIGH URGENCY

### 🟡 HIGH — Optional Storage Params Mask DI Failures
- **File:** `apps/signals/cases/signal.py:48-49`
- `signal_version_storage: SignalVersionStorage = None` and `signal_run_storage: SignalRunStorage = None`
- Silent `AttributeError` at runtime instead of loud startup failure
- **Status:** TODO #826

### 🟢 RESOLVED — CORS Configuration (Previously flagged as CRITICAL)
- **Finding:** CORS defaults to `https://app.forwardlane.com` via env var with safe fallback
- **File:** `settings/common.py:99-105`
- `*` only appears in test fixtures (`conftest.py`), NOT production
- **Status:** RESOLVED — no action needed

### 🟢 MITIGATED — SQL Injection in EXPLAIN
- **Finding:** `validate_select_only()` in `core/shared/sql_validator.py` uses sqlglot AST parsing + regex
- Enforces SELECT-only, blocks DML/DDL/dangerous functions, rejects multi-statement
- System prepends `EXPLAIN` to validated SQL — user cannot control the EXPLAIN keyword
- `EXPLAIN` is in FORBIDDEN_PATTERNS regex so users can't inject it themselves
- **Status:** MITIGATED — risk is low, monitor for edge cases

---

## P0 — Critical

- [ ] **#832** Encrypt webhook secrets (AES-256-GCM, migration script required)
- [ ] **#826** Fix optional storage params → required (startup failure instead of silent None)
- [ ] **#822** Celery task idempotency (duplicate task execution risk)
- [ ] **#325/355** Fix silent exception swallowing on signal delete
- [ ] **#354** CI security pipeline (pip-audit, bandit, mypy gates)

## P1 — High Priority

- [ ] **#833** JWT key rotation implementation (versioned keys, zero-downtime rotation)
- [ ] **#827** Signal scheduling via Celery Beat (cron fields + dynamic schedule)
- [ ] **#831** Alembic check in CI (detect unapplied migrations)
- [ ] **#834** Production Dockerfile — audit for dev dependencies leaking into prod image (ipython CVEs)
- [ ] **#823** Pagination on signal list endpoints (unbounded queries → OOM risk)
- [ ] **#824** Webhook delivery reliability (retry + dead-letter queue)
- [ ] **#825** Translator unit tests (schema builder coverage)
- [ ] **#204** Signal versioning rollback API
- [ ] **#205** Dry-run execution mode (validate signal before running)
- [ ] **#206** Audit log for signal operations (SOC2)
- [ ] **#219** IDOR: signal access authorization check
- [ ] **#327/353** Rate limiting middleware (exists but needs more scenarios)
- [ ] **#328/352** Pydantic v2 + FastAPI upgrade
- [ ] **#329/392** Test coverage for schema builder + schema translators
- [ ] **#391** Mypy type error reduction (blocking strict mode)
- [ ] **#456** Celery task lock (prevent concurrent execution of same signal)
- [ ] **#457** Orphaned node cleanup (dangling nodes after edge failures)
- [ ] **#458** Validator caching optimization verification (DI scope: Factory not Singleton?)

## P2 — Medium Priority

- [ ] **#835** selectinload for signal list (N+1 fix — quick win)
- [ ] **#330** Redis caching for signal trees (expensive graph computation)
- [ ] **#331** Signal webhooks (outbound event notifications)
- [ ] **#393** Remove Flask admin (still in codebase, dead dependency)
- [ ] **#394** Fix N+1 batch create queries
- [ ] **#203/830** Pin Pipfile dependencies (no wildcard versions)
- [ ] **#829** OpenTelemetry tracing
- [ ] **#828** Signal run status API (GET endpoints for run history)
- [ ] **#836** Export to CSV/Excel endpoints
- [ ] **#837** Redis cache for SQL translation (same nodes → same SQL, memoize)

## P3 — Low Priority / Housekeeping

- [ ] Remove `.ipython/` from repo + add to `.gitignore`
- [ ] Fix duplicate HMAC computation in `webhook_signer.py`
- [ ] Run `pre-commit autoupdate`
- [ ] Add `pytest-cov` with 75% minimum coverage enforcement
- [ ] Centralize magic string constants per app module
- [ ] Add docstrings to all public `case` methods
- [ ] Consolidate duplicate `conftest.py` fixtures
- [ ] Upgrade outdated deps: pandas 2.1→2.2, alembic 1.9→1.13, asyncpg 0.27→0.29

## Done (Recent Sprint)

- [x] jsonpickle removed (SBB-002) ✅
- [x] JWT refresh revocation with Redis JTI blacklist (TODO-582) ✅
- [x] PyJWT + argon2-cffi — python-jose CVE fixed (TODO-583) ✅
- [x] HMAC-SHA256 webhook signing (TODO-581) ✅
- [x] organization_id non-nullable (TODO-580) ✅
- [x] Validator instance caching (TODO-396) ✅
- [x] Celery deduplication lock (TODO-397) ✅
- [x] Multi-tenant isolation tests (SBB-003) ✅
- [x] Signal run history table + storage (TODO-584) ✅
- [x] sqlglot SQL validation gate (validate_select_only) ✅

---
*Scored by Judge Subagent | 2026-03-14 16:01 UTC | Tier 1*
