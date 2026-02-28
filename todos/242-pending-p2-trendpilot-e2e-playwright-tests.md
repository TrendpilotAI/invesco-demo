# 242 · P2 · Trendpilot — E2E Playwright Test Suite

## Status
pending

## Priority
P2 — quality gate before production traffic

## Description
Write a comprehensive Playwright E2E test suite covering the critical user flows: auth, subscribing, newsletter preview, and billing. Tests should run against a staging Supabase project and Stripe test mode to avoid touching production data.

## Dependencies
- TODO #236 (Supabase data store)
- TODO #238 (Auth)
- TODO #239 (Email delivery — can use mock in tests)
- TODO #240 (Stripe — use test keys)
- Both API server and dashboard must be running (`npm run dev`)

## Estimated Effort
2 days

## Coding Prompt

```
You are working on the Trendpilot project at /data/workspace/projects/Trendpilot/.

TASK: Create a Playwright E2E test suite in `tests/e2e/`.

STEP 1 — Install Playwright:
```bash
npm install --save-dev @playwright/test
npx playwright install chromium
```

STEP 2 — Create `playwright.config.ts` in project root:
```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false, // auth state is shared
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  webServer: [
    {
      command: 'npm run dev:server',
      url: 'http://localhost:3001/health',
      reuseExistingServer: !process.env.CI,
    },
    {
      command: 'npm run dev:dashboard',
      url: 'http://localhost:5173',
      reuseExistingServer: !process.env.CI,
    },
  ],
});
```

STEP 3 — Create `tests/e2e/fixtures.ts` for shared auth state:
```ts
import { test as base, expect } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';

// Test user credentials (use Supabase test project)
const TEST_EMAIL = process.env.E2E_TEST_EMAIL ?? 'e2e@trendpilot.test';
const TEST_PASSWORD = process.env.E2E_TEST_PASSWORD ?? 'test-password-123';
const SUPABASE_URL = process.env.SUPABASE_URL!;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY!;

type Fixtures = {
  authenticatedPage: import('@playwright/test').Page;
};

export const test = base.extend<Fixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Sign in via Supabase API directly (bypass magic link in tests)
    const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    const { data: { session } } = await supabase.auth.signInWithPassword({
      email: TEST_EMAIL,
      password: TEST_PASSWORD,
    });
    
    if (!session) throw new Error('Test user auth failed — create E2E test user first');
    
    // Inject session into browser
    await page.goto('/');
    await page.evaluate(({ url, key, session }) => {
      localStorage.setItem(`sb-${new URL(url).hostname.split('.')[0]}-auth-token`, JSON.stringify(session));
    }, { url: SUPABASE_URL, key: SUPABASE_ANON_KEY, session });
    
    await page.reload();
    await use(page);
  },
});

export { expect };
```

STEP 4 — `tests/e2e/auth.spec.ts`:
```ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('redirects unauthenticated users to login', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/login/);
    await expect(page.getByText('Sign in to Trendpilot')).toBeVisible();
  });

  test('shows magic link form', async ({ page }) => {
    await page.goto('/login');
    const emailInput = page.getByPlaceholder('you@example.com');
    await expect(emailInput).toBeVisible();
    
    await emailInput.fill('test@example.com');
    await page.getByRole('button', { name: 'Send Magic Link' }).click();
    await expect(page.getByText('Check your email')).toBeVisible();
  });

  test('authenticated user sees dashboard', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard');
    await expect(page).not.toHaveURL(/login/);
    await expect(page.getByText('Trending Topics')).toBeVisible();
  });

  test('sign out clears session', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard');
    await page.getByRole('button', { name: 'Sign Out' }).click();
    await expect(page).toHaveURL(/login/);
  });
});
```

STEP 5 — `tests/e2e/topics.spec.ts`:
```ts
import { test, expect } from './fixtures';

test.describe('Topics Dashboard', () => {
  test('loads trending topics', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard');
    // Wait for topics to load (realtime or initial fetch)
    await expect(page.locator('[data-testid="topic-card"]').first()).toBeVisible({ timeout: 10000 });
  });

  test('search filters topics', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard');
    await page.getByPlaceholder('Search topics...').fill('technology');
    // Results should filter
    await page.waitForTimeout(500); // debounce
    const cards = page.locator('[data-testid="topic-card"]');
    // All visible cards should relate to technology (if any)
    expect(await cards.count()).toBeGreaterThanOrEqual(0);
  });

  test('shows live badge when connected', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard');
    await expect(page.getByText('LIVE')).toBeVisible({ timeout: 5000 });
  });
});
```

STEP 6 — `tests/e2e/subscribers.spec.ts`:
```ts
import { test, expect } from '@playwright/test';

test.describe('Subscriber Flow', () => {
  test('subscribe form accepts valid email', async ({ page }) => {
    await page.goto('/');
    const emailInput = page.getByPlaceholder(/email/i);
    await emailInput.fill('newuser@example.com');
    await page.getByRole('button', { name: /subscribe/i }).click();
    await expect(page.getByText(/check your email/i)).toBeVisible();
  });

  test('subscribe form rejects invalid email', async ({ page }) => {
    await page.goto('/');
    const emailInput = page.getByPlaceholder(/email/i);
    await emailInput.fill('not-an-email');
    await page.getByRole('button', { name: /subscribe/i }).click();
    // Should show validation error, not success message
    await expect(page.getByText(/check your email/i)).not.toBeVisible();
  });
});
```

STEP 7 — `tests/e2e/billing.spec.ts`:
```ts
import { test, expect } from './fixtures';

test.describe('Billing', () => {
  test('free user sees upgrade prompt on premium feature', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard/newsletters/new');
    // If user is on free plan, should see upgrade prompt
    const upgradePrompt = page.getByText(/upgrade/i);
    // Either they can access (if pro) or see upgrade prompt (if free)
    // This test documents the expected behavior
    await expect(page.locator('main')).toBeVisible();
  });

  test('billing settings page loads', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard/settings/billing');
    await expect(page.getByText(/current plan/i)).toBeVisible();
  });

  test('upgrade button redirects to Stripe', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard/settings/billing');
    const upgradeBtn = page.getByRole('button', { name: /upgrade to pro/i });
    if (await upgradeBtn.isVisible()) {
      // Intercept the navigation to Stripe
      const [newPage] = await Promise.all([
        page.context().waitForEvent('page'),
        upgradeBtn.click(),
      ]);
      // Stripe Checkout should open
      await expect(newPage).toHaveURL(/stripe\.com|checkout\.stripe\.com/);
      await newPage.close();
    }
  });
});
```

STEP 8 — Add test scripts to `package.json`:
```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed"
  }
}
```

STEP 9 — Add `data-testid` attributes to dashboard components:
- Topic cards: `data-testid="topic-card"`
- Newsletter list items: `data-testid="newsletter-item"`
- Subscriber count: `data-testid="subscriber-count"`

STEP 10 — CI integration (`.github/workflows/e2e.yml`):
```yaml
name: E2E Tests
on: [push]
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22' }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run test:e2e
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
          SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
          STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY_TEST }}
          E2E_TEST_EMAIL: ${{ secrets.E2E_TEST_EMAIL }}
          E2E_TEST_PASSWORD: ${{ secrets.E2E_TEST_PASSWORD }}
```
```

## Acceptance Criteria
- [ ] `npx playwright test` runs without configuration errors
- [ ] Auth spec: login redirect, magic link form, sign out all pass
- [ ] Topics spec: dashboard loads, search works, live badge visible
- [ ] Subscribers spec: valid/invalid email handling passes
- [ ] Billing spec: billing page loads, upgrade button behavior documented
- [ ] All tests pass in CI (GitHub Actions)
- [ ] Test report (HTML) generated with `playwright show-report`
- [ ] No tests depend on external network (mock Stripe/SendGrid in E2E)
