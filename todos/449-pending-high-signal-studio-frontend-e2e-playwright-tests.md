# TODO-449: E2E Tests — Playwright Auth + Signal CRUD Flows

**Repo:** signal-studio-frontend  
**Priority:** High  
**Effort:** M (2-3 days)  
**Status:** pending

## Description

Playwright is configured (`playwright.config.ts` exists, `playwright-report/` is empty) but zero test files exist. Add E2E tests for critical user flows: auth, signal CRUD, and chat.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/tests/:

1. Create tests/auth.spec.ts:
```typescript
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('unauthenticated user is redirected to login', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveURL(/\/login/)
  })

  test('login with valid credentials', async ({ page }) => {
    await page.goto('/login')
    await page.fill('[name="email"]', process.env.TEST_USER_EMAIL!)
    await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD!)
    await page.click('[type="submit"]')
    await expect(page).toHaveURL(/\/dashboard|\/signals/)
  })

  test('login with invalid credentials shows error', async ({ page }) => {
    await page.goto('/login')
    await page.fill('[name="email"]', 'bad@example.com')
    await page.fill('[name="password"]', 'wrongpassword')
    await page.click('[type="submit"]')
    await expect(page.getByText(/invalid|incorrect/i)).toBeVisible()
  })
})
```

2. Create tests/signals.spec.ts:
```typescript
import { test, expect } from '@playwright/test'

// Use auth fixture to pre-authenticate
test.use({ storageState: 'tests/.auth/user.json' })

test.describe('Signal CRUD', () => {
  test('signals page shows signal list', async ({ page }) => {
    await page.goto('/signals')
    await expect(page.getByRole('heading', { name: /signals/i })).toBeVisible()
  })

  test('create a new signal', async ({ page }) => {
    await page.goto('/signals/new')
    await page.fill('[name="name"]', 'Test Signal E2E')
    await page.fill('[name="description"]', 'Created by Playwright')
    await page.click('[type="submit"]')
    await expect(page.getByText('Test Signal E2E')).toBeVisible()
  })

  test('delete a signal', async ({ page }) => {
    await page.goto('/signals')
    await page.click('[data-testid="signal-menu"]')
    await page.click('text=Delete')
    await page.click('text=Confirm')
    await expect(page.getByText('Test Signal E2E')).not.toBeVisible()
  })
})
```

3. Create tests/setup/auth.setup.ts for shared auth state:
```typescript
import { test as setup } from '@playwright/test'

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[name="email"]', process.env.TEST_USER_EMAIL!)
  await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD!)
  await page.click('[type="submit"]')
  await page.waitForURL(/\/dashboard/)
  await page.context().storageState({ path: 'tests/.auth/user.json' })
})
```

4. Add .env.test with TEST_USER_EMAIL and TEST_USER_PASSWORD (use dedicated test Supabase user)
5. Add `data-testid` attributes to key interactive elements in signal components
```

## Dependencies
- TODO-445 (APIs must be wired — tests need real data)
- TODO-444 (auth middleware required for redirect tests)

## Acceptance Criteria
- [ ] Auth flow tests pass (redirect, login, error states)
- [ ] Signal list renders and shows data
- [ ] Create signal E2E flow completes successfully
- [ ] Delete signal removes from list
- [ ] Tests run in CI pipeline
