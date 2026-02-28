# TODO-311: Remove Duplicate ReactFlow Package

**Repo:** signal-studio
**Priority:** P1
**Effort:** M (2-4 hours)
**Status:** pending

## Description
Both `reactflow@^11.11.4` AND `@xyflow/react@^12.9.0` are installed in package.json.
These are the same library — `@xyflow/react` is the v12 rebrand of `reactflow`.
Having both doubles the bundle size (~300KB wasted).

## Acceptance Criteria
- `reactflow` removed from package.json dependencies
- All imports migrated from `reactflow` to `@xyflow/react`
- Visual builder still works (ReactFlow nodes render correctly)
- Bundle size reduced by ~150-300KB

## Coding Prompt
```
1. Search for all files importing from 'reactflow':
   grep -rn "from 'reactflow'" /data/workspace/projects/signal-studio/components/ /data/workspace/projects/signal-studio/app/ --include="*.ts" --include="*.tsx"

2. For each file, replace:
   - `from 'reactflow'` → `from '@xyflow/react'`
   - `import 'reactflow/dist/style.css'` → `import '@xyflow/react/dist/style.css'`

3. Remove from package.json:
   "reactflow": "^11.11.4"

4. Run: cd /data/workspace/projects/signal-studio && pnpm install

5. Test: pnpm build (should succeed)

Note: @xyflow/react v12 API is mostly compatible with reactflow v11 but check:
- `ReactFlowProvider` import
- `useReactFlow` hook
- `Node`, `Edge` type imports
```

## Dependencies
- None

## Notes
AUDIT.md DEP-002
