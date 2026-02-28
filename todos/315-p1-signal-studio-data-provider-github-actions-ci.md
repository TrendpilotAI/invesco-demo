# TODO 315 — Add GitHub Actions CI Pipeline

**Priority:** P1 🟠  
**Repo:** signal-studio-data-provider  
**Effort:** S (1-2 hours)  
**Status:** pending

---

## Description

No CI pipeline exists. Add GitHub Actions with pytest, ruff, mypy, and pip-audit.

---

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-data-provider/.github/workflows/ci.yml:

name: CI

on:
  push:
    branches: [main, develop]
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
          cache: pip
      - run: pip install -e ".[dev]"
      - run: pip install ruff mypy pip-audit
      - name: Lint
        run: ruff check .
      - name: Type check
        run: mypy . --ignore-missing-imports
      - name: Security audit
        run: pip-audit
      - name: Tests
        run: pytest tests/ -v --tb=short
      - name: Coverage
        run: pip install pytest-cov && pytest tests/ --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v4
        if: always()

Also add pyproject.toml configuration:
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = false
ignore_missing_imports = true
```

---

## Dependencies

- TODO 312 (async fix), TODO 311 (JWT fix) — tests should be green before CI

## Acceptance Criteria

- [ ] CI file created at .github/workflows/ci.yml
- [ ] Pipeline runs on push and PR
- [ ] All checks pass on main branch
- [ ] Coverage report uploaded to codecov
