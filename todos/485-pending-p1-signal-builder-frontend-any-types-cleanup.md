# TODO-485: Eliminate `any` Types in RTK Query API Layer — 76 Instances

**Project:** signal-builder-frontend
**Priority:** P1 (HIGH impact, M effort)
**Estimated Effort:** 4-6 hours
**Dependencies:** TODO-479 (TypeScript 5.x upgrade)

## Description

76 `any` type instances exist, concentrated in the RTK Query API layer. These mask runtime errors and defeat TypeScript's purpose. Replace with proper typed interfaces.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Replace all `any` types with proper TypeScript types.

STEPS:
1. Find all any instances:
   grep -rn ": any\|as any\|<any>" src/ --include="*.ts" --include="*.tsx" | grep -v node_modules | grep -v "*.d.ts"

2. Categorize by location:
   - RTK Query endpoints (API response types)
   - Redux slice actions/payloads
   - Component props
   - Utility functions

3. For RTK Query endpoints:
   - Create proper response types in src/redux/builder/types/ or src/shared/types/
   - Type all createApi endpoint definitions with proper generics:
     build.query<SignalListResponse, SignalListParams>({...})

4. For Redux slices:
   - Type all action payloads with PayloadAction<T>
   - Replace any[] with proper typed arrays

5. For components:
   - Add proper prop interfaces
   - Type event handlers correctly

6. Fix all 11 @ts-ignore suppressors — replace with proper types or @ts-expect-error with explanation

7. Run: pnpm typecheck — must pass with ZERO any (or document exceptions with @ts-expect-error + reason)

CONSTRAINTS:
- Don't use `unknown` as a lazy replacement — use actual types
- Create reusable type definitions in shared/types/
- Each @ts-expect-error must have a comment explaining why
```

## Acceptance Criteria
- [ ] `grep -rn ": any" src/` returns <5 results (documented exceptions only)
- [ ] All RTK Query endpoints have typed request/response generics
- [ ] All @ts-ignore replaced with typed solutions or @ts-expect-error + reason
- [ ] `pnpm typecheck` passes
- [ ] New type definitions in shared/types/ or redux/builder/types/
