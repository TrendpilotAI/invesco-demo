# TODO-614: Playwright E2E Tests

**Repo:** signalhaus-website  
**Priority:** P2  
**Effort:** M (4-6 hours)  
**Status:** pending

## Description
Zero tests currently. Add Playwright E2E for critical user journeys.

## Test Suites to Create
1. **Contact form** — fill form, submit, see success message
2. **ROI Calculator** — enter values, see calculated results
3. **Blog navigation** — listing page loads, click post, content renders
4. **Navigation** — all nav links route to correct pages
5. **404 page** — invalid URL shows not-found page

## Coding Prompt
```bash
npm install -D @playwright/test
npx playwright install
```

Create `tests/contact.spec.ts`:
```ts
import { test, expect } from '@playwright/test'

test('contact form submits successfully', async ({ page }) => {
  await page.goto('/contact')
  await page.fill('[name="name"]', 'Test User')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="message"]', 'This is a test message for E2E testing')
  await page.click('button[type="submit"]')
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible()
})
```

Add `playwright.config.ts` and `npm run test:e2e` script.
Add to CI workflow.

## Acceptance Criteria
- [ ] Contact form test passes
- [ ] ROI calculator test passes  
- [ ] Blog navigation test passes
- [ ] Tests run in CI on PRs
- [ ] Mocked API responses for form submission

## Dependencies
- TODO-611 (CI pipeline)
