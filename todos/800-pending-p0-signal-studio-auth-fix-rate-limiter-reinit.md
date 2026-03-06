# 800 — Fix Rate Limiter Re-initialization on Every Request

**Repo:** signal-studio-auth  
**Priority:** P0 (performance bug)  
**Effort:** S (2-3 hours)  
**Dependencies:** none

## Problem

In `routes/auth_routes.py`, the `_redis_or_memory_check()` function creates a new `RedisStorage` and `SlidingWindowRateLimiter` object on **every single request**. This defeats connection pooling and adds unnecessary latency to every auth call.

## Acceptance Criteria

- [ ] `RedisStorage` and `SlidingWindowRateLimiter` are initialized once at module load time
- [ ] All existing rate limit tests continue to pass
- [ ] Dead code `_build_rate_limiter()` is removed
- [ ] `_LimiterShim` backward-compat interface preserved (for test compatibility)

## Coding Prompt

```
In /data/workspace/projects/signal-studio-auth/routes/auth_routes.py:

1. Remove the `_build_rate_limiter()` function entirely (it's dead code — never called).

2. Refactor `_redis_or_memory_check()` so that `RedisStorage` and `SlidingWindowRateLimiter`
   are initialized ONCE at module level (not inside the closure that runs on every request).
   Pattern:
   
   # Module-level initialization
   _redis_storage = None
   _redis_limiter_instance = None
   try:
       from limits.storage import RedisStorage
       from limits.strategies import SlidingWindowRateLimiter
       _redis_storage = RedisStorage(REDIS_URL)
       _redis_limiter_instance = SlidingWindowRateLimiter(_redis_storage)
   except Exception:
       pass  # Falls back to in-memory
   
   Then in _redis_or_memory_check(), use the module-level instances if available.

3. Run existing tests to verify nothing is broken:
   cd /data/workspace/projects/signal-studio-auth && python -m pytest tests/ -x -q

4. Ensure the in-memory fallback still works when Redis is unavailable.
```
