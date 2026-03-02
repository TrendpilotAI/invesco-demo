# TODO-402: Replace In-Memory Rate Limiter with Redis

**Repo:** signal-studio-auth  
**Priority:** CRITICAL  
**Effort:** M (4-6 hours)  
**Dependencies:** None (Redis URL env var)

## Problem
Current `_RateLimiter` in `routes/auth_routes.py` is in-memory:
- Resets on every restart (login abuse window reset on deploy)
- Doesn't work across multiple replicas (Railway scales horizontally)
- No persistence across pod restarts

## Task
Replace the `_RateLimiter` class with a Redis sliding-window implementation.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-auth/routes/auth_routes.py:

1. Add optional Redis dependency to requirements.txt: `redis>=5.0.0`

2. Create a new `RedisRateLimiter` class that:
   - Accepts `redis_url: str | None` in constructor
   - Falls back to existing in-memory `_RateLimiter` if redis_url is None
   - Uses Redis ZADD + ZREMRANGEBYSCORE + ZCARD sliding window algorithm
   - Key format: `ratelimit:{endpoint}:{ip}`
   - Sets TTL on keys to window_seconds

3. Load REDIS_URL from environment in config/supabase_config.py:
   REDIS_URL: str | None = os.environ.get("REDIS_URL")

4. Update _login_limiter and _signup_limiter to use the new implementation

5. Add tests in tests/test_security.py for Redis rate limiter using fakeredis

6. Update MIGRATION_GUIDE.md with Redis setup instructions for Railway
```

## Acceptance Criteria
- [ ] Rate limit persists across app restarts
- [ ] Multiple replicas share the same rate limit counters
- [ ] Falls back gracefully to in-memory if REDIS_URL not set
- [ ] All existing rate limit tests still pass
- [ ] New tests cover Redis-backed limiting
