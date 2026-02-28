# 235 · P1 · signal-builder-frontend · Fix @ts-ignore Suppressors & Circular Imports

## Status
pending

## Priority
P1 — 11 @ts-ignore + ESLint no-cycle suppressed on Redux files = hidden type errors + circular dep bugs

## Description
The codebase has 11 `@ts-ignore` suppressors hiding real type mismatches and ESLint `import/no-cycle` suppressed on `rootReducer.ts` and `store.tsx` indicating real circular dependencies. Both categories can cause hard-to-debug runtime errors.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: List all @ts-ignore locations
grep -rn "@ts-ignore" src/ --include="*.ts" --include="*.tsx"

Known locations (from audit):
1. src/shared/ui/ChipsInput/ChipsItem.tsx:35 — event handler type
2. src/modules/builder/hooks/builder.hook/builder.hook.tabs.ts:83 — selectActiveTab return type
3. src/modules/builder/containers/RightBar/Dataset/DatasetContent.tsx:81 — JSX comment
4. src/modules/builder/libs/builder.lib.ts:383 — filter.id access
5. src/modules/onboarding/hooks/onboarding.hook.ts:208, 218 — nodeData.id.includes
6. src/modules/onboarding/steps/actions.lib.ts:540, 551, 567, 596 — DOM hacks
7. src/modules/onboarding/helpers.ts:128 — unknown type

Step 2: Fix each @ts-ignore with proper typing

For ChipsItem.tsx:35:
  Read the line. The event handler likely needs `React.ChangeEvent<HTMLInputElement>` or similar.
  Remove @ts-ignore and add proper type annotation.

For builder.hook.tabs.ts:83 — selectActiveTab:
  Find the selector definition. If it returns `TTab | undefined`, update the consuming code:
  const activeTab = useAppSelector(selectActiveTab);
  if (!activeTab) return null; // guard instead of ignore

For builder.lib.ts:383 — filter.id:
  Add proper type guard: if ('id' in filter) { ... }

For onboarding hooks — nodeData.id.includes:
  Add type guard: if (typeof nodeData.id === 'string') { ... }

For actions.lib.ts DOM hacks:
  These are intentional DOM manipulations. Replace @ts-ignore with:
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error - Native input value setter required for React synthetic event dispatch
  This is more explicit and self-documenting.

Step 3: Fix circular imports in Redux

Read src/redux/rootReducer.ts and src/redux/store.tsx
Common fix patterns:
A) Move shared types to a separate `src/redux/types.ts` file
B) Use dynamic imports or factory functions to break initialization cycles
C) Extract slice type definitions from slice implementation files

The goal: remove the `// eslint-disable-next-line import/no-cycle` comments by fixing the actual cycles.

Step 4: Fix ESLint suppressors in component files
For each file suppressing `@typescript-eslint/no-unused-vars`:
  - Run the file through ESLint to see what's actually unused
  - Remove unused imports/variables
  - Remove the suppressor comment

For `react/no-unstable-nested-components` in Table.tsx and Select.tsx:
  - Extract nested component definitions to module-level functions
  - Pass props explicitly

Step 5: Verify
yarn lint --max-warnings=0
yarn typecheck

Commit: "refactor: fix @ts-ignore suppressors, resolve circular imports, remove ESLint suppressors"
```

## Dependencies
- 229 (type system improvements) — do that first to make some of these fixes easier

## Effort Estimate
M (1–2 days)

## Acceptance Criteria
- [ ] Zero `@ts-ignore` in codebase (or replaced with `@ts-expect-error` with explanation)
- [ ] `import/no-cycle` rule no longer suppressed in rootReducer.ts and store.tsx
- [ ] No file-level ESLint suppressors for `no-unused-vars` or `no-unstable-nested-components`
- [ ] `yarn lint` passes clean
- [ ] `yarn typecheck` passes clean
