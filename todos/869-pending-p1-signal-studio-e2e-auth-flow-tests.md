# 869 — Add E2E Auth Flow + Easy Button Tests (Playwright)

**Repo:** signal-studio  
**Priority:** P1 — High  
**Effort:** 2 days  
**Status:** pending

## Problem
Only 2 E2E specs exist (health checks and chat-rag). No tests for:
- Login/logout flow
- JWT expiry → redirect to /login
- CSRF validation
- Easy Button (core business feature)
- Signal Library browsing

## Task
Create comprehensive E2E test suites covering critical user journeys.

## Coding Prompt (for autonomous agent)
```typescript
// 1. Create /data/workspace/projects/signal-studio/tests/e2e/auth-flows.spec.ts

import { test, expect } from '@playwright/test'

test.describe('Authentication Flows', () => {
  test('redirects unauthenticated users to /login', async ({ page }) => {
    await page.goto('/signal-library')
    await expect(page).toHaveURL(/\/login/)
  })

  test('login page renders correctly', async ({ page }) => {
    await page.goto('/login')
    await expect(page.getByRole('heading', { name: /sign in/i })).toBeVisible()
  })

  test('login with invalid credentials shows error', async ({ page }) => {
    await page.goto('/login')
    await page.fill('[type="email"]', 'bad@example.com')
    await page.fill('[type="password"]', 'wrongpassword')
    await page.click('[type="submit"]')
    await expect(page.getByText(/invalid/i)).toBeVisible()
  })

  test('authenticated users can access protected pages', async ({ page, request }) => {
    // Login via API first
    const loginRes = await request.post('/api/auth/login', {
      data: { email: process.env.TEST_EMAIL, password: process.env.TEST_PASSWORD }
    })
    const { token } = await loginRes.json()
    
    // Set auth cookie
    await page.context().addCookies([{
      name: 'auth-token', value: token, domain: 'localhost', path: '/'
    }])
    
    await page.goto('/signal-library')
    await expect(page).not.toHaveURL(/\/login/)
  })

  test('API returns 401 without Authorization header', async ({ request }) => {
    const response = await request.get('/api/signals')
    expect(response.status()).toBe(401)
  })

  test('API rejects invalid CSRF token on POST', async ({ request }) => {
    const response = await request.post('/api/signals', {
      headers: {
        'Authorization': 'JWT fake-token',
        'x-csrf-token': 'invalid-token',
        // Deliberately not setting csrf-token cookie
      },
      data: { name: 'test' }
    })
    expect(response.status()).toBe(403)
  })
})

// 2. Create /data/workspace/projects/signal-studio/tests/e2e/easy-button.spec.ts

test.describe('Easy Button (Salesforce Feature)', () => {
  test.beforeEach(async ({ page }) => {
    // Set up authenticated session
    await page.goto('/easy-button')
  })

  test('loads signal templates', async ({ page }) => {
    await expect(page.getByText(/signal templates/i)).toBeVisible()
  })

  test('can select a signal template', async ({ page }) => {
    const firstTemplate = page.locator('[data-testid="signal-template"]').first()
    await firstTemplate.click()
    await expect(page.getByText(/selected/i)).toBeVisible()
  })

  test('meeting prep modal renders', async ({ page }) => {
    await page.click('[data-testid="meeting-prep"]')
    await expect(page.getByRole('dialog')).toBeVisible()
  })

  test('Salesforce embed iframe loads', async ({ page }) => {
    const embed = page.locator('[data-testid="salesforce-embed"]')
    await expect(embed).toBeVisible()
  })
})
```

Also add `tests/e2e/signal-library.spec.ts` covering browse, filter, search.

Update `bitbucket-pipelines.yml` to run Playwright after unit tests.

## Acceptance Criteria
- [ ] Auth redirect test passes
- [ ] Login error state test passes
- [ ] Authenticated access test passes
- [ ] 401 unauthenticated API test passes
- [ ] 403 CSRF mismatch test passes
- [ ] Easy Button template load test passes
- [ ] E2E tests run in CI pipeline
- [ ] All tests pass in CI

## Dependencies
- Depends on #864 (fix SKIP_AUTH) — auth tests need real auth to work
