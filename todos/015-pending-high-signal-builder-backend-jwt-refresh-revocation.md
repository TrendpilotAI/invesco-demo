---
status: pending
priority: high
issue_id: "015"
tags: [signal-builder-backend, security, auth, jwt, token-refresh, redis]
dependencies: []
---

# TODO 015 — JWT Token Refresh and Revocation

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** M (2-3 days)

## Problem Statement

The backend uses `fastapi-jwt-auth` for authentication. The current implementation likely issues access tokens with long lifetimes and has no mechanism to:

1. **Refresh** tokens without requiring re-login (bad UX)
2. **Revoke** tokens on logout or security event (security gap)
3. **Invalidate** tokens for compromised accounts

Without token revocation, a stolen JWT remains valid until expiry. Without refresh tokens, users are forced to re-authenticate frequently.

## Findings

- `core/auth/auth_token.py` manages JWT token operations
- `core/auth/routes.py` has auth endpoints
- `fastapi-jwt-auth` is already installed (supports refresh tokens natively)
- Redis is available (ideal for revocation blocklist — O(1) lookup)
- `core/auth/dependencies.py` likely validates tokens on every request

## Proposed Solutions

### Option A: Refresh Token + Redis Blocklist (Recommended)
- Short-lived access tokens (15min)
- Long-lived refresh tokens (7 days, stored in Redis)
- Revocation: add token JTI to Redis blocklist on logout
- Blocklist check: on every access token validation

**Pros:** Secure, standard OAuth2 pattern, fast revocation  
**Cons:** Redis dependency for auth (must handle Redis downtime)

### Option B: Rotating Refresh Tokens Only
Issue new access token on each refresh, invalidate old refresh token.

**Pros:** Simpler  
**Cons:** No immediate revocation capability

**Recommendation:** Option A — full refresh + revocation with Redis blocklist.

## Coding Prompt

```
You are implementing JWT token refresh and revocation for signal-builder-backend.

Repository: /data/workspace/projects/signal-builder-backend/
Stack: FastAPI, fastapi-jwt-auth, Redis, Python 3.11

TASK: Add refresh token endpoint and Redis-backed token revocation.

1. Read existing auth code:
   - core/auth/auth_token.py
   - core/auth/routes.py
   - core/auth/dependencies.py
   - core/auth/schemas/

2. Update JWT configuration:
   - Access token TTL: 15 minutes (ACCESS_TOKEN_EXPIRE_MINUTES=15)
   - Refresh token TTL: 7 days (REFRESH_TOKEN_EXPIRE_DAYS=7)
   - Enable JWT_ALGORITHM: "HS256" (or current algorithm)
   - Enable denylist: JWT_DENYLIST_ENABLED=true, JWT_DENYLIST_TOKEN_CHECKS=["access","refresh"]

3. Create core/auth/token_blocklist.py:
   class TokenBlocklist:
       def __init__(self, redis_client):
           self.redis = redis_client
       
       async def add_to_blocklist(self, jti: str, token_type: str, expires_in: int):
           # Store JTI in Redis with TTL matching token expiry
           key = f"blocklist:{token_type}:{jti}"
           await self.redis.setex(key, expires_in, "revoked")
       
       async def is_blocked(self, jti: str, token_type: str) -> bool:
           key = f"blocklist:{token_type}:{jti}"
           return await self.redis.exists(key) > 0

4. Add token blocklist check to fastapi-jwt-auth denylist callback:
   @AuthJWT.load_config
   def get_config():
       return [("authjwt_denylist_enabled", True), ...]
   
   @AuthJWT.token_in_denylist_loader
   async def check_if_token_in_denylist(decrypted_token):
       jti = decrypted_token["jti"]
       token_type = decrypted_token["type"]
       return await token_blocklist.is_blocked(jti, token_type)

5. Add new endpoints in core/auth/routes.py:

   POST /auth/refresh:
   - Requires valid refresh token (in body or cookie)
   - Returns new access token
   - Does NOT invalidate the refresh token (use /auth/logout for that)
   - Rate limit: 10/minute (see TODO 011)

   POST /auth/logout:
   - Requires valid access token
   - Adds both access token JTI AND refresh token JTI to blocklist
   - Returns 200 {"message": "Successfully logged out"}

   POST /auth/logout-all:  (optional bonus)
   - Invalidates ALL tokens for the user by incrementing a user token_version
   - Stored in user record or Redis hash

6. Update login endpoint:
   - Return both access_token AND refresh_token in response
   - Include token_type, expires_in fields
   - Schema:
     {"access_token": "...", "refresh_token": "...", 
      "token_type": "bearer", "expires_in": 900}

7. Add to settings:
   ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
   REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

8. Create tests/auth/test_token_refresh.py:
   - Test successful refresh returns new access token
   - Test refresh with revoked refresh token returns 401
   - Test logout revokes both tokens
   - Test access with revoked access token returns 401
   - Mock Redis blocklist

9. Update API documentation (docstrings on route handlers) with:
   - Expected token in Authorization header
   - How to use refresh flow
   - Error codes: 401 (expired), 422 (malformed)

10. Run: python -m pytest tests/auth/ -v

Constraints:
- Refresh token must ONLY work at /auth/refresh endpoint (not general API)
- Blocklist TTL must match token TTL (don't store forever — wastes Redis memory)
- If Redis is down, fail OPEN for read operations (allow valid tokens through)
- Refresh token should be treated as sensitive — log but don't expose JTI in responses
- All token operations must be atomic (use Redis pipelines where needed)
```

## Acceptance Criteria

- [ ] Access tokens expire in 15 minutes (configurable)
- [ ] Refresh tokens expire in 7 days (configurable)
- [ ] `POST /auth/refresh` returns new access token
- [ ] `POST /auth/logout` revokes both access and refresh tokens
- [ ] Revoked tokens return 401 on subsequent use
- [ ] Token blocklist stored in Redis with matching TTL
- [ ] Login response includes both `access_token` and `refresh_token`
- [ ] `tests/auth/test_token_refresh.py` passes with mocked Redis
- [ ] Redis downtime does NOT block valid access tokens (fail-open for reads)
- [ ] No plaintext tokens logged

## Dependencies

- TODO 011 (Rate Limiting) — recommended to rate-limit `/auth/refresh` and `/auth/logout` after 011 is implemented, but not a hard blocker.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Identified missing token refresh/revocation from auth code review
- Designed Redis-backed blocklist for O(1) revocation
- fastapi-jwt-auth already supports denylist callbacks natively

**Learnings:**
- fastapi-jwt-auth denylist is synchronous by default — may need async workaround
- TTL on Redis blocklist keys must match token TTL to avoid memory leak
