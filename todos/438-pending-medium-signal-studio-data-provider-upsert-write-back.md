# TODO-438: Add Upsert Support to write_back()

**Repo:** signal-studio-data-provider  
**Priority:** P2 — Feature Completeness  
**Effort:** M (3h)  
**Status:** pending

## Task

Add `upsert_back()` method to all providers with dialect-specific conflict resolution:

```python
async def upsert_back(
    self, 
    table: str, 
    data: list[dict[str, Any]], 
    org_id: str,
    conflict_columns: list[str],
    update_columns: list[str] | None = None,
) -> int:
```

- **PostgreSQL/Supabase:** `INSERT INTO ... ON CONFLICT (id) DO UPDATE SET col = EXCLUDED.col`
- **Snowflake:** `MERGE INTO target USING source ON ... WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...`
- **Oracle:** `MERGE INTO ... USING ... ON ... WHEN MATCHED/NOT MATCHED`

## Acceptance Criteria

- All 3 providers implement upsert_back()
- `DataProvider` Protocol updated with upsert_back signature  
- Tests cover: insert new, update existing, conflict on composite key
- Identifier validation applied to all dynamic names
