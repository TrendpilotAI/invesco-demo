# TODO-337: DRY — Consolidate FilterContent Triplication

**Repo:** signal-builder-frontend  
**Priority:** P1 | **Effort:** S (2-4h)  
**Status:** pending

## Problem
FilterContent logic exists in 3 separate files:
- `src/modules/builder/containers/FlowNode/Filter/FilterContent.tsx`
- `src/modules/builder/containers/RightBar/Filter/FilterContent.tsx`
- `src/shared/ui/FilterContent/FilterContent.tsx`

Bug fixes and feature changes must be applied in 3 places. High drift risk.

## Task
1. Audit all 3 implementations to find the shared logic and view-specific divergence
2. Parameterize with `viewMode: 'node' | 'sidebar'` prop
3. Consolidate into `src/shared/ui/FilterContent/FilterContent.tsx`
4. Update all imports to point to shared version
5. Delete the two module-local copies

## Coding Prompt (for autonomous agent)
```
In /data/workspace/projects/signal-builder-frontend:
1. Read all 3 FilterContent implementations and diff their props/logic
2. Create a unified FilterContent in src/shared/ui/FilterContent/FilterContent.tsx
   with props including `viewMode: 'node' | 'sidebar'` to handle display differences
3. Replace imports in FlowNode.tsx and BuilderRightBar.tsx to use shared version
4. Delete src/modules/builder/containers/FlowNode/Filter/FilterContent.tsx
5. Delete src/modules/builder/containers/RightBar/Filter/FilterContent.tsx
6. Run: cd /data/workspace/projects/signal-builder-frontend && npm run typecheck && npm run lint
```

## Acceptance Criteria
- [ ] Single FilterContent implementation in shared/ui
- [ ] typecheck passes
- [ ] lint passes
- [ ] Visual behavior unchanged in both node and sidebar contexts
