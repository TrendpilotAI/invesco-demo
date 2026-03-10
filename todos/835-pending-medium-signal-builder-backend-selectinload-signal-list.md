# TODO-835: Add selectinload to Signal List Queries (Fix N+1)

**Repo:** signal-builder-backend  
**Priority:** MEDIUM  
**Effort:** S (2-4 hours)  
**Status:** pending

## Problem

`apps/signals/storages/signal.py` — list queries likely don't specify eager loading strategies for signal relationships (`signal_nodes`, `signal_edges`, `signal_versions`). SQLAlchemy's default is lazy loading, which creates N+1 queries when iterating over a list of signals and accessing their relationships.

Example: Fetching 50 signals and accessing `signal.signal_nodes` for each = 51 queries (1 list + 50 node queries).

## Fix

Add explicit `options(selectinload(...))` to list queries:

```python
# apps/signals/storages/signal.py
from sqlalchemy.orm import selectinload

class SignalStorage(StorageBase):
    def get_all_by_org(self, org_id: str, ...) -> list[Signal]:
        stmt = (
            select(Signal)
            .where(Signal.organization_id == org_id)
            .options(
                selectinload(Signal.signal_nodes),
                selectinload(Signal.signal_edges),
                # Don't eagerly load signal_versions (potentially many) unless needed
            )
            .order_by(Signal.created_at.desc())
        )
        return self._session.scalars(stmt).all()
```

Note: `lazy='noload'` is already on `client_signal_result` (good). Apply the same discipline to the remaining relationships.

## Coding Prompt

```
1. Find apps/signals/storages/signal.py
2. Find the method that lists signals (get_all_by_org or similar)
3. Check if .options(selectinload/joinedload) is present
4. If not, add selectinload for signal_nodes and signal_edges
5. Run: EXPLAIN ANALYZE on "SELECT signals..." before and after to verify query count drops
6. Add test: test that listing 10 signals makes ≤ 3 queries total (using pytest-postgresql and query counting)
```

## Acceptance Criteria
- `get_all_by_org` uses `selectinload` for signal_nodes and signal_edges
- Query count for listing N signals is O(1) not O(N)
- Verified via SQLAlchemy event listener counting queries in tests
- No regression in existing signal tests
