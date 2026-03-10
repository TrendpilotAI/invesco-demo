# 316 — Add JWT Auth Middleware to Template REST Router

**Priority:** HIGH  
**Effort:** M  
**Status:** pending

---

## Task Description

The `createTemplateRouter` Express router exposes all 20 template execution endpoints with no authentication. Any caller can run arbitrary signal queries against the database. Add JWT middleware that validates ForwardLane session tokens before any template endpoint is reachable. Also add rate limiting to prevent DB hammering.

---

## Autonomous Coding Prompt

```
REPO: /data/workspace/projects/signal-studio-templates

TASK: Add JWT authentication + rate limiting to the template REST API router.

STEPS:
1. Install dependencies:
   pnpm add jsonwebtoken express-rate-limit
   pnpm add -D @types/jsonwebtoken

2. Create src/middleware/auth.ts:
   - Export jwtAuthMiddleware: RequestHandler
   - Read Authorization: Bearer <token> header
   - Verify JWT using process.env.JWT_SECRET (HS256) or RS256 public key
     (check which ForwardLane Django uses — look at forwardlane-backend if available,
      otherwise default to HS256 with JWT_SECRET env var)
   - On success: attach decoded payload to req.user
   - On failure: return 401 { error: 'Unauthorized' }
   - Export AuthenticatedRequest type extending Request with user field

3. Create src/middleware/rateLimiter.ts:
   - windowMs: 15 * 60 * 1000 (15 min)
   - max: 100 requests per IP (configurable via RATE_LIMIT_MAX env var)
   - Standard headers: true
   - Return 429 { error: 'Too many requests' }

4. Update src/router/templateRouter.ts (or wherever createTemplateRouter lives):
   - Apply rateLimiter globally to the router
   - Apply jwtAuthMiddleware globally to the router
   - Pass req.user.tenantId (or similar) to TemplateEngine.execute() for
     future tenant scoping (even if not used yet, thread it through)

5. Create src/middleware/__tests__/auth.test.ts:
   - Test: valid JWT → req.user populated, next() called
   - Test: missing Authorization header → 401
   - Test: expired JWT → 401
   - Test: invalid signature → 401
   - Test: malformed Bearer format → 401

6. Update README or add docs/auth.md explaining:
   - JWT_SECRET env var requirement
   - How ForwardLane backend should generate compatible tokens
   - Tenant claim name in JWT payload

7. Add env var validation in src/config.ts (create if not exists):
   - Validate JWT_SECRET is set at startup; throw descriptive error if missing
   - Validate DATABASE_URL is set

ACCEPTANCE: All template routes return 401 without valid JWT.
Rate limit returns 429 after 100 requests/15min.
Auth unit tests pass.
```

---

## Dependencies

- **315** (SQL injection fix) — should be in place before auth, but can run in parallel

---

## Acceptance Criteria

- [ ] All template endpoints return 401 without a valid Bearer token
- [ ] JWT verified with `JWT_SECRET` env var (HS256)
- [ ] Rate limiter: 100 req/15min per IP, returns 429
- [ ] Startup validation fails loudly if `JWT_SECRET` or `DATABASE_URL` missing
- [ ] Auth middleware unit tests all pass
- [ ] `req.user` typed via `AuthenticatedRequest`
