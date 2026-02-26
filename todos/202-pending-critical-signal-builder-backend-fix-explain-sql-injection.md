# TODO 202 — Fix EXPLAIN SQL Injection (CRITICAL)

**Project:** signal-builder-backend  
**Priority:** CRITICAL  
**Estimated Effort:** 2 hours  
**Status:** pending  
**Dependencies:** none  

---

## Task Description

`apps/signals/features/client_signal_result/client_signal_result.py` contains an `is_sql_code_correct()` function that executes user-influenced SQL directly in an `EXPLAIN` statement. Because `EXPLAIN` in PostgreSQL can execute arbitrary SQL (e.g., `EXPLAIN (ANALYZE, FORMAT TEXT) DROP TABLE ...` or via subqueries), this is a **SQL injection vulnerability** — even though it's wrapped in `EXPLAIN`, it can still expose data or cause damage.

**Root cause:** The translated SQL from the signal node tree is passed without sanitization into a raw `EXPLAIN {sql}` statement executed against the **analytical database** (which contains real client/adviser data).

**Fix:**
1. Replace the raw `EXPLAIN` string concatenation with a parameterized or sandboxed approach.
2. Validate the SQL structure before executing — reject any SQL containing DDL (DROP, CREATE, ALTER), DML (INSERT, UPDATE, DELETE), or suspicious patterns.
3. Use `sqlparse` or `sqlglot` to parse and validate the query is a SELECT-only statement.
4. Wrap in a read-only transaction with statement timeout.

---

## Coding Prompt (Autonomous Agent)

```
TASK: Fix SQL injection vulnerability in is_sql_code_correct() in signal-builder-backend

REPO: /data/workspace/projects/signal-builder-backend/

FILE: apps/signals/features/client_signal_result/client_signal_result.py
FUNCTION: is_sql_code_correct() (or similar — search for EXPLAIN usage)

STEPS:

1. Locate the vulnerability:
   ```bash
   grep -rn "EXPLAIN\|explain" apps/ --include="*.py"
   ```
   Find the function that builds and executes `EXPLAIN {user_sql}`.

2. Install `sqlglot` (add to Pipfile):
   ```
   sqlglot = ">=18.0.0"
   ```
   Run `pipenv install sqlglot`.

3. Create a SQL validation utility at `core/shared/sql_validator.py`:
   ```python
   """SQL safety validation for signal-generated queries."""
   import re
   import sqlglot
   from sqlglot import exp
   
   # DDL/DML keywords that must never appear in signal SQL
   FORBIDDEN_PATTERNS = re.compile(
       r'\b(DROP|CREATE|ALTER|INSERT|UPDATE|DELETE|TRUNCATE|GRANT|REVOKE|EXECUTE|EXEC|'
       r'pg_read_file|pg_exec|pg_sleep|dblink|lo_import|lo_export|COPY)\b',
       re.IGNORECASE
   )
   
   class SQLValidationError(ValueError):
       """Raised when signal SQL fails safety checks."""
   
   def validate_select_only(sql: str) -> str:
       """
       Validate that sql is a safe, SELECT-only query.
       Returns the normalized SQL string.
       Raises SQLValidationError if unsafe.
       """
       if not sql or not sql.strip():
           raise SQLValidationError("SQL cannot be empty")
       
       # Pattern-based fast check
       if FORBIDDEN_PATTERNS.search(sql):
           raise SQLValidationError(
               f"SQL contains forbidden keyword. Only SELECT statements are allowed."
           )
       
       # Parse and validate with sqlglot
       try:
           statements = sqlglot.parse(sql, dialect="postgres")
       except Exception as e:
           raise SQLValidationError(f"SQL parse error: {e}")
       
       if not statements:
           raise SQLValidationError("No valid SQL statement found")
       
       if len(statements) > 1:
           raise SQLValidationError("Multi-statement SQL is not allowed")
       
       stmt = statements[0]
       if not isinstance(stmt, exp.Select):
           raise SQLValidationError(
               f"Only SELECT statements are allowed, got: {type(stmt).__name__}"
           )
       
       # Check for subquery DML (e.g., INSERT INTO ... SELECT)
       for node in stmt.walk():
           if isinstance(node, (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create)):
               raise SQLValidationError("Nested DML/DDL in SELECT is not allowed")
       
       return sql.strip()
   ```

4. Modify `is_sql_code_correct()` in client_signal_result.py:
   
   BEFORE (vulnerable):
   ```python
   async def is_sql_code_correct(self, sql: str, db_session) -> bool:
       try:
           await db_session.execute(f"EXPLAIN {sql}")
           return True
       except Exception:
           return False
   ```
   
   AFTER (safe):
   ```python
   from core.shared.sql_validator import validate_select_only, SQLValidationError
   
   async def is_sql_code_correct(self, sql: str, db_session) -> tuple[bool, str | None]:
       """
       Validate SQL safety and syntactic correctness.
       Returns (is_valid, error_message).
       """
       # Step 1: Safety validation (no DDL/DML/injection)
       try:
           validated_sql = validate_select_only(sql)
       except SQLValidationError as e:
           logger.warning(f"SQL safety check failed: {e} | sql_preview={sql[:200]}")
           return False, str(e)
       
       # Step 2: Syntax check via EXPLAIN in read-only transaction with timeout
       try:
           async with db_session.begin():
               # Set statement timeout: 10 seconds max
               await db_session.execute("SET LOCAL statement_timeout = '10s'")
               # Set read-only mode for this transaction
               await db_session.execute("SET LOCAL default_transaction_read_only = true")
               # Use text() with explicit casting to avoid injection
               from sqlalchemy import text
               await db_session.execute(text(f"EXPLAIN {validated_sql}"))
           return True, None
       except Exception as e:
           logger.info(f"SQL syntax check failed: {e}")
           return False, f"SQL syntax error: {str(e)}"
   ```

5. Update all callers of `is_sql_code_correct()` to handle the new return signature `(bool, str | None)`.

6. Add `sqlglot` to Pipfile:
   ```toml
   sqlglot = ">=18.0.0,<25.0.0"
   ```

7. Write tests in `tests/test_sql_validator.py`:
   ```python
   import pytest
   from core.shared.sql_validator import validate_select_only, SQLValidationError
   
   def test_valid_select():
       sql = "SELECT id, name FROM advisors WHERE org_id = 1"
       assert validate_select_only(sql) == sql.strip()
   
   def test_rejects_drop():
       with pytest.raises(SQLValidationError):
           validate_select_only("DROP TABLE advisors")
   
   def test_rejects_insert():
       with pytest.raises(SQLValidationError):
           validate_select_only("INSERT INTO advisors VALUES (1, 'hacked')")
   
   def test_rejects_explain_with_analyze():
       # EXPLAIN ANALYZE can run the query — must be blocked
       with pytest.raises(SQLValidationError):
           validate_select_only("EXPLAIN ANALYZE SELECT 1")
   
   def test_rejects_multi_statement():
       with pytest.raises(SQLValidationError):
           validate_select_only("SELECT 1; DROP TABLE advisors")
   
   def test_rejects_pg_read_file():
       with pytest.raises(SQLValidationError):
           validate_select_only("SELECT pg_read_file('/etc/passwd')")
   
   def test_rejects_empty():
       with pytest.raises(SQLValidationError):
           validate_select_only("")
   
   def test_allows_complex_select():
       sql = """
       SELECT a.id, a.name, SUM(f.amount) as total
       FROM advisors a
       JOIN flows f ON a.id = f.advisor_id
       WHERE a.org_id = 5
       GROUP BY a.id, a.name
       HAVING SUM(f.amount) > 1000000
       ORDER BY total DESC
       LIMIT 100
       """
       assert validate_select_only(sql)
   ```

8. Commit: "security: fix SQL injection in is_sql_code_correct via sqlglot validation + read-only transaction"

VERIFICATION:
- `grep -rn "f\"EXPLAIN\|f'EXPLAIN" apps/` should return 0 raw f-string EXPLAIN usages
- All tests in test_sql_validator.py pass
- Existing signal validation flow still works end-to-end
```

---

## Dependencies

- None — can be executed immediately

## Acceptance Criteria

- [ ] No raw f-string `EXPLAIN {sql}` execution exists in the codebase
- [ ] `validate_select_only()` utility exists and blocks DDL, DML, and injection patterns
- [ ] `is_sql_code_correct()` runs EXPLAIN in a read-only transaction with statement timeout
- [ ] `sqlglot` added to Pipfile with a pinned version range
- [ ] 8+ tests covering injection vectors all pass
- [ ] Callers updated to handle the new `(bool, str | None)` return type
- [ ] Committed and pushed
