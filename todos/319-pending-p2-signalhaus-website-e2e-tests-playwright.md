# TODO 319: SignalHaus Website — E2E Tests with Playwright

**Priority:** P2 (Quality)
**Effort:** M (4-8 hours)
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Description
Zero tests exist. Adding Playwright E2E tests ensures critical user journeys don't break on deploys.

## Acceptance Criteria
- [ ] Playwright installed and configured
- [ ] Tests run in CI (GitHub Actions)
- [ ] Test: Homepage loads with correct H1
- [ ] Test: Navigation links work (all pages return 200)
- [ ] Test: Contact form shows validation errors on empty submit
- [ ] Test: Contact form success path (mock Resend API)
- [ ] Test: Pricing page shows all 3 tiers
- [ ] Test: Blog page lists posts

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/:

1. Install Playwright:
   npm install -D @playwright/test
   npx playwright install --with-deps chromium

2. Create playwright.config.ts:
   - baseURL: http://localhost:3000
   - webServer: { command: "npm run dev", url: "http://localhost:3000", reuseExistingServer: true }
   - testDir: ./tests/e2e

3. Create tests/e2e/homepage.spec.ts:
   - test("homepage loads"): navigate to /, expect h1 to contain "Pragmatic AI"
   - test("CTA links work"): click "Book a Free Consultation", expect URL to be /contact
   - test("navigation works"): click each nav item, verify correct page loads

4. Create tests/e2e/contact.spec.ts:
   - test("form validation"): submit empty form, expect error messages
   - test("form success"): fill valid data, mock /api/contact to return 200, verify success message

5. Create tests/e2e/pages.spec.ts:
   - test.each(["/", "/about", "/services", "/pricing", "/blog", "/contact"])
   - Each page should return 200 and have correct <title>

6. Add to package.json scripts:
   "test:e2e": "playwright test"

7. Update .github/workflows/ci.yml to add Playwright test step
```

## Dependencies
None (can run against local dev server)
