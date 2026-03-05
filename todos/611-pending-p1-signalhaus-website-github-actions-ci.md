# TODO-611: GitHub Actions CI Pipeline

**Repo:** signalhaus-website  
**Priority:** P1  
**Effort:** S (2 hours)  
**Status:** pending

## Description
No CI pipeline. Every PR merges without build verification. Add GitHub Actions to run build + type check on every PR.

## Tasks
1. Create `.github/workflows/ci.yml`
2. Run on: push to main, PRs to main
3. Steps: checkout, setup Node 20, npm ci, npm run build, tsc --noEmit

## Coding Prompt
Create `.github/workflows/ci.yml`:
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - run: npx tsc --noEmit
```

## Acceptance Criteria
- [ ] CI runs on every PR
- [ ] Build failures block merge
- [ ] Type errors block merge
- [ ] Badge in README

## Dependencies
- GitHub repo must be connected
