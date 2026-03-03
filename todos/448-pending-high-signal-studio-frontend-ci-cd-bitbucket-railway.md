# TODO-448: CI/CD Pipeline — Bitbucket Pipelines + Railway Deploy

**Repo:** signal-studio-frontend  
**Priority:** High  
**Effort:** M (1 day)  
**Status:** pending

## Description

No CI/CD exists. PRs are merged without lint, type check, or test verification. Railway deployments are manual. Set up Bitbucket Pipelines for automated testing and deploy.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/:

1. Create/update bitbucket-pipelines.yml:

```yaml
image: node:20-alpine

definitions:
  caches:
    npm: ~/.npm
  steps:
    - step: &lint-typecheck
        name: Lint + Type Check
        caches: [npm]
        script:
          - npm ci
          - npm run lint
          - npx tsc --noEmit
    - step: &unit-tests
        name: Unit Tests
        caches: [npm]
        script:
          - npm ci
          - npm run test:ci
    - step: &build
        name: Build
        caches: [npm]
        script:
          - npm ci
          - npm run build

pipelines:
  pull-requests:
    '**':
      - parallel:
          - step: *lint-typecheck
          - step: *unit-tests
      - step: *build

  branches:
    main:
      - parallel:
          - step: *lint-typecheck
          - step: *unit-tests
      - step: *build
      - step:
          name: Deploy to Railway Production
          deployment: production
          script:
            - npm install -g @railway/cli
            - railway up --service signal-studio-frontend
          environment:
            RAILWAY_TOKEN: $RAILWAY_TOKEN
```

2. Create prettier.config.js:
```javascript
module.exports = {
  semi: false,
  singleQuote: true,
  tabWidth: 2,
  trailingComma: 'es5',
  printWidth: 100,
}
```

3. Set up husky pre-commit:
```bash
npm install -D husky lint-staged
npx husky init
echo 'npx lint-staged' > .husky/pre-commit
```

4. Add lint-staged config to package.json:
```json
"lint-staged": {
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md}": ["prettier --write"]
}
```

5. Add RAILWAY_TOKEN to Bitbucket repository variables (Settings → Repository Variables)
```

## Acceptance Criteria
- [ ] PRs trigger automatic lint + type check + test run
- [ ] Failed lint/tests block PR merge
- [ ] Merge to main triggers Railway production deploy
- [ ] Prettier formats code consistently on commit
