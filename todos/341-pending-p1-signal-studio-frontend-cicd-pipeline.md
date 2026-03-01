# TODO-341: CI/CD GitHub Actions Pipeline

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (1-2 hours)  
**Dependencies:** none

## Description
No CI/CD exists. Add GitHub Actions for lint, type-check, and build on every PR and push to main.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Create .github/workflows/ci.yml:
   - Trigger: push to main, PRs
   - Job: lint-and-build
     - uses: actions/checkout@v4
     - uses: actions/setup-node@v4 with node 22
     - npm ci
     - npm run lint
     - npx tsc --noEmit
     - npm run build
   - Cache: node_modules via actions/cache

2. Create .github/workflows/preview.yml (Vercel preview deploys):
   - Trigger: pull_request
   - Use: vercel/action or amondnet/vercel-action
   - Comment PR with preview URL

3. Add .eslintrc.json if missing (extends next/core-web-vitals)

4. Add lint-staged + husky for pre-commit:
   - npm install --save-dev husky lint-staged
   - Configure in package.json: "lint-staged": {"*.{ts,tsx}": ["eslint --fix", "prettier --write"]}
```

## Acceptance Criteria
- [ ] CI runs on every PR
- [ ] Build fails on TypeScript errors
- [ ] Build fails on ESLint errors
- [ ] Pre-commit hooks prevent committing broken code
