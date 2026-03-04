# TODO-498: Wire Bitbucket CI/CD → Railway Auto-Deploy

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (3-4 hours)  
**Status:** pending

## Description
Both `bitbucket-pipelines.yml` and `railway.json` exist but may not be wired together. Implement full CI/CD: test on PR, deploy to staging on develop merge, deploy to production on main merge.

## Coding Prompt
Update `bitbucket-pipelines.yml`:

```yaml
pipelines:
  pull-requests:
    '**':
      - step:
          name: Test
          image: node:20
          caches: [node]
          script:
            - npm i -g pnpm
            - pnpm install --frozen-lockfile
            - pnpm lint
            - pnpm test:ci
            - pnpm build
  branches:
    develop:
      - step:
          name: Deploy to Staging
          script:
            - curl -X POST "$RAILWAY_STAGING_WEBHOOK"
    main:
      - step:
          name: Deploy to Production
          script:
            - curl -X POST "$RAILWAY_PRODUCTION_WEBHOOK"
```

Set Bitbucket repo variables: `RAILWAY_STAGING_WEBHOOK`, `RAILWAY_PRODUCTION_WEBHOOK` (from Railway dashboard → Deployments → Deploy Hooks).

## Acceptance Criteria
- [ ] PR opens → tests run automatically
- [ ] Merge to develop → staging deploys
- [ ] Merge to main → production deploys
