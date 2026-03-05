# TODO-582: JWT Refresh Token Revocation on Logout/Password Change

**Priority:** P1 (High Security)
**Repo:** signal-builder-backend
**Effort:** S (2-4 hours)
**Status:** Pending

## Problem
JWT refresh tokens are not invalidated when a user logs out or changes their password. A stolen refresh token remains valid until natural expiry.

## Task
1. Store issued refresh token JTI (JWT ID) in Redis with TTL = token expiry
2. On logout: delete JTI from Redis
3. On password change: delete all JTIs for that user from Redis
4. In refresh token middleware: check JTI exists in Redis before accepting

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend/apps/users/routers/auth.py:

1. When issuing a refresh token, include a unique `jti` claim (uuid4)
2. Store in Redis: SET jwt:jti:{jti} 1 EX {refresh_token_ttl_seconds}
3. On logout endpoint: get jti from token, DEL jwt:jti:{jti} from Redis
4. On password change: scan Redis for jwt:jti:* where user matches and delete all
   (Alternative: store per-user token version in Redis, increment on password change)
5. In the refresh token validation middleware: check if jti exists in Redis
   If missing → 401 Unauthorized
6. Add tests for revocation flow
```

## Acceptance Criteria
- [ ] Logout invalidates refresh token immediately
- [ ] Password change invalidates all refresh tokens for that user
- [ ] Revoked tokens return 401 on next use
- [ ] Integration tests cover the full revocation flow
