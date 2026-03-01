# TODO 352 — Add Rate Limiting to Auth Routes
**Repo:** signal-studio-auth
**Priority:** CRITICAL
**Effort:** 2 hours
**Status:** pending

## Description
`/auth/login` and `/auth/signup` have no rate limiting. Attackers can brute-force credentials
or spam account creation without restriction.

## Coding Prompt
In `/data/workspace/projects/signal-studio-auth/`:

1. Add to `requirements.txt`:
```
slowapi>=0.1.9
redis>=5.0.0
```

2. Create `middleware/rate_limiter.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

3. In `routes/auth_routes.py`, import and apply limits:
```python
from fastapi import Request
from middleware.rate_limiter import limiter

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, body: LoginRequest):
    ...

@router.post("/signup")  
@limiter.limit("10/hour")
async def signup(request: Request, body: SignupRequest):
    ...
```

4. In the main FastAPI app setup, register the limiter:
```python
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from middleware.rate_limiter import limiter

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

5. Add tests in `tests/test_rate_limiting.py` that verify 429 is returned after limit exceeded.

## Acceptance Criteria
- [ ] Login limited to 5 requests/minute per IP
- [ ] Signup limited to 10 requests/hour per IP
- [ ] 429 Too Many Requests returned when limit exceeded
- [ ] Rate limit headers included in response
- [ ] Tests pass for rate limit enforcement
