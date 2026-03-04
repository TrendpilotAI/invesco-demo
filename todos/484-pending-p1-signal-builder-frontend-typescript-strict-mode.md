# 484 — Enable TypeScript Strict Mode

**Priority:** P1  
**Repo:** signal-builder-frontend  
**Effort:** Small-Medium (1-2 days)  
**Dependencies:** None

## Task Description
TypeScript strict mode is not enabled, allowing `any` types and null-safety issues to slip through. Enabling strict mode prevents runtime errors and improves IDE support.

## Coding Prompt
```
Enable TypeScript strict mode in /data/workspace/projects/signal-builder-frontend/.

1. Edit tsconfig.json — add under compilerOptions:
   "strict": true,
   "noImplicitAny": true,
   "strictNullChecks": true,
   "strictFunctionTypes": true

2. Run: yarn typecheck 2>&1 | tee /tmp/ts-errors.txt
   Count errors: grep -c "error TS" /tmp/ts-errors.txt

3. For each error type, apply systematic fixes:
   - 'any' type: replace with proper type or 'unknown'
   - null/undefined: add null checks or use optional chaining (?.)
   - Missing return types: add explicit return type annotations
   - Implicit any in function params: add types

4. Focus on highest-impact files first:
   - src/shared/lib/getAxiosInstance.ts
   - src/shared/lib/auth.ts  
   - src/pages/builder/
   - src/modules/builder/

5. For third-party libs without types, add @types/* packages or declare module

6. DO NOT use // @ts-ignore to suppress — fix the actual types

7. Run yarn typecheck again — must show 0 errors before PR
```

## Acceptance Criteria
- [ ] "strict": true in tsconfig.json
- [ ] yarn typecheck returns 0 errors
- [ ] No @ts-ignore suppressions added
- [ ] All existing tests still pass
