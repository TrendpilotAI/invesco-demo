# TODO-221: Rate Limiting on Auth Routes (signal-studio-auth)

**Priority:** CRITICAL  
**Repo:** signal-studio-auth  
**Status:** pending  

## Description
The `/auth/login` and `/auth/signup` routes in `routes/auth_routes.py` have no rate limiting.
This makes them vulnerable to brute force and credential stuffing attacks.

## Task
Add `slowapi` (FastAPI rate limiter backed by Redis) to limit:
- `/auth/login`: 5 requests/minute per IP
- `/auth/signup`: 3 requests/minute per IP

## Coding Prompt
```
In /data/workspace/projects/signal-studio-auth/:

1. Add to requirements.txt:
   slowapi>=0.1.9
   limits>=3.6.0

2. Create middleware/rate_limit.py:
   - Initialize Limiter with Redis backend (use REDIS_URL env var, fallback to in-memory)
   - Export `limiter` instance

3. Update routes/auth_routes.py:
   - Import limiter
   - Decorate login: @limiter.limit("5/minute")
   - Decorate signup: @limiter.limit("3/minute")
   - Add SlowAPIMiddleware to app if not present

4. Update tests/test_auth.py:
   - Add test that 6th login attempt returns 429

5. Document in MIGRATION_GUIDE.md under "Security Hardening" section
```

## Dependencies
- Redis available in Railway environment (already configured)

## Estimated Effort
S (2-3 hours)

## Acceptance Criteria
- Login returns 429 after 5 attempts/min from same IP
- Signup returns 429 after 3 attempts/min from same IP
- Tests pass in CI
