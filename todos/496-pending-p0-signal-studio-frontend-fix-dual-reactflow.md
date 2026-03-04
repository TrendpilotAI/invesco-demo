# TODO-496: Remove Duplicate ReactFlow Dependency

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (2-3 hours)  
**Status:** pending

## Description
`package.json` contains both `reactflow@^11.11.4` (old) and `@xyflow/react@^12.9.0` (new). These are the same library — XYFlow rebranded. This causes double bundle size (~400KB wasted) and potential type conflicts.

## Coding Prompt
1. `grep -r "from 'reactflow'" app/ components/ lib/ --include="*.tsx" --include="*.ts"` — find all old imports
2. Update all old imports: `from 'reactflow'` → `from '@xyflow/react'`
3. Update type references: `ReactFlowInstance` → `ReactFlowInstance` (same in v12, but verify)
4. Remove `reactflow` from `package.json` dependencies
5. Run `pnpm install` to update lockfile
6. Run `pnpm build` to verify no breaking changes
7. Test visual builder at `/visual-builder/builder`

## Acceptance Criteria
- [ ] No `reactflow` in package.json
- [ ] `pnpm build` succeeds
- [ ] Visual builder renders correctly
- [ ] Bundle size reduced (verify with `pnpm build --analyze` or next-bundle-analyzer)
