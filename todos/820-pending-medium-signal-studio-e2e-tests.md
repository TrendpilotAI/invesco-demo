# TODO-820: Add Playwright E2E tests for critical flows

**Priority**: MEDIUM (P2)
**Repo**: signal-studio
**Source**: BRAINSTORM.md → 3.2, AUDIT.md → AUDIT-011

## Description
Playwright is configured but the playwright-report directory is empty and no E2E test specs exist. Add tests for the most critical user flows.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Create tests/e2e/login.spec.ts:
   - Navigate to /login
   - Fill in valid credentials (from env: E2E_USERNAME, E2E_PASSWORD)
   - Verify redirect to dashboard
   - Verify JWT token set in storage

2. Create tests/e2e/signal-library.spec.ts:
   - Login first (use shared auth fixture)
   - Navigate to /signal-library
   - Verify signals load (wait for signal cards to appear)
   - Test search/filter functionality
   - Test drag-and-drop reordering

3. Create tests/e2e/easy-button.spec.ts:
   - Navigate to /easy-button
   - Verify client list loads
   - Select a client → verify meeting prep modal opens
   - Verify signal results display

4. Create tests/e2e/oracle-query.spec.ts:
   - Login
   - Navigate to /oracle-connect
   - Test connection health check
   - Browse tables
   - Run a simple SELECT query
   - Verify results display

5. Create tests/e2e/fixtures/auth.ts:
   Shared login fixture that logs in once per test suite (session reuse).

6. Add to bitbucket-pipelines.yml for staging branch:
   - pnpm test:e2e (runs against STAGING_BASE_URL)
   Add env: E2E_BASE_URL, E2E_USERNAME, E2E_PASSWORD to CI secrets.
```

## Acceptance Criteria
- [ ] All 4 E2E spec files exist and pass
- [ ] E2E tests run in CI against staging environment
- [ ] Auth fixture enables session reuse across tests
- [ ] Tests are stable (no flakiness on retry)

## Effort
1 week

## Dependencies
TODO-2.3 Staging environment (tests run against staging)
