# TODO #843 — Second-Opinion: Playwright E2E Test Suite

**Priority:** P1  
**Effort:** M (3 days)  
**Repo:** /data/workspace/projects/Second-Opinion/  
**Created:** 2026-03-08 by Judge Agent v2

## Task Description

Add automated Playwright E2E tests for the critical medical analysis flow. Several one-off e2e-test.ts scripts exist but are not integrated into CI.

## Implementation

### Setup
```bash
# playwright already in devDependencies
npx playwright install chromium

# Create tests/ directory structure
mkdir -p tests/e2e
```

### Test Files to Create

**tests/e2e/auth.spec.ts** — Auth flow
```typescript
test('user can sign up and verify email', async ({ page }) => {
  await page.goto('/');
  await page.click('[data-testid="sign-up-btn"]');
  // ...
});
```

**tests/e2e/analysis.spec.ts** — Core analysis flow
```typescript
test('user can upload file and get analysis', async ({ page }) => {
  // Login with test account
  await loginAsTestUser(page);
  // Upload test medical document
  await page.setInputFiles('[data-testid="file-upload"]', 'tests/fixtures/test-report.pdf');
  // Wait for analysis pipeline
  await page.waitForSelector('[data-testid="analysis-result"]', { timeout: 30000 });
  // Assert key elements present
  await expect(page.locator('[data-testid="confidence-score"]')).toBeVisible();
});
```

**tests/e2e/demo.spec.ts** — Guided demo flow (no auth required)
- Navigate guided demo steps
- Assert all 4 stages complete successfully

### CI Integration
Add to .github/workflows/ (or existing CI):
```yaml
- name: E2E Tests
  run: npx playwright test tests/e2e/
  env:
    TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
    TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
```

### Acceptance Criteria
- [ ] Auth flow E2E test passes
- [ ] Analysis flow E2E test passes (with mock/demo mode)
- [ ] Guided demo E2E test passes
- [ ] Tests run in CI on every PR
- [ ] Test artifacts (screenshots, videos) uploaded on failure

## Dependencies
- None for demo flow tests
- Test Firebase project needed for auth flow tests
