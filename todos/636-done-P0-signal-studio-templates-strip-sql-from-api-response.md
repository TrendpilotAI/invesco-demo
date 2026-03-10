---
id: 636
status: pending
priority: P0
repo: signal-studio-templates
title: Strip SQL from API response (security)
effort: XS (1 hour)
dependencies: []
---

# Strip ExecutionResult.sql from API Response

## Problem
`api/templates.ts` execute endpoint returns the full `ExecutionResult` including the raw `sql` field. This leaks database table names, column names, and query structure to any API consumer — a significant security issue for a financial data product.

## Task
Strip the `sql` field before returning the execute response. Keep it internally for logging.

## Coding Prompt
```
Edit /data/workspace/projects/signal-studio-templates/api/templates.ts

In the POST /templates/:id/execute handler:
1. After getting the result from engine.execute(), destructure out the sql field:
   const { sql: _sql, ...safeResult } = result;
2. Return safeResult instead of result
3. Log the sql internally (to console.debug or a logger) for debugging
4. Add a comment explaining why sql is stripped

Also update the TypeScript return type for the execute endpoint to exclude sql.

Optionally: Add a separate internal-only debug endpoint (protected by a separate 
admin-only JWT scope) that returns the full result including sql.
```

## Acceptance Criteria
- [ ] `sql` field absent from execute API response
- [ ] SQL still logged internally for debugging
- [ ] Existing tests updated to not check for `sql` in response
- [ ] `pnpm test` passes
