# TODO-001: CRITICAL — Enforce Test Pass in CI

**Priority:** CRITICAL
**Status:** pending
**Category:** test_coverage, code_quality

## Problem
The CI workflow (`.github/workflows/ci.yml`) has `npm test || true`, meaning test failures are silently swallowed and broken code can be merged/deployed.

## Fix
```yaml
# Change from:
- run: npm test || true
# To:
- run: npm test
```

## Impact
Without this, the 23 test files (~3600 LOC of tests) provide zero regression protection in the automated pipeline.

## Files
- `.github/workflows/ci.yml`
