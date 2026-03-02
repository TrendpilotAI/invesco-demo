# TODO-403: Refresh Token Rotation + Revocation

**Repo:** signal-studio-auth  
**Priority:** CRITICAL  
**Effort:** M (4-6 hours)  
**Dependencies:** TODO-402 (Redis preferred for revocation list)

## Problem
Current `/auth/refresh` route passes the refresh_token to Supabase but:
- No server-side revocation list (stolen tokens can't be invalidated)
- No rotation tracking (same token reused indefinitely)

## Coding Prompt
```
In /data/workspace/projects/signal-studio-auth/routes/auth_routes.py:

1. Add a `TokenRevocationStore` class:
   - Backed by Redis SET with TTL (falls back to in-memory set if no Redis)
   - `revoke(token_jti: str, ttl_seconds: int)` — adds to revoked set
   - `is_revoked(token_jti: str) -> bool` — checks revocation

2. Update `refresh` route:
   - After successful Supabase refresh, extract old token's `jti` claim
   - Add old refresh token jti to revocation store (TTL = token expiry)
   - Return new tokens from Supabase response

3. Update `logout` route:
   - After Supabase logout, also add token's jti to revocation store

4. Update middleware `_verify_supabase_jwt`:
   - After signature verification, check if `jti` is in revocation store
   - Return 401 "Token has been revoked" if found

5. Add tests for rotation and revocation flows
```

## Acceptance Criteria
- [ ] Logging out revokes the token server-side
- [ ] Refreshing invalidates the old refresh token
- [ ] Revoked tokens rejected by middleware
- [ ] Falls back gracefully without Redis
