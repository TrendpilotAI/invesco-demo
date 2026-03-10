# SBB-003 Done: Multi-Tenant Isolation Tests

**Completed:** 2026-03-10
**Repo:** TrendpilotAI/signal-builder-backend
**Branch:** feat/p0-todos-352-356
**Commit:** 38f1bf5

## Summary

Added comprehensive multi-tenant isolation tests to `apps/signals/tests/test_multi_tenant_isolation.py`.

## Tests Written: 23

### Test Breakdown by Scenario:

| Scenario | Tests | Status |
|----------|-------|--------|
| 1. Org A cannot GET Org B's signals | 3 | ✅ PASS |
| 2. Org A cannot PUT/PATCH Org B's signals | 3 | ✅ PASS |
| 3. Org A cannot DELETE Org B's signals | 4 | ✅ PASS |
| 4. List endpoint only returns own org's signals | 5 | ✅ PASS |
| 5. Org A cannot run/preview Org B's signals | 3 | ✅ PASS |
| 6. Signal creation binds to authenticated org | 2 | ✅ PASS |
| 7. Signal model enforces non-nullable org_id | 3 | ✅ PASS |

**Total: 23/23 PASSED**

## Was Isolation Working?

**YES — Isolation was already correctly implemented.** No bugs were found.

The existing codebase correctly:
- Passes `organization_id` to all storage queries (get, list, count, delete)
- `get_by_id()` always includes both `user_id` AND `organization_id` in the filter
- `list_objects()` and `count_objects()` always scope by org
- `preview_signal()` verifies ownership before executing SQL
- `create_signal()` always binds `organization_id` from the authenticated user
- `Signal` model has `organization_id: Mapped[int]` (NOT NULL) — added in TODO-580

The tests are committed as **regression coverage** to prevent future regressions.

## Files Changed

- `apps/signals/tests/__init__.py` — new (package marker)
- `apps/signals/tests/conftest.py` — new (local test bootstrap)
- `apps/signals/tests/test_multi_tenant_isolation.py` — new (23 tests)
- `conftest.py` — updated (fixed sentry stub attrs, added apps/core/loggers package stubs for unit test isolation)

## Commit Hash: 38f1bf5

## Test Run Output

```
23 passed in 0.93s
```

## Notes

- Tests run without a database (pure unit tests with mocked storage)
- The root `conftest.py` was enhanced to properly stub `apps` and `core` top-level packages, enabling unit tests inside `apps/*/tests/` to run without the full stack
- Branch pushed to Bitbucket: `feat/p0-todos-352-356`
