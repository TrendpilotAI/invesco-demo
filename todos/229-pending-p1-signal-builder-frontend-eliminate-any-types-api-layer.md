# 229 · P1 · signal-builder-frontend · Eliminate `any` Types in API Layer

## Status
pending

## Priority
P1 — 76 instances of `: any` across codebase; worst concentration in `src/redux/builder/api.ts`

## Description
Every RTK Query endpoint uses `any` as generic args, preventing TypeScript from catching API contract violations. This task types all endpoints in the builder API and enables the ESLint no-explicit-any rule.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Audit all `any` usages
Run: grep -rn ": any\|<any\|as any" src/redux/ src/shared/lib/auth.ts --include="*.ts" --include="*.tsx"

Step 2: Type all RTK Query endpoints in `src/redux/builder/api.ts`

For each build.query / build.mutation, replace `any` generics with proper types:
- `getSchema: build.query<TSchemaDTO, void>` (no args needed)
- `getSignals: build.query<TSignalsResponse, TGetSignalsArgs>` 
- `getSignal: build.query<TSignal, string>` (signal id)
- `createSignal: build.mutation<TSignal, TCreateSignalArgs>`
- `updateSignal: build.mutation<TSignal, TUpdateSignalArgs>`
- `deleteSignal: build.mutation<void, string>`
- `getSignalResult: build.query<TSignalResultResponse, TGetSignalResultArgs>`
- `getSignalUI: build.query<TSignalUIResponse, string>`
- `publishSignal: build.mutation<TSignal, string>`

Step 3: Create missing arg types in `src/redux/builder/types/`
Create `types.api.ts` with:
```typescript
export interface TGetSignalsArgs {
  page_number?: number;
  page_count?: number;
  collection_id?: string;
  search?: string;
}

export interface TCreateSignalArgs {
  name: string;
  collection_id?: string;
  is_draft?: boolean;
}

export interface TUpdateSignalArgs extends Partial<TCreateSignalArgs> {
  id: string;
}

export interface TGetSignalResultArgs {
  signal_id: string;
  page_number?: number;
  page_count?: number;
}
```

Step 4: Fix `catch (error: any)` → `catch (error: unknown)` in all catch blocks
In `src/redux/builder/api.ts` lines ~36, 74, 174:
```typescript
catch (error: unknown) {
  const message = error instanceof Error ? error.message : 'Unknown error';
  console.error('[API Error]', message); // temporary until Sentry added
}
```

Step 5: Fix `any` in ReactFlow callbacks in `src/modules/builder/containers/Main/Flow.tsx`
Import proper types from 'reactflow':
```typescript
import type { NodeChange, EdgeChange, Connection, DragEvent as ReactFlowDragEvent } from 'reactflow';
const onNodesChange = useCallback((changes: NodeChange[]) => ...
const onDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => ...
```

Step 6: Enable ESLint rule (add to .eslintrc.json):
```json
"@typescript-eslint/no-explicit-any": "warn"
```
(Start as warn, promote to error after fixing remaining usages.)

Run `yarn typecheck` and fix all new type errors. Run `yarn lint` to verify.
Commit: "refactor: eliminate any types in API layer and ReactFlow callbacks"
```

## Dependencies
- Should be done before 230 (Sentry integration replaces the console.error calls added here)

## Effort Estimate
M (1–2 days)

## Acceptance Criteria
- [ ] `grep -rn ": any" src/redux/builder/api.ts` returns zero results
- [ ] All RTK Query endpoints have explicit generic types
- [ ] `src/redux/builder/types/types.api.ts` exists with arg interfaces
- [ ] All catch blocks use `error: unknown` in the API layer
- [ ] `yarn typecheck` passes with no new errors
- [ ] ESLint `no-explicit-any` rule set to at least `warn`
