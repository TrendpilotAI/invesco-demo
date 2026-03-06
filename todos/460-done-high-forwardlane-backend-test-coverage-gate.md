# TODO-460: DONE - Add Test Coverage Gate to CI

**Completed:** 2026-03-06
**Branch:** railway-deploy
**Commit:** a8a2cdb

## What was implemented
- Added `pytest-cov = "*"` to Pipfile [dev-packages]
- Updated `pytest.ini` addopts with `--cov=. --cov-report=term-missing --cov-fail-under=50 --cov-report=xml`
- Updated `tox.ini` pytest command with same coverage flags
- Added `coverage.xml` as pipeline artifact in `bitbucket-pipelines.yml`

## Acceptance Criteria
- [x] `pytest --cov` runs in CI
- [x] Build fails if coverage drops below 50%
- [x] Coverage report artifact in CI output
