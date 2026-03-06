# TODO 728: Bulk Upsert in write_back()

**Repo:** signal-studio-data-provider  
**Priority:** HIGH  
**Effort:** S (1 day)  
**Dependencies:** None

## Description
`write_back()` currently does row-by-row inserts. Add bulk upsert with conflict resolution using each provider's native mechanism. Add `conflict_columns` parameter for upsert key specification.

## Acceptance Criteria
- [ ] `write_back(table, data, org_id, conflict_columns=None)` signature updated
- [ ] Snowflake: uses `MERGE INTO ... USING (VALUES ...) ON (key cols)` 
- [ ] Supabase: uses asyncpg `executemany` + `ON CONFLICT DO UPDATE`
- [ ] Oracle: uses `MERGE INTO`
- [ ] Batch size configurable (default 1000 rows)
- [ ] Returns count of inserted + updated rows separately
- [ ] Tests cover upsert conflict resolution

## Coding Prompt
```python
# In providers/base.py, update protocol:
async def write_back(
    self, 
    table: str, 
    data: list[dict[str, Any]], 
    org_id: str,
    conflict_columns: list[str] | None = None,
    batch_size: int = 1000,
) -> dict[str, int]:  # {"inserted": N, "updated": M}
    ...

# Snowflake MERGE implementation:
async def write_back(self, table, data, org_id, conflict_columns=None, batch_size=1000):
    if not conflict_columns:
        # Simple bulk insert
        cols = list(data[0].keys())
        placeholders = ", ".join(f"%({c})s" for c in cols)
        sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
        cursor.executemany(sql, data)
        return {"inserted": len(data), "updated": 0}
    
    # MERGE for upsert
    cols = list(data[0].keys())
    merge_condition = " AND ".join(f"target.{c} = source.{c}" for c in conflict_columns)
    update_cols = [c for c in cols if c not in conflict_columns]
    update_set = ", ".join(f"target.{c} = source.{c}" for c in update_cols)
    insert_cols = ", ".join(cols)
    insert_vals = ", ".join(f"source.{c}" for c in cols)
    
    sql = f"""
    MERGE INTO {table} AS target
    USING (SELECT {insert_cols} FROM VALUES (...)) AS source
    ON {merge_condition}
    WHEN MATCHED THEN UPDATE SET {update_set}
    WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals})
    """
```
