# 318 — Test Coverage: 80%+ (SQL Safety, Schema, TemplateEngine, REST API)

**Priority:** HIGH  
**Effort:** M  
**Status:** pending

---

## Task Description

Current test coverage is estimated at ~20%. The repo needs comprehensive unit and integration tests before features are added or Invesco goes live. Target: 80%+ coverage overall, 100% on SQL safety utils and schema validation.

---

## Autonomous Coding Prompt

```
REPO: /data/workspace/projects/signal-studio-templates

TASK: Achieve 80%+ test coverage. Write unit, integration, and contract tests.

PREREQUISITE: TODO 315 (SQL injection fix) should be merged first so tests validate
the parameterized query implementation, not the broken interpolation.

STEPS:

1. Audit existing tests:
   - List all files in tests/ or __tests__/ directories
   - Run: pnpm test --coverage to see current coverage report
   - Note which files have 0% coverage

2. SQL Safety Utils — tests/utils/sql-safety.test.ts:
   - Test every exported function
   - Injection vectors: "'; DROP TABLE advisors; --"
   - UNION SELECT attacks
   - Nested quote escaping: "O''Brien"
   - Unicode escapes: \u0027 ('), \u003B (;)
   - Comment injection: /* ... */ and -- inline comments
   - Null bytes: \x00
   - Verify each is caught/sanitized appropriately
   - Target: 100% branch coverage on sql-safety.ts

3. Template Schema Validation — tests/schema/templateSchema.test.ts:
   - Import all 20 templates (dynamically from templates/**/index.ts or registry)
   - For each template assert:
     * id: non-empty string matching kebab-case pattern
     * name: non-empty string
     * category: one of known categories
     * sqlTemplate: non-empty string
     * parameters: array with valid type/name/required fields
     * outputSchema: array with valid name/type fields (OutputFieldType union)
     * visualBuilderNodes: present (array, even if empty)
     * requiredDataSources: array of known DataSource values
   - Assert no duplicate template IDs across all 20

4. TemplateEngine Unit Tests — tests/engine/TemplateEngine.test.ts:
   - Mock DataProvider (jest.fn() returning fixture rows)
   - Mock AIProvider (jest.fn() returning mock talking points)
   - Test execute() happy path: returns { rows, talkingPoints }
   - Test: missing required param → throws ValidationError
   - Test: unknown templateId → throws NotFoundError
   - Test: DataProvider throws → error propagated correctly
   - Test: AIProvider failure → graceful degradation (talkingPoints null, rows still returned)
   - Test: param type coercion (string "42" for a number param)

5. REST API Integration Tests — tests/api/router.test.ts:
   - Use supertest + express
   - Mount createTemplateRouter on a test Express app
   - For each of the ~20 template endpoints:
     * GET /templates → returns list of all templates
     * POST /templates/:id/execute with valid body → 200 with rows
     * POST /templates/:id/execute with missing required param → 400
     * POST /templates/:nonexistent/execute → 404
   - Test JWT auth middleware (see TODO 316):
     * No auth header → 401
     * Valid JWT → passes through
   - Use jest.mock() to mock TemplateEngine so no DB needed

6. SQL Rendering Contract Tests — tests/contracts/sqlRendering.test.ts:
   - For each template, call buildParameterizedQuery(template.sqlTemplate, sampleParams)
   - Assert: returned SQL contains correct $1, $2, ... placeholders
   - Assert: values array has correct length and types
   - Assert: no {{}} remain in rendered SQL

7. TypeScript compilation test (add to CI, not Jest):
   - Add to package.json: "typecheck": "tsc --noEmit"
   - Ensure it runs in Bitbucket pipeline (see TODO 317)

8. Configure Jest coverage thresholds in jest.config.ts:
   coverageThreshold: {
     global: { branches: 75, functions: 80, lines: 80, statements: 80 },
     './src/utils/sql-safety.ts': { lines: 100, functions: 100 }
   }

9. Run full suite: pnpm test --coverage
   Fix any failures. All thresholds must pass.

ACCEPTANCE: pnpm test --coverage exits 0. Global coverage ≥80%.
sql-safety.ts at 100%. No skipped/todo tests.
```

---

## Dependencies

- **315** (parameterized queries — test the fixed implementation)
- **316** (JWT auth — test auth middleware)
- **317** (CI — coverage runs in pipeline)

---

## Acceptance Criteria

- [ ] Global test coverage ≥ 80% (branches, functions, lines, statements)
- [ ] `src/utils/sql-safety.ts` at 100% line/function coverage
- [ ] All 20 templates validated by schema tests
- [ ] TemplateEngine tested with mocked providers (no DB)
- [ ] REST API integration tests cover all endpoints (supertest)
- [ ] Contract tests: no `{{}}` in rendered parameterized SQL
- [ ] Jest coverage thresholds enforced (CI fails if coverage drops)
- [ ] `pnpm test` exits 0
