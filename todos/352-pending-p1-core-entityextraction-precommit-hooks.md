# 352 — Add Pre-commit Hooks (ruff, black, mypy, bandit)

**Repo:** core-entityextraction
**Priority:** P1 (Code Quality)
**Effort:** S (~1 hour)
**Dependencies:** 230 (dead code removed), 233 (tests exist for mypy to scan)

## Problem
No linting, formatting, or security scanning in the development workflow. Code quality depends entirely on developer discipline. Type annotation gaps and dead code can slip through undetected.

## Solution
Add `.pre-commit-config.yaml` with ruff (lint+format), mypy (types), and bandit (security).

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Create .pre-commit-config.yaml:
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
           args: [--ignore-missing-imports, --strict]
           additional_dependencies:
             - pydantic>=2.0.0
             - types-psycopg2

     - repo: https://github.com/PyCQA/bandit
       rev: 1.7.8
       hooks:
         - id: bandit
           args: [-r, ., -x, tests/]

     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.5.0
       hooks:
         - id: trailing-whitespace
         - id: end-of-file-fixer
         - id: check-yaml
         - id: check-merge-conflict
         - id: debug-statements

2. Create pyproject.toml (or ruff.toml) with ruff config:
   [tool.ruff]
   line-length = 100
   target-version = "py311"
   select = ["E", "F", "I", "N", "W", "UP"]
   ignore = ["E501"]

   [tool.mypy]
   python_version = "3.11"
   strict = true
   ignore_missing_imports = true

3. Add to requirements-dev.txt (create if not exists):
   pre-commit>=3.6.0
   ruff>=0.3.0
   mypy>=1.9.0
   bandit>=1.7.8
   types-psycopg2>=2.9.0

4. Add Makefile targets:
   lint:
       ruff check .
   format:
       ruff format .
   typecheck:
       mypy main.py persistence.py
   security:
       bandit -r . -x tests/
   hooks-install:
       pre-commit install

5. Update bitbucket-pipelines.yml or .github/workflows/ci.yml:
   Add pre-commit run --all-files step before tests.

6. Fix any ruff/mypy errors surfaced in main.py and persistence.py
   (focus on return type annotations identified in AUDIT.md).

7. Commit: "chore: add pre-commit hooks (ruff, mypy, bandit)"
```

## Dependencies
- 230 (dead Flask files removed — mypy won't scan dead code)
- 233 (tests in place — mypy can validate test files too)

## Acceptance Criteria
- [ ] `.pre-commit-config.yaml` present and valid
- [ ] `pre-commit run --all-files` passes cleanly
- [ ] `ruff check .` returns 0 errors
- [ ] `mypy main.py persistence.py` returns 0 errors
- [ ] `bandit` returns no HIGH severity findings
- [ ] CI pipeline runs pre-commit checks
- [ ] requirements-dev.txt created with dev dependencies
