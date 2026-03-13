# TODO: Fix API Auth Middleware - Protect All Unprotected Routes

## Priority: P0 Critical
## Repo: signal-studio-frontend

### Problem
32 of 44 API routes have no authentication checks. The middleware configuration allows all /api/ routes to bypass auth validation, creating critical security vulnerabilities in production.

### Action Items
- Audit all Next.js API routes under `src/app/api/` and `src/pages/api/`
- Apply auth middleware (withAuth wrapper or Next.js middleware.ts matcher) to every route
- Fix the middleware.ts matcher config to NOT have wildcard bypass
- Add integration tests verifying unauthenticated requests to protected routes return 401
- Deploy and verify in staging before production push

### Impact
- Eliminates critical security vulnerability (unauthorized data access)
- Required before any public/customer-facing deployment
- Blocks all other production readiness work

### References
- AUDIT.md security section
- Current middleware.ts configuration
