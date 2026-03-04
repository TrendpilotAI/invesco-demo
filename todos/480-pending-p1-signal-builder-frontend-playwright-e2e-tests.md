# 480 — E2E Tests with Playwright for Signal Builder Frontend

**Priority:** P1  
**Repo:** signal-builder-frontend  
**Effort:** Large (3-5 days)  
**Dependencies:** None (can run against dev server)

## Task Description
The Signal Builder Frontend has 129 TSX components but only 7 test files. E2E tests are completely absent. This blocks confidence in deployments and is a major quality gap for an enterprise product.

## Coding Prompt
```
Set up Playwright E2E tests for /data/workspace/projects/signal-builder-frontend/.

1. Install Playwright:
   yarn add -D @playwright/test
   npx playwright install chromium

2. Create playwright.config.ts at project root with:
   - baseURL: http://localhost:5173
   - Test dir: e2e/
   - Screenshots on failure
   - Video on retry

3. Write the following test files in e2e/:

   auth.spec.ts — Login flow
   - Navigate to /login
   - Fill credentials, submit
   - Assert redirect to /builder or /collections
   - Assert auth token stored

   builder.spec.ts — Core builder journey
   - Login, navigate to Builder
   - Add a new signal node (drag from palette)
   - Connect two nodes
   - Configure node settings
   - Save signal
   - Assert success toast

   collections.spec.ts — Collections list
   - Login, navigate to Collections
   - Assert signals list renders
   - Filter by name
   - Click signal → assert opens in builder or preview

   preview.spec.ts — Signal preview
   - Navigate to an existing signal preview
   - Assert metrics/data renders
   - Test export button

4. Add to package.json scripts:
   "test:e2e": "playwright test"
   "test:e2e:ui": "playwright test --ui"

5. Add to bitbucket-pipelines.yml or create GitHub Actions:
   - Install deps, start dev server in background
   - Run playwright tests
   - Upload test artifacts (screenshots, videos) on failure
```

## Acceptance Criteria
- [ ] Playwright installed and configured
- [ ] At least 4 test files (auth, builder, collections, preview)
- [ ] All tests pass against dev server
- [ ] CI pipeline runs E2E tests on PRs
- [ ] Failure artifacts (screenshots) uploaded in CI
