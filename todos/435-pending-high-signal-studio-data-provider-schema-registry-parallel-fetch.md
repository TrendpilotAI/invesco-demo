# TODO-435: Parallelize SchemaRegistry Column Fetches

**Repo:** signal-studio-data-provider  
**Priority:** P1 — Performance  
**Effort:** M (2-3h)  
**Status:** pending

## Problem

`SchemaRegistry.get_schema()` fetches columns for each table serially:
```python
for table in info.tables:
    cols = await self._provider.get_columns(table.name, org_id)
```
For an org with 50 tables, this is 50 sequential DB roundtrips. At 10ms each = 500ms just for schema load.

## Task

```python
import asyncio

async def get_schema(self, org_id: str, *, force_refresh: bool = False) -> SchemaInfo:
    # ... cache check ...
    info = await self._provider.get_schema(org_id)
    
    # Parallel column fetch
    tables_needing_cols = [t for t in info.tables if not t.columns]
    if tables_needing_cols:
        results = await asyncio.gather(*[
            self._provider.get_columns(t.name, org_id) 
            for t in tables_needing_cols
        ])
        for table, cols in zip(tables_needing_cols, results):
            table.columns = cols
            self._column_cache[f"{org_id}:{table.name}"] = (now, cols)
    
    # ... rest unchanged ...
```

## Acceptance Criteria

- Schema load time scales with max single roundtrip, not sum
- Tests verify all columns populated correctly
- No regression in existing schema registry tests
