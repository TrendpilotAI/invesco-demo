# TODO — signal-builder-backend
> Judge Swarm Tier 1 | Updated: 2026-03-11 | Score: 7.5/10
> Business Priority: 🔴 HIGH — Signal generation engine, core product feature

## ⚠️ CRITICAL FLAGS

### 🔴 SECURITY — Webhook Secrets Stored in Plaintext
- **File:** `apps/webhooks/models/webhook.py:16`
- `secret: Mapped[str | None] = mapped_column(String(255))` — plaintext DB storage
- If DB is compromised, all webhook consumer secrets exposed
- **Fix:** AES-256-GCM encryption via `cryptography` lib + app-level key from env
- Requires migration script for existing secrets
- **Status:** TODO #832

### 🟡 HIGH — Optional Storage Params Hide Wiring Failures
- **File:** `apps/signals/cases/signal.py:SignalCases.__init__`
- `signal_version_storage=None` and `signal_run_storage=None` — silent None if DI fails
- Runtime `AttributeError` instead of startup failure
- **Fix:** Make required params; DI container fails loudly
- **Status:** TODO #826 (826-pending)

### 🟡 HIGH — JWT Key Rotation Not Implemented
- No secret rotation mechanism for JWT signing keys
- **Status:** TODO #833

### 🔴 CRITICAL — Silent Exception Swallowing on Delete
- **Status:** TODO #325/355

### 🔴 CRITICAL — SQL Injection in EXPLAIN endpoint
- **Status:** TODO #219/202

---

## P0 — Critical

- [ ] **#832** Encrypt webhook secrets (AES-256-GCM, not plaintext DB)
- [ ] **#821** Remove jsonpickle — DONE but verify no re-introduction
- [ ] **#822** Celery task idempotency (duplicate task execution risk)
- [ ] **#325/355** Fix silent exception swallowing on signal delete
- [ ] **#202/219** SQL injection in EXPLAIN endpoint — parameterize
- [ ] **#200** CORS wildcard (`*`) — lock down to allowed origins
- [ ] **#201** Remove hardcoded JWT secrets from codebase
- [ ] **#354** CI security pipeline (pip-audit, bandit, mypy gates)

## P1 — High Priority

- [ ] **#826** Fix optional storage params → make required (fail at startup)
- [ ] **#827** Signal scheduling via Celery Beat
- [ ] **#831** Alembic check in CI (detect unapplied migrations)
- [ ] **#833** JWT key rotation implementation
- [ ] **#834** Production Dockerfile — audit for dev dependencies
- [ ] **#823** Pagination on signal list endpoints (unbounded queries)
- [ ] **#824** Webhook delivery reliability (retry + DLQ)
- [ ] **#825** Translator unit tests (schema builder coverage)
- [ ] **#204** Signal versioning (track changes over time)
- [ ] **#205** Dry-run execution mode (validate before running)
- [ ] **#206** Audit log for signal operations
- [ ] **#219** IDOR: signal access authorization check
- [ ] **#327** Rate limiting middleware
- [ ] **#328** Pydantic v2 + FastAPI upgrade (v2 migration)
- [ ] **#329** Test coverage for schema builder (currently low)
- [ ] **#352** Pydantic v2 migration (TODO #352)
- [ ] **#353** Rate limiting implementation
- [ ] **#391** Mypy type error reduction (currently many errors)
- [ ] **#392** Test coverage for schema translators + analytical DB

## P1 — New (2026-03-11)

- [ ] **#456** Celery task lock (prevent concurrent execution of same signal)
- [ ] **#457** Orphaned node cleanup (dangling nodes after edge failures)
- [ ] **#458** Validator caching (hot path optimization)

## P2 — Medium Priority

- [ ] **#330** Redis caching for signal trees (expensive graph computation)
- [ ] **#331** Signal webhooks (outbound event notifications)
- [ ] **#393** Remove Flask dependencies (Flask admin still in codebase)
- [ ] **#394** Fix N+1 batch create queries
- [ ] **#395** Upgrade dev dep CVEs (lower priority, dev-only)
- [ ] **#203/830** Pin Pipfile dependencies (no wildcard versions)
- [ ] **#829** OpenTelemetry tracing (observability)
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
- [x] Auth deps upgrade (TODO-583) ✅
- [x] Celery task dedup (done-397) ✅
- [x] Webhook HMAC signing ✅
- [x] Org-id non-nullable ✅
