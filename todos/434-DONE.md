# TODO-434 DONE — Fix Snowflake Parameter Binding

**Repo:** TrendpilotAI/signal-studio-data-provider  
**Commit:** `a1af2f9`  
**Status:** ✅ Fixed, tested, and pushed to GitHub (`origin/master`)

## What Was Done

### Bug
`SnowflakeProvider.get_tables()` and `get_columns()` were passing query parameters as dicts
(e.g. `{"1": self._sf.schema_name}`), but Snowflake's Python connector requires positional
params as a **list or tuple** for `%s` placeholders. Dict params were silently ignored,
causing WHERE clauses to run unbound and return all rows regardless of schema.

### Fix Applied

**`get_tables()`** — `providers/snowflake_provider.py`:
```python
# Before (broken):
params={"1": self._sf.schema_name}

# After (fixed):
params=[self._sf.schema_name]
```

**`get_columns()`** — `providers/snowflake_provider.py`:
```python
# Before (broken):
params={"1": table, "2": self._sf.schema_name}

# After (fixed):
params=[table, self._sf.schema_name]
```

### Tests Added

**`tests/test_providers.py`** — Two new async tests:
- `test_snowflake_get_tables_passes_list_param` — mocks `execute_query`, asserts params is a list with `[schema_name]`
- `test_snowflake_get_columns_passes_list_param` — mocks `execute_query`, asserts params is `[table, schema_name]`

## Files Changed
- `providers/snowflake_provider.py` — parameter binding fix
- `tests/test_providers.py` — regression tests for TODO-434
