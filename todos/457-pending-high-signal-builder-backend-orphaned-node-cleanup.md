# TODO-457: Orphaned Node Cleanup on Signal Edge Creation Failure

**Repo:** signal-builder-backend  
**Priority:** High  
**Effort:** 1h  
**Status:** Pending

## Description
In `apps/signals/features/signal_construction/cases/signal_node.py:108`, if signal edge creation fails after node creation, the node is left orphaned in the database. There's a TODO comment acknowledging this but no fix implemented.

## Files
- `apps/signals/features/signal_construction/cases/signal_node.py` (line 108)

## Coding Prompt
```
Fix orphaned signal node on edge creation failure:

1. Wrap the node+edge creation in a single DB transaction
2. If edge creation raises an exception, the node should be rolled back
3. Pattern: use SQLAlchemy async session context manager with rollback

Alternatively, if transaction scope is hard to apply here:
- Catch the edge creation exception
- Delete the orphaned node explicitly
- Re-raise the original exception

Add a test case: create a scenario where edge creation fails and assert no orphaned node remains.
```

## Acceptance Criteria
- [ ] Node creation rolls back if edge creation fails
- [ ] No orphaned nodes in DB after failed signal construction
- [ ] Test covers the failure scenario
