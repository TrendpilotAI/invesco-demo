# 231 · P1 · signal-builder-frontend · Unit Tests for builder.lib.ts (Core Signal Logic)

## Status
pending

## Priority
P1 — CRITICAL: Zero tests on core signal serialization logic; bugs here silently corrupt signals

## Description
`src/modules/builder/libs/builder.lib.ts` contains deeply recursive filter tree functions that are the heart of signal serialization. A single bug corrupts saved signals silently. This task creates comprehensive unit tests using the installed Jest + React Testing Library setup.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Read the source files to understand the function signatures:
- src/modules/builder/libs/builder.lib.ts
- src/modules/builder/libs/builder.lib.helpers.ts
- src/modules/builder/libs/builder.lib.drawing.ts

Step 2: Create `src/modules/builder/libs/builder.lib.test.ts`

Test all exported pure functions with edge cases. Use the patterns:
```typescript
import {
  replaceFilterRuleById,
  findFilterById,
  findFilterGroupByRuleId,
  deleteFilterById,
  prepareFilterData,
  generateNewTab,
  updateNodes,
  updateEdges,
} from './builder.lib';
import { ESignalNodeTypes } from 'redux/builder/types';

// Build fixture factories for TFilterGroup, TFilterRule, TNodeData, TTab
const makeFilterRule = (id: string, overrides = {}): TFilterRule => ({
  id,
  prop_type: 'QUANTITATIVE',
  property: 'revenue',
  operator: 'GREATER_THAN',
  value: '100',
  param_type: null,
  ...overrides,
});

const makeFilterGroup = (id: string, rules: TFilterRule[] = []): TFilterGroup => ({
  id,
  condition: 'AND',
  rules,
  groups: [],
});

describe('replaceFilterRuleById', () => {
  it('replaces a rule at root level', () => { ... });
  it('replaces a rule nested 3 levels deep', () => { ... });
  it('returns original tree if id not found', () => { ... });
  it('handles empty rule array', () => { ... });
});

describe('findFilterById', () => {
  it('finds rule at root level', () => { ... });
  it('finds rule nested in group', () => { ... });
  it('returns undefined if not found', () => { ... });
});

describe('deleteFilterById', () => {
  it('deletes a rule at root level', () => { ... });
  it('deletes a rule nested in sub-group', () => { ... });
  it('does not mutate the original tree', () => {
    const original = makeFilterGroup('g1', [makeFilterRule('r1')]);
    const result = deleteFilterById(original, 'r1');
    expect(original.rules).toHaveLength(1); // not mutated
    expect(result.rules).toHaveLength(0);
  });
});

describe('prepareFilterData', () => {
  it('strips filter rules with no value set', () => { ... });
  it('remaps PLAIN_PROPERTY_TYPES correctly', () => { ... });
  it('returns undefined for empty filter groups', () => { ... });
  it('handles deeply nested groups', () => { ... });
});

describe('generateNewTab', () => {
  it('creates a tab with correct initial nodes', () => { ... });
  it('preserves existing nodes when updating', () => { ... });
});
```

Step 3: Create `src/modules/builder/libs/builder.lib.helpers.test.ts`
Test `getNodeTypeFromId`, `hasSignalNodeHint`, and other exported helpers.

Step 4: Create `src/modules/builder/libs/builder.lib.drawing.test.ts`
Test canvas layout calculation functions.

Step 5: Run tests and fix failures:
yarn test --testPathPattern="builder.lib" --watchAll=false

Ensure all tests pass. Aim for >90% line coverage on builder.lib.ts.
Commit: "test: add unit tests for builder.lib.ts core signal logic"
```

## Dependencies
- None (pure function tests, no backend needed)

## Effort Estimate
M (1–2 days)

## Acceptance Criteria
- [ ] `builder.lib.test.ts` exists with >15 test cases
- [ ] All tree operations tested: find, replace, delete, nested variants
- [ ] `prepareFilterData` tested with all known PLAIN_PROPERTY_TYPES
- [ ] Immutability verified (original not mutated by any function)
- [ ] `yarn test --testPathPattern="builder.lib"` passes 100%
- [ ] Coverage report shows >85% for `builder.lib.ts`
