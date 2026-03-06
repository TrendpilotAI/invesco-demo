# 811 — Add Pre-commit Hooks (ruff, mypy)

**Repo:** signal-studio-auth  
**Priority:** P2  
**Effort:** S (30 mins)  
**Dependencies:** none

## Acceptance Criteria

- [ ] `.pre-commit-config.yaml` with ruff lint + format, mypy
- [ ] `Makefile` with `make lint`, `make test`, `make check` targets
- [ ] Instructions in README for setting up pre-commit

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-auth/.pre-commit-config.yaml:

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]

Create Makefile:
lint:
    ruff check . && mypy routes/ middleware/ config/ mapping/ models.py --ignore-missing-imports
test:
    pytest tests/ -v
check: lint test

Add to README: "Run `pip install pre-commit && pre-commit install` to enable hooks."
```
