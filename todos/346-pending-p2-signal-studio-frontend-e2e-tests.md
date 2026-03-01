# TODO-346: Playwright E2E Test Suite

**Repo:** signal-studio-frontend  
**Priority:** P2  
**Effort:** M (4-6 hours)  
**Dependencies:** TODO-340, TODO-336

## Description
No tests exist. Add Playwright E2E covering critical user journeys.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Install: npm install --save-dev @playwright/test
2. npx playwright install chromium

3. Create playwright.config.ts:
   - baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000'
   - testDir: './tests/e2e'
   - Use chromium only for CI speed

4. Create tests/e2e/auth.spec.ts:
   - Test: login with valid credentials → redirected to dashboard
   - Test: login with wrong password → error message shown
   - Test: signup flow (use test+timestamp@example.com)
   - Test: forgot password → success message

5. Create tests/e2e/dashboard.spec.ts:
   - Test: authenticated user sees dashboard
   - Test: stat cards render (even if 0 values)
   - Test: quick action links navigate correctly

6. Create tests/e2e/signals.spec.ts:
   - Test: signals list page renders
   - Test: create new signal button navigates to builder
   - Test: signal builder canvas loads

7. Add to GitHub Actions CI: npx playwright test --reporter=html
```

## Acceptance Criteria
- [ ] Auth flows fully tested
- [ ] Dashboard renders tested
- [ ] Signals list tested
- [ ] Tests run in CI
- [ ] HTML report generated on failure
