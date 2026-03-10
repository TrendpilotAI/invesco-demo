# TODO-888: Consolidate Duplicate FilterContent Components (DRY Violation)

**Repo:** signal-builder-frontend  
**Priority:** P2 (Medium)  
**Effort:** S (1 day)  
**Status:** pending

## Problem

`FilterContent` exists in two places:
1. `src/shared/ui/FilterContent/FilterContent.tsx` — shared UI component
2. `src/modules/builder/containers/RightBar/Filter/FilterContent.tsx` — module-specific copy

These likely started as the same component and diverged. Bug fixes must be applied twice. Any UI changes need to be duplicated.

## Coding Prompt

```
1. Read both FilterContent implementations:
   cat src/shared/ui/FilterContent/FilterContent.tsx
   cat src/modules/builder/containers/RightBar/Filter/FilterContent.tsx

2. Identify differences between the two (props, logic, styling).

3. Merge into src/shared/ui/FilterContent/FilterContent.tsx with variant props:
   interface FilterContentProps {
     variant?: 'inline' | 'sidebar';  // or whatever makes sense from the diff
     // ... other shared props
   }

4. Update src/modules/builder/containers/RightBar/Filter/FilterContent.tsx
   to re-export from shared:
   export { FilterContent } from '@shared/ui/FilterContent';
   OR simply delete the module-specific version and update all imports.

5. Run TypeScript: yarn typecheck
   Run tests: yarn test
   Verify no regressions.

6. Do the same analysis for FilterRow if it's also duplicated:
   grep -r "FilterRow" src/ --include="*.tsx"
```

## Acceptance Criteria
- [ ] Single FilterContent implementation exists
- [ ] Module-specific copy deleted or re-exports from shared
- [ ] All imports updated to use single source
- [ ] TypeScript compiles without errors
- [ ] No visual regressions (run Storybook to verify)
- [ ] Bug fixes only need to be made once
