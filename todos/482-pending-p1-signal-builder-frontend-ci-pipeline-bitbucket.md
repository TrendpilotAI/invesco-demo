# TODO-482: Add Full CI Pipeline to bitbucket-pipelines.yml

**Project:** signal-builder-frontend
**Priority:** P1 (HIGH impact, S effort)
**Estimated Effort:** 2-3 hours
**Dependencies:** TODO-476 (Playwright E2E tests)

## Description

Currently CI only runs lint + typecheck. Add jest unit tests and Playwright E2E tests. Block merge on failures.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Expand CI pipeline to include tests.

STEPS:
1. Read bitbucket-pipelines.yml (or create if missing)

2. Create/update pipeline with stages:
   pipelines:
     default:
       - parallel:
         - step:
             name: Lint
             caches: [node]
             script:
               - pnpm install --frozen-lockfile
               - pnpm lint
         - step:
             name: Type Check
             caches: [node]
             script:
               - pnpm install --frozen-lockfile
               - pnpm typecheck
         - step:
             name: Unit Tests
             caches: [node]
             script:
               - pnpm install --frozen-lockfile
               - pnpm test -- --coverage --ci
         - step:
             name: E2E Tests
             caches: [node]
             script:
               - pnpm install --frozen-lockfile
               - npx playwright install chromium --with-deps
               - pnpm build
               - pnpm e2e
             artifacts:
               - test-results/**

     pull-requests:
       '**':
         - parallel:
           # same steps as above

3. Run: validate pipeline YAML syntax
4. Commit and push to verify pipeline triggers

CONSTRAINTS:
- Use pnpm (not npm)
- Parallel steps where possible for speed
- E2E artifacts saved on failure for debugging
- Block merge on any failure
```

## Acceptance Criteria
- [ ] bitbucket-pipelines.yml has lint + typecheck + unit test + e2e steps
- [ ] Steps run in parallel where independent
- [ ] PR builds block merge on failure
- [ ] E2E test artifacts captured
