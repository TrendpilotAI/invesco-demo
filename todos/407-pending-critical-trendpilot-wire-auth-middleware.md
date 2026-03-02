# 407 — Wire Authentication Middleware to All API Routes

**Priority:** CRITICAL (P0) — Security blocker before any deployment  
**Repo:** Trendpilot  
**Effort:** S (½ day)  
**Dependencies:** None — auth middleware already implemented

## Problem
`authGuard` and `apiKeyAuth` middleware exist in `src/middleware/` but are **never imported or applied** in `src/api/index.ts`. Every endpoint — admin, compliance, audit, tenant management, GDPR deletion — is publicly accessible with zero auth.

## Coding Prompt
```
In /data/workspace/projects/Trendpilot/src/api/index.ts:

1. Import authGuard from '@/middleware/authGuard'
2. Import apiKeyAuth from '@/middleware/apiKeyAuth'  
3. Apply apiKeyAuth to ALL routes except:
   - GET /api/health (public)
   - POST /api/subscribers/opt-in (public — email confirmation)
   - GET /api/subscribers/confirm/:token (public)
   - POST /api/sso/callback (handled separately — see below)
4. Apply authGuard to all /api/admin/* routes (requires valid session, not just API key)
5. For SSO stubs in src/services/sso/index.ts — add explicit:
   throw new Error('SSO not implemented: do not use in production')
   to handleSAMLCallback() and handleOAuthCallback() to prevent auth bypass
6. Add rate limiting middleware (express-rate-limit) to /api/* — 100 req/15min default
7. Add CORS middleware to restrict origins to dashboard domain
```

## Acceptance Criteria
- [ ] All /api/admin/* routes return 401 without valid auth
- [ ] All /api/tenants/* mutation routes protected
- [ ] All /api/compliance/* routes protected
- [ ] /api/health returns 200 without auth
- [ ] SSO routes throw NotImplementedError
- [ ] Tests updated to include auth headers
