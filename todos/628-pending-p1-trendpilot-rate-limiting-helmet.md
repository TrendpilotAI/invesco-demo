# TODO 628: Trendpilot — Add Rate Limiting & Security Headers

**Priority:** P1 — High (security basics before launch)
**Effort:** S (half day)
**Repo:** /data/workspace/projects/Trendpilot/
**Created:** 2026-03-05

## Problem
No rate limiting on public API routes (`/api/trends`, `/api/subscribers/opt-in`). No security headers (X-Frame-Options, CSP, etc.). These are basic production hardening requirements.

## Acceptance Criteria
- [ ] `helmet()` middleware applied globally
- [ ] Rate limit: 100 req/min per IP on public routes
- [ ] Rate limit: 20 req/min per IP on auth routes
- [ ] 429 response with Retry-After header when rate limited

## Coding Prompt
```
cd /data/workspace/projects/Trendpilot
npm install helmet express-rate-limit

In src/api/index.ts, after creating app:
1. import helmet from 'helmet'
2. import rateLimit from 'express-rate-limit'
3. app.use(helmet())
4. const publicLimiter = rateLimit({ windowMs: 60_000, max: 100 })
5. const authLimiter = rateLimit({ windowMs: 60_000, max: 20 })
6. app.use('/api/trends', publicLimiter)
7. app.use('/api/subscribers', publicLimiter)
8. app.use('/api/auth', authLimiter)
9. app.use('/api/sso', authLimiter)

Add types: npm install --save-dev @types/helmet
```
