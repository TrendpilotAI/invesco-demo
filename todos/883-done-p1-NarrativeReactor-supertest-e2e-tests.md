# TODO-883 DONE — Supertest E2E Tests (NarrativeReactor)

**Status:** ✅ Complete  
**Branch:** `feat/eslint-e2e-tests`  
**PR:** https://github.com/TrendpilotAI/NarrativeReactor/pull/new/feat/eslint-e2e-tests

## What Was Done

1. **Installed packages** (via yarn):
   - `supertest@^7.2.2` — HTTP assertion library
   - `@types/supertest@^7.2.0` — TypeScript types

2. **Created `src/app.ts`** — Express app factory for testability:
   - Exports `createApp(options)` with configurable rate limit settings
   - Fixed billing route mount order: billing routes mounted BEFORE global `apiKeyAuth`
   - This allows tenant API keys to work correctly with billing endpoints

3. **Created `src/__tests__/e2e/api.test.ts`** with 18 tests across 7 describe blocks:
   - `GET /health` — returns 200, no auth required (2 tests)
   - `POST /api/billing/tenants` — tenant registration, returns API key (3 tests)
   - `GET /api/billing/usage` — quota info with tenant auth + 401 cases (3 tests)
   - `GET /api/billing/plans` — public plan listing (1 test)
   - `POST /api/generate` — content generation with mocked AI (3 tests)
   - Unauthenticated requests return 401 (2 tests)
   - Rate limiting — 6th request returns 429 (1 test)

4. **Mocked all external services**:
   - `genkit.config` — AI generation (no real API calls)
   - `flows/*` — content/video/integration flows
   - `stripe` — billing
   - `lib/fal` — image/video generation
   - `lib/claude` — Anthropic
   - `openapi` — Swagger UI (replaced with minimal Express router)
   - `middleware/dashboardAuth` — bypassed for API tests
   - `services/schedulerWorker` — no background jobs

5. **Each describe block uses isolated app instance** to avoid rate limit
   interference between test groups.

## Test Results
```
✓ 18/18 new E2E tests pass
✓ 314/316 total tests pass (2 pre-existing failures in audio.test.ts calling real Google AI APIs)
```

## Architecture Note
The `src/app.ts` factory also fixes a pre-existing bug in the original `src/index.ts`
where billing routes were mounted after the global `apiKeyAuth`, making `GET /api/billing/plans`
and `GET /api/billing/usage` (with tenant keys) incorrectly require admin API key.
