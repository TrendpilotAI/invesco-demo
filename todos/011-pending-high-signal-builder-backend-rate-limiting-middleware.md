---
status: pending
priority: high
issue_id: "011"
tags: [signal-builder-backend, security, middleware, rate-limiting, redis]
dependencies: []
---

# TODO 011 — Rate Limiting Middleware

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** M (1-2 days)

## Problem Statement

The FastAPI backend has no rate limiting. Any authenticated (or unauthenticated) client can flood the API with requests, causing:

- Denial of service risk on the signal translation endpoints (CPU-heavy SQL generation)
- Analytical DB sync endpoints triggerable without throttle
- JWT auth endpoints vulnerable to brute-force
- No per-tenant isolation of request budgets

The only middleware currently present is `core/middlewares/auth_middleware.py` — no rate limiting.

## Findings

- `core/middlewares/auth_middleware.py` is the sole middleware file
- Redis is already a project dependency (`redis = "*"` in Pipfile) and is used by Celery
- FastAPI supports `@app.middleware("http")` and Starlette middleware classes
- The most impactful endpoints to protect:
  - `POST /signals/translate` (SQL translation — CPU heavy)
  - `POST /auth/login` (brute-force risk)
  - `POST /analytical-db/sync` (triggers expensive DB operations)

## Proposed Solutions

### Option A: slowapi (Recommended)
Use `slowapi` (FastAPI/Starlette port of Flask-Limiter) with Redis backend.

**Pros:** Battle-tested, decorator-based, easy per-route limits  
**Cons:** Additional dependency

### Option B: Custom Redis Sliding Window Middleware
Implement a custom Starlette middleware using Redis ZADD/ZRANGEBYSCORE for sliding window rate limiting.

**Pros:** No new dependency, full control  
**Cons:** More code to maintain

**Recommendation:** Option A (`slowapi`) for rapid implementation, Redis backend for distributed enforcement.

## Coding Prompt

```
You are adding rate limiting to signal-builder-backend.

Repository: /data/workspace/projects/signal-builder-backend/
Stack: FastAPI 0.92, Python 3.11, Redis (already available), Starlette middleware

TASK: Implement rate limiting middleware using slowapi with Redis backend.

1. Add dependency to Pipfile [packages]:
   slowapi = "*"

2. Create core/middlewares/rate_limiter.py:
   - Import and configure slowapi Limiter with Redis storage
   - Storage URL: read from settings.REDIS_URL
   - Default limits: "100/minute" per IP
   - Key function: use X-Forwarded-For → remote IP fallback
   - Export: `limiter` singleton instance

3. Update core/internals/__init__.py (or wherever get_application is defined):
   - Import the limiter
   - Add SlowAPIMiddleware to the FastAPI app
   - Register exception handler for RateLimitExceeded → 429 JSON response:
     {"error": "rate_limit_exceeded", "detail": "Too many requests. Try again later."}

4. Apply per-route limits via decorators:

   In apps/translators/main.py (or relevant router):
   @limiter.limit("20/minute")  # SQL translation is expensive
   async def translate_signal(...):

   In core/auth/routes.py:
   @limiter.limit("10/minute")  # Protect login from brute-force
   async def login(...):

   In apps/analytical_db/routers/ (sync trigger):
   @limiter.limit("5/minute")  # Sync is heavy
   async def trigger_sync(...):

5. Create tests/test_rate_limiting.py:
   - Test that 429 is returned after limit exceeded
   - Test that different IPs get independent counters
   - Test that rate limit headers (X-RateLimit-*) are present in response
   - Mock Redis to avoid test DB requirement

6. Update core/middlewares/__init__.py to export the limiter

7. Add to Pipfile [dev-packages]:
   pytest-mock = "*"  # if not present

8. Add REDIS_URL to settings (if not already present):
   - Read from os.environ["REDIS_URL"]
   - Fallback: "redis://localhost:6379"

9. Run: python -m pytest tests/test_rate_limiting.py -v

Constraints:
- Rate limits must be configurable via environment variables (not hardcoded)
- Add RATE_LIMIT_DEFAULT, RATE_LIMIT_AUTH, RATE_LIMIT_TRANSLATE to settings
- 429 response must include Retry-After header
- Do not break existing middleware chain
- Document rate limits in README.md
```

## Acceptance Criteria

- [ ] `slowapi` added to Pipfile and `pip install` succeeds
- [ ] `core/middlewares/rate_limiter.py` created with Redis-backed limiter
- [ ] Login endpoint limited to 10 req/min per IP
- [ ] Signal translation endpoint limited to 20 req/min per IP
- [ ] Analytical DB sync limited to 5 req/min per IP
- [ ] 429 response returns JSON `{"error": "rate_limit_exceeded", ...}` with `Retry-After` header
- [ ] Rate limit values configurable via env vars
- [ ] `tests/test_rate_limiting.py` passes with mocked Redis
- [ ] No regression in existing middleware/auth tests

## Dependencies

None — Redis already available. Can execute immediately.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Identified missing rate limiting from codebase review
- Redis already a dependency via Celery — reuse for rate limit storage
- Selected slowapi as fastest implementation path

**Learnings:**
- The auth middleware is the only middleware — rate limiting is a clear gap
- slowapi is idiomatic for FastAPI and well-maintained
