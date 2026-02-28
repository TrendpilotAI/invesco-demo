# TODO-320: GitHub Actions CI Pipeline — Signal Studio Frontend

**Priority:** P0  
**Repo:** signal-studio-frontend  
**Effort:** S (2h)  
**Status:** pending  

## Description
Set up GitHub Actions CI pipeline for signal-studio-frontend. Currently no automated checks exist — PRs can merge broken TypeScript or lint errors.

## Task
Create `.github/workflows/ci.yml` that runs on every push and PR to main/develop:
1. Checkout code
2. Setup Node 22
3. `npm ci` (with node_modules cache)
4. `npm run lint`
5. `npx tsc --noEmit`
6. `npm run build`

Also add Husky + lint-staged for pre-commit:
- ESLint on staged `.ts/.tsx` files
- Prettier format check

## Coding Prompt (Autonomous Agent)
```
In repo /data/workspace/projects/signal-studio-frontend:

1. Create .github/workflows/ci.yml:
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm run build

2. Install husky and lint-staged: npm install --save-dev husky lint-staged
3. Add to package.json:
   "lint-staged": { "*.{ts,tsx}": ["eslint --fix", "prettier --write"] }
4. Run: npx husky init
5. Create .husky/pre-commit with: npx lint-staged
```

## Dependencies
- None

## Acceptance Criteria
- [ ] `.github/workflows/ci.yml` exists and is valid YAML
- [ ] CI passes on a clean build
- [ ] Pre-commit hook prevents committing lint errors
