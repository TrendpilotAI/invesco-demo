# TODO-881: Add Playwright E2E Tests for Critical Builder Flows

**Repo:** signal-builder-frontend  
**Priority:** P1 (High)  
**Effort:** M (2-3 days)  
**Status:** pending

## Problem

No E2E tests exist. The critical builder flow (create signal → add nodes → connect → publish) has zero automated coverage. Regressions discovered only after client-facing deployments.

## Implementation Plan

### Setup
```bash
yarn add -D @playwright/test
npx playwright install chromium
```

Create `playwright.config.ts` at repo root:
```ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './e2e',
  webServer: {
    command: 'yarn dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:3000',
    // Inject auth cookie for authenticated tests
    storageState: 'e2e/auth.json',
  },
});
```

### Test Files to Create

**e2e/auth.setup.ts** — auth state setup (run once before test suite)
```ts
// Use page.route() to mock auth API
// Set cookie via page.context().addCookies()
// Save to 'e2e/auth.json'
```

**e2e/builder.spec.ts** — builder CRUD flow
```
Test 1: Create new signal
  - Navigate to /builder
  - Click "New Signal"
  - Enter name and description
  - Assert: redirected to builder canvas

Test 2: Add dataset node
  - On empty canvas, click "Add Node" or drag from sidebar
  - Select "Dataset" node type
  - Configure dataset name
  - Assert: node appears on canvas

Test 3: Add filter node and connect
  - Add Filter node
  - Draw edge from Dataset → Filter
  - Configure filter rule (field + operator + value)
  - Assert: edge visible, filter form saves

Test 4: Validate and publish signal
  - Click "Validate"
  - Assert: no validation errors shown
  - Click "Publish"
  - Assert: success toast, signal status = published
```

**e2e/collections.spec.ts** — collections CRUD
**e2e/catalog.spec.ts** — signal catalog browsing

### Bitbucket Pipeline Integration
Add to `bitbucket-pipelines.yml`:
```yaml
- step:
    name: E2E Tests
    script:
      - yarn install
      - npx playwright install-deps chromium
      - yarn test:e2e
    artifacts:
      - playwright-report/**
```

Add to `package.json` scripts:
```json
"test:e2e": "playwright test"
```

## Acceptance Criteria
- [ ] Playwright installed and configured
- [ ] Auth setup test runs and saves state
- [ ] Builder create+add+connect+publish flow passes
- [ ] Collections CRUD flow passes
- [ ] Tests run in Bitbucket CI on PR
- [ ] Playwright report artifact saved on failure
- [ ] Tests use `page.route()` mocking — no real backend needed in CI
