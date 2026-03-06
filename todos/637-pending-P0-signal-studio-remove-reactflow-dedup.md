# TODO-637: Remove Duplicate ReactFlow Package from Signal Studio

**Priority:** P0  
**Effort:** S (4hrs)  
**Repo:** signal-studio  
**Category:** Dependencies / Performance  

## Problem

`package.json` contains both `reactflow@11.11.4` and `@xyflow/react@12.9.0`. These are the same library — ReactFlow v12 was renamed/rebranded to `@xyflow/react`. Having both installed:
- Inflates JS bundle by ~300KB
- Causes potential version conflicts in visual builder
- Wastes Railway build time

## Task Description

1. Run `rg "from 'reactflow'" --type ts --type tsx` across `app/`, `src/`, `components/`, `lib/`
2. For each import found, migrate to `@xyflow/react` equivalent:
   - `ReactFlow` → `ReactFlow` (same)
   - `useReactFlow` → `useReactFlow` (same)
   - `addEdge`, `applyNodeChanges`, etc. → same names in new package
   - CSS: `import 'reactflow/dist/style.css'` → `import '@xyflow/react/dist/style.css'`
3. Run `pnpm remove reactflow`
4. Run `pnpm build` and verify no import errors
5. Manual test: open `/visual-builder` and verify nodes render + connect correctly

## Coding Prompt (Autonomous Execution)

```
In /data/workspace/projects/signal-studio:
1. Run: grep -rn "from 'reactflow'" --include="*.ts" --include="*.tsx" app/ src/ components/ lib/ hooks/
2. For each file returned, update the import to use '@xyflow/react' instead of 'reactflow'
3. Run: grep -rn "reactflow/dist" --include="*.ts" --include="*.tsx" app/ src/ components/ lib/
4. Update any CSS imports to '@xyflow/react/dist/style.css'
5. Run: pnpm remove reactflow
6. Run: pnpm build
7. Fix any build errors
8. Verify package.json no longer contains 'reactflow' (only '@xyflow/react')
```

## Acceptance Criteria

- [ ] `package.json` contains only `@xyflow/react`, no `reactflow`
- [ ] `pnpm build` succeeds with zero errors
- [ ] Visual builder (`/visual-builder`) renders correctly
- [ ] Nodes can be dragged and connected
- [ ] Bundle analyzer shows reduction in JS size (optional but ideal)

## Dependencies

None

## Notes

API surface between v11 and v12 is nearly identical. Most changes are just import path.
Potential gotcha: `MarkerType` enum may have changed. Test edge arrow rendering.
