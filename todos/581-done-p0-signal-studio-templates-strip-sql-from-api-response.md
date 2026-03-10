# TODO 581: Strip SQL from API Response (Security)

**Repo:** signal-studio-templates  
**Priority:** P0 (Security — leaks DB schema to API consumers)  
**Effort:** S (30 min)  
**Status:** pending

## Description

`ExecutionResult.sql` (the raw generated SQL) is currently returned in API responses. This exposes database table names, column names, and schema structure to any API consumer — a serious security concern for financial data systems.

The SQL string is useful internally for debugging/logging but must not be sent over the wire.

## Fix

In `api/templates.ts`, when returning execute results, destructure and omit `sql`:

```typescript
// In the execute route handler:
const result = await engine.execute(templateId, params, options);
const { sql, ...safeResult } = result; // strip SQL

// Log it internally
logger.debug({ templateId, sql, executionTimeMs: result.executionTimeMs }, "template executed");

// Return only safe fields
res.json(safeResult);
```

Alternatively, create a `PublicExecutionResult` type that omits `sql`:
```typescript
type PublicExecutionResult = Omit<ExecutionResult, "sql">;
```

## Acceptance Criteria

- [ ] `sql` field removed from all API responses
- [ ] SQL logged server-side for debugging
- [ ] `PublicExecutionResult` type exported from engine
- [ ] Test: execute endpoint response does NOT contain `sql` field
- [ ] No breaking changes to internal engine usage
