---
status: pending
priority: p1
issue_id: "200"
tags: [testing, typescript, signal-builder-frontend, react, jest]
dependencies: []
---

# 200 — Unit Tests: `builder.lib.ts` Filter Tree Functions

## Problem Statement

The core signal serialization logic in `src/modules/builder/libs/builder.lib.ts` has **zero test coverage**. This file contains deeply recursive tree operations (`replaceFilterRuleById`, `findFilterById`, `findFilterGroupByRuleId`, `deleteFilterById`, `prepareFilterData`, `generateNewTab`) that are central to how signals are built and persisted. A silent bug here would corrupt saved signals without any visible error.

## Findings

- `builder.lib.ts` contains: `replaceFilterRuleById`, `findFilterById`, `findFilterGroupByRuleId`, `deleteFilterById`, `prepareFilterData`, `findLastFilter`, `generateNewTab`, `generateFilterGroup`, `generateFilterRule`
- All recursive tree operations use `JSON.parse(JSON.stringify(...))` for deep cloning — fragile and slow
- `prepareFilterData` has a `// TODO: duplicated functionality` comment
- `replaceFilterRuleById` and `deleteFilterById` accept `any` typed sub-filters, bypassing TypeScript safety
- Existing tests only cover UI components in `src/shared/ui/` (Button, Checkbox, Icon, Popover, Radio)

## Proposed Solutions

### Option A: Jest unit tests in-place (Recommended)
Create `src/modules/builder/libs/builder.lib.test.ts` with full coverage of all exported functions.
- **Pros:** Low setup overhead, matches existing test tooling (Jest via CRA/CRACO)
- **Cons:** None
- **Effort:** M (~4-6h)
- **Risk:** Low

### Option B: Property-based testing with fast-check
Use `fast-check` to generate random filter trees and verify invariants.
- **Pros:** Catches edge cases automatically
- **Cons:** Additional dependency, more complex setup
- **Effort:** L
- **Risk:** Medium (team familiarity)

## Recommended Action

Implement Option A. Create comprehensive Jest unit tests for all exported functions in `builder.lib.ts`.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Create unit tests for src/modules/builder/libs/builder.lib.ts

1. Create the file: src/modules/builder/libs/builder.lib.test.ts

2. Import the functions to test:
   import {
     generateNewTab,
     generateFilterGroup,
     generateFilterRule,
     replaceFilterRuleById,
     findFilterById,
     findFilterGroupByRuleId,
     deleteFilterById,
     prepareFilterData,
     findLastFilter,
     EFilterOperatorKeys,
     BOOLEAN_FILTER_OPERATOR_KEYS,
   } from './builder.lib';
   import { EFilterConjunction, EFilterType } from 'src/redux/builder/types';

3. Write the following test suites:

describe('generateFilterRule', () => {
  it('creates a filter rule with default null values')
  it('creates a filter rule with provided values')
  it('generates unique IDs for each rule')
})

describe('generateFilterGroup', () => {
  it('creates a filter group with correct conjunction and filters')
  it('generates unique IDs for each group')
})

describe('replaceFilterRuleById', () => {
  it('replaces a rule at root level when IDs match')
  it('replaces a rule nested 3 levels deep')
  it('returns original tree unchanged if id not found')
  it('handles empty filter groups gracefully')
})

describe('findFilterById', () => {
  it('returns the filter at root level by id')
  it('finds a deeply nested filter by id')
  it('returns null when filter not found')
  it('handles filter_rule type correctly')
})

describe('findFilterGroupByRuleId', () => {
  it('returns the parent filter group containing the rule')
  it('finds nested group containing rule')
  it('returns null when rule not in any group')
})

describe('deleteFilterById', () => {
  it('removes a filter rule at root level')
  it('removes a filter rule from nested group')
  it('returns undefined when deleting the root filter')
  it('removes entire group when last child is deleted')
})

describe('prepareFilterData', () => {
  it('strips incomplete filter rules (isFilterRuleIncomplete returns true)')
  it('remaps PLAIN_PROPERTY_TYPES correctly to PLAIN_PROPERTY_TYPE')
  it('returns undefined for empty filter groups after stripping')
  it('preserves complete filter rules unchanged')
  it('handles deeply nested mixed groups')
})

describe('generateNewTab', () => {
  it('returns copy of currentTab when currentNodeData is undefined')
  it('adds new node to tab on non-delete operation')
  it('removes node hints on delete operation')
})

4. Use realistic TFilter/TFilterGroup/TFilterRule fixtures that match the actual TypeScript types
5. Ensure all tests pass: cd /data/workspace/projects/signal-builder-frontend && yarn test src/modules/builder/libs/builder.lib.test.ts --watchAll=false
6. Aim for >= 90% branch coverage of builder.lib.ts
```

## Dependencies

None — this can be implemented immediately.

## Estimated Effort

**Medium** — 4-6 hours

## Acceptance Criteria

- [ ] File `src/modules/builder/libs/builder.lib.test.ts` exists
- [ ] All test suites listed in the coding prompt are implemented
- [ ] `yarn test src/modules/builder/libs/builder.lib.test.ts --watchAll=false` passes with 0 failures
- [ ] Branch coverage for `builder.lib.ts` is ≥ 90%
- [ ] Tests cover both happy paths and edge cases (empty inputs, not-found IDs, deeply nested structures)
- [ ] No test uses `any` type assertions without justification

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Analyzed builder.lib.ts structure and identified untested functions
- Designed test suite covering all exported functions
- Confirmed Jest is available via CRACO test runner

**Learnings:**
- The recursive filter tree functions are the highest-risk untested code in the repo
- `JSON.parse/JSON.stringify` deep cloning in these functions is fragile — tests will expose this
