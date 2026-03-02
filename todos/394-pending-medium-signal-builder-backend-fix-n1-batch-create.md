# TODO-394: Fix N+1 Query — Batch Create Signal Nodes

**Repo:** signal-builder-backend  
**Priority:** Medium  
**Status:** Pending  
**Created:** 2026-03-02  

## Description

`apps/signals/features/signal_construction/cases/signal_node.py:57` has a TODO comment:
`# TODO: create with batch create` — currently inserts signal nodes in a loop,
causing N+1 database calls for complex signals with many nodes.

## Execution Prompt

```
You are fixing an N+1 query in signal-builder-backend at 
/data/workspace/projects/signal-builder-backend/apps/signals/features/signal_construction/cases/signal_node.py

Steps:
1. Read the file, find the loop doing individual inserts (~line 57)
2. Replace individual insert loop with SQLAlchemy bulk insert:
   ```python
   # Instead of:
   for node_data in nodes:
       node = SignalNode(**node_data)
       session.add(node)
   await session.flush()
   
   # Use:
   await session.execute(
       insert(SignalNode),
       [node_data for node_data in nodes]
   )
   await session.flush()
   ```
3. Also check apps/signals/features/signal_construction/cases/signal_edge.py for same pattern
4. Check if any similar loops exist in schema_builder storages
5. Add a test confirming bulk creation works (insert 50+ nodes, verify count)
6. Run pytest to confirm existing tests pass

Acceptance: Signal construction with 50 nodes requires ≤ 3 DB round-trips.
```

## Effort Estimate
- S (1-2 hours)

## Acceptance Criteria
- [ ] signal_node.py uses bulk insert
- [ ] signal_edge.py uses bulk insert if applicable
- [ ] Tests pass including new bulk creation test
- [ ] No regression in signal construction behavior
