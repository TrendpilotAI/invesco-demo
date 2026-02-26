---
status: pending
priority: p1
issue_id: "203"
tags: [typescript, type-safety, rtk-query, signal-builder-frontend]
dependencies: []
---

# 203 — Eliminate `any` Types in API Layer

## Problem Statement

`src/redux/builder/api.ts` uses `any` as the request argument type for nearly every RTK Query endpoint. There are 76 instances of `: any` across the codebase. This completely bypasses TypeScript's type safety — callers can pass any shape of data to mutations and queries without compilation errors, and response shapes are unchecked.

## Findings

Key `any` usages in `builder/api.ts`:
```typescript
getSchema: build.query<TSchemaDTO, any>        // query arg should be void
createSignal: build.mutation<TSignal, any>     // should be TCreateSignalArgs
getSignals: build.query<TSignalsResponse, any> // should be TGetSignalsArgs  
getSignal: build.query<TSignal, any>           // should be string (id)
updateSignal: build.mutation<TSignal, any>     // should be TUpdateSignalArgs
validateSignal: build.mutation({...})          // no generics at all
publishSignal: build.mutation({...})           // response/arg both any
getSignalColumns: build.query<any, any>        // fully untyped
getSignalResult: build.query<any, any>         // fully untyped
getSignalUI: build.query<TSignalUIData, any>   // signalId should be string
updateSignalUI: build.mutation<TSignalUIData, any>  // should be TUpdateSignalUIArgs
createSignalNode: build.mutation<TSignalNodeData, any>  // should be typed args
updateSignalNode: build.mutation<TSignalNodeData, any>  // should be typed args
deleteSignalNode: build.mutation<null, any>    // should be TDeleteSignalNodeArgs
```

Also found in hooks: error caught as `error: any` should be `error: unknown`.

## Proposed Solutions

### Option A: Define explicit types in builder/types (Recommended)
Add request arg interfaces to the existing types directory, then update all endpoint definitions.
- **Pros:** Full type safety, TypeScript can catch call-site errors
- **Cons:** Medium effort
- **Effort:** M (~4-6h)
- **Risk:** Low — compile-time only change

### Option B: Enable `@typescript-eslint/no-explicit-any` as error
Just add the ESLint rule to force developers to fix `any` usages incrementally.
- **Pros:** Enforces going forward
- **Cons:** Doesn't fix existing issues
- **Effort:** XS
- **Risk:** Low (but incomplete)

## Recommended Action

Option A first, then add the ESLint rule to prevent regression.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Replace 'any' types in src/redux/builder/api.ts with explicit types

1. Add new type definitions to src/redux/builder/types/types.signal.ts or create
   src/redux/builder/types/types.api.ts:

   // Query argument types
   export type TGetSignalsArgs = {
     collection?: string;
     itemsPerPage: number;
     page: number;
   };

   export type TGetSignalResultArgs = {
     id: string;
     page: number;
     count: number;
   };

   // Mutation argument types  
   export type TCreateSignalArgs = {
     verboseName: string;
     active?: boolean;
     selectedNodeId?: string;
     data: { nodes: Node<TNodeData>[] };
   };

   export type TUpdateSignalArgs = {
     id: string;
     verbose_name: string;
     default_weight?: number;
     response_singular?: string;
   };

   export type TPublishSignalArgs = {
     id: string;
     columns: Record<string, unknown>;
   };

   export type TUpdateSignalUIArgs = {
     requestData: unknown;
     signalId: string;
   };

   export type TCreateSignalNodeArgs = {
     requestData: unknown;
     signalId: string;
   };

   export type TUpdateSignalNodeArgs = {
     requestData: unknown;
     signalId: string;
     signalNodeId: string;
   };

   export type TDeleteSignalNodeArgs = {
     signalId: string;
     signalNodeId: string;
   };

2. Update src/redux/builder/api.ts to use these types:
   - getSchema: build.query<TSchemaDTO, void>
   - createSignal: build.mutation<TSignal, TCreateSignalArgs>
   - getSignals: build.query<TSignalsResponse, TGetSignalsArgs>
   - getSignal: build.query<TSignal, string>
   - updateSignal: build.mutation<TSignal, TUpdateSignalArgs>
   - validateSignal: build.mutation<unknown, string>
   - publishSignal: build.mutation<unknown, TPublishSignalArgs>
   - getSignalColumns: build.query<unknown[], string>
   - getSignalResult: build.query<unknown, TGetSignalResultArgs>
   - getSignalUI: build.query<TSignalUIData, string>
   - updateSignalUI: build.mutation<TSignalUIData, TUpdateSignalUIArgs>
   - createSignalNode: build.mutation<TSignalNodeData, TCreateSignalNodeArgs>
   - updateSignalNode: build.mutation<TSignalNodeData, TUpdateSignalNodeArgs>
   - deleteSignalNode: build.mutation<null, TDeleteSignalNodeArgs>
   - Change 'error: any' to 'error: unknown' in all catch blocks

3. Fix any call-site TypeScript errors that surface (the compiler will guide you)

4. Enable ESLint rule in .eslintrc.json:
   "@typescript-eslint/no-explicit-any": "warn"
   (Use "warn" not "error" initially to avoid CI failures during migration)

5. Run: cd /data/workspace/projects/signal-builder-frontend && yarn typecheck
   Fix all errors before committing.

6. Run: yarn lint
   Fix or suppress any new lint errors with justification.
```

## Dependencies

None — this is a standalone TypeScript improvement.

## Estimated Effort

**Medium** — 4-6 hours

## Acceptance Criteria

- [ ] All RTK Query endpoints in `builder/api.ts` use explicit type parameters (no `any`)
- [ ] New type definitions are exported from `src/redux/builder/types/`
- [ ] All `catch (error: any)` changed to `catch (error: unknown)`
- [ ] `@typescript-eslint/no-explicit-any: "warn"` added to `.eslintrc.json`
- [ ] `yarn typecheck` passes with 0 errors
- [ ] `yarn lint` passes with 0 new errors
- [ ] No runtime behavior is changed — this is types-only

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Audited all 14 RTK Query endpoint definitions in builder/api.ts
- Found every query/mutation uses `any` for the arg type
- Found `getSignalColumns` and `getSignalResult` are fully untyped (both generics are any)
