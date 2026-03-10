# TODO-887: Add Tests + Coverage Gate to CI Pipeline

**Repo:** signal-studio-frontend  
**Priority:** P0  
**Effort:** S (1-2 hours)  
**Status:** pending  
**Identified:** 2026-03-10 by Judge Agent v2

## Problem

`bitbucket-pipelines.yml` runs only `pnpm lint` and `pnpm build`. 
**Tests never run in CI.** This means:
- Auth bypass (32 routes) would not be caught by CI
- Regressions in oracle-service, chat-service, vector-service not auto-detected
- No coverage gate — coverage can drop to 0% silently

## Coding Prompt

```
Update /data/workspace/projects/signal-studio-frontend/bitbucket-pipelines.yml to add:

1. Test step with coverage:
  - step:
      name: Test
      caches:
        - node
      script:
        - pnpm install --frozen-lockfile
        - pnpm test:ci
      services:
        - docker  # if Oracle mocking needed

2. Security audit step:
  - step:
      name: Security Audit
      script:
        - pnpm audit --audit-level=high
        # Fail if any HIGH or CRITICAL CVEs found

3. Playwright smoke tests (after build):
  - step:
      name: E2E Smoke Tests
      script:
        - pnpm exec playwright install --with-deps chromium
        - pnpm exec playwright test --project=chromium tests/smoke/

Also update jest.config.js to raise the global threshold:
  coverageThreshold: {
    global: {
      branches: 60,
      functions: 65,
      lines: 70,
      statements: 70
    }
  }
```

## Acceptance Criteria
- [ ] `bitbucket-pipelines.yml` has lint + build + test steps in sequence
- [ ] `pnpm audit` step fails pipeline on HIGH CVEs
- [ ] Jest coverage threshold raised from 10% to 60%/70%
- [ ] Pipeline turns red if tests fail

## Notes
- The Oracle unit tests in `__tests__/lib/` may require mocking — jest.setup.js already has some Oracle mocking
- Run `pnpm test:ci` locally first to verify it passes before adding to CI
