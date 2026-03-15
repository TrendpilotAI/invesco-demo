# TODO-007: MEDIUM — Wire Up E2E Tests in CI

**Priority:** MEDIUM
**Status:** pending
**Category:** test_coverage

## Problem
E2E test files exist (`e2e-test.ts`, `e2e-test-v2.ts`, `production-test.ts`, `comprehensive-test.ts`) but aren't integrated into the CI pipeline. Playwright is a devDependency but no CI job runs E2E tests.

## Tasks
- Create a CI workflow for E2E tests (or add to existing ci.yml)
- Configure Playwright to run against a preview/staging deploy
- Add E2E test for the core analysis pipeline flow

## Files
- `.github/workflows/ci.yml`
- `e2e-test.ts`, `e2e-test-v2.ts`
