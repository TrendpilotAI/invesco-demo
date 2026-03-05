# TODO-585: Add Coverage Threshold (70%) to CI

**Priority:** P1
**Repo:** signal-builder-backend
**Effort:** XS (30 min)
**Status:** Pending

## Task
Add `--cov-fail-under=70` to pytest in CI to prevent coverage regression. Currently 666 tests exist but coverage % is unknown and not enforced.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend/:

1. Open pytest.ini, add:
   [pytest]
   addopts = --cov=apps --cov-fail-under=70 --cov-report=term-missing

2. Install pytest-cov if not present: pipenv install pytest-cov --dev
3. Run: pipenv run pytest tests/ to get current baseline coverage %
4. If below 70%, lower threshold to current - 5% and create TODO to increase
5. Update bitbucket-pipelines.yml test step to report coverage
```

## Acceptance Criteria
- [ ] CI fails if coverage drops below threshold
- [ ] Coverage % is visible in CI output
- [ ] Baseline established and documented
