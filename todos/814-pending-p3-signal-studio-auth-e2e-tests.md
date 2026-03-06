# 814 — Add E2E Integration Tests Against Supabase Sandbox

**Repo:** signal-studio-auth  
**Priority:** P3  
**Effort:** M (1 day)  
**Dependencies:** 803 (Docker)

## Acceptance Criteria

- [ ] `tests/e2e/` directory with integration tests
- [ ] Tests gated by `SUPABASE_TEST_URL` env var (skipped if not set)
- [ ] Tests cover: signup → login → /me → refresh → logout full flow
- [ ] Tests verify opaque token behavior (can't reuse consumed refresh token)
- [ ] Runs in CI via a separate `e2e` job (not blocking main CI)

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-auth/tests/e2e/test_full_flow.py:

import os
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.skipif(
    not os.environ.get("SUPABASE_TEST_URL"),
    reason="E2E tests require SUPABASE_TEST_URL"
)

@pytest.mark.asyncio
async def test_full_auth_flow():
    """Test complete signup → login → /me → refresh → logout flow."""
    base_url = "http://localhost:8000"
    
    async with AsyncClient(base_url=base_url) as client:
        # Signup
        signup_resp = await client.post("/auth/signup", json={
            "email": f"test_{uuid.uuid4()}@example.com",
            "password": "TestPass123!"
        })
        assert signup_resp.status_code == 200
        
        # Login
        login_resp = await client.post("/auth/login", json={
            "email": signup_resp.json()["user"]["email"],
            "password": "TestPass123!"
        })
        assert login_resp.status_code == 200
        tokens = login_resp.json()
        
        # Refresh
        refresh_resp = await client.post("/auth/refresh", json={
            "refresh_token": tokens["refresh_token"]
        })
        assert refresh_resp.status_code == 200
        
        # Old refresh token should be invalid now
        replay_resp = await client.post("/auth/refresh", json={
            "refresh_token": tokens["refresh_token"]
        })
        assert replay_resp.status_code == 401

Add to .github/workflows/e2e.yml as a separate workflow.
```
