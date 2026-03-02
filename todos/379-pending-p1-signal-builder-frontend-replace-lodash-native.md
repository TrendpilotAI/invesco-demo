# TODO-379: Replace Lodash Full Bundle with Native Equivalents

**Repo:** signal-builder-frontend  
**Priority:** P1 (High)  
**Effort:** M (Medium, ~4 hrs)  
**Created:** 2026-03-02

## Description

28 files import from the full `lodash` package. Since Vite tree-shakes ES modules but NOT CommonJS, the full lodash bundle (~70KB gzip) is included in production even for a single `capitalize` call.

**Affected production files (18):**

| File | Import |
|------|--------|
| `src/shared/widgets/Navigation/Navigation.tsx` | `capitalize` |
| `src/shared/ui/Checkbox/Checkbox.tsx` | `uniqueId` |
| `src/shared/ui/ChipsInput/MainInput.tsx` | `isEmpty` |
| `src/shared/ui/SearchDropdown/SearchDropdown.tsx` | `isEmpty` |
| `src/modules/builder/hooks/builder.hook/builder.hook.schema.ts` | `flatMap, isEmpty` |
| `src/modules/builder/hooks/builder.hook/builder.hook.signalNodes.ts` | `get` |
| `src/modules/builder/containers/Main/Flow.tsx` | `isEmpty` |
| `src/modules/builder/containers/Builder.container.tsx` | `isEmpty` |
| `src/modules/builder/containers/FlowNode/FlowNode.tsx` | `isEmpty, isEqual` |
| `src/modules/builder/containers/FlowNode/GroupFunction/GroupFunctionContent.tsx` | `isArray` |
| `src/modules/builder/containers/FlowNode/Filter/components/AddFilterItemButton/AddFilterItemButton.tsx` | `capitalize` |
| `src/modules/builder/containers/FlowNode/Filter/components/FilterRow/FilterRow.tsx` | `isEmpty` |
| `src/modules/builder/containers/FlowNode/Filter/components/FilterRule/FilterRule.tsx` | `upperCase` |
| `src/modules/builder/containers/RightBar/Filter/FilterContent.tsx` | `upperCase` |
| `src/modules/builder/containers/RightBar/Filter/components/TextOperatorForm/BaseTextOperatorForm.tsx` | `isEmpty` |
| `src/modules/builder/containers/RightBar/Filter/components/InOperatorForm/InOperatorForm.tsx` | `isEqual` |
| `src/modules/builder/containers/RightBar/Filter/components/FilterPropertySelectView/FilterParamSelectView.tsx` | `isEmpty` |
| `src/modules/builder/containers/Header/Preview/ExportModal.tsx` | `isEmpty` |
| `src/modules/builder/containers/Header/Preview/Preview.container.tsx` | `isEmpty, isEqual` |
| `src/modules/builder/containers/Header/PublishModal/PublishModal.container.tsx` | `isEmpty` |
| `src/modules/builder/libs/builder.lib.helpers.ts` | `isEmpty` |
| `src/modules/builder/libs/builder.lib.drawing.ts` | `get, isEmpty, max` |
| `src/modules/collections/containers/Tab/Tab.tsx` | `capitalize` |

## Native Replacements

- `isEmpty(v)` → `!v || v.length === 0 || Object.keys(v).length === 0`
- `capitalize(s)` → `s.charAt(0).toUpperCase() + s.slice(1).toLowerCase()`
- `upperCase(s)` → `s.toUpperCase()`
- `isArray(v)` → `Array.isArray(v)`
- `flatMap(arr, fn)` → `arr.flatMap(fn)`
- `get(obj, path)` → optional chaining `obj?.a?.b`
- `uniqueId()` → `crypto.randomUUID()` or React 18 `useId()`
- `isEqual(a, b)` → install `dequal` (1KB) or `fast-deep-equal`
- `max(arr)` → `Math.max(...arr)`

## Coding Prompt

```
In /data/workspace/projects/signal-builder-frontend/:

1. Run: grep -r "from 'lodash'" src/ --include="*.ts" --include="*.tsx" -l
2. For each production file (not test/stories), replace lodash imports with:
   - Native JS equivalents where possible (see replacements above)
   - For `isEqual`, add `dequal` package: yarn add dequal
3. Remove `lodash` from dependencies in package.json if all production uses removed
4. Keep lodash in devDependencies only if test/stories files still need it
5. Run: yarn build && yarn test to verify nothing breaks
6. Run bundle analyzer to confirm size reduction
```

## Acceptance Criteria
- No production files import from `lodash` (CJS)
- Build succeeds, all tests pass
- Bundle size reduced by ~50-70KB gzip
- `isEqual` uses `dequal` or native `JSON.stringify` comparison
