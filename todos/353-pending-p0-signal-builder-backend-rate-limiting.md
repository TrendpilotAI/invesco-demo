# TODO-353: Add Rate Limiting with slowapi
**Project:** signal-builder-backend  
**Priority:** P0  
**Effort:** S (1 day)  
**Status:** pending  
**Created:** 2026-03-01

---

## Description

Auth endpoints and compute-heavy signal execution endpoints have no rate limiting, exposing the service to brute-force attacks and resource exhaustion. Add `slowapi` middleware to protect `/users/login`, `/users/refresh` at 10/minute per IP, and signal execution endpoints at 30/minute per user.

---

## Full Autonomous Coding Prompt

```
You are working on the signal-builder-backend FastAPI service at /data/workspace/projects/signal-builder-backend/.

TASK: Add rate limiting using slowapi.

STEP 1 — Install slowapi:
```
cd /data/workspace/projects/signal-builder-backend
pipenv install slowapi
```
Add to Pipfile: `slowapi = ">=0.1.9"`

STEP 2 — Create rate limiting middleware at core/rate_limit.py:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

def get_user_id(request: Request) -> str:
    """Use user ID from JWT if available, fall back to IP."""
    # Try to get user from request state (set by auth middleware)
    user = getattr(request.state, "user", None)
    if user and hasattr(user, "id"):
        return str(user.id)
    return get_remote_address(request)

limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": f"Rate limit exceeded: {exc.detail}",
            "error": "RATE_LIMIT_EXCEEDED"
        },
        headers={"Retry-After": "60"}
    )
```

STEP 3 — Register middleware in apps/main.py:
```python
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from core.rate_limit import limiter

# Add to app setup:
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
```

STEP 4 — Apply rate limits to auth endpoints in apps/users/routers/user.py (or wherever login/refresh routes are defined):
```
grep -rn "login\|refresh" apps/users/ --include="*.py" -l
```
Add decorators:
```python
from core.rate_limit import limiter

@router.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, ...):
    ...

@router.post("/refresh")
@limiter.limit("10/minute")
async def refresh_token(request: Request, ...):
    ...
```
NOTE: slowapi requires `request: Request` as the first parameter.

STEP 5 — Apply rate limits to signal execution endpoints in apps/signals/routers/:
```
grep -rn "execute\|run\|validate" apps/signals/routers/ --include="*.py" -l
```
Apply `@limiter.limit("30/minute")` to signal execution and validation endpoints.

STEP 6 — Add rate limit settings to core/settings.py:
```python
RATE_LIMIT_AUTH: str = "10/minute"
RATE_LIMIT_SIGNAL_EXECUTE: str = "30/minute"
RATE_LIMIT_DEFAULT: str = "200/minute"
```
Update core/rate_limit.py to read from settings.

STEP 7 — Test rate limiting:
```
pipenv run pytest apps/users/ -v -k "rate" 
# Write a test that calls login 11 times and asserts 429 on the 11th call
```
Create test file apps/users/tests/test_rate_limiting.py:
```python
import pytest
from fastapi.testclient import TestClient
from apps.main import app

client = TestClient(app)

def test_login_rate_limit():
    """11th login attempt should return 429."""
    for i in range(10):
        resp = client.post("/users/login", json={"email": "x@x.com", "password": "wrong"})
        assert resp.status_code != 429, f"Got 429 on attempt {i+1}"
    resp = client.post("/users/login", json={"email": "x@x.com", "password": "wrong"})
    assert resp.status_code == 429
    assert "Retry-After" in resp.headers
```

STEP 8 — Verify rate limit headers in all responses:
After adding SlowAPIMiddleware, all responses should include:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`
```

---

## Dependencies

- Pydantic v2 migration (TODO-352) should ideally be complete first, but this can run in parallel on a branch
- No hard blockers

---

## Effort Estimate

**1 day** — slowapi integrates cleanly with FastAPI. Main work is finding all the endpoints and ensuring `request: Request` is properly threaded through.

---

## Acceptance Criteria

- [ ] `slowapi` in Pipfile and installed
- [ ] `SlowAPIMiddleware` registered in `apps/main.py`
- [ ] `/users/login` limited to 10/minute → returns 429 with `Retry-After` header on exceeded
- [ ] `/users/refresh` limited to 10/minute → returns 429 on exceeded
- [ ] Signal execution/validation endpoints limited to 30/minute
- [ ] Rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`) present in responses
- [ ] `test_rate_limiting.py` passes
- [ ] No existing tests broken
