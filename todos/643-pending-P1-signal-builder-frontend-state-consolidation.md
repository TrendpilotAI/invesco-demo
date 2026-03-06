# TODO-643: Consolidate State Management in Signal Builder Frontend

**Repo:** signal-builder-frontend  
**Priority:** P1  
**Effort:** Medium (2-3 days)  
**Category:** Code Quality

## Description
The frontend currently uses THREE state management libraries simultaneously:
- Redux Toolkit (global state, auth)
- Jotai v1 (atom-based local state)
- React Query v4 (server state)

This creates cognitive overhead, inconsistent patterns, and maintenance burden. Jotai is redundant with React Query for server state and Redux for global state.

## Task
Remove Jotai from the codebase. Migrate any Jotai atoms to either:
- React Query (if it's server/async state)
- Redux Toolkit (if it's global UI state)
- React useState/useReducer (if it's local component state)

## Coding Prompt
```
Audit all Jotai usage in /data/workspace/projects/signal-builder-frontend/src/:
1. Find all files importing from 'jotai' with: grep -r "from 'jotai'" src/
2. For each atom, classify: server state → React Query, global UI → Redux, local → useState
3. Migrate each atom to its target
4. Remove jotai from package.json dependencies
5. Run: yarn build && yarn typecheck to verify no errors
6. Update imports in all affected files
```

## Acceptance Criteria
- [ ] No `jotai` imports in codebase
- [ ] `jotai` removed from package.json
- [ ] All state still functions correctly
- [ ] `yarn typecheck` passes
- [ ] `yarn build` succeeds

## Dependencies
None
