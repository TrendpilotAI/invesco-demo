# TODO-392: Add Test Coverage — schema_builder, translators, analytical_db

**Repo:** signal-builder-backend  
**Priority:** High  
**Status:** Pending  
**Created:** 2026-03-02  

## Description

Three core modules have zero or near-zero test coverage despite being critical business logic:
- `apps/schema_builder/` — builds analytical DB schemas from signal definitions
- `apps/translators/` — converts signal graphs to SQL queries (most complex logic)
- `apps/analytical_db/` — executes translated queries against analytical PostgreSQL

Coverage gap: ~40-50% of critical paths untested.

## Dependencies
- None (can run in parallel with TODO-391)

## Execution Prompt

```
You are adding test coverage for three critical modules in signal-builder-backend at 
/data/workspace/projects/signal-builder-backend/.

## Module 1: apps/translators/
This converts signal graph definitions to SQL queries via sqlglot.
Read: apps/translators/ (all .py files)
Tests to write in: tests/test_translators.py

Focus on:
- Unit test each translator class's `translate()` method
- Test happy path (valid signal → expected SQL)
- Test edge cases (empty signals, null fields, complex joins)
- Test error handling (TranslationError raised for invalid input)
- Mock the DB session — translators should be testable in isolation

## Module 2: apps/schema_builder/cases/schema.py
This builds analytical DB schemas from signal definitions.
Read: apps/schema_builder/cases/schema.py, apps/schema_builder/operations/
Tests to write in: tests/test_schema_builder.py

Focus on:
- Test schema creation from various signal types
- Test operation chaining (basic_operators, group_functions)
- Test schema validation and error cases
- Test ordering operations

## Module 3: apps/analytical_db/
This manages schema sync and query execution against analytical PostgreSQL.
Read: apps/analytical_db/ (all .py files)
Tests to write in: tests/test_analytical_db.py

Focus on:
- Mock the analytical DB connection
- Test schema sync cases (create, update, delete operations)
- Test query preparation and execution
- Test error handling for DB connection failures
- Test the signal preview dry-run path

## General approach:
- Use pytest-asyncio for async tests
- Follow conftest.py patterns from existing tests/
- Use faker for test data
- Mock external dependencies (DB, Redis) per existing test patterns
- Each test file should have at least 10 test functions
- Run pytest after writing to confirm all pass

Acceptance: `pytest tests/test_translators.py tests/test_schema_builder.py tests/test_analytical_db.py -v` all green.
```

## Effort Estimate
- L (4-8 hours)

## Acceptance Criteria
- [ ] tests/test_translators.py with ≥ 10 test functions passing
- [ ] tests/test_schema_builder.py with ≥ 10 test functions passing  
- [ ] tests/test_analytical_db.py with ≥ 10 test functions passing
- [ ] Overall test count increases from 134 to ≥ 160
