# 237 · P2 · signal-builder-frontend · DRY: Consolidate Filter Tree Logic

## Status
pending

## Priority
P2 — Same filter update pattern repeated in 3+ locations; `JSON.parse/stringify` deep clones are slow and error-prone

## Description
The `REPEATING_FILTER_VALUE_PROCESSING` pattern (identified by the developers themselves with a TODO) exists in 3 locations. Filter tree manipulation uses `JSON.parse(JSON.stringify(...))` for deep clones. This task consolidates all filter logic and replaces deep clone with `structuredClone()`.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Audit all filter manipulation locations
grep -rn "replaceFilterRuleById\|REPEATING_FILTER_VALUE_PROCESSING\|JSON.parse(JSON.stringify" src/ --include="*.ts" --include="*.tsx"

Step 2: Create shared filter utility at `src/shared/lib/filterTree.ts`
```typescript
import { TFilterGroup, TFilterRule } from 'redux/builder/types';

/**
 * Deep clone a filter tree using structuredClone (faster + safer than JSON.parse/stringify)
 */
export const cloneFilterTree = <T>(tree: T): T => structuredClone(tree);

/**
 * Find a filter rule by ID in a tree (recursive)
 */
export const findFilterRuleById = (
  group: TFilterGroup,
  id: string
): TFilterRule | undefined => {
  const inRules = group.rules.find(r => r.id === id);
  if (inRules) return inRules;
  for (const subGroup of group.groups) {
    const found = findFilterRuleById(subGroup, id);
    if (found) return found;
  }
  return undefined;
};

/**
 * Replace a filter rule by ID, returning a new tree (immutable)
 */
export const replaceFilterRuleById = (
  group: TFilterGroup,
  id: string,
  newRule: TFilterRule
): TFilterGroup => {
  return {
    ...group,
    rules: group.rules.map(r => r.id === id ? newRule : r),
    groups: group.groups.map(g => replaceFilterRuleById(g, id, newRule)),
  };
};

/**
 * Delete a filter rule by ID, returning a new tree (immutable)
 */
export const deleteFilterRuleById = (
  group: TFilterGroup,
  id: string
): TFilterGroup => {
  return {
    ...group,
    rules: group.rules.filter(r => r.id !== id),
    groups: group.groups.map(g => deleteFilterRuleById(g, id)),
  };
};

/**
 * Apply a filter rule update and call the signal node modifier
 * Consolidates the REPEATING_FILTER_VALUE_PROCESSING pattern
 */
export const applyFilterRuleUpdate = (
  nodeData: TNodeData,
  filterId: string,
  newFilterData: TFilterRule,
  modifySignalNode: (data: TNodeData) => void
): void => {
  const updatedFilter = replaceFilterRuleById(
    nodeData.value?.filter,
    filterId,
    newFilterData
  );
  modifySignalNode({
    ...nodeData,
    nodeType: ESignalNodeTypes.FILTER,
    value: { filter: updatedFilter },
  });
};
```

Step 3: Replace `JSON.parse(JSON.stringify(...))` occurrences
Find all occurrences: grep -rn "JSON.parse(JSON.stringify" src/
Replace each with `structuredClone(...)`:
```typescript
// Before:
const copy = JSON.parse(JSON.stringify(filterGroup));
// After:
const copy = structuredClone(filterGroup);
```

Step 4: Update call sites to use the shared utility
In each of the 3+ locations where `REPEATING_FILTER_VALUE_PROCESSING` appears:
1. `src/modules/builder/containers/FlowNode/Filter/components/FilterRule/FilterRule.tsx`
2. `src/modules/builder/containers/RightBar/Filter/filter.helpers.ts`
3. `src/modules/builder/containers/RightBar/Filter/components/InOperatorForm/InOperatorForm.tsx`

Replace duplicated pattern with:
```typescript
import { applyFilterRuleUpdate } from 'shared/lib/filterTree';
// ...
applyFilterRuleUpdate(data, filter.id, filterData, modifySignalNodeHook);
```

Step 5: Delete the `SearchDropdown` if only used minimally
Per brainstorm: `SearchDropdown.tsx` has a TODO to use the base `Dropdown` component.
Check usage: grep -rn "SearchDropdown" src/
If ≤3 usages: extend `Dropdown` with `searchable` prop and migrate call sites.

Step 6: Write unit tests for new shared utilities
Create `src/shared/lib/filterTree.test.ts`:
- Test all 4 exported functions
- Verify immutability (original not mutated)
- Verify nested group traversal works correctly

Commit: "refactor: consolidate filter tree logic into shared utility, replace JSON clone with structuredClone"
```

## Dependencies
- 231 (builder.lib tests) — validates that the consolidation doesn't break existing behavior

## Effort Estimate
M (1–2 days)

## Acceptance Criteria
- [ ] `src/shared/lib/filterTree.ts` exists with all tree operation utilities
- [ ] Zero `JSON.parse(JSON.stringify` in filter-related files
- [ ] The `REPEATING_FILTER_VALUE_PROCESSING` pattern exists in exactly 1 place (the shared util)
- [ ] `filterTree.test.ts` with passing tests for all 4 utilities
- [ ] Existing filter functionality works after refactor (manual smoke test)
