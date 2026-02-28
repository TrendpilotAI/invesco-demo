# TODO: Test Coverage for analytical_db and schema_builder (signal-builder-backend)

**Priority:** Medium  
**Repo:** signal-builder-backend  
**Effort:** 6 hours  
**Status:** pending

## Description
Zero tests for analytical_db synchronization and schema_builder modules. These are core business features.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend:

1. Create tests/analytical_db/ directory with __init__.py

2. Create tests/analytical_db/test_synchronization.py:
   - Test DB resource creation
   - Test schema synchronization endpoint (mock the DB calls)
   - Test error cases (DB unreachable, permission denied)

3. Create tests/schema_builder/ directory with __init__.py

4. Create tests/schema_builder/test_schema_cases.py:
   - Test schema creation with valid data
   - Test schema validation failures
   - Test schema retrieval by tenant

5. Follow existing test patterns from tests/signals/cases/ for consistency:
   - Use pytest-asyncio for async tests
   - Use faker for test data
   - Mock external dependencies with pytest fixtures

6. Add to tox.ini to ensure coverage runs on new paths
```

## Dependencies
- None (foundational testing work)

## Acceptance Criteria
- 80%+ coverage on analytical_db and schema_builder modules
- All new tests pass in CI
- Tests runnable with: pytest tests/analytical_db/ tests/schema_builder/ -v
