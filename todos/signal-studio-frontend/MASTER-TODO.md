# MASTER-TODO: signal-studio-frontend
**Scored:** 2026-03-13 | **Composite:** 6.35/10 | **Tier:** 2

## Score Breakdown
| Dimension       | Score |
|----------------|-------|
| code_quality   | 6.0   |
| test_coverage  | 4.0   |
| security       | 4.0   |
| documentation  | 7.0   |
| architecture   | 6.5   |
| business_value | 7.5   |
| **COMPOSITE**  | **6.35** |

## 🚨 CRITICAL FLAGS
- **32 out of 44 API routes have NO authentication checks** — unauthenticated access to critical APIs
- **Middleware bypasses ALL /api/ routes auth** — major security risk in production
- **CI pipeline does not run tests** — undetected regressions shipping to prod
- TypeScript strict mode disabled — masking type safety bugs
- No runtime input validation (missing Zod schemas on POST/PUT routes)

---

## P0 — Fix Now (Blockers)
- [ ] Implement `requireAuth()` middleware and add auth checks to all 32 unprotected API routes
- [ ] Fix CI pipeline to run `pnpm test:ci`, add Playwright smoke tests, enforce coverage thresholds
- [ ] Audit and fix the middleware that bypasses /api/ route auth

## P1 — This Sprint
- [ ] Enable TypeScript strict mode in `tsconfig.json`, fix all resulting type errors, remove `any` usage
- [ ] Add Zod schema validation to all POST/PUT API routes for runtime input validation
- [ ] Archive stale root-level markdown docs and debug/setup scripts into `docs/archive` or `scripts/debug`
- [ ] Add CSP security headers to Next.js config

## P2 — Next Sprint
- [ ] Increase unit test coverage to 60%+ for API route handlers
- [ ] Add component tests for critical financial signal views
- [ ] Implement E2E tests for key user journeys (login → signal view → export)
- [ ] Add API rate limiting to expensive Oracle DB queries

## P3 — Backlog
- [ ] Refactor large page components into smaller focused components
- [ ] Add API documentation (OpenAPI spec or similar)
- [ ] Performance: review Oracle DB query patterns, add caching layer
- [ ] Implement feature flags for gradual rollouts
