# TODO 357 — Add Integration Tests for Auth Routes
**Repo:** signal-studio-auth
**Priority:** MEDIUM
**Effort:** 4 hours
**Status:** pending
**Depends on:** 351, 352, 353, 354, 356

## Description
Current tests cover middleware and JWT verification but NOT the actual route handlers.
Need TestClient integration tests for all auth routes with mocked Supabase API.

## Coding Prompt
Create `/data/workspace/projects/signal-studio-auth/tests/test_routes.py`:

```python
"""Integration tests for auth routes with mocked Supabase API."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routes.auth_routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

MOCK_SUPABASE_LOGIN_RESPONSE = {
    "access_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 3600,
    "refresh_token": "r_token",
    "user": {"id": "uuid", "email": "test@example.com"}
}


class TestSignup:
    def test_signup_success(self):
        with patch("routes.auth_routes.httpx.AsyncClient") as mock_client:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"id": "uuid", "email": "test@example.com"}
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_resp)
            
            resp = client.post("/auth/signup", json={
                "email": "test@example.com",
                "password": "SecurePass123!",
                "first_name": "Jane"
            })
            assert resp.status_code == 200

    def test_signup_invalid_email(self):
        resp = client.post("/auth/signup", json={
            "email": "not-an-email",
            "password": "pass"
        })
        assert resp.status_code == 422


class TestLogin:
    def test_login_success(self):
        with patch("routes.auth_routes.httpx.AsyncClient") as mock_client:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = MOCK_SUPABASE_LOGIN_RESPONSE
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_resp)
            
            resp = client.post("/auth/login", json={
                "email": "test@example.com",
                "password": "password"
            })
            assert resp.status_code == 200
            assert "access_token" in resp.json()

    def test_login_supabase_error_propagated(self):
        with patch("routes.auth_routes.httpx.AsyncClient") as mock_client:
            mock_resp = MagicMock()
            mock_resp.status_code = 400
            mock_resp.json.return_value = {"error": "invalid_credentials"}
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_resp)
            
            resp = client.post("/auth/login", json={
                "email": "test@example.com",
                "password": "wrong"
            })
            assert resp.status_code == 400


class TestInviteToOrg:
    def test_invite_requires_admin(self):
        # No auth header -> should fail
        resp = client.post("/auth/invite-to-org", json={
            "email": "new@example.com",
            "organization_id": 1
        })
        assert resp.status_code in (401, 403)
```

## Acceptance Criteria
- [ ] Tests for signup, login, logout, refresh, me, forgot-password, reset-password, invite-to-org
- [ ] All Supabase API calls are mocked (no real network calls)
- [ ] Tests run in CI (no env vars required beyond test fixtures)
- [ ] Coverage > 80% on routes/auth_routes.py
