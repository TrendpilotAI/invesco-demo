# Add Test Coverage for schema_builder and translators

**Repo:** signal-builder-backend  
**Priority:** high  
**Effort:** M (3-5 days)  
**Phase:** 2

## Problem
`apps/schema_builder/` and `apps/translators/` have no visible unit test coverage. These are core to signal execution — untested bugs here cause production failures.

## Task
1. Audit `apps/schema_builder/` — map all public methods
2. Write unit tests for schema building logic (use pytest + faker)
3. Audit `apps/translators/` — map translator classes
4. Write unit tests with known signal graph → expected SQL output
5. Add integration tests for end-to-end signal translation
6. Target: >80% coverage on these modules
7. Add coverage reporting to CI

## Acceptance Criteria
- `apps/schema_builder/` has >80% test coverage
- `apps/translators/` has >80% test coverage
- Tests run in CI and block merge on failure
- Coverage report generated as CI artifact
