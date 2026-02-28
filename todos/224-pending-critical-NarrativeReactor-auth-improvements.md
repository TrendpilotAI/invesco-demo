# 224 · NarrativeReactor · Auth Improvements (JWT + Scoped Keys)

**Status:** pending  
**Priority:** critical  
**Project:** NarrativeReactor  
**Created:** 2026-02-27

---

## Task Description

Current auth is a single shared API key (`X-API-Key` header) with a dangerous fallback: if `API_KEY` env var is unset, auth is completely disabled. No JWT, no scoped permissions, no key rotation. This needs hardening for multi-tenant or production use.

---

## Coding Prompt (agent-executable)

```
Working in /data/workspace/projects/NarrativeReactor/src/middleware/auth.ts and related files:

1. Remove the "auth disabled" fallback — if API_KEY is unset, FAIL CLOSED (return 500 with config error).

2. Add JWT support alongside API key auth:
   - Install: npm i jsonwebtoken @types/jsonwebtoken
   - Accept Bearer <jwt> in Authorization header OR X-API-Key header
   - JWT secret from JWT_SECRET env var
   - JWT payload: { sub: string, scopes: string[], iat, exp }
   - Add middleware factory: `requireScope(scope: string)` that checks jwt.scopes

3. Create src/lib/auth.ts with:
   - `generateToken(sub: string, scopes: string[], expiresIn?: string)` 
   - `verifyToken(token: string)` → payload or null
   - Predefined scopes: 'content:generate', 'content:publish', 'admin', 'read'

4. Add POST /api/auth/token endpoint (protected by master API key):
   - Body: { sub: string, scopes: string[], expiresIn?: string }
   - Returns: { token: string, expiresAt: string }

5. Update tests in src/__tests__/ to cover:
   - Auth disabled = 500
   - Invalid key = 401
   - Valid JWT = 200
   - Expired JWT = 401
   - Missing scope = 403

6. Document in docs/auth.md
```

---

## Dependencies

- None (foundational security fix)

## Effort Estimate

4–5 hours

## Acceptance Criteria

- [ ] No auth bypass possible when API_KEY is unset
- [ ] JWT tokens issued via /api/auth/token
- [ ] Scope-based middleware available for routes
- [ ] All auth tests pass
- [ ] No timing-attack vulnerability (use `crypto.timingSafeEqual` for key compare)
