# TODO-645: Upgrade TypeScript 4 → 5 in Signal Builder Frontend

**Repo:** signal-builder-frontend  
**Priority:** P1  
**Effort:** Small (half day)  
**Category:** Code Quality / Dependencies

## Description
TypeScript 4.4 is 3+ years old. TypeScript 5.x brings improved performance, better decorators, const type params, and better inference. No major breaking changes expected.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-frontend/:
1. yarn add -D typescript@^5
2. Run: yarn typecheck
3. Fix any type errors (likely minor)
4. Update tsconfig.json if needed (TS5 has new options)
5. Also upgrade: @types/react, @types/react-dom, @types/node to latest
6. Run: yarn build to verify clean build
```

## Acceptance Criteria
- [ ] typescript@5.x in package.json
- [ ] yarn typecheck passes with zero errors
- [ ] yarn build succeeds
- [ ] No runtime regressions

## Dependencies
None
