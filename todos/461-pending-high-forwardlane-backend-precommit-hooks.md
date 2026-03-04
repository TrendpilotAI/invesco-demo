# TODO-461: Add Pre-commit Hooks (ruff + black + bandit)

**Priority:** HIGH  
**Repo:** forwardlane-backend  
**Effort:** XS (1 hour)  
**Dependencies:** None

## Description
No pre-commit hooks exist. Add `ruff` (fast Python linter), `black` (formatter), and `bandit` (security scanner) to catch issues before they hit CI.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Create .pre-commit-config.yaml:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: [-r, ., -x, tests]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: debug-statements
```

2. Add to Pipfile [dev-packages]:
   pre-commit = "*"

3. Run: pre-commit install (document in README)
4. Run: pre-commit run --all-files (fix violations)
5. Add to README.md: "Run `pre-commit install` after cloning"
6. Commit: "dev: add pre-commit hooks (ruff, black, bandit)"
```

## Acceptance Criteria
- [ ] `.pre-commit-config.yaml` in repo root
- [ ] `pre-commit run --all-files` passes
- [ ] README documents setup step
