# TODO 571 — GitHub Actions CI Pipeline

**Priority:** HIGH  
**Repo:** Ultrafone  
**Effort:** 4 hours  
**Status:** pending

## Description
No CI pipeline exists. Need automated checks on every PR/push.

## Coding Prompt
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install ruff mypy pytest pytest-asyncio httpx
      - run: pip install -r backend/requirements.txt
      - run: ruff check backend/
      - run: mypy backend/ --ignore-missing-imports
      - run: pytest backend/tests/ -x

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: cd frontend && bun install
      - run: cd frontend && bun run lint
      - run: cd frontend && bun run build

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Acceptance Criteria
- [ ] CI runs on every push and PR
- [ ] Backend: ruff lint + pytest pass
- [ ] Frontend: lint + build pass
- [ ] gitleaks secret scanning enabled
- [ ] Badge in README

## Dependencies
- TODO 568 (secrets removed from repo)
