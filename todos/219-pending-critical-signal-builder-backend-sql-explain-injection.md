# TODO: Fix SQL Injection via EXPLAIN + Write Isolation (signal-builder-backend)

**Priority:** CRITICAL  
**Repo:** signal-builder-backend  
**Effort:** 3 hours  
**Status:** pending

## Description
The analytical DB module may allow EXPLAIN queries or bypass read-only transaction enforcement. The sqlglot-based SQL validator (141c1b1) only checks direct DML — EXPLAIN + subquery can bypass it.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend:

1. Find all SQL execution paths in apps/analytical_db/:
   grep -rn "execute\|EXPLAIN\|text(" apps/analytical_db/ core/

2. Audit the sqlglot validation in apps/analytical_db/ — check if:
   - EXPLAIN SELECT ... (with nested write) is blocked
   - CTEs with write operations are blocked (WITH t AS (INSERT ...) SELECT ...)
   - Multiple statements (semicolon-separated) are blocked

3. Strengthen validation in the SQL validator:
   - Parse the full AST, walk all nodes including subqueries and CTEs
   - Block: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE in ANY node
   - Block: EXPLAIN of write statements
   - Use sqlglot.parse() (multi-statement) not parse_one()

4. Wrap ALL analytical DB execution in READ ONLY transaction explicitly:
   async with session.begin():
       await session.execute(text("SET TRANSACTION READ ONLY"))
       result = await session.execute(text(user_sql))

5. Add test cases in tests/test_sql_validator.py:
   - EXPLAIN INSERT INTO ... 
   - WITH evil AS (DELETE ...) SELECT * FROM evil
   - Multiple statements: SELECT 1; DROP TABLE signals;
```

## Dependencies
- None (security critical — do first)

## Acceptance Criteria
- All EXPLAIN+write combinations rejected
- CTE with write operations rejected  
- Multi-statement SQL rejected
- All transactions run in READ ONLY mode
- New test cases pass
