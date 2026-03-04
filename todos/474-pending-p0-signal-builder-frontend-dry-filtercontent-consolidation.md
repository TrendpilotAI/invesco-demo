# TODO-474: DRY — Consolidate 3x FilterContent into shared/ui

**Project:** signal-builder-frontend
**Priority:** P0 (HIGH impact, S effort)
**Estimated Effort:** 2-3 hours
**Dependencies:** None (standalone refactor)

## Description

Three separate FilterContent implementations exist:
1. `src/modules/builder/containers/FlowNode/Filter/FilterContent.tsx` (node inline view)
2. `src/modules/builder/containers/RightBar/Filter/FilterContent.tsx` (sidebar detail view)
3. `src/shared/ui/FilterContent/FilterContent.tsx` (shared — possibly the original)

Consolidate into a single parameterized component at `src/shared/ui/FilterContent/FilterContent.tsx` with a `viewMode: 'node' | 'sidebar'` prop to handle layout differences.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Consolidate 3 duplicate FilterContent components into one.

STEPS:
1. Read all three FilterContent files:
   - src/modules/builder/containers/FlowNode/Filter/FilterContent.tsx
   - src/modules/builder/containers/RightBar/Filter/FilterContent.tsx
   - src/shared/ui/FilterContent/FilterContent.tsx

2. Diff them to identify:
   - Shared logic (likely 80%+ identical)
   - View-specific differences (node compact vs sidebar expanded)

3. Create a unified FilterContent in src/shared/ui/FilterContent/FilterContent.tsx:
   - Add a `viewMode: 'node' | 'sidebar'` prop
   - Use conditional rendering/styling for layout differences
   - Export from src/shared/ui/FilterContent/index.ts

4. Update all import sites:
   - src/modules/builder/containers/FlowNode/Filter/ — import from @shared/ui/FilterContent, pass viewMode='node'
   - src/modules/builder/containers/RightBar/Filter/ — import from @shared/ui/FilterContent, pass viewMode='sidebar'

5. Delete the two redundant FilterContent.tsx files (FlowNode and RightBar versions)

6. Run: pnpm typecheck && pnpm lint && pnpm test
7. Verify no broken imports: grep -r "FilterContent" src/ to confirm all point to shared/ui

CONSTRAINTS:
- Do NOT change any FilterContent behavior or visual output
- Keep all existing props and interfaces
- Ensure both view modes render identically to their originals
```

## Acceptance Criteria
- [ ] Only ONE FilterContent.tsx exists (in shared/ui)
- [ ] `viewMode` prop controls node vs sidebar rendering
- [ ] All imports updated across codebase
- [ ] `pnpm typecheck` passes
- [ ] `pnpm test` passes
- [ ] Visual output unchanged in both contexts
