# TODO-328: Playwright E2E Test Setup — Signal Builder Frontend

**Priority:** P1 (Medium)
**Status:** Pending
**Project:** signal-builder-frontend
**Effort:** L (1 week)
**Depends On:** Module integration tests (P1-005) ideally done first
**Source:** PLAN.md → P1-006

---

## Task Description

Set up Playwright for end-to-end testing and implement tests for the three critical production paths: full signal creation + publish flow, onboarding completion, and authentication flow.

---

## Coding Prompt

```
You are working in the Signal Builder Frontend repo at /data/workspace/projects/signal-builder-frontend.

Set up Playwright E2E testing and write tests for critical user paths.

1. Install Playwright:
   ```
   yarn add -D @playwright/test
   npx playwright install --with-deps chromium
   ```

2. Initialize Playwright config — create `playwright.config.ts` at project root:
   ```ts
   import { defineConfig, devices } from '@playwright/test';

   export default defineConfig({
     testDir: './e2e',
     fullyParallel: true,
     forbidOnly: !!process.env.CI,
     retries: process.env.CI ? 2 : 0,
     workers: process.env.CI ? 1 : undefined,
     reporter: [['html', { open: 'never' }], ['list']],
     use: {
       baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
       trace: 'on-first-retry',
       screenshot: 'only-on-failure',
     },
     projects: [
       { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
     ],
     // Start dev server before tests (optional — remove if running against staging)
     // webServer: {
     //   command: 'yarn start',
     //   port: 3000,
     //   reuseExistingServer: !process.env.CI,
     // },
   });
   ```

3. Create test helpers — `e2e/helpers/auth.ts`:
   ```ts
   import { Page } from '@playwright/test';

   export async function loginAs(page: Page, email: string, password: string) {
     await page.goto('/login');
     await page.fill('[data-testid="email-input"]', email);
     await page.fill('[data-testid="password-input"]', password);
     await page.click('[data-testid="login-button"]');
     await page.waitForURL('**/dashboard');
   }

   export async function loginAsTestUser(page: Page) {
     await loginAs(page, process.env.E2E_TEST_EMAIL!, process.env.E2E_TEST_PASSWORD!);
   }
   ```

4. Write E2E Test 1 — Authentication: `e2e/auth.spec.ts`
   ```ts
   import { test, expect } from '@playwright/test';

   test.describe('Authentication', () => {
     test('user can log in with valid credentials', async ({ page }) => {
       await page.goto('/login');
       await page.fill('[data-testid="email-input"]', process.env.E2E_TEST_EMAIL!);
       await page.fill('[data-testid="password-input"]', process.env.E2E_TEST_PASSWORD!);
       await page.click('[data-testid="login-button"]');
       await expect(page).toHaveURL(/dashboard/);
     });

     test('shows error for invalid credentials', async ({ page }) => {
       await page.goto('/login');
       await page.fill('[data-testid="email-input"]', 'wrong@example.com');
       await page.fill('[data-testid="password-input"]', 'wrongpassword');
       await page.click('[data-testid="login-button"]');
       await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
     });

     test('user can log out', async ({ page }) => {
       await loginAsTestUser(page);
       await page.click('[data-testid="user-menu"]');
       await page.click('[data-testid="logout-button"]');
       await expect(page).toHaveURL(/login/);
     });
   });
   ```

5. Write E2E Test 2 — Signal Creation: `e2e/signal-creation.spec.ts`
   ```ts
   import { test, expect } from '@playwright/test';
   import { loginAsTestUser } from './helpers/auth';

   test.describe('Signal Creation and Publish', () => {
     test.beforeEach(async ({ page }) => {
       await loginAsTestUser(page);
     });

     test('user can create and publish a signal', async ({ page }) => {
       // Navigate to builder
       await page.goto('/builder/new');
       
       // Add a node from catalog
       await page.click('[data-testid="add-node-button"]');
       await page.click('[data-testid="node-catalog-item"]:first-child');
       
       // Verify node appears on canvas
       await expect(page.locator('[data-testid="builder-node"]')).toBeVisible();
       
       // Configure the node
       await page.click('[data-testid="builder-node"]:first-child');
       await page.fill('[data-testid="node-name-input"]', 'Test Signal Node');
       
       // Publish
       await page.click('[data-testid="publish-button"]');
       await expect(page.locator('[data-testid="publish-success-toast"]')).toBeVisible();
     });
   });
   ```

6. Write E2E Test 3 — Onboarding: `e2e/onboarding.spec.ts`
   ```ts
   import { test, expect } from '@playwright/test';

   test.describe('Onboarding', () => {
     test('new user can complete onboarding', async ({ page }) => {
       // This may require a fresh test account per run — use API to create one
       // or use a dedicated test account that gets reset
       await page.goto('/onboarding');
       
       // Step 1
       await page.fill('[data-testid="company-name-input"]', 'Test Company');
       await page.click('[data-testid="next-button"]');
       
       // Step 2 — select use case
       await page.click('[data-testid="use-case-option"]:first-child');
       await page.click('[data-testid="next-button"]');
       
       // Complete onboarding
       await page.click('[data-testid="complete-onboarding-button"]');
       await expect(page).toHaveURL(/dashboard/);
     });
   });
   ```

7. Add `data-testid` attributes to components:
   - Audit the tests above and add missing `data-testid` attributes to:
     - Login form inputs and buttons
     - Builder canvas nodes, add-node button
     - Publish button and success toast
     - User menu and logout button
     - Onboarding form inputs and navigation buttons

8. Add `.env.e2e` (gitignored) for test credentials:
   ```
   E2E_BASE_URL=http://localhost:3000
   E2E_TEST_EMAIL=test@example.com
   E2E_TEST_PASSWORD=testpassword123
   ```

9. Add to `package.json`:
   ```json
   "e2e": "playwright test",
   "e2e:ui": "playwright test --ui",
   "e2e:report": "playwright show-report"
   ```

10. Update `bitbucket-pipelines.yml` to run E2E against staging deployment.

Adapt all `data-testid` values to match what actually exists in the codebase — inspect components to find real selectors before writing tests.
```

---

## Acceptance Criteria

- [ ] Playwright installed and `playwright.config.ts` created
- [ ] `e2e/` directory with at least 3 spec files (auth, signal-creation, onboarding)
- [ ] `data-testid` attributes added to all elements referenced in tests
- [ ] All 3 E2E test suites pass against local dev server
- [ ] Test helpers (`e2e/helpers/auth.ts`) extracted for reuse
- [ ] `.env.e2e` documented (template committed, actual credentials gitignored)
- [ ] `yarn e2e` script in `package.json`
- [ ] CI pipeline updated to run E2E tests against staging
- [ ] Playwright HTML report generated on CI failures
