# 802 — Add GitHub Actions CI/CD Pipeline

**Repo:** signal-studio-auth  
**Priority:** P0  
**Effort:** M (half day)  
**Dependencies:** 803 (Docker), 806 (dep pinning)

## Problem

No CI/CD pipeline. PRs are merged without automated lint/test validation. No automated deployment.

## Acceptance Criteria

- [ ] `.github/workflows/ci.yml` — runs on every PR: ruff lint, mypy type check, pytest
- [ ] `.github/workflows/deploy.yml` — deploys to Railway on merge to main
- [ ] Tests run with Redis mock (no real Redis needed in CI)
- [ ] CI fails on lint errors or test failures

## Coding Prompt

```
Create .github/workflows/ci.yml:

name: CI
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy routes/ middleware/ config/ mapping/ models.py --ignore-missing-imports
  
  test:
    runs-on: ubuntu-latest
    services:
      redis:
        image: redis:7
        ports: ["6379:6379"]
    env:
      REDIS_URL: redis://localhost:6379
      SUPABASE_URL: https://placeholder.supabase.co
      SUPABASE_SERVICE_KEY: placeholder-key
      SUPABASE_JWT_SECRET: placeholder-secret-32-chars-min!!
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --tb=short

Also create .github/workflows/deploy.yml with Railway deploy on push to main.
Reference: https://docs.railway.app/guides/github-actions
```
