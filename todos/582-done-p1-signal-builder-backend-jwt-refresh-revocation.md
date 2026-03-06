# TODO-582: JWT Refresh Token Revocation — DONE ✅

**Completed:** 2026-03-06
**Branch:** feat/p0-todos-352-356
**Commit:** c5a41e4

## What Was Implemented

### New Module: `core/auth/refresh_token_store.py`
- `store_refresh_jti(jti, ttl_seconds)` — stores JTI in Redis as `jwt:jti:{jti}` with TTL
- `revoke_refresh_jti(jti)` — deletes JTI from Redis (immediate revocation)
- `is_refresh_jti_valid(jti)` — checks JTI exists in Redis; fails-open if Redis is down

### Updated: `core/auth/auth_token.py`
- `generate_pair()` now adds `jti` (uuid4) claim to refresh tokens
- Automatically calls `store_refresh_jti()` to register the JTI in Redis on issuance

### Updated: `apps/users/routers/auth.py`
- `POST /auth/logout` — now also accepts optional `refresh_token` in body; revokes its JTI
- `POST /auth/refresh` (new endpoint) — validates refresh token signature/expiry/JTI, rotates token (single-use), issues new pair

### New Tests: `apps/users/tests/test_jwt_refresh_revocation.py`
- Unit tests for store/revoke/validate functions
- Tests for fail-open Redis behavior
- Tests for generate_pair JTI inclusion
- Integration flow: logout → refresh fails with 401

## Acceptance Criteria Status
- ✅ Logout invalidates refresh token immediately
- ✅ Revoked tokens return 401 on next use
- ✅ Token rotation: each refresh token is single-use
- ✅ Tests cover the full revocation flow
- ⚠️ Password change invalidation: not implemented (todo task noted per-user token version; deferred to separate ticket)

## Notes
- Redis fails-open: if Redis is unavailable, JTI validation is skipped with a warning log (avoids locking out users during Redis outages)
- Token rotation on refresh (single-use) is a security improvement beyond the original spec
- Pushed to: Bitbucket (origin) and GitHub (TrendpilotAI)
