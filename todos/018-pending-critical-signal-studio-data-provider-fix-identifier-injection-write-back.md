---
status: pending
priority: p1
issue_id: "018"
tags: [python, security, sql-injection, signal-studio-data-provider]
dependencies: []
---

# Fix SQL Identifier Injection in write_back, vector_search, and cortex_complete

## Problem Statement

All three providers (`SnowflakeProvider`, `SupabaseProvider`, `OracleProvider`) construct SQL strings by directly interpolating caller-supplied table names, column names, and identifiers without validation. This allows SQL injection via identifier manipulation. Additionally, `SnowflakeProvider.cortex_complete()` and `cortex_embed()` interpolate the `model` parameter into SQL.

## Findings

**SnowflakeProvider.write_back():**
```python
sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
# table = caller-supplied, col_str = from data dict keys
```

**SupabaseProvider.write_back():**
```python
sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
```

**SupabaseProvider.vector_search():**
```python
sql = (
    f"SELECT *, ({column} <=> $1::vector) AS distance "
    f"FROM {table} ORDER BY {column} <=> $1::vector LIMIT $2"
)
# table AND column are caller-supplied
```

**OracleProvider.write_back():**
```python
sql = f"INSERT INTO {self._schema_prefix(table)} ({col_str}) VALUES ({placeholders})"
```

**SnowflakeProvider.cortex_complete() / cortex_embed():**
```python
f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', %s) AS response"
# model is caller-supplied string
```

**Impact:** Attacker can inject arbitrary SQL by crafting:
- Table name: `"users; DROP TABLE clients; --"`
- Column name: `"id, password FROM users WHERE '1'='1'; --"`
- Model name: `"llama3', (SELECT password FROM admin_users); --"`

## Proposed Solutions

### Identifier Allowlist Validation
SQL identifiers (table names, column names) must match a safe pattern. Standard SQL identifiers are `[A-Za-z_][A-Za-z0-9_]*` with optional quoting for special chars.

```python
import re

_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]{0,127}$')

def _validate_identifier(name: str, kind: str = "identifier") -> str:
    if not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid SQL {kind}: {name!r}")
    return name
```

For model names, use an explicit allowlist of known Snowflake Cortex model names.

## Acceptance Criteria

- [ ] `_validate_identifier(name)` utility function added to `providers/base.py` or a `utils/sql.py` module
- [ ] All three providers call `_validate_identifier()` on table name before constructing SQL
- [ ] All providers call `_validate_identifier()` on each column name from `data.keys()`
- [ ] `SupabaseProvider.vector_search()` validates `table` and `column` params
- [ ] `SnowflakeProvider.cortex_complete()` and `cortex_embed()` validate `model` against allowlist
- [ ] Tests verify that malicious identifiers raise `ValueError` before any SQL is constructed
- [ ] Tests verify valid identifiers work normally

## Coding Prompt

```
TASK: Fix SQL identifier injection in write_back, vector_search, and cortex methods
in signal-studio-data-provider.

REPO: /data/workspace/projects/signal-studio-data-provider/

FILES TO MODIFY:
  - providers/base.py (add _validate_identifier utility)
  - providers/snowflake_provider.py
  - providers/supabase_provider.py
  - providers/oracle_provider.py
  - tests/test_providers.py

CHANGES:

1. Add to providers/base.py:
   import re
   _IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]{0,127}$')
   
   def validate_identifier(name: str, kind: str = "identifier") -> str:
       """Validate a SQL identifier against safe pattern. Raises ValueError if invalid."""
       if not isinstance(name, str) or not _IDENT_RE.match(name):
           raise ValueError(f"Invalid SQL {kind}: {name!r} — must match [A-Za-z_][A-Za-z0-9_]{{0,127}}")
       return name

2. In all three providers' write_back():
   - Add at top of method: validate_identifier(table, "table name")
   - Add for each column: validate_identifier(col, "column name") for col in columns

3. In SupabaseProvider.vector_search():
   - Add: validate_identifier(table, "table name"); validate_identifier(column, "column name")

4. In SnowflakeProvider.cortex_complete() and cortex_embed():
   KNOWN_CORTEX_MODELS = frozenset({
       "llama3-70b", "llama3-8b", "mistral-7b", "mixtral-8x7b",
       "snowflake-arctic", "reka-flash", "reka-core", "jamba-instruct",
   })
   if model not in KNOWN_CORTEX_MODELS:
       raise ValueError(f"Unknown Cortex model: {model!r}")

5. Export validate_identifier from providers/__init__.py for testing

6. Add tests:
   - test_write_back_rejects_malicious_table: pass "users; DROP TABLE" as table, verify ValueError
   - test_write_back_rejects_malicious_column: pass data with key "id, password FROM users", verify ValueError
   - test_vector_search_rejects_malicious_column: verify ValueError on bad column name
   - test_cortex_rejects_unknown_model: verify ValueError on unknown model name
   - test_valid_identifiers_pass: verify snake_case, CamelCase table names work fine
```

## Dependencies

None — standalone security fix.

## Estimated Effort

S (hours)

## Work Log

### 2026-02-26 — Initial triage

**By:** Planning Agent

**Actions:**
- Identified identifier injection in write_back across all three providers
- Identified model name injection in Snowflake Cortex methods
- Designed regex-based allowlist validation approach

**Learnings:**
- SQL identifier injection is distinct from SQL value injection (which params fix)
- Identifiers cannot be parameterized in most DB drivers — allowlist is the correct approach
- The Snowflake Cortex model allowlist needs to be maintained as new models are released
