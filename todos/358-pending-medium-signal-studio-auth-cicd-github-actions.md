# TODO 358 — Add CI/CD GitHub Actions Pipeline
**Repo:** signal-studio-auth
**Priority:** MEDIUM
**Effort:** 2 hours
**Status:** pending
**Depends on:** 357

## Description
No CI/CD pipeline. PRs can merge broken code. Need automated test + lint + security scan.

## Coding Prompt
Create `/data/workspace/projects/signal-studio-auth/.github/workflows/test.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      
      - name: Install dependencies
        run: pip install -r requirements.txt ruff mypy bandit pytest-cov
      
      - name: Lint (ruff)
        run: ruff check .
      
      - name: Type check (mypy)
        run: mypy . --ignore-missing-imports --no-strict-optional
      
      - name: Security scan (bandit)
        run: bandit -r . -ll --exclude ./tests
      
      - name: Run tests with coverage
        env:
          SUPABASE_JWT_SECRET: "test-secret-at-least-32-chars-long!!"
          SUPABASE_URL: "http://localhost:54321"
          AUTH_MODE: "dual"
        run: pytest tests/ -v --cov=. --cov-report=xml --cov-fail-under=70
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
```

Also create `pyproject.toml`:
```toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "W", "I", "N", "UP"]

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

## Acceptance Criteria
- [ ] GitHub Actions workflow runs on push and PR
- [ ] Lint (ruff), type check (mypy), security scan (bandit) all pass
- [ ] Tests run with coverage report
- [ ] Pipeline blocks merge on test failure
- [ ] pyproject.toml configures all tools consistently
