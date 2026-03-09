# Delete Dead Rete Editor Component

**Repo:** signal-studio-frontend  
**Priority:** P0  
**Effort:** S (5 minutes)

## Description
`components/visual-editor/rete-editor.tsx` is 491 lines of dead code. Zero imports anywhere in the codebase. ReactFlow v12 migration is complete; Rete.js editor is fully superseded.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend:
1. Run: grep -rn "rete-editor" . --include="*.ts" --include="*.tsx" | grep -v node_modules
2. Confirm zero results
3. Delete: rm components/visual-editor/rete-editor.tsx
4. Run: pnpm build to confirm no regression
5. Commit: git add -A && git commit -m "chore: remove dead rete-editor component (superseded by ReactFlow v12)"
```

## Acceptance Criteria
- [ ] `rete-editor.tsx` deleted
- [ ] `pnpm build` passes
- [ ] No test failures

## Dependencies
None
