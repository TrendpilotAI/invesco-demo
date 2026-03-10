# 864 — Remove NEXT_PUBLIC_SKIP_AUTH=true from .env.production

**Repo:** signal-studio  
**Priority:** P0 — Critical Security  
**Effort:** 30 minutes  
**Status:** pending

## Problem
`.env.production` contains `NEXT_PUBLIC_SKIP_AUTH=true`. This environment variable causes middleware.ts to skip ALL authentication checks — any user can access any route without credentials in production.

**File:** `/data/workspace/projects/signal-studio/.env.production` (line 2)

## Impact
- All protected API routes accessible without JWT
- All protected pages accessible without login
- Rate limiting still applies but auth is completely bypassed

## Task
1. Remove `NEXT_PUBLIC_SKIP_AUTH=true` from `.env.production`
2. Verify Railway env vars have proper auth config (JWT_SECRET, etc.)
3. Test login flow works end-to-end after change
4. Redeploy to Railway

## Coding Prompt (for autonomous agent)
```
Edit /data/workspace/projects/signal-studio/.env.production
Remove the line: NEXT_PUBLIC_SKIP_AUTH=true
Leave NEXT_PUBLIC_CORE_API untouched.

Then verify the Railway deployment has these env vars set:
- JWT_SECRET (for token signing)
- CORE_API (Django backend URL)
Check that login flow works: POST /api/auth/login returns a JWT, and protected routes return 401 without it.
```

## Acceptance Criteria
- [ ] `.env.production` does NOT contain NEXT_PUBLIC_SKIP_AUTH
- [ ] `GET /api/signals` returns 401 without Authorization header
- [ ] Login flow works and returns usable JWT
- [ ] Protected pages redirect to /login without auth cookie
