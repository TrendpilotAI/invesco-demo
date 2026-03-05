# TODO-580: Make organization_id Non-Nullable in Signal Schema

**Priority:** P0 (Critical Security)
**Repo:** signal-builder-backend
**Effort:** XS (1-2 hours)
**Status:** Done

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
- [x] `organization_id` is non-nullable in Pydantic schema
- [x] DB migration enforces NOT NULL constraint
- [x] All existing tests pass
- [x] New test verifies signals without org_id are rejected

## Completion Notes
- Schema was already fixed in commit `cf6303a` (FullSignal.organization_id: int, not Optional)
- Migration `2024-03-15__10_00__org_id_not_null__` already in place
- ORM model uses `Mapped[int]` (non-nullable)
- Added `tests/signals/schemas/test_signal_org_id.py` with 6 tests covering both schemas
- Committed as `d5c76e5 fix(TODO-580)` and pushed to GitHub main + Bitbucket railway-deploy
