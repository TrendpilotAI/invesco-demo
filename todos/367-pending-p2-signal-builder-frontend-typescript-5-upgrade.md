# TODO-343: Upgrade TypeScript 4.4 → 5.x

**Repo:** signal-builder-frontend  
**Priority:** P2 | **Effort:** S (2-4h)  
**Status:** pending

## Problem
TypeScript 4.4.2 is significantly outdated. TS 5.x brings:
- `satisfies` operator (better type narrowing without widening)
- `const` type params
- Improved inference for generics
- Better performance on large projects

## Task
1. Update `typescript` in package.json to `^5.4.0`
2. Run `npm run typecheck` and fix errors
3. Update `@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin` to v7+

## Coding Prompt
```
cd /data/workspace/projects/signal-builder-frontend
1. npm install --save-dev typescript@^5.4 @typescript-eslint/parser@^7 @typescript-eslint/eslint-plugin@^7
2. npm run typecheck 2>&1 | head -50 — fix any new errors
3. Review tsconfig.json — add "strict": true if not set
4. npm run lint — fix new lint errors from updated rules
5. npm run build — verify production build works
```

## Acceptance Criteria
- [ ] TypeScript 5.x in package.json
- [ ] typecheck passes with 0 errors
- [ ] lint passes
- [ ] build succeeds
