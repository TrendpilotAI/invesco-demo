# TODO-828: Fix Rate Limiter Code Duplication in signal-studio-auth

**Repo:** signal-studio-auth  
**Priority:** P1 (High)  
**Effort:** 2 hours  
**Status:** pending

## Problem
`routes/auth_routes.py` has 3 implementations of essentially the same rate limiting logic:
1. `_build_rate_limiter()` — DEAD CODE, never called
2. `_make_shim_check()` — in-memory only
3. `_redis_or_memory_check()` — the live one, but re-creates RedisStorage on every request (performance bug)

## Task
1. Delete `_build_rate_limiter()`
2. Remove inner `from config.redis_config import REDIS_URL` (duplicate import)
3. Create `class RateLimiter` that caches RedisStorage + SlidingWindowRateLimiter instances
4. Expose `._calls` property for backward test compat

## Acceptance Criteria
- [ ] `_build_rate_limiter` removed
- [ ] RedisStorage created once, not per-request
- [ ] All existing rate limit tests still pass
- [ ] Rate limiter code reduced from ~100 to ~50 lines
