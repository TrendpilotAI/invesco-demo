# Complete CI/CD Pipeline (Tests + Auto-Deploy)

**Repo:** signal-studio-frontend  
**Priority:** P0  
**Effort:** M (3-4 hours)

## Description
`bitbucket-pipelines.yml` only runs lint + build. No tests, no E2E, no deploy. This means broken code can merge and there's no production deployment path.

## Coding Prompt
```
Update /data/workspace/projects/signal-studio-frontend/bitbucket-pipelines.yml:

1. Change image to node:20 with pnpm (or use node:20 + install pnpm)
2. Pull-request pipeline: lint → build → test
3. Main branch pipeline: lint → build → test → deploy to Vercel

Use this structure:
pipelines:
  pull-requests:
    '**':
      - step:
          name: Lint
          script:
            - npm install -g pnpm
            - pnpm install --frozen-lockfile
            - pnpm lint
      - step:
          name: Build & Test
          script:
            - npm install -g pnpm
            - pnpm install --frozen-lockfile
            - pnpm build
            - pnpm test:ci
  branches:
    main:
      - step:
          name: Build & Test
          script:
            - npm install -g pnpm
            - pnpm install --frozen-lockfile
            - pnpm build
            - pnpm test:ci
      - step:
          name: Deploy to Vercel
          deployment: production
          script:
            - npm install -g vercel
            - vercel --prod --token $VERCEL_TOKEN

Also add pnpm audit --audit-level=high to fail on HIGH severity CVEs.

Commit: "ci: add test step and Vercel auto-deploy to pipeline"
```

## Acceptance Criteria
- [ ] CI runs tests on every PR
- [ ] Main branch auto-deploys to Vercel on green
- [ ] `pnpm audit` fails on HIGH CVEs

## Dependencies
- 853 (auth fixes should pass before CI gate active)
