# TODO-580: Make organization_id Non-Nullable in Signal Schema

**Priority:** P0 (Critical Security)
**Repo:** signal-builder-backend
**Effort:** XS (1-2 hours)
**Status:** Pending

## Problem
`apps/signals/schemas/signal.py:89` has `organization_id: int | None`. This allows signals to be created without org scoping, creating a potential IDOR vulnerability where cross-tenant data access is possible.

## Task
1. Change `organization_id: int | None` to `organization_id: int` in the signal Pydantic schema
2. Add an Alembic migration to enforce NOT NULL at DB level (if not already enforced)
3. Update any tests that create signals without org_id
4. Add an integration test that verifies a signal cannot be created/accessed across org boundaries

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend/:

1. Open apps/signals/schemas/signal.py, find organization_id field (line ~89), change type from `int | None` to `int`
2. Check if there are related schemas that also have this nullable pattern and fix them
3. Run: grep -r "organization_id" apps/signals/schemas/ to find all occurrences
4. Create Alembic migration: pipenv run auto_migration "make_org_id_not_null_signals"
5. Add integration test in tests/signals/ verifying org isolation
6. Run: pipenv run pytest tests/ -x to confirm all tests pass
```

## Acceptance Criteria
- [ ] `organization_id` is non-nullable in Pydantic schema
- [ ] DB migration enforces NOT NULL constraint
- [ ] All existing tests pass
- [ ] New test verifies cross-org signal access is rejected
