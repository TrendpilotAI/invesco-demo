---
status: pending
priority: high
issue_id: "010"
tags: [signal-builder-backend, testing, sql, translator, coverage]
dependencies: []
---

# TODO 010 — Signal SQL Translation Test Suite (Edge Cases)

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** L (3-5 days)

## Problem Statement

The signal-nodes-to-SQL translation engine is the core value driver of this product, yet test coverage for complex edge cases is shallow. The existing tests in `tests/translators/` cover basic happy paths but the TODOs in the code itself call out untested scenarios:

```python
# TODO: test group_functions:
# 1. without params (like count)
# 2. with different prop and param types
# 3. with date type
```

Untested edge cases include:
- Deeply nested filter trees (AND/OR with 3+ levels)
- Multiple datasets with conflicting column names
- Group functions with no parameters (COUNT)
- Date/time property types in filters and ordering
- Empty signal trees (no nodes)
- Signals with only ordering but no filters
- SQL injection-like strings in property names
- Very large node trees (20+ nodes)
- Circular-reference prevention in tree traversal

## Findings

- Translators live in `apps/translators/signal_data_translators/` with one file per translator type
- Tests live in `tests/translators/semantic_layer_translators/`
- `test_translate_signal_nodes_tree_to_semantic_layer.py` has only 1 test with `# TODO` markers
- `conftest.py` uses a fixture (`translator_manager`) that requires `@pytest.mark.with_db` — blocking fast unit tests
- Most translator logic is pure functional — could be tested without DB

## Proposed Solutions

### Option A: Pure Unit Tests (Recommended)
Extract translator logic into pure functions, mock DB calls, run fast unit tests. Add parameterized test cases for all edge cases.

**Pros:** Fast, isolated, no DB required  
**Cons:** Some refactoring needed

### Option B: Integration Tests Only
Add more `@pytest.mark.with_db` tests using fixtures.

**Pros:** Tests real DB round-trip  
**Cons:** Slow, requires DB setup in CI

**Recommendation:** Option A for edge case unit tests + keep existing integration tests

## Coding Prompt

```
You are adding comprehensive edge-case tests to the signal-builder-backend SQL translation engine.

Repository: /data/workspace/projects/signal-builder-backend/
Language: Python 3.11, pytest, pytest-asyncio

TASK: Add test files to tests/translators/ covering the following edge cases.

1. Read the existing test files:
   - tests/translators/test_translate_signal_nodes_tree_to_semantic_layer.py
   - tests/translators/conftest.py
   - tests/translators/semantic_layer_translators/test_filter_translations.py
   - tests/translators/semantic_layer_translators/test_group_function_translator.py
   - apps/translators/signal_data_translators/ (all translator files)

2. Create tests/translators/test_edge_cases.py with parameterized tests for:

   a) FILTER EDGE CASES:
      - AND/OR nesting 3+ levels deep
      - Single filter with NULL check ($operator: "is_null")
      - Filter with date type property (ISO 8601 string param)
      - Filter with empty string param
      - Filter with numeric zero param (not falsy check failure)
      - Filter on nested JSON property path

   b) GROUP FUNCTION EDGE CASES:
      - COUNT without parameters (no $property key)
      - SUM with integer vs float $param
      - GROUP_FUNCTION with date type property
      - Multiple group functions on same dataset

   c) ORDERING EDGE CASES:
      - Ordering with "least" direction
      - Ordering referencing a group_function result by alias
      - No ordering node at all

   d) DATASET EDGE CASES:
      - Multiple datasets with same column names (aliasing required)
      - Dataset with no filters or group functions
      - Dataset referencing non-existent table name

   e) TREE STRUCTURE EDGE CASES:
      - Empty node list (should raise TranslationError gracefully)
      - Tree with only $target and no datasets
      - Maximum depth nesting (10+ levels)

3. Create tests/translators/test_sql_output_validation.py:
   - For each edge case in (2), also validate the final SQL string output
   - Assert SQL contains expected keywords (JOIN, WHERE, GROUP BY, ORDER BY)
   - Assert SQL does not contain injection strings if malformed input provided
   - Use pytest.mark.parametrize for table-driven tests

4. Update tests/translators/conftest.py:
   - Add lightweight fixtures that do NOT require DB (mock the DB layer)
   - Use unittest.mock or pytest-mock to patch storage/query layers

5. Run: cd /data/workspace/projects/signal-builder-backend && python -m pytest tests/translators/ -v
   - All new tests must pass
   - No regressions in existing tests

6. Add coverage report: pytest --cov=apps/translators --cov-report=term-missing
   - Target: 70%+ coverage on translators module

Constraints:
- Do NOT change production code unless a bug is discovered
- Mark tests requiring DB with @pytest.mark.with_db
- Pure unit tests should run without any external services
- Use faker library (already in dev-packages) for generating test data
```

## Acceptance Criteria

- [ ] `tests/translators/test_edge_cases.py` created with 20+ parameterized test cases
- [ ] `tests/translators/test_sql_output_validation.py` validates final SQL output
- [ ] All tests pass with `pytest tests/translators/ -v`
- [ ] Coverage on `apps/translators/` reaches ≥70%
- [ ] COUNT (no-param) group function is explicitly tested
- [ ] Date-type properties are tested in filters and ordering
- [ ] 3-level deep AND/OR filter nesting is tested
- [ ] Empty tree edge case raises graceful error (not unhandled exception)
- [ ] No DB required for unit test suite (mock-based fixtures)

## Dependencies

None — can execute immediately.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Identified gap in translator test coverage from BRAINSTORM.md + code review
- Found inline `# TODO: test group_functions` comment in existing test file
- Scoped to pure unit tests + SQL output validation

**Learnings:**
- Most translator logic is pure functional — ideal for fast unit tests
- DB fixtures slow down CI; mocking is preferred for edge cases
