---
id: 702
status: pending
repo: signal-studio-templates
priority: P1
effort: S
created: 2026-03-10
---

# TODO 702 — API Hardening: Zod Validation + Query Timeout + JWT Audience

**Repo:** signal-studio-templates  
**Priority:** P1 — Security gaps before any production exposure  
**Effort:** S (3-4 hours)

## Problem

Three security/reliability gaps found in AUDIT.md:

1. **No request body validation** — `POST /templates/:id/execute` destructures `req.body` without schema validation. Adversarial payloads could cause unexpected behavior.
2. **No query execution timeout** — `await dataProvider.executeSQL()` has no timeout. One slow/locked query can block the API worker indefinitely.
3. **JWT audience not validated** — `express-jwt` config is missing `audience` claim validation, allowing token reuse across services.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates:

### Part 1: Zod Request Body Validation

1. pnpm add zod

2. Create api/schemas.ts:
   import { z } from 'zod';
   
   export const ExecuteRequestSchema = z.object({
     parameters: z.record(z.unknown()).optional().default({}),
     includeTalkingPoints: z.boolean().optional().default(false),
     customizations: z.record(z.unknown()).optional(),
   });
   
   export const CustomizeRequestSchema = z.object({
     customizations: z.record(z.unknown()),
   });
   
   export type ExecuteRequest = z.infer<typeof ExecuteRequestSchema>;

3. In api/templates.ts, POST /templates/:id/execute handler:
   Replace:
     const { parameters = {}, includeTalkingPoints = true } = req.body;
   With:
     const parseResult = ExecuteRequestSchema.safeParse(req.body);
     if (!parseResult.success) {
       return res.status(400).json({ error: 'Invalid request body', details: parseResult.error.flatten() });
     }
     const { parameters, includeTalkingPoints } = parseResult.data;
   
   Note: change includeTalkingPoints default to false (was incorrectly true, wasting OpenAI calls).

### Part 2: Query Execution Timeout

In engine/template-engine.ts, wrap executeSQL calls:

const QUERY_TIMEOUT_MS = parseInt(process.env.QUERY_TIMEOUT_MS || '30000', 10);

async function executeWithTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error(`Query timeout after ${timeoutMs}ms`)), timeoutMs)
    ),
  ]);
}

In TemplateEngine.execute():
  const rows = await executeWithTimeout(
    this.dataProvider.executeSQL(sql, params),
    QUERY_TIMEOUT_MS
  );

In api/templates.ts, catch timeout errors and return 408:
  } catch (err: any) {
    if (err.message?.includes('timeout')) {
      return res.status(408).json({ error: 'Query execution timed out' });
    }
    // existing error handling...
  }

### Part 3: JWT Audience Validation

In src/middleware/auth.ts:
Add audience validation to express-jwt config:
  audience: process.env.JWT_AUDIENCE,  // e.g. 'https://api.signal-studio.forwardlane.com'

In .env.example, add:
  JWT_AUDIENCE=https://api.signal-studio.forwardlane.com

Make JWT_AUDIENCE optional (only validate if set — some envs may not need it initially).

### Tests

Update __tests__/api.test.ts to cover:
- Missing required parameters → 400 with Zod error details
- Invalid parameter types → 400
- Valid body → proceeds to execution
```

## Files

- `api/schemas.ts` (new)
- `api/templates.ts` (update body validation + timeout error handling + default includeTalkingPoints=false)
- `engine/template-engine.ts` (add executeWithTimeout)
- `src/middleware/auth.ts` (add JWT_AUDIENCE)
- `.env.example` (add JWT_AUDIENCE)
- `__tests__/api.test.ts` (update tests)
- `package.json` (add zod)

## Acceptance Criteria

- POST with malformed body returns 400 + structured error
- Slow query times out after 30s (or QUERY_TIMEOUT_MS env var) with 408
- All existing 35 tests still pass + new validation tests added
- `includeTalkingPoints` defaults to false (reduces unnecessary OpenAI calls)
