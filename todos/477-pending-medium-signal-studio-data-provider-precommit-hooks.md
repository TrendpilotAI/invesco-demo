---
id: "477"
status: pending
priority: medium
repo: signal-studio-data-provider
title: "Add .pre-commit-config.yaml with ruff + mypy"
effort: XS
dependencies: ["472"]
created: "2026-03-04"
---

## Task Description

CI has lint/type checks but no pre-commit hooks. Developers can push bad code that only fails in CI. Add pre-commit for immediate local feedback.

## Coding Prompt

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.5
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.0
          - pandas-stubs

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: debug-statements
```

Add to README.md developer setup section:
```markdown
## Development Setup

```bash
pip install pre-commit
pre-commit install
```
```

## Acceptance Criteria
- [ ] `.pre-commit-config.yaml` created
- [ ] ruff linting and formatting hooks
- [ ] mypy type check hook
- [ ] README documents `pre-commit install` setup step
- [ ] `pre-commit run --all-files` passes on current codebase
