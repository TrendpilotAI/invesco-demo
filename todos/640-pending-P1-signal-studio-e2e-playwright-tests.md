# TODO-640: E2E Playwright Tests for Critical User Flows

**Priority:** P1  
**Effort:** M (2 days)  
**Repo:** signal-studio  
**Category:** Testing / Quality  

## Problem

`tests/e2e/` only has `chat-rag.spec.ts` and `health-endpoints.spec.ts`. 6 critical user flows have zero automated coverage.

## Task Description

Write Playwright E2E tests for these flows and wire them to the Bitbucket CI pipeline so deploys are gated on green.

## Flows to Cover

### 1. Authentication flow
```typescript
// tests/e2e/auth.spec.ts
test('login → dashboard redirect', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[name=email]', process.env.TEST_EMAIL)
  await page.fill('[name=password]', process.env.TEST_PASSWORD)
  await page.click('[type=submit]')
  await expect(page).toHaveURL('/signal-library')
})
```

### 2. Signal library browse + run
```typescript
// tests/e2e/signal-library.spec.ts
test('browse signals and run one', async ({ page }) => {
  // login first...
  await page.goto('/signal-library')
  await expect(page.locator('[data-testid=signal-card]')).toHaveCount({ min: 1 })
  await page.locator('[data-testid=signal-card]').first().click()
  await page.click('[data-testid=run-signal-btn]')
  await expect(page.locator('[data-testid=signal-result]')).toBeVisible({ timeout: 10000 })
})
```

### 3. AI Chat streaming
```typescript
// tests/e2e/chat.spec.ts
test('chat sends message and gets streaming response', async ({ page }) => {
  await page.goto('/chat')
  await page.fill('[data-testid=chat-input]', 'What signals are available?')
  await page.keyboard.press('Enter')
  await expect(page.locator('[data-testid=chat-response]')).toBeVisible({ timeout: 15000 })
})
```

### 4. Oracle query execution
```typescript
// tests/e2e/oracle.spec.ts
test('execute oracle query and see results', async ({ page }) => {
  await page.goto('/oracle-connect')
  await page.fill('[data-testid=sql-input]', 'SELECT 1 FROM dual')
  await page.click('[data-testid=execute-btn]')
  await expect(page.locator('[data-testid=result-table]')).toBeVisible({ timeout: 10000 })
})
```

### 5. Visual builder create + connect
```typescript
// tests/e2e/visual-builder.spec.ts
test('create signal in visual builder', async ({ page }) => {
  await page.goto('/visual-builder')
  await page.dragAndDrop('[data-testid=node-palette-filter]', '[data-testid=canvas]')
  await expect(page.locator('.react-flow__node')).toHaveCount(1)
})
```

### 6. Easy Button embed
```typescript
// tests/e2e/easy-button.spec.ts
test('easy button embed renders', async ({ page }) => {
  await page.goto('/easy-button/embed')
  await expect(page.locator('[data-testid=easy-button-widget]')).toBeVisible()
})
```

## Coding Prompt (Autonomous Execution)

```
In /data/workspace/projects/signal-studio:
1. Review playwright.config.ts to understand current setup
2. Create TEST_EMAIL and TEST_PASSWORD env vars in .env.example
3. Create a shared auth helper: tests/e2e/helpers/auth.ts with login() function
4. Create the 6 spec files listed above in tests/e2e/
5. Add data-testid attributes to key elements in the app where missing
6. Update bitbucket-pipelines.yml to run `pnpm test:e2e` as a deployment gate
7. Run `pnpm test:e2e` locally to verify (use --headed for debugging)
```

## Acceptance Criteria

- [ ] 6 E2E spec files created in `tests/e2e/`
- [ ] All 6 pass locally with `pnpm test:e2e`
- [ ] Bitbucket CI runs E2E tests before Railway deploy
- [ ] Failed E2E blocks deploy
- [ ] Playwright HTML report saved as CI artifact

## Dependencies

- TODO-638 (health endpoint) should exist before writing health-check E2E
- TEST credentials stored as Railway env vars (TEST_EMAIL, TEST_PASSWORD)
