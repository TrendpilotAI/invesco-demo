# TODO-227: GitHub Actions CI Pipeline

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (2-4 hours)  
**Status:** pending

## Problem
No CI/CD exists. PRs merge without linting, type checking, or tests.

## Acceptance Criteria
- Every PR triggers: ESLint, TypeScript check, Jest tests
- Failures block merge
- Build verification on PRs targeting main

## Coding Prompt

```
Create .github/workflows/ci.yml:

name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

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
      - run: npm test -- --ci --coverage
      - run: npm run build
        env:
          NEXT_PUBLIC_API_URL: http://localhost:3001/api
          NEXT_PUBLIC_SUPABASE_URL: https://placeholder.supabase.co
          NEXT_PUBLIC_SUPABASE_ANON_KEY: placeholder

Also add eslint config if not present:
- Install eslint-config-next (likely already there with Next.js)
- Add .eslintrc.json: { "extends": "next/core-web-vitals" }
```

## Dependencies
- TODO-226 (Jest tests must exist for test step to be meaningful)
