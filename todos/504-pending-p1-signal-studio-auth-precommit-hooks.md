# TODO-504: Pre-commit Hooks Setup

**Priority:** P1  
**Effort:** XS (~1h)  
**Repo:** signal-studio-auth  
**Status:** pending

## Description
No pre-commit hooks exist. Devs can push unformatted, type-unsafe, or secret-containing code.

## .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: detect-private-key
      - id: check-yaml
```

## Acceptance Criteria
- [ ] `.pre-commit-config.yaml` in repo root
- [ ] `pre-commit install` documented in README
- [ ] CI runs `pre-commit run --all-files`
