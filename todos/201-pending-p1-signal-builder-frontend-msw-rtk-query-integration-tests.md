---
status: pending
priority: p1
issue_id: "201"
tags: [testing, msw, rtk-query, redux, signal-builder-frontend]
dependencies: ["200"]
---

# 201 — MSW Integration Tests for RTK Query Endpoints

## Problem Statement

MSW (Mock Service Worker v2.1.5) is installed and has a service worker file at `public/mockServiceWorker.js`, but is only used in `src/modules/onboarding/api/onboarding.api.mock.ts`. The entire builder API layer (`src/redux/builder/api.ts`) has no integration tests. This means API contract regressions go undetected until QA or production.

## Findings

- `package.json` has `msw: ^2.1.5` installed
- `public/mockServiceWorker.js` exists (proper MSW v2 setup)
- `src/setupTests.ts` exists but has no MSW setup
- `src/redux/builder/api.ts` exports 17 RTK Query hooks with no tests
- Error handlers in `api.ts` have `// TODO:` comments and use `console.log` / `console.error`
- `createSignal` uses `console.log(error)` (not even `console.error`) in its catch block

## Proposed Solutions

### Option A: MSW v2 + RTK Query test utilities (Recommended)
Use MSW server for Node.js + `@reduxjs/toolkit`'s `setupListeners` + Testing Library wrappers.
- **Pros:** Tests the full Redux → RTK Query → MSW → Response → Redux cycle
- **Cons:** Requires Redux store setup in tests
- **Effort:** M (~5-8h)
- **Risk:** Low

### Option B: Mock `axios` directly
Mock the axios instance used by RTK Query.
- **Pros:** Simpler setup
- **Cons:** Doesn't test the RTK Query layer, brittle
- **Effort:** S
- **Risk:** High (tests too implementation-specific)

## Recommended Action

Implement Option A. This aligns with the existing MSW infrastructure and tests the real integration contract.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Create MSW integration tests for src/redux/builder/api.ts

1. Set up MSW server in src/setupTests.ts:
   import { setupServer } from 'msw/node';
   export const server = setupServer();
   beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
   afterEach(() => server.resetHandlers());
   afterAll(() => server.close());

2. Create src/redux/builder/api.test.ts

3. Create a test Redux store helper:
   import { configureStore } from '@reduxjs/toolkit';
   import { Api } from '../api';
   import { builderReducer } from './slice';
   const createTestStore = () => configureStore({
     reducer: { builder: builderReducer, [Api.reducerPath]: Api.reducer },
     middleware: (getDefault) => getDefault().concat(Api.middleware),
   });

4. Write the following test cases using MSW handlers:

describe('getSchema endpoint', () => {
  it('fetches schema and dispatches setSchema to Redux store')
  it('handles 500 error without crashing (error goes to console.error, not unhandled rejection)')
  it('falls back to mockSchema when response is empty/null')
})

describe('createSignal endpoint', () => {
  it('creates a signal and dispatches createNewTab to Redux store')
  it('handles 400 error gracefully')
})

describe('getSignals endpoint', () => {
  it('passes page_number, collection, page_count as query params')
  it('returns TSignalsResponse typed data')
})

describe('publishSignal endpoint', () => {
  it('sends POST to correct URL with column data')
  it('handles 403 forbidden error')
})

describe('getSignalResult endpoint', () => {
  it('passes id, page_number, page_count to API')
})

5. Use http.get / http.post from 'msw' for handlers
6. Import API_PATHS from '@shared/config' for endpoint URLs
7. Run: cd /data/workspace/projects/signal-builder-frontend && yarn test src/redux/builder/api.test.ts --watchAll=false
8. All tests must pass with 0 failures
```

## Dependencies

- 200 (unit tests for builder.lib.ts) — establishes test patterns; not a hard blocker

## Estimated Effort

**Medium** — 5-8 hours

## Acceptance Criteria

- [ ] `src/redux/builder/api.test.ts` exists
- [ ] MSW server is configured in `src/setupTests.ts`
- [ ] Tests cover: `getSchema`, `createSignal`, `getSignals`, `publishSignal`, `getSignalResult`
- [ ] Both success and error paths are tested for each endpoint
- [ ] `yarn test src/redux/builder/api.test.ts --watchAll=false` passes with 0 failures
- [ ] Redux store integration is verified (dispatched actions reach the reducer)
- [ ] No direct axios mocking — MSW intercepts at the network level

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Verified MSW v2 is installed and public/mockServiceWorker.js exists
- Identified 17 untested RTK Query hooks in builder/api.ts
- Found console.log (not even console.error) in createSignal error handler — a bug to fix alongside tests
