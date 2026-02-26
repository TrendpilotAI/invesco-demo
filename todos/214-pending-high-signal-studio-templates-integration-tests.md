# 214 — Integration Tests: Mock DataProvider, Test execute() End-to-End, SQL + Validation Edge Cases

**Priority:** high  
**Project:** signal-studio-templates  
**Repo:** /data/workspace/projects/signal-studio-templates/  
**Status:** pending  
**Estimated Effort:** 4h  

---

## Context

The signal-studio-templates TemplateEngine has no integration tests. With 20 templates each executing SQL against Invesco's analytical database, untested code changes risk producing incorrect signals or crashing production. A mock DataProvider enables safe end-to-end testing of the full execute() path without hitting real databases.

---

## Task Description

1. Install test dependencies:
   ```bash
   npm install --save-dev jest @types/jest ts-jest
   ```
2. Configure `jest.config.js` for TypeScript with ts-jest.
3. Add `"test": "jest"` and `"test:coverage": "jest --coverage"` scripts to `package.json`.
4. Create `src/__mocks__/DataProvider.mock.ts` — a mock DataProvider that:
   - Accepts a fixture map of `{ sql: string } → rows: Record<string, unknown>[]`
   - Validates that queries are parameterized (no raw user values in SQL string)
   - Records all queries executed (for assertion)
   - Simulates connection errors on demand
5. Write integration tests in `src/__tests__/`:
   - `template-engine.test.ts` — test TemplateEngine loads all 20 templates, execute() returns expected shape
   - `sql-generation.test.ts` — for each template, generateSQL() with valid params produces valid ParameterizedQuery, with invalid params throws
   - `validation.test.ts` — edge cases: missing required params, out-of-range values, wrong types
   - `error-handling.test.ts` — DataProvider connection failure, query timeout, malformed results
6. Achieve ≥80% code coverage across all template files.

---

## Coding Prompt (Autonomous Agent)

```
You are writing integration tests for signal-studio-templates.

REPO: /data/workspace/projects/signal-studio-templates/

Steps:
1. Run: npm install --save-dev jest @types/jest ts-jest
2. Create jest.config.js:
   module.exports = {
     preset: 'ts-jest',
     testEnvironment: 'node',
     testMatch: ['**/__tests__/**/*.test.ts'],
     collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts'],
     coverageThreshold: { global: { branches: 70, functions: 80, lines: 80, statements: 80 } },
   };
3. Add to package.json scripts:
   "test": "jest",
   "test:coverage": "jest --coverage",
   "test:watch": "jest --watch"
4. Read all source files in src/ to understand the DataProvider interface and TemplateEngine API
5. Create src/__mocks__/MockDataProvider.ts implementing the DataProvider interface with:
   - In-memory fixture map
   - Query recorder (this.executedQueries array)
   - simulateError() method
6. Write src/__tests__/template-engine.test.ts:
   - Test: TemplateEngine initializes with all templates registered
   - Test: execute() with MockDataProvider returns { data: rows[], metadata: {...} }
   - Test: execute() with unknown templateId throws TemplateNotFoundError
7. Write src/__tests__/sql-generation.test.ts:
   - For each of the 20 templates, call generateSQL() with valid fixture params
   - Assert result has { sql: string, params: unknown[] } shape
   - Assert no user values appear literally in sql string
   - Call generateSQL() with missing required params, assert throws
8. Write src/__tests__/validation.test.ts:
   - Test each template's parameter validation schema
   - Edge cases: null, undefined, empty string, negative numbers, future dates
9. Run: npm test
10. Fix all test failures
11. Run: npm run test:coverage
12. Report: test count, pass/fail, coverage percentage per file
```

---

## Dependencies

- **211** (build must work)
- **213** (SQL hardening — tests should validate the new parameterized approach)

---

## Acceptance Criteria

- [ ] `jest.config.js` exists and `npm test` runs without configuration errors
- [ ] ≥ 20 test cases covering all 20 templates' execute() paths
- [ ] ≥80% line coverage across `src/`
- [ ] All tests pass (exit code 0)
- [ ] MockDataProvider records executed queries — tests assert queries are parameterized
- [ ] Edge case tests: missing params, wrong types, out-of-range values all throw with descriptive errors
- [ ] `npm run test:coverage` generates coverage report in `coverage/`
