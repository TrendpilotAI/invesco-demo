# TODO-500: E2E Playwright Test Suite — Critical Flows

**Repo:** signal-studio-frontend  
**Priority:** P2  
**Effort:** M (1-2 days)  
**Status:** pending

## Description
`playwright.config.ts` exists but E2E test coverage for critical user flows is unknown/minimal. Add tests for the flows that matter most.

## Coding Prompt
Create `tests/e2e/` directory with:

1. **`tests/e2e/auth.spec.ts`**: Login flow
   - Navigate to `/login`
   - Fill credentials
   - Assert redirect to dashboard
   - Assert middleware protects `/signal-library` when not logged in

2. **`tests/e2e/signal-library.spec.ts`**: 
   - Browse signals page loads
   - Filter by collection
   - Drag-and-drop reorder
   - Search signals

3. **`tests/e2e/ai-chat.spec.ts`**:
   - Chat page loads
   - Send message
   - Assert streaming response appears
   - Assert no JS errors in console

4. **`tests/e2e/oracle-connect.spec.ts`** (skip if no test Oracle):
   - Connection form renders
   - Error state when invalid credentials
   - Table list appears on valid connection
   - SQL preview works

5. **`tests/e2e/visual-builder.spec.ts`**:
   - Builder page loads
   - Can add a node
   - Can connect nodes
   - Save/export works

Add to `bitbucket-pipelines.yml` as separate step after unit tests.

## Acceptance Criteria
- [ ] `pnpm test:e2e` runs without failures in headless mode
- [ ] All 5 test files created with passing tests
- [ ] CI pipeline runs E2E on PR
