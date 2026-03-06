# TODO-601: Integration Tests for Redis Auth Paths

**Repo:** signal-studio-auth  
**Priority:** P0 (HIGH)  
**Effort:** 4h  
**Status:** ✅ DONE — commit f4f1974 (pushed to GitHub/TrendpilotAI/signal-studio-auth)

## Problem
`tests/test_rate_limit_and_tokens.py` exists but critical integration paths are untested:
- `/refresh` Redis round-trip (token consumed + new token issued)
- `/refresh` with consumed (already-rotated) token → should 401
- `/logout` Redis revocation verified (token blacklisted)
- `/invite-to-org` role escalation: analyst/viewer tries to invite → 403
- Rate limit enforcement: 6th request within window → 429

## Required Test Cases

```python
# tests/test_redis_integration.py

import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock

class TestRefreshTokenRotation:
    async def test_refresh_issues_new_token_and_revokes_old(self, client, redis_mock):
        """POST /auth/refresh with valid token returns new token, old token consumed."""
        ...

    async def test_refresh_with_consumed_token_returns_401(self, client, redis_mock):
        """POST /auth/refresh with already-used token returns 401."""
        ...

    async def test_refresh_with_unknown_token_returns_401(self, client):
        """POST /auth/refresh with fabricated token returns 401."""
        ...

class TestLogoutRevocation:
    async def test_logout_revokes_refresh_token_in_redis(self, client, redis_mock):
        """POST /auth/logout removes token from Redis; subsequent refresh fails."""
        ...

class TestInviteToOrgRBAC:
    async def test_analyst_cannot_invite(self, client, analyst_token):
        """POST /auth/invite-to-org with analyst role returns 403."""
        ...

    async def test_viewer_cannot_invite(self, client, viewer_token):
        """POST /auth/invite-to-org with viewer role returns 403."""
        ...

    async def test_admin_can_invite(self, client, admin_token, supabase_mock):
        """POST /auth/invite-to-org with admin role succeeds."""
        ...

class TestRateLimiting:
    async def test_login_rate_limit_enforced(self, client):
        """6th POST /auth/login within 60s window returns 429."""
        ...

    async def test_signup_rate_limit_enforced(self, client):
        """4th POST /auth/signup within 60s returns 429."""
        ...
```

## Implementation Notes
- Use `fakeredis` for Redis mocking: `pip install fakeredis[aioredis]`
- Use `pytest-asyncio` with `asyncio_mode = "auto"`
- Patch `config.redis_config.get_redis` to return fakeredis instance
- Add `requirements-dev.txt` if not exists: `pytest-asyncio`, `fakeredis`, `pytest-cov`

## Files to Create/Modify
- `tests/test_redis_integration.py` (new)
- `tests/conftest.py` (create or update with fixtures)
- `requirements-dev.txt` (add test deps)

## Acceptance Criteria
- [ ] All 10+ test cases pass
- [ ] Redis paths covered: rotate, revoke, consume
- [ ] RBAC paths covered: all 3 roles × invite endpoint
- [ ] Rate limit paths covered: login + signup
- [ ] CI runs tests in pipeline

## Dependencies
- TODO-600 (httpx pooling — test fixtures may need adjustment)
