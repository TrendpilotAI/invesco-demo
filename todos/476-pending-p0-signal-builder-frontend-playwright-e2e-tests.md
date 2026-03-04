# TODO-476: Playwright E2E Tests for Critical Flows

**Project:** signal-builder-frontend
**Priority:** P0 (HIGH impact, M effort)
**Estimated Effort:** 6-8 hours
**Dependencies:** None (MSW already configured)

## Description

Zero E2E tests exist. Add Playwright test suite covering critical user flows: authentication, signal creation (add filter nodes, connect edges), publish, and preview. Use existing MSW v2 mocks for API responses.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Set up Playwright E2E test suite with critical flow coverage.

STEPS:
1. Install Playwright:
   pnpm add -D @playwright/test
   npx playwright install chromium

2. Create playwright.config.ts:
   - baseURL: 'http://localhost:3000'
   - webServer: { command: 'pnpm dev', port: 3000, reuseExistingServer: true }
   - Use chromium only (speed)
   - Screenshot on failure

3. Create e2e/ directory with tests:

   e2e/auth.spec.ts:
   - Test login flow (navigate to login, enter credentials, verify redirect to builder)
   - Test unauthenticated redirect (hit /builder without token, verify redirect to login)

   e2e/signal-builder.spec.ts:
   - Test create new signal (click "New Signal", verify canvas loads)
   - Test add filter node (drag from palette or click add, verify node appears on canvas)
   - Test configure filter (click node, verify right sidebar opens with FilterContent)
   - Test connect nodes (verify edge creation between nodes)
   - Test publish signal (click publish, verify modal, confirm, verify success notification)

   e2e/catalog.spec.ts:
   - Test signal list loads (verify table renders with mock data)
   - Test search/filter (type in search, verify filtered results)
   - Test navigate to builder from catalog (click signal, verify builder opens)

   e2e/preview.spec.ts:
   - Test signal preview renders (navigate to preview page, verify data table)

4. Create e2e/fixtures/ directory with MSW handlers for E2E (reuse from src/redux/mocks/ if available)

5. Add scripts to package.json:
   "e2e": "playwright test",
   "e2e:ui": "playwright test --ui"

6. Run: pnpm e2e — verify all tests pass

CONSTRAINTS:
- Use data-testid attributes where needed (add to components minimally)
- MSW or Playwright route mocking for API calls
- Tests must be deterministic (no flaky waits — use Playwright auto-waiting)
- Each test file should be independent (no shared state between files)
```

## Acceptance Criteria
- [ ] Playwright configured with chromium
- [ ] ≥10 E2E tests covering auth, builder, catalog, preview flows
- [ ] All tests pass against dev server with mocked API
- [ ] Screenshots captured on failure
- [ ] `pnpm e2e` script works
- [ ] No hardcoded waits/sleeps in tests
