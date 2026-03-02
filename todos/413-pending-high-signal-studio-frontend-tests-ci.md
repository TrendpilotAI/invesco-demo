# TODO-413: Add Tests + CI/CD — Signal Studio Frontend

**Priority:** High  
**Repo:** signal-studio-frontend  
**Status:** pending  
**Effort:** M (3-4 days)

## Description

Zero test coverage. No CI/CD pipeline. Blocking production launch.

## What to Build

### 1. Unit Tests (Vitest)
```bash
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/user-event jsdom
```

Test targets:
- `src/lib/utils.ts` — `formatRelativeTime`, `cn`
- `src/lib/api/client.ts` — auth header injection, error handling, SKIP_AUTH mode
- Login/signup form validation

### 2. E2E Tests (Playwright)
```bash
npm install -D @playwright/test
npx playwright install
```

Test scenarios:
- Auth: signup → email verify → login → dashboard render
- Signals: create → view → run → delete
- Templates: browse → use template → signal created

### 3. GitHub Actions CI

`.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  lint-type-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npx vitest run
  e2e:
    runs-on: ubuntu-latest
    needs: lint-type-test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test
        env:
          NEXT_PUBLIC_SKIP_AUTH: "true"
          NEXT_PUBLIC_API_URL: http://localhost:3001/api
```

## Acceptance Criteria

- [ ] `npm test` runs Vitest unit tests
- [ ] `npm run test:e2e` runs Playwright E2E tests
- [ ] GitHub Actions passes on every PR
- [ ] Auth flow covered by E2E
- [ ] Signal CRUD covered by E2E
- [ ] `src/lib/utils.ts` at 100% unit test coverage
