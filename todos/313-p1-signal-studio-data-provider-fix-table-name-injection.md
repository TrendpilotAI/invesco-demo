# TODO 313 — Fix Table Name SQL Injection in write_back()

**Priority:** P1 🟠  
**Repo:** signal-studio-data-provider  
**File:** providers/snowflake_provider.py, supabase_provider.py, oracle_provider.py  
**Effort:** S (< 2 hours)  
**Status:** pending

---

## Description

All three providers build INSERT SQL using f-strings with unvalidated `table` and column names:
```python
sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
```
A caller supplying `"users; DROP TABLE users--"` as `table` would execute arbitrary SQL.

---

## Coding Prompt

```
Add a shared identifier validator to providers/base.py:

import re

def _safe_identifier(name: str) -> str:
    """Validate a SQL identifier (table or column name). Raises ValueError if invalid."""
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*', name):
        raise ValueError(f"Invalid SQL identifier: {name!r}")
    return name

Then in each provider's write_back() method, validate before building the SQL:
    safe_table = _safe_identifier(table)
    safe_columns = [_safe_identifier(k) for k in data[0].keys()]

Apply to: snowflake_provider.py, supabase_provider.py, oracle_provider.py

Add tests in tests/test_providers.py:
- write_back() with malicious table name raises ValueError
- write_back() with malicious column name raises ValueError
- write_back() with valid table name succeeds
```

---

## Dependencies

- TODO 311 (JWT fix) — independent, can be done in parallel

## Acceptance Criteria

- [ ] `_safe_identifier` in base.py or a shared util module
- [ ] All 3 providers use it in write_back()
- [ ] Tests for malicious and valid identifiers
- [ ] No regression in existing tests
