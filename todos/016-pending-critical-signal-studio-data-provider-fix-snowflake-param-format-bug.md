---
status: pending
priority: p1
issue_id: "016"
tags: [python, snowflake, bug, signal-studio-data-provider]
dependencies: []
---

# Fix Param Format Bug in SnowflakeProvider.get_tables and get_columns

## Problem Statement

`SnowflakeProvider.get_tables()` and `get_columns()` pass query parameters using a dict with string integer keys (`{"1": val}`, `{"1": val, "2": val}`), but `snowflake.connector` expects either positional sequences (tuples/lists) or named parameters with `%(name)s` syntax. The current format is silently ignored, causing the `WHERE TABLE_SCHEMA = %s` clause to match nothing (or everything, depending on driver behavior), returning wrong schema data to the NL→SQL translator.

## Findings

**Broken code in `get_tables()`:**
```python
result = await self.execute_query(
    "SELECT TABLE_NAME, ROW_COUNT, COMMENT "
    "FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s",
    {"1": self._sf.schema_name},   # ← WRONG: dict key "1" != positional %s
)
```

**Broken code in `get_columns()`:**
```python
result = await self.execute_query(
    "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COMMENT "
    "FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s AND TABLE_SCHEMA = %s",
    {"1": table, "2": self._sf.schema_name},   # ← WRONG
)
```

**Impact:** The WHERE clauses are not filtering correctly:
- `get_tables()` may return tables from ALL schemas, not just the org's schema
- `get_columns()` may return columns from ALL tables named X across all schemas
- The NL→SQL translator gets an incorrect schema, generating wrong SQL
- This is a data correctness bug that silently produces bad results

**Snowflake connector parameter formats:**
```python
# Positional (tuple):
cur.execute("SELECT * FROM t WHERE a = %s AND b = %s", (val1, val2))

# Named (dict with %(name)s placeholders):
cur.execute("SELECT * FROM t WHERE a = %(a)s AND b = %(b)s", {"a": val1, "b": val2})
```

The `execute_query` method passes params as `cur.execute(sql, params or {})`. When params is `{"1": val}`, the connector treats it as named params but can't match `%s` placeholders to `"1"` key.

## Proposed Solutions

### Option A: Change to Positional Tuple Format
```python
# get_tables:
result = await self.execute_query(
    "SELECT TABLE_NAME, ROW_COUNT, COMMENT "
    "FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s",
    (self._sf.schema_name,),  # positional tuple
)

# get_columns:
result = await self.execute_query(
    "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COMMENT "
    "FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s AND TABLE_SCHEMA = %s",
    (table, self._sf.schema_name),  # positional tuple
)
```

This requires changing `execute_query` to accept `params: dict | tuple | None`.

### Option B: Use Named Param Syntax (%(name)s)
```python
result = await self.execute_query(
    "SELECT TABLE_NAME ... WHERE TABLE_SCHEMA = %(schema)s",
    {"schema": self._sf.schema_name},
)
```

This is cleaner but requires SQL string changes. Recommended approach.

## Recommended Action

Option B: switch to named `%(name)s` syntax throughout SnowflakeProvider, and update `execute_query` signature to accept `dict[str, Any] | None`. This is more readable and self-documenting.

## Acceptance Criteria

- [ ] `get_tables()` correctly filters by `TABLE_SCHEMA` (test with mocked cursor returning schema-specific data)
- [ ] `get_columns()` correctly filters by both `TABLE_NAME` and `TABLE_SCHEMA`
- [ ] `execute_query` accepts `params: dict[str, Any] | None` and passes it correctly to `cur.execute()`
- [ ] All existing tests pass
- [ ] Add test `test_get_tables_passes_correct_schema_param` that verifies the cursor was called with the right schema value
- [ ] Add test `test_get_columns_passes_table_and_schema_params`

## Coding Prompt

```
TASK: Fix Snowflake parameter format bug in SnowflakeProvider in signal-studio-data-provider.

REPO: /data/workspace/projects/signal-studio-data-provider/

FILES TO MODIFY:
  - providers/snowflake_provider.py
  - tests/test_providers.py

CHANGES:

1. In get_tables(), change params from {"1": self._sf.schema_name} to:
   {"schema": self._sf.schema_name}
   And update SQL placeholder from %s to %(schema)s

2. In get_columns(), change params from {"1": table, "2": self._sf.schema_name} to:
   {"table": table, "schema": self._sf.schema_name}
   And update SQL placeholders accordingly.

3. In execute_query(), verify the line `cur.execute(sql, params or {})` works correctly
   with dict params. Snowflake connector accepts dict for %(name)s style, so no change needed.

4. Remove dead import: `from functools import lru_cache` is imported but never used. Delete it.

5. Add tests:
   - test_get_tables_filters_by_schema: mock cursor, call get_tables("org1"), 
     assert cursor.execute was called with args containing self._sf.schema_name
   - test_get_columns_filters_by_table_and_schema: same pattern for get_columns
   - test_execute_query_passes_params_to_cursor: verify params dict is forwarded to cursor.execute

IMPORTANT: After this fix, table/column queries should ONLY return data for the configured schema.
```

## Dependencies

- May be done concurrently with TODO-014 (async fix), but should be tested after that fix is applied

## Estimated Effort

S (hours)

## Work Log

### 2026-02-26 — Initial triage

**By:** Planning Agent

**Actions:**
- Traced the param format mismatch: `{"1": val}` dict keys don't match `%s` positional placeholders
- Confirmed Snowflake connector param passing behavior with both dict and tuple formats
- Identified dead `lru_cache` import as bonus quick win in same file

**Learnings:**
- This bug is invisible in tests because the mock cursor doesn't validate params
- The wrong data returned would cause the NL→SQL translator to generate incorrect queries
- Named params `%(name)s` are more readable and less error-prone than positional `%s`
