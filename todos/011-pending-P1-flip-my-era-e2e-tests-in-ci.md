---
status: pending
priority: P1
issue_id: "011"
tags: [flip-my-era, playwright, e2e, ci, github-actions]
dependencies: []
---

# 011 — Add E2E Tests to GitHub Actions CI

## Overview

FlipMyEra has 10 Playwright E2E spec files in `e2e/` (smoke, auth, navigation, landing, wizard-flow, plans, ux-quality, performance, accessibility, auth-flow) and a fully configured `playwright.config.ts`. However, the GitHub Actions CI workflow (`.github/workflows/ci.yml`) runs only lint, typecheck, unit tests, and build — Playwright is completely skipped.

**Why P1:** E2E tests are the last line of defense before a deployment breaks the live user journey (sign up → story creation → ebook generation → checkout). Without them in CI, regressions can ship to production. The config already exists — this is purely a wiring task.

## Coding Prompt

You are working on FlipMyEra, a React 18 + TypeScript + Vite SaaS app at `/data/workspace/projects/flip-my-era/`.

**Task:** Add Playwright E2E tests to the GitHub Actions CI pipeline.

### Step 1 — Audit existing e2e tests

Read the test files in `e2e/` to understand what they do and what env vars they need:
- `e2e/smoke.spec.ts` — basic page load checks
- `e2e/auth.spec.ts` and `e2e/auth-flow.spec.ts` — login/signup flows
- `e2e/wizard-flow.spec.ts` — story creation wizard
- `e2e/landing.spec.ts` — landing page checks

Note: Tests that test authenticated flows (`auth.spec.ts`, `wizard-flow.spec.ts`) will need a test user. Tests that only check public pages (landing, navigation, smoke) can run without credentials.

### Step 2 — Update CI workflow

File: `.github/workflows/ci.yml`

Add a new job `e2e` that runs after the `ci` job succeeds:

```yaml
e2e:
  name: E2E Tests
  runs-on: ubuntu-latest
  needs: ci
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 22
        cache: npm
    - run: npm ci
    - name: Install Playwright browsers
      run: npx playwright install --with-deps chromium
    - name: Run E2E tests (public pages only)
      run: npx playwright test e2e/smoke.spec.ts e2e/landing.spec.ts e2e/navigation.spec.ts e2e/plans.spec.ts
      env:
        VITE_SUPABASE_URL: ${{ secrets.VITE_SUPABASE_URL }}
        VITE_SUPABASE_ANON_KEY: ${{ secrets.VITE_SUPABASE_ANON_KEY }}
    - name: Upload test artifacts on failure
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: playwright-report
        path: playwright-report/
        retention-days: 7
```

**Important:** Only run the public-page specs in CI (smoke, landing, navigation, plans). The auth/wizard specs need real Supabase credentials and a seeded test user — skip those for now or mark them with `test.skip` if no test env is configured. Document what would be needed to enable the auth tests (test user credentials as GitHub secrets).

### Step 3 — Fix any failing public-page tests

Run `npx playwright test e2e/smoke.spec.ts e2e/landing.spec.ts` locally (or note what would need to run). Review each test and fix any that:
- Reference deprecated selectors
- Assume Clerk auth (app migrated to Supabase — check for any `clerk` references in e2e tests and update)
- Have hardcoded timeouts that are too short

### Step 4 — Add playwright to package.json scripts

In `package.json`, ensure these scripts exist:
```json
"test:e2e": "playwright test",
"test:e2e:ui": "playwright test --ui",
"test:e2e:public": "playwright test e2e/smoke.spec.ts e2e/landing.spec.ts e2e/navigation.spec.ts e2e/plans.spec.ts"
```

### Step 5 — Document auth test requirements

Create `e2e/README.md` explaining:
- Which tests run in CI (public-page tests)
- What GitHub Secrets are needed for auth tests
- How to run locally with auth

## Dependencies

None — can be done independently.

## Effort

S (3-5 hours)

## Acceptance Criteria

- [ ] `.github/workflows/ci.yml` has an `e2e` job
- [ ] CI runs at minimum smoke + landing + navigation tests on every push to main/PR
- [ ] No Clerk references in e2e tests (all use Supabase auth patterns)
- [ ] Playwright artifacts (screenshots, traces) uploaded on failure
- [ ] `e2e/README.md` documents how to run locally and what's needed for full auth tests
- [ ] CI pipeline passes on main branch
