---
status: pending
priority: p1
issue_id: "204"
tags: [ci-cd, bitbucket, testing, typescript, signal-builder-frontend]
dependencies: ["200", "201"]
---

# 204 — Add `typecheck` + `test` Steps to Bitbucket Pipelines

## Problem Statement

`bitbucket-pipelines.yml` runs only `CI=false yarn run build` for both QA and Demo pipelines. The `CI=false` flag suppresses TypeScript and lint warnings from failing the build. Type errors and failing unit tests do not block deployments — broken code ships to production.

## Findings

Current pipeline structure (both `qa` and `demo`):
```yaml
- step:
    name: Build
    script:
      - yarn install
      - CI=false yarn run build   # CI=false = warnings ignored!
```

No steps for:
- `yarn lint`
- `yarn typecheck`  
- `yarn test`

No `pull-requests` pipeline defined — no automated PR validation.

The `package.json` has all the scripts defined:
- `"typecheck": "tsc --noEmit"`
- `"test": "craco test"`
- `"lint": "eslint ./src --ext .ts,.tsx"`

## Proposed Solutions

### Option A: Add validation steps to existing pipelines (Recommended)
Add lint + typecheck + test steps before the build step in both QA and Demo pipelines.
- **Pros:** Immediate protection for all deployments
- **Effort:** S (~30min)
- **Risk:** Low (but will expose existing errors — fix those first)

### Option B: Add PR pipeline only
Add a separate `pull-requests` pipeline for PR validation.
- **Pros:** Doesn't affect existing deployment flow
- **Cons:** Only catches issues at PR time, not on direct pushes to develop
- **Effort:** S
- **Risk:** Low

## Recommended Action

Implement both: add a `pull-requests` pipeline for PR validation AND add typecheck+test to the existing QA/demo pipelines. Start with a `pull-requests` pipeline first (less risk), then expand to deployment pipelines once type/test issues are fixed (TODO 203, 200, 201).

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Update bitbucket-pipelines.yml to add CI quality gates

1. Add a pull-requests pipeline section at the top level:

pipelines:
  pull-requests:
    '**':
      - step:
          name: Lint & Type Check
          image: node:18.8.0
          caches:
            - node
          script:
            - yarn install --frozen-lockfile
            - yarn lint
            - yarn typecheck
      - step:
          name: Unit Tests
          image: node:18.8.0
          caches:
            - node
          script:
            - yarn install --frozen-lockfile
            - CI=true yarn test --watchAll=false --passWithNoTests
          artifacts:
            - coverage/**

2. Add a shared validation step to each existing pipeline (demo and qa), 
   BEFORE the existing Build step:

      - step:
          name: Lint & Type Check
          caches:
            - node
          script:
            - yarn install --frozen-lockfile
            - yarn lint
            - yarn typecheck
      - step:
          name: Unit Tests
          caches:
            - node
          script:
            - yarn install --frozen-lockfile
            - CI=true yarn test --watchAll=false --passWithNoTests
          artifacts:
            - coverage/**

3. In the existing Build steps, change:
   CI=false yarn run build
   to:
   yarn run build
   (Remove the CI=false flag — treat warnings as errors)
   NOTE: Only remove CI=false after TODO-203 (type fixes) is complete.
   For now, keep CI=false in build but add typecheck as a separate step.

4. Add node cache definition at the definitions level:
definitions:
  caches:
    node: node_modules

5. Verify the YAML is valid:
   cat bitbucket-pipelines.yml | python3 -c "import sys,yaml; yaml.safe_load(sys.stdin); print('YAML valid')"
```

## Dependencies

- 200 (builder.lib.ts unit tests) — tests must exist before CI can run them
- 201 (MSW integration tests) — more tests to run in CI

## Estimated Effort

**Small** — 30-60 minutes (mostly YAML editing + validation)

## Acceptance Criteria

- [ ] `bitbucket-pipelines.yml` has a `pull-requests: '**'` pipeline
- [ ] PR pipeline runs: `yarn lint`, `yarn typecheck`, `yarn test --watchAll=false`
- [ ] Both QA and Demo pipelines have lint+typecheck steps before Build
- [ ] `definitions.caches.node` is configured for node_modules caching
- [ ] YAML is valid (`python3 -c "import yaml; yaml.safe_load(open('bitbucket-pipelines.yml'))"` succeeds)
- [ ] `--passWithNoTests` flag ensures pipeline doesn't fail if test files are missing
- [ ] CI artifacts include coverage reports

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Read current bitbucket-pipelines.yml — confirmed only build step exists
- Verified package.json has typecheck, test, lint scripts
- Identified CI=false flag as a quality gate bypass
