# TODO-606: Fix SQL Injection Protection in Oracle Query Route

**Repo:** signal-studio-frontend  
**Priority:** P0 (Critical Security)  
**Effort:** XS (1-2 hours)  
**Status:** pending

## Description

The `/api/oracle/query` route uses a keyword blocklist approach to prevent SQL injection. This can be bypassed via case variations, Unicode substitution, or comment injection. Must switch to Oracle's parameterized bind variable API so user input never reaches the SQL string directly.

## Acceptance Criteria
- [ ] All user-supplied filter values use Oracle bind variables (`SELECT * FROM t WHERE col = :val`)
- [ ] Table/column name inputs validated against an allowlist (from schema discovery)
- [ ] No string interpolation of user input into SQL strings
- [ ] Existing SQL injection test cases pass
- [ ] New test: attempt `'; DROP TABLE --` and verify it's rejected safely

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/app/api/oracle/query/route.ts:

1. Audit all places where req.body values are interpolated into SQL strings
2. Replace with Oracle bind variable syntax: WHERE col = :bindvar
3. Pass binds as the second argument to connection.execute(sql, binds, options)
4. For table/column names (which can't be parameterized), validate against a whitelist derived from schema discovery
5. Remove the keyword blocklist approach (it's not sufficient)
6. Add tests in __tests__/api/oracle-query.test.ts for SQL injection attempts
```

## Dependencies
- None
