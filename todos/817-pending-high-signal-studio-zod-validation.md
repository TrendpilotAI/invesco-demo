# TODO-817: Add Zod request validation to all API routes

**Priority**: HIGH (P1)
**Repo**: signal-studio
**Source**: BRAINSTORM.md → 2.4, AUDIT.md → AUDIT-004

## Description
API routes use ad-hoc validation and `any` types for request bodies. Centralize with Zod schemas for type safety and consistent error responses.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Create lib/validation.ts with Zod schemas:
   - OracleQuerySchema: { sql: string, binds?: array }
   - SignalRunSchema: { signal_id: string, params?: object }
   - ChatMessageSchema: { messages: array, model?: string }
   
2. Create lib/api-helpers.ts with HOFs:
   - validateBody<T>(schema: ZodSchema<T>): validates req body, returns typed data or 400
   - withErrorHandling(handler): catches unhandled errors, returns 500 with structured error
   
3. Update these routes to use validateBody():
   - app/api/oracle/query/route.ts
   - app/api/signals/run/route.ts  
   - app/api/chat/route.ts
   - app/api/agent/route.ts
   
4. Replace catch (error: any) with catch (error: unknown) + type guard:
   const message = error instanceof Error ? error.message : 'Unknown error'

5. Add tests in __tests__/api/ for validation rejection cases (missing fields, wrong types).
```

## Acceptance Criteria
- [ ] All listed routes use Zod validation
- [ ] Invalid request bodies return 400 with descriptive message
- [ ] No `any` type in API route handlers
- [ ] Tests cover validation rejection

## Effort
1 day

## Dependencies
None (zod already in package.json likely; check)
