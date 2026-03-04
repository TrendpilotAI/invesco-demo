# TODO-483: ReactFlow v11 → v12 Upgrade

**Project:** signal-builder-frontend
**Priority:** P1 (MEDIUM impact, M effort)
**Estimated Effort:** 4-6 hours
**Dependencies:** TODO-474 (DRY FilterContent — cleaner codebase first)

## Description

ReactFlow v12 has better performance, new edge routing, TypeScript improvements. Required before adding collaborative editing. Migration guide available — mostly compatible.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Upgrade ReactFlow from v11 to v12.

STEPS:
1. Check current version: cat package.json | grep reactflow
2. Read ReactFlow v11→v12 migration guide: https://reactflow.dev/learn/troubleshooting/migrate-to-v12

3. Upgrade:
   pnpm add reactflow@^12 @reactflow/core@^12 @reactflow/background@^12 @reactflow/controls@^12 @reactflow/minimap@^12

4. Common breaking changes to fix:
   - Import paths may change (check migration guide)
   - `nodeTypes` and `edgeTypes` API changes
   - Event handler signatures may differ
   - CSS import path changes

5. Update all ReactFlow usage in:
   - src/modules/builder/containers/Main/Flow.tsx (main canvas)
   - src/modules/builder/containers/FlowNode/ (all node types)
   - src/modules/builder/containers/FlowEdge/
   - Any other files importing from 'reactflow'

6. Verify nodeTypes/edgeTypes are defined outside component render (performance critical — already confirmed safe per brainstorm)

7. Run: pnpm typecheck && pnpm build && pnpm test
8. Manual test: load builder page, drag nodes, connect edges, verify all interactions work

CONSTRAINTS:
- Follow official migration guide exactly
- Don't change visual appearance
- Keep all existing node/edge functionality
- Ensure custom node components still receive correct props
```

## Acceptance Criteria
- [ ] ReactFlow ≥12.x in package.json
- [ ] All custom nodes and edges render correctly
- [ ] Drag, drop, connect, delete all work
- [ ] `pnpm typecheck` passes
- [ ] `pnpm build` succeeds
- [ ] No console errors/warnings from ReactFlow
