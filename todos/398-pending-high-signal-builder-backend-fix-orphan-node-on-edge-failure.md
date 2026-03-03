# TODO-398: Fix Orphan Node on Edge Creation Failure

**Status:** pending
**Priority:** high
**Repo:** signal-builder-backend
**Effort:** XS

## Problem
In `apps/signals/features/signal_construction/cases/signal_node.py` line 108:
```python
# TODO: delete signal_node if signal_edge was not created
```
If a node is created but the subsequent edge creation fails, the orphan node is left in the DB with no parent edge — breaking signal graph integrity.

## Task
Wrap node creation + edge creation in a transaction or add cleanup on edge failure.

## Coding Prompt
```
In apps/signals/features/signal_construction/cases/signal_node.py, fix the create_node method:

Option A (preferred): Wrap the entire node + edge creation in a DB transaction using SQLAlchemy's async session context manager. If edge creation fails, the whole transaction rolls back.

Option B: Add try/except around bulk_create_edges — if it fails, call signal_node_storage.delete(signal_node.id) before re-raising.

Implement Option A if the storage layer supports transaction context, otherwise Option B.

Add integration test: mock edge creation to raise, verify no orphan node exists in DB after the exception.
```

## Acceptance Criteria
- No orphan nodes left if edge creation fails
- Transaction rollback or explicit cleanup implemented
- Test confirming no orphan on failure
