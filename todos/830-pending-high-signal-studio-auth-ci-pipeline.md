# TODO-830: Add GitHub Actions CI Pipeline to signal-studio-auth

**Repo:** signal-studio-auth  
**Priority:** P1 (High)  
**Effort:** 1 hour  
**Status:** pending

## Task
Create `.github/workflows/ci.yml` with:
- Lint: `ruff check .`
- Type check: `mypy .`  
- Test: `pytest --cov=. --cov-report=xml`
- Security: `bandit -r .` + `pip-audit`
- Trigger: push/PR to main

Also add `.pre-commit-config.yaml` and `pyproject.toml` with ruff + mypy config.

## Acceptance Criteria
- [ ] CI passes on clean repo
- [ ] Coverage report uploaded to codecov or PR comment
- [ ] Security scan fails on known CVE packages
