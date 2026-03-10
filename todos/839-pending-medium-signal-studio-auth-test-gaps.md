# TODO-839: Fill Test Gaps — Dual-Mode Auth, Concurrent Refresh Race, Token Expiry

**Repo:** signal-studio-auth
**Priority:** P2 (Medium)
**Effort:** 3 hours
**Status:** pending
**Dependencies:** TODO-832 (refactored /refresh route), TODO-833 (password validator)
**Created:** 2026-03-10

## Problem

Three critical test gaps exist:

### 1. Dual-Mode Auth Switching
`AUTH_MODE` can be `supabase`, `forwardlane`, or `dual` (config/supabase_config.py line 56). The auth middleware (`middleware/supabase_auth_middleware.py`) presumably switches behavior based on this. **Zero tests verify mode switching works correctly.**

### 2. Concurrent Refresh Race Condition
Two simultaneous `/refresh` calls with the same token should:
- First call succeeds and marks token consumed
- Second call detects consumed token → theft → revoke family
But there's no test proving this works under concurrency. The current code marks consumed with `r.hset()` which is not atomic with the check.

### 3. Token Expiry Mid-Rotation
If a token's Redis TTL expires between the consumed check and the Supabase call:
- `r.hgetall()` returns data (token exists)
- Supabase refresh succeeds
- `_issue_family_token()` creates new token
- But old token may have expired between steps
This edge case needs a test to document expected behavior.

## Files to Create/Change

- `tests/test_dual_mode_auth.py` — NEW: test AUTH_MODE switching
- `tests/test_concurrent_refresh.py` — NEW: test race conditions
- `tests/test_redis_integration.py` — ADD: token expiry mid-rotation test

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-auth/tests/test_dual_mode_auth.py:

"""Tests for AUTH_MODE switching (supabase / forwardlane / dual)."""
import os
import pytest
from unittest.mock import patch

# Test that AUTH_MODE=supabase only validates Supabase JWTs
# Test that AUTH_MODE=forwardlane only validates ForwardLane JWTs
# Test that AUTH_MODE=dual accepts both JWT formats
# Test that invalid AUTH_MODE raises ValueError

@pytest.fixture
def supabase_mode():
    with patch.dict(os.environ, {"AUTH_MODE": "supabase"}):
        yield

@pytest.fixture
def forwardlane_mode():
    with patch.dict(os.environ, {"AUTH_MODE": "forwardlane"}):
        yield

# Add tests that exercise the middleware with each mode
# Verify JWT validation uses the correct secret per mode

Create /data/workspace/projects/signal-studio-auth/tests/test_concurrent_refresh.py:

"""Tests for concurrent refresh token race conditions."""
import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Test: Two simultaneous /refresh with same token
# First should succeed, second should get 401 (theft detected)
# Use asyncio.gather to simulate concurrency

# Test: Rapid sequential refreshes (not truly concurrent but fast)
# Verify only one succeeds

# Test: Token expires between check and rotation
# Mock Redis TTL to expire mid-operation
# Verify graceful handling (not a crash)

Run: cd /data/workspace/projects/signal-studio-auth && python -m pytest tests/test_dual_mode_auth.py tests/test_concurrent_refresh.py -v
```

## Acceptance Criteria

- [ ] Dual-mode auth tests cover all 3 modes (supabase, forwardlane, dual)
- [ ] Concurrent refresh test proves theft detection works under race conditions
- [ ] Token expiry mid-rotation test documents expected behavior
- [ ] At least 10 new test cases added across the new files
- [ ] All existing tests still pass
- [ ] Test coverage for auth_routes.py increases by ≥5%
