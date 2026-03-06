---
id: 639
status: pending
priority: P1
repo: signal-studio-templates
title: Add Zod schema validation for API request bodies
effort: S (1 day)
dependencies: []
---

# Zod Validation for API Request Bodies

## Problem
The execute and customize endpoints use manual parameter checks. No schema validation library means malformed requests can cause confusing errors rather than clean 400 responses.

## Task
Add `zod` for API request body validation and return structured 400 errors.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-templates/:

1. pnpm add zod

2. Create src/validation/api-schemas.ts with:
   - ExecuteRequestSchema: z.object({ parameters: z.record(z.unknown()).optional() })
   - CustomizeRequestSchema: z.object({ overrides: z.record(z.unknown()) })
   - Reusable validateBody<T> middleware factory

3. In api/templates.ts:
   - Add validateBody(ExecuteRequestSchema) middleware before execute handler
   - Add validateBody(CustomizeRequestSchema) middleware before customize handler
   - Return { error: 'Validation failed', details: zodError.errors } on 400

4. Add tests in __tests__/api.test.ts:
   - POST /templates/:id/execute with invalid body → 400
   - POST /templates/:id/execute with empty body → 400
   - POST /templates/:id/execute with valid body → 200
```

## Acceptance Criteria
- [ ] Zod validation on execute and customize endpoints
- [ ] Clean 400 responses with structured error details
- [ ] Tests cover validation rejection cases
- [ ] `pnpm test` passes
