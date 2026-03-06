# TODO-461: DONE - Add Pre-commit Hooks (ruff + black + bandit)

**Completed:** 2026-03-06
**Branch:** railway-deploy
**Commit:** a8a2cdb

## What was implemented
- Created `.pre-commit-config.yaml` with hooks: ruff, ruff-format, black, bandit, trailing-whitespace, end-of-file-fixer, check-yaml, debug-statements
- Added `pre-commit = "*"` to Pipfile [dev-packages]
- Added "Development Setup" section to README.md with `pre-commit install` instructions

## Acceptance Criteria
- [x] `.pre-commit-config.yaml` in repo root
- [x] README documents setup step
