# TODO-882: Add lint + typecheck + test Gates to Bitbucket CI

**Repo:** signal-builder-frontend  
**Priority:** P1  
**Effort:** S (2-3 hours)  
**Status:** pending

## Problem

Bitbucket pipelines only run `yarn build`. Type errors, lint violations, and failing tests can be merged and deployed without any CI enforcement. This has already allowed broken patterns (REACT_APP_* vars, `any` types) to reach production.

## Coding Prompt

```
Update bitbucket-pipelines.yml to add quality gate steps before the build step,
for BOTH demo: and qa: pipelines:

Before "yarn build", add these steps in order:

Step: Lint
  script:
    - yarn lint

Step: Type Check  
  script:
    - yarn typecheck

Step: Unit Tests
  script:
    - yarn test --ci --coverage --coverageThreshold='{"global":{"lines":50}}'

After E2E tests are added (TODO-881), also add:
Step: E2E Tests
  script:
    - yarn test:e2e

Also update package.json scripts to ensure all commands work in CI:
  "test": "jest --passWithNoTests"  (add --passWithNoTests so empty test suites don't fail)
  "typecheck": "tsc --noEmit"       (should already exist)

Set CI=false for the build step to suppress React warnings-as-errors:
  - CI=false yarn build  (keep existing pattern)
```

## Acceptance Criteria
- [ ] `yarn lint` runs in CI before build
- [ ] `yarn typecheck` runs in CI before build  
- [ ] `yarn test --ci` runs in CI
- [ ] Pipeline fails fast on lint/type/test failures
- [ ] Both demo and qa pipelines have these gates
- [ ] Coverage report generated (even if threshold is low initially)
