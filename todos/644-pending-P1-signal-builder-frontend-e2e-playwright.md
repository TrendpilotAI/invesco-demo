# TODO-644: Add Playwright E2E Tests for Signal Builder Frontend

**Repo:** signal-builder-frontend  
**Priority:** P1  
**Effort:** Medium (3-4 days)  
**Category:** Testing

## Description
Zero E2E test coverage. Critical user flows are untested: auth, builder canvas, signal save, catalog browsing. MSW is already installed for API mocking.

## Task
Set up Playwright E2E test suite covering:
1. Auth flow (login → redirect to collections)
2. Collections page (browse, open signal)
3. Builder canvas (open, add node, connect, save)
4. Catalog page (browse, filter, preview)

## Coding Prompt
```
In /data/workspace/projects/signal-builder-frontend/:
1. Install: yarn add -D @playwright/test
2. Create playwright.config.ts at root
3. Create e2e/ directory with:
   - e2e/auth.spec.ts — login flow
   - e2e/collections.spec.ts — browse, open
   - e2e/builder.spec.ts — canvas interactions
   - e2e/catalog.spec.ts — browse, filter
4. Use MSW to mock API responses
5. Add 'test:e2e' script to package.json: 'playwright test'
6. Add E2E step to bitbucket-pipelines.yml
```

## Acceptance Criteria
- [ ] Playwright installed and configured
- [ ] 4 spec files covering critical flows
- [ ] Tests pass against local dev server
- [ ] CI pipeline runs E2E on PR

## Dependencies
None
