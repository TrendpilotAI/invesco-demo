# TODO-714: Complete CI/CD Pipeline + Pre-commit Hooks

**Repo**: signal-studio-frontend  
**Priority**: P1  
**Effort**: S (< 1 day)  
**Status**: pending

## Description
Set up pre-commit hooks and verify/complete the Bitbucket CI pipeline.

## Coding Prompt
```
Set up development workflow tooling for signal-studio-frontend:

1. Install and configure Husky + lint-staged:
   npm install --save-dev husky lint-staged
   npx husky init
   
   .husky/pre-commit should run:
   - npx lint-staged
   - npm run typecheck (tsc --noEmit)

   package.json lint-staged config:
   "*.{ts,tsx}": ["eslint --fix", "prettier --write"]
   "*.{json,md,css}": ["prettier --write"]

2. Update bitbucket-pipelines.yml to include:
   - Step: Install (npm ci)
   - Step: Lint (npm run lint)
   - Step: TypeCheck (npx tsc --noEmit)
   - Step: Unit Tests (npm run test:ci)
   - Step: Build (npm run build)
   Fail fast: each step depends on previous.

3. Add to package.json:
   "typecheck": "tsc --noEmit"

4. Separate test pipelines:
   - "test:unit" runs tests that don't need Oracle (use jest --testPathIgnorePatterns)
   - CI runs test:unit only (integration tests need Oracle connection)
```

## Acceptance Criteria
- [ ] `git commit` triggers pre-commit hooks
- [ ] Bitbucket pipeline runs lint + typecheck + unit tests on every PR
- [ ] Build step validates Next.js compiles successfully
