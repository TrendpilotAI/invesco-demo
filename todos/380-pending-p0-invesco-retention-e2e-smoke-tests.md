# TODO-380: E2E Smoke Tests for Invesco Demo App

**Repo:** invesco-retention
**Priority:** P0
**Effort:** M (2-3 hours)
**Status:** pending

## Description
Add Playwright E2E smoke tests for all 4 demo routes to catch regressions before demo day.

## Acceptance Criteria
- [ ] Playwright installed in demo-app
- [ ] Tests for: `/`, `/dashboard`, `/salesforce`, `/create`, `/mobile`
- [ ] Each test asserts: page loads, key UI elements visible, no console errors
- [ ] Tests run in CI (GitHub Actions)
- [ ] README updated with `npm run test:e2e`

## Coding Prompt
```
Add Playwright E2E smoke tests to /data/workspace/projects/invesco-retention/demo-app/

1. Install: npm install -D @playwright/test
2. Create playwright.config.ts at root
3. Create tests/smoke.spec.ts with tests for each route:
   - / (landing)
   - /dashboard (advisor list + signals)
   - /salesforce (Signal Studio panel, Dr. Sarah Chen loaded)
   - /create (signal creation flow)
   - /mobile (mobile brief view)
4. Each test: navigate → assert heading visible → assert no console errors
5. Add "test:e2e": "playwright test" to package.json scripts
6. Create .github/workflows/e2e.yml to run on push to main
```

## Dependencies
- None

## Notes
Critical for demo day confidence. If a code change breaks a route, we need to know before Brian Kiley sees it.
