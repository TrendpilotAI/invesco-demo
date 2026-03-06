# TODO-712: Dead Code Cleanup & Middleware Consolidation

**Repo**: signal-studio-frontend  
**Priority**: P0  
**Effort**: S (< 1 day)  
**Status**: pending

## Description
Remove dead code and resolve middleware conflict to stabilize the codebase.

## Tasks
1. Delete `/components/visual-editor/rete-editor.tsx` (Rete.js not in package.json, will fail to compile)
2. Resolve middleware conflict: `/middleware.ts` (cookie-auth) vs `/src/middleware.ts` (Supabase) — pick one, delete the other
3. Move stale markdown files to `/docs/archive/`: `AI-CHAT-FINAL.md`, `BRANCH-COMPLETE.md`, `IMPLEMENTATION-COMPLETE.md`, `MVP-FINAL-STATUS.md`, `PHASE3-COMPLETE.md` etc.
4. Delete `check-admin-table-access.js` and `check-user-privileges.js` from root
5. Verify `browser-history-search/` directory is intentional or delete

## Acceptance Criteria
- [ ] `npm run build` succeeds with no dead import errors
- [ ] Only one middleware file active
- [ ] Root directory has < 5 markdown files (README, CONTRIBUTING, AUDIT, BRAINSTORM, PLAN)
