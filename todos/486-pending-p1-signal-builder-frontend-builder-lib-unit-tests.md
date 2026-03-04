# TODO-486: Unit Tests for builder.lib.ts — Zero Coverage

**Project:** signal-builder-frontend
**Priority:** P1 (HIGH impact, M effort)
**Estimated Effort:** 4-6 hours
**Dependencies:** None

## Description

builder.lib.ts is the core business logic (graph manipulation, node operations, validation) with ZERO test coverage. This is the most critical file to test.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Add comprehensive unit tests for builder.lib.ts.

STEPS:
1. Read src/modules/builder/libs/ to understand all exported functions
2. Read src/redux/builder/ to understand data structures (node types, edge types, signal schema)

3. Create src/modules/builder/libs/__tests__/builder.lib.test.ts

4. Test categories:
   a. Node operations:
      - Create filter node, dataset node, group function node, target node
      - Delete node (verify edges cleaned up)
      - Update node properties
   
   b. Edge operations:
      - Connect two nodes
      - Validate connection rules (which node types can connect)
      - Delete edge
   
   c. Graph validation:
      - Valid complete signal graph
      - Missing required nodes
      - Circular dependencies
      - Disconnected nodes
   
   d. Signal serialization:
      - Graph → API payload conversion
      - API response → graph conversion
   
   e. Edge cases:
      - Empty graph
      - Single node
      - Maximum nodes/edges

5. Target: ≥80% coverage on builder.lib.ts
6. Run: pnpm test -- --coverage --collectCoverageFrom="src/modules/builder/libs/**"

CONSTRAINTS:
- Pure unit tests — no DOM, no React, no Redux store
- Use real data structures from redux/builder/types
- Each test should be independent
- Use descriptive test names: "should remove connected edges when deleting a node"
```

## Acceptance Criteria
- [ ] ≥30 unit tests for builder.lib.ts
- [ ] ≥80% line coverage on builder/libs/
- [ ] Tests cover node ops, edge ops, validation, serialization
- [ ] All tests pass: `pnpm test`
- [ ] No mock of internal functions (test real behavior)
