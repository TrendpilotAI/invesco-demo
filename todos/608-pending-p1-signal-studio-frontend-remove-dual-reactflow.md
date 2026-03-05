# TODO-608: Remove Dual ReactFlow Dependency (~400KB Bundle Reduction)

**Repo:** signal-studio-frontend  
**Priority:** P1 (Performance)  
**Effort:** S (4-8 hours)  
**Status:** pending

## Description

package.json has both `reactflow` (v11) and `@xyflow/react` (v12). They're different packages with different APIs but similar functionality. This adds ~400KB to the bundle unnecessarily. Migrate everything to `@xyflow/react` v12 and remove `reactflow` v11.

## Acceptance Criteria
- [ ] `reactflow` removed from package.json
- [ ] All imports updated from `reactflow` to `@xyflow/react`
- [ ] API differences between v11 and v12 resolved (check node/edge type changes)
- [ ] Visual builder still works (flow-editor, reactflow-editor)
- [ ] Bundle size reduced by ~400KB (verify with `next build` output)

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend:

1. Run: grep -r "from 'reactflow'" --include="*.ts" --include="*.tsx" . | grep -v node_modules
2. For each file, update imports to use @xyflow/react
3. Check v11→v12 API differences: https://reactflow.dev/learn/troubleshooting/migrate-to-v12
   Key changes: ReactFlowProvider import, nodeTypes registration, edge handling
4. Run npm install to update lock file
5. Remove reactflow: "^11.x" from package.json dependencies
6. Run npm run build and verify no errors
7. Test visual builder in browser
```

## Dependencies
- None (standalone refactor)
