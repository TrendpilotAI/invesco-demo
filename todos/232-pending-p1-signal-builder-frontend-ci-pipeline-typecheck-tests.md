# 232 · P1 · signal-builder-frontend · Add TypeCheck + Tests to CI Pipeline

## Status
pending

## Priority
P1 — CI currently runs `CI=false yarn build` only; broken TypeScript and failing tests ship undetected

## Description
`bitbucket-pipelines.yml` only runs a build step with `CI=false` (warnings suppressed). Type errors and test failures don't block deployments. This task adds lint, typecheck, test, and PR validation pipeline steps.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Read the current bitbucket-pipelines.yml to understand its structure

Step 2: Update bitbucket-pipelines.yml

Add a reusable validation step group and PR pipeline:

```yaml
definitions:
  steps:
    - step: &validate
        name: Lint & Type Check
        image: node:18
        caches:
          - node
        script:
          - yarn install --frozen-lockfile
          - yarn lint --max-warnings=0
          - yarn typecheck
    - step: &test
        name: Unit Tests
        image: node:18
        caches:
          - node
        script:
          - yarn install --frozen-lockfile
          - CI=true yarn test --coverage --watchAll=false --passWithNoTests
        artifacts:
          - coverage/**
    - step: &security
        name: Security Audit
        image: node:18
        caches:
          - node
        script:
          - yarn install --frozen-lockfile
          - yarn audit --level high || true   # Report but don't fail yet (too many existing)
          - if [ "$REACT_APP_IS_DEV_AUTH_METHOD" = "true" ]; then echo "ERROR: Dev auth in pipeline!"; exit 1; fi

pipelines:
  pull-requests:
    '**':
      - step: *validate
      - step: *test
  
  branches:
    develop:
      - step: *validate
      - step: *test
      - step: *security
      # Then existing QA deploy steps...
```

Step 3: Fix `CI=false` in existing build steps
Change existing build steps from `CI=false yarn run build` to `CI=true yarn run build`
(After fixing lint warnings that were previously suppressed)

Step 4: Add `typecheck` script to package.json if it doesn't exist:
```json
"scripts": {
  "typecheck": "tsc --noEmit"
}
```

Step 5: Fix any immediate lint errors that would block CI
Run `yarn lint` locally and fix all errors (not warnings). 
Common quick fixes:
- Remove unused imports flagged by ESLint
- Fix `@typescript-eslint/no-unused-vars` violations
- Address any critical errors (not just warnings)

Commit: "ci: add typecheck, test, and security steps to Bitbucket pipelines"
```

## Dependencies
- None, but coordinate with TODO 229 (any types) and 231 (tests) to ensure they don't cause immediate CI failures

## Effort Estimate
S (4–6 hours)

## Acceptance Criteria
- [ ] PR pipeline runs on all pull requests with lint + typecheck + tests
- [ ] `develop` branch pipeline includes security audit
- [ ] `package.json` has `typecheck` script
- [ ] `CI=false` removed from build steps (or justified with a comment)
- [ ] Pipeline runs successfully on a test branch
- [ ] No broken deploy pipelines (QA/Demo still work)
