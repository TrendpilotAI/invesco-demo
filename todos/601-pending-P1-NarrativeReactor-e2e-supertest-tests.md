# TODO-601: E2E Supertest Tests — NarrativeReactor

**Priority:** P1 (Quality)
**Repo:** NarrativeReactor
**Effort:** 2 days
**Dependencies:** TODO-597 (JWT expiry)

## Problem
No integration/E2E tests that spin up the full Express app. Unit tests cover logic but not HTTP layer (routing, middleware chain, auth enforcement, rate limiting).

## Task
Create supertest-based E2E tests for all major route groups.

## Acceptance Criteria
- [ ] `supertest` installed as devDependency
- [ ] `src/__tests__/e2e/app.test.ts` created
- [ ] Tests for: health endpoint, auth enforcement (valid/invalid/missing API key), rate limiting (basic), content generation route, brand management routes, campaign CRUD, webhook signature verification
- [ ] All E2E tests run in CI (added to vitest config)
- [ ] Test isolation: each test suite uses in-memory SQLite

## Agent Prompt
```
In /data/workspace/projects/NarrativeReactor:
1. Run: yarn add -D supertest @types/supertest
2. Create src/__tests__/e2e/app.test.ts
3. Import the Express app from src/index.ts (export app before server listen)
4. Use supertest(app) to make HTTP requests in tests
5. Test cases:
   - GET /health → 200 { status: 'ok' }
   - GET /api/content without X-API-Key → 401
   - GET /api/content with wrong API key → 401
   - GET /api/content with valid X-API-Key → 200 or valid response
   - POST /webhooks/... without signature → 403
   - GET /docs/openapi.json → 200 with valid JSON
   - GET /login → 200 HTML
   - POST /login with wrong password → 401 or redirect
6. Mock external services (Fal, Blotato, AI) with vi.mock
7. Run: npm test to verify all pass
```
