# TODO 619 — Second-Opinion: Type Safety Cleanup
**Priority**: P2 | **Effort**: 1 day | **Repo**: Second-Opinion

## Description
Multiple files have `any` type leakage (heicConverter.ts: 15 hits, health.ts: 11 hits, others). Replace with proper TypeScript types to improve reliability and catch bugs at compile time.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:

1. Run: grep -rn ": any\|as any\| any " src/ services/ hooks/ --include="*.ts" --include="*.tsx" | grep -v node_modules
2. For each `any` hit:
   a. Determine the actual shape of the data
   b. Create a proper TypeScript interface/type in types.ts if needed
   c. Replace `any` with the proper type
3. Priority files: heicConverter.ts, health.ts (functions/src/), geminiService.ts
4. Add Zod schemas for external API responses (Gemini responses, Firestore documents)
5. Verify `tsc --noEmit` passes with zero errors after changes
6. Add "strict": true to tsconfig.json if not already present

Do NOT break any existing functionality. If a type is truly unknown, use `unknown` + type guard instead of `any`.
```

## Acceptance Criteria
- [ ] `tsc --noEmit` passes with zero errors
- [ ] `any` count reduced by >80% from current baseline
- [ ] Zod schemas added for Gemini API response types
- [ ] No runtime behavior changes

## Dependencies
None
