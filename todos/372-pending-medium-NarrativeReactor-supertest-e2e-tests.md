# 372 — Add Supertest E2E Tests for Express Routes

## Task Description
The existing 287 tests cover services and middleware in isolation but no test exercises the full HTTP layer end-to-end (request → middleware → route → service → SQLite → response). Add supertest-based integration tests covering critical paths.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

Add supertest E2E tests under `src/__tests__/e2e/`. Use an in-memory or temp-file SQLite database that resets between test suites.

Install supertest if not present: `npm install --save-dev supertest @types/supertest`

Create the following test files:

### `src/__tests__/e2e/app.e2e.test.ts`
- `GET /health` → 200 with `{ status: 'ok' }`
- `GET /docs/openapi.json` → 200 with valid OpenAPI object
- `GET /api/anything` without API key → 401
- `GET /api/anything` with wrong API key → 401
- `GET /api/anything` with valid API key → not 401

### `src/__tests__/e2e/campaigns.e2e.test.ts`
- `POST /api/campaigns` with valid body → 201 with campaign object
- `GET /api/campaigns` → 200 with array
- `GET /api/campaigns/:id` → 200 with campaign
- `GET /api/campaigns/nonexistent` → 404
- `PATCH /api/campaigns/:id` → 200 with updated fields
- `DELETE /api/campaigns/:id` → 200 or 204

### `src/__tests__/e2e/dashboard.e2e.test.ts`
- `GET /dashboard` without session → redirect to `/login`
- `POST /login` with correct password → 200 + sets cookie
- `POST /login` with wrong password → 401
- `GET /dashboard` with valid session cookie → 200

### Setup/teardown
- Use `beforeAll` to initialize the Express app with `NODE_ENV=test` and a temp SQLite file
- Use `afterAll` to close DB connection and delete temp file
- Mock external AI calls (Genkit `ai.generate`) so tests don't hit real APIs — use `vi.mock`

Read `src/index.ts` and route files to understand the actual route paths before writing tests. Adjust test expectations to match real behavior.

Run `npm test` when done — all new E2E tests should pass, existing tests must continue passing.

## Dependencies
370 (DB indexes should be in place), 369 (CI will run these)

## Estimated Effort
L

## Acceptance Criteria
- [ ] `src/__tests__/e2e/` contains at least 3 test files
- [ ] Health endpoint E2E test passes
- [ ] Auth middleware E2E test (reject without key, accept with key) passes
- [ ] Campaign CRUD happy path E2E test passes
- [ ] Dashboard login/logout E2E test passes
- [ ] Tests use in-memory/temp SQLite, not production DB
- [ ] External AI calls are mocked (no real API calls in tests)
- [ ] All 287 existing tests continue to pass
- [ ] Total test count increases by ≥ 20 new assertions
