# TODO-835: Complete CI/CD Pipeline

**Repo**: signal-studio-frontend  
**Priority**: P1  
**Effort**: M (2-3 days)  
**Status**: pending

## Description
bitbucket-pipelines.yml exists but is incomplete. No PR gates, no automated tests in CI, no deploy automation.

## Coding Prompt
```
Update bitbucket-pipelines.yml:

image: node:20

definitions:
  caches:
    pnpm: ~/.pnpm-store

pipelines:
  pull-requests:
    '**':
      - step:
          name: Type Check & Lint
          caches: [pnpm]
          script:
            - npm install -g pnpm
            - pnpm install --frozen-lockfile
            - pnpm tsc --noEmit
            - pnpm lint
      - step:
          name: Unit Tests
          caches: [pnpm]
          script:
            - pnpm install --frozen-lockfile
            - pnpm test:ci
  branches:
    main:
      - step:
          name: Build & Deploy
          caches: [pnpm]
          script:
            - pnpm install --frozen-lockfile
            - pnpm build
            - curl -fsSL https://railway.app/install.sh | sh
            - railway up --detach
          deployment: production

Also add to package.json:
  "typecheck": "tsc --noEmit",
  "ci": "pnpm lint && pnpm typecheck && pnpm test:ci"

Also add pnpm audit to PR pipeline to catch CVEs.
```

## Acceptance Criteria
- PRs blocked if type-check fails
- PRs blocked if unit tests fail
- main branch auto-deploys to Railway on merge
- Pipeline completes in under 5 minutes
