# 807 — Rate Limit /reset-password and /update-password

**Repo:** signal-studio-auth  
**Priority:** P1 (security)  
**Effort:** S (30 mins)  
**Dependencies:** 800 (rate limiter refactor ideally done first)

## Acceptance Criteria

- [ ] `/auth/reset-password` rate limited to 3 requests per 60s per IP
- [ ] `/auth/update-password` rate limited to 5 requests per 60s per user ID (not IP)
- [ ] Tests verify 429 is returned when limit exceeded

## Coding Prompt

```
In /data/workspace/projects/signal-studio-auth/routes/auth_routes.py:

1. Create a reset_password rate limiter (3/60s per IP):
   _reset_limiter = _LimiterShim(
       _redis_or_memory_check(_reset_calls, _reset_lock, max_calls=3, window_seconds=60),
       _reset_calls,
   )
   _reset_calls: dict[str, list[float]] = defaultdict(list)
   _reset_lock = Lock()

2. In reset_password() handler, add at the top:
   _reset_limiter.check(_client_ip(request))

3. For update_password(), rate limit by user_id (not IP) to 5/60s:
   user_key = getattr(request.state.user, "sub", _client_ip(request))
   _update_limiter.check(user_key)

4. Add tests in tests/test_security.py for both endpoints hitting the rate limit.
```
