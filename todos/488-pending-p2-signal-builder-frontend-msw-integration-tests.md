# TODO-488: MSW Integration Tests for RTK Query Endpoints

**Project:** signal-builder-frontend
**Priority:** P2 (MEDIUM impact, M effort)
**Estimated Effort:** 4-6 hours
**Dependencies:** TODO-485 (any types cleanup — need typed responses first)

## Description

RTK Query endpoints have unit-tested Redux slices but thunks and API layer are untested. Add integration tests using existing MSW v2 mocks. Cover error states (network failure, 401, 500).

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Add MSW integration tests for RTK Query API endpoints.

STEPS:
1. Read src/redux/mocks/ to understand existing MSW handlers
2. Read src/redux/builder/ and any RTK Query API definitions

3. Create test files alongside API definitions:
   src/redux/__tests__/api.integration.test.ts

4. Test pattern:
   - Set up MSW server with handlers
   - Create real Redux store with RTK Query
   - Dispatch queries/mutations
   - Assert on store state, loading states, error states

5. Test scenarios per endpoint:
   a. Success: returns correct data shape
   b. 401 Unauthorized: triggers auth error handling
   c. 500 Server Error: sets error state correctly
   d. Network failure: sets error state, retries if configured
   e. Stale-while-revalidate: cached data returned while refetching

6. Run: pnpm test -- --coverage

CONSTRAINTS:
- Use real Redux store (not mock)
- Use MSW for API mocking (already configured)
- Test the full RTK Query lifecycle (pending → fulfilled/rejected)
- Cover at least 5 API endpoints
```

## Acceptance Criteria
- [ ] ≥15 integration tests for RTK Query endpoints
- [ ] Success, 401, 500, and network error scenarios covered
- [ ] Tests use real Redux store + MSW
- [ ] All tests pass: `pnpm test`
