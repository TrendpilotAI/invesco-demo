# TODO-715: E2E Test Suite (Playwright)

**Repo**: signal-studio-frontend  
**Priority**: P1  
**Effort**: M (2-3 days)  
**Status**: pending

## Description
Add Playwright E2E tests for critical user flows. Playwright is already configured.

## Coding Prompt
```
Create Playwright E2E tests for signal-studio-frontend. Playwright is already configured in playwright.config.ts.

Create test files:

1. e2e/auth.spec.ts
   - Test: Unauthenticated user visiting /signals is redirected to /login
   - Test: Login with valid credentials → redirected to /signals
   - Test: Login with invalid credentials → shows error message
   - Test: Logged-in user can access all protected routes
   - Test: Logout clears session and redirects to /login

2. e2e/signals.spec.ts
   - Test: Signal library page loads and displays signal cards
   - Test: Filter signals by category
   - Test: Search signals by name
   - Test: Click signal card shows detail view

3. e2e/chat.spec.ts
   - Test: AI chat page loads with empty state
   - Test: User sends message, receives AI response
   - Test: Chat history persists within session

4. e2e/oracle-connect.spec.ts
   - Test: Oracle connect page loads
   - Test: Connection test with invalid credentials shows error
   - (Skip actual Oracle connection in CI — use env flag)

Use page.getByRole(), page.getByTestId() for selectors.
Add data-testid attributes to key elements in the React components as needed.
Use test.use({ storageState: 'e2e/.auth/user.json' }) for pre-authenticated tests.
```

## Acceptance Criteria
- [ ] `npm run test:e2e` passes all tests against local dev server
- [ ] Auth flow fully covered
- [ ] Signal library browse covered
- [ ] Tests run in CI (except Oracle integration tests)
