# TODO-434: Fix Snowflake Parameter Binding in get_tables/get_columns

**Repo:** signal-studio-data-provider  
**Priority:** P0 — Silent Data Bug  
**Effort:** S (30m)  
**Status:** pending

## Problem

`SnowflakeProvider.get_tables()` and `get_columns()` pass params as dicts:
```python
{"1": self._sf.schema_name}
```
Snowflake connector's `execute(sql, params)` requires a sequence (list/tuple) for `%s` positional placeholders. Dict params are silently ignored — WHERE clause runs without binding, returning all tables/columns for all schemas.

## Task

1. In `get_tables()`: change `{"1": self._sf.schema_name}` → `(self._sf.schema_name,)`
2. In `get_columns()`: change dict → tuple `(table, self._sf.schema_name)`
3. Verify param binding format matches `%s` positional style throughout
4. Add test asserting correct schema filtering behavior

## Acceptance Criteria

- `get_tables()` returns only tables for the configured schema
- `get_columns()` returns only columns for the specified table
- Unit tests mock cursor and assert correct params passed
