# TODO-598: Helmet Security Headers — NarrativeReactor

**Priority:** P0 (Security Critical)
**Repo:** NarrativeReactor
**Effort:** 1 hour
**Dependencies:** None

## Problem
No security headers set. Dashboard is vulnerable to XSS (no CSP), clickjacking (no X-Frame-Options), and protocol downgrade (no HSTS).

## Task
Add `helmet` npm package and configure it in `src/index.ts` before all routes. Configure CSP to allow Swagger UI assets and dashboard scripts.

## Acceptance Criteria
- [ ] `helmet` installed and in package.json dependencies
- [ ] `app.use(helmet())` applied before all routes in src/index.ts
- [ ] CSP configured to allow: self, swagger-ui CDN assets
- [ ] X-Frame-Options: DENY set
- [ ] HSTS enabled for production
- [ ] All existing tests pass
- [ ] Manual check: `curl -I http://localhost:3401/health` shows security headers

## Agent Prompt
```
In /data/workspace/projects/NarrativeReactor:
1. Run: yarn add helmet
2. In src/index.ts, add after imports: import helmet from 'helmet';
3. Add before CORS setup: app.use(helmet({ contentSecurityPolicy: { directives: { defaultSrc: ["'self'"], scriptSrc: ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"], styleSrc: ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"], imgSrc: ["'self'", "data:"] } } }));
4. Run: npm test to verify all tests pass
5. Add a test to src/__tests__/health-and-guards.test.ts verifying X-Frame-Options header is present
```
