# FL-024: Raise Test Coverage Gate from 50% to 75%

**Repo:** forwardlane-backend  
**Priority:** P1  
**Effort:** L (4-5 days)  
**Status:** pending

## Task Description
Raise pytest coverage gate from 50% to 75%, adding tests focused on the highest-risk, lowest-coverage modules: `pipeline_engine/`, `ai/`, `client_ranking/tasks.py`, and `adapters/`.

## Problem
50% coverage gate is too low for enterprise financial software. Key business logic (pipeline engine ETL, Celery tasks, LLM flows) has unknown/low coverage. Without adequate test coverage, we can't safely refactor or deploy with confidence.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

STEP 1 — Discover coverage gaps:
Run: pytest --cov=. --cov-report=term-missing --cov-fail-under=0 --no-header -q 2>/dev/null | grep -E "^[a-z].*%" | sort -t% -k1 -n | head -50

Focus on modules with < 50% coverage.

STEP 2 — Add tests for pipeline_engine/ (highest risk):
- pipeline_engine/config_loader.py — test loading from env and file
- pipeline_engine/executor.py (or similar) — test pipeline step execution with mocked steps
- pipeline_engine/validators.py — test validation rules

STEP 3 — Add tests for client_ranking/tasks.py:
```python
import pytest
from celery.contrib.pytest import celery_app, celery_worker

@pytest.mark.celery(task_always_eager=True)
def test_ranking_task_executes(client_ranking_fixture):
    from client_ranking.tasks import update_client_rankings
    result = update_client_rankings.delay(client_id=client_ranking_fixture.id)
    assert result.successful()
```

STEP 4 — Add tests for adapters/octane/:
- Test data transformation functions
- Test error handling on malformed input
- Mock external API calls

STEP 5 — Add Celery task tests for content_ingestion:
- Test ingestion pipeline with fixture data
- Test error handling and retry logic

STEP 6 — Update coverage configuration:
In pytest.ini:
  Change: --cov-fail-under=50
  To:     --cov-fail-under=75

In tox.ini:
  Change: --cov-fail-under=50
  To:     --cov-fail-under=75

STEP 7 — Add coverage report to CI:
In bitbucket-pipelines.yml, add after test step:
  - coverage xml
  - coverage report --skip-covered

Files to create/modify:
- pipeline_engine/tests/ (create new test files)
- client_ranking/tests/test_tasks.py (new)
- adapters/tests/test_octane.py (new/expand)
- content_ingestion/tests/ (expand)
- pytest.ini (update threshold)
- tox.ini (update threshold)
```

## Acceptance Criteria
- [ ] `pytest --cov-fail-under=75` passes in CI
- [ ] `pipeline_engine/` coverage ≥ 70%
- [ ] `ai/` coverage ≥ 65%
- [ ] `client_ranking/tasks.py` coverage ≥ 80%
- [ ] Coverage report generated as artifact in CI
- [ ] No existing tests were deleted or weakened

## Dependencies
- FL-016 (LLM flow tests) — should be done first to cover ai/ module.
- FL-017 (Celery task tests) — complementary work.
