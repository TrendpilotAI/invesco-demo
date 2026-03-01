# TODO-352: Remove Duplicate ReactFlow Package

**Priority:** P0 (Critical - Bundle Bloat)
**Effort:** M
**Repo:** signal-studio
**Status:** pending

## Description
Both `reactflow@^11.11.4` AND `@xyflow/react@^12.9.0` are installed. These are the same library (v11 vs v12 rebrand). Doubles ReactFlow bundle size (~300KB duplicate).

## Coding Prompt
```
In /data/workspace/projects/signal-studio:
1. Find all files importing from 'reactflow':
   grep -rn "from 'reactflow'" components/ app/ lib/ --include="*.ts" --include="*.tsx"
   grep -rn 'from "reactflow"' components/ app/ lib/ --include="*.ts" --include="*.tsx"

2. For each file found, update imports:
   - Old: import { X } from 'reactflow'
   - New: import { X } from '@xyflow/react'
   Note: Check API compatibility between v11 and v12 — some APIs changed (e.g. ReactFlowProvider, useNodes, etc.)
   Ref: https://reactflow.dev/whats-new/v12

3. Remove the old package:
   pnpm remove reactflow

4. Run pnpm build to verify no import errors

5. Test the visual builder at /signals/canvas to confirm ReactFlow still works

6. Commit: "perf(deps): remove duplicate reactflow v11, migrate to @xyflow/react v12 (~300KB bundle reduction)"
```

## Dependencies
- TODO-351 (fix TypeScript errors first so migrations are visible)

## Acceptance Criteria
- `package.json` has no `reactflow` entry
- All imports use `@xyflow/react`
- Visual builder loads without errors
- Bundle analyzer shows ~300KB reduction
