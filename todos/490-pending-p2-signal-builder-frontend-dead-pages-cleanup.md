# TODO-490: Remove 4 Stub/Abandoned Pages

**Project:** signal-builder-frontend
**Priority:** P2 (LOW impact, XS effort)
**Estimated Effort:** 30 minutes
**Dependencies:** None

## Description

4 stub/abandoned pages identified (TODO-378 from judge). Remove dead routes and their components to reduce bundle size and confusion.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Identify and remove stub/abandoned pages.

STEPS:
1. Read src/pages/ — identify which pages are stubs (empty, placeholder, or unused)
2. Check src/app/router/ — find routes pointing to stub pages
3. For each stub page:
   - Verify it's not linked from any live UI
   - Remove the page component
   - Remove the route
   - Remove any imports
4. Run: pnpm typecheck && pnpm build
5. grep -r for any dangling references to removed pages

CONSTRAINTS:
- Only remove confirmed stubs/abandoned pages
- Keep any page that has real functionality even if incomplete
- Document what was removed in commit message
```

## Acceptance Criteria
- [ ] All stub pages removed
- [ ] Routes cleaned up
- [ ] `pnpm typecheck` passes
- [ ] `pnpm build` succeeds
- [ ] No dangling imports
