# TODO-396: Fix Missing Caching in Signal Validators (Hot Path)

**Status:** pending
**Priority:** high
**Repo:** signal-builder-backend
**Effort:** S

## Problem
Three validators have `# TODO: cache` comments indicating repeated DB queries on hot paths:
- `apps/signals/features/signal_construction/cases/validators/base_validators/base_filter_value_validator.py` lines 147, 245, 339
- `apps/signals/features/signal_construction/cases/validators/base_validators/base_ordering_validator.py` line 214

Each signal node validation call hits the DB multiple times for data that doesn't change within a request.

## Task
Implement request-scoped caching (using `functools.lru_cache` or a simple dict cache on the validator instance) for the repeated DB queries in these validators.

## Coding Prompt
```
In the signal-builder-backend repo, find all # TODO: cache comments in:
- apps/signals/features/signal_construction/cases/validators/base_validators/base_filter_value_validator.py
- apps/signals/features/signal_construction/cases/validators/base_validators/base_ordering_validator.py

For each marked method:
1. Identify what DB query is being repeated
2. Add instance-level caching (store result on self after first call)
3. Ensure cache doesn't leak across request boundaries
4. Add a unit test confirming DB is only called once per validator instance

Use the existing test patterns in tests/translators/ or tests/unit/ as reference.
```

## Acceptance Criteria
- No repeated DB calls for the same data within a single validator run
- All existing tests still pass
- New unit test added for cache behavior
