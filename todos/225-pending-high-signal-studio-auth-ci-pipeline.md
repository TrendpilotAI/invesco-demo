# TODO-225: GitHub Actions CI Pipeline (signal-studio-auth)

**Priority:** HIGH  
**Repo:** signal-studio-auth  
**Status:** pending  

## Description
No CI pipeline. Regressions can be merged without test failures being caught.

## Task
Add `.github/workflows/ci.yml` with lint + type check + pytest.

## Coding Prompt
```
Create /data/workspace/projects/signal-studio-auth/.github/workflows/ci.yml:

name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install deps
        run: pip install -r requirements.txt ruff mypy
      
      - name: Lint
        run: ruff check .
      
      - name: Type check
        run: mypy middleware/ routes/ config/ mapping/ --ignore-missing-imports
      
      - name: Test
        env:
          SUPABASE_JWT_SECRET: test-secret-at-least-32-chars-long!!
          SUPABASE_URL: http://localhost:54321
          AUTH_MODE: dual
        run: pytest tests/ -v --tb=short

Also create .pre-commit-config.yaml:
  repos:
    - repo: https://github.com/astral-sh/ruff-pre-commit
      rev: v0.3.0
      hooks:
        - id: ruff
          args: [--fix]
    - repo: https://github.com/pre-commit/pre-commit-hooks
      rev: v4.5.0
      hooks:
        - id: trailing-whitespace
        - id: end-of-file-fixer
```

## Estimated Effort
S (1-2 hours)

## Acceptance Criteria
- CI runs on every PR
- Lint, type check, and tests all pass
- Badge in README shows CI status
