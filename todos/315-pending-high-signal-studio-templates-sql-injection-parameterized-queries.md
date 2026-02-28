# 315 — Fix SQL Injection: Replace `{{param}}` with Parameterized Queries

**Priority:** HIGH (CRITICAL security)  
**Effort:** M  
**Status:** pending

---

## Task Description

The template engine uses string interpolation (`{{param}}`) to inject user-supplied values directly into SQL strings. This is a critical SQL injection vulnerability. Every template in `templates/*/` renders SQL with `sqlTemplate.replace(/\{\{param\}\}/g, value)` (or similar), bypassing Postgres's query plan safety.

Fix: Replace all `{{param}}` interpolation with Postgres parameterized queries (`$1`, `$2`, …) in the template engine's `renderTemplate` / `execute` path.

---

## Autonomous Coding Prompt

```
REPO: /data/workspace/projects/signal-studio-templates

TASK: Fix SQL injection vulnerability across all 20 signal templates.

STEPS:
1. Audit utils/sql-safety.ts and src/engine/TemplateEngine.ts (or wherever renderTemplate lives).
   Find all places where {{param}} interpolation happens.

2. Create/update src/utils/renderTemplate.ts:
   - Export function buildParameterizedQuery(sqlTemplate: string, params: Record<string, unknown>):
       { sql: string; values: unknown[] }
   - Replace each {{paramName}} occurrence with $1, $2, … (positional).
   - Return the rewritten SQL and an ordered array of values.
   - Throw if a referenced param name is not in the params object.

3. Update TemplateEngine.execute() to call buildParameterizedQuery and pass
   { text: sql, values } to the pg client (node-postgres parameterized query API).

4. Update all 20 templates under templates/*/ to ensure sqlTemplate strings use
   {{paramName}} consistently (the new utility handles the $N conversion).
   No template should do its own string interpolation.

5. Update utils/sql-safety.ts:
   - Keep existing allowlist/reject functions as a secondary defense.
   - Add a validateNoRawInterpolation(sql: string) guard that throws if the
     rendered SQL still contains {{ — use in tests.

6. Add unit tests in tests/utils/renderTemplate.test.ts:
   - Happy path: correct $1/$2 substitution with values array.
   - Missing param: throws descriptive error.
   - Injection attempts: "'; DROP TABLE advisors; --", UNION SELECT, nested quotes.
   - Unicode escape sequences that could break naive sanitizers.

7. Run: pnpm typecheck && pnpm test
   All tests must pass. Fix any type errors.

ACCEPTANCE: No {{}} interpolation remains in any SQL execution path. 
All injection test cases pass. pnpm build succeeds.
```

---

## Dependencies

- None (this is foundational — blocks everything else)

---

## Acceptance Criteria

- [ ] `buildParameterizedQuery` utility created and exported
- [ ] `TemplateEngine.execute()` uses parameterized queries exclusively
- [ ] All 20 templates verified to use `{{paramName}}` in sqlTemplate (source of truth only — no runtime interpolation)
- [ ] Injection unit tests: `'; DROP TABLE`, `UNION SELECT`, Unicode escapes all handled safely
- [ ] `pnpm build` and `pnpm test` pass with zero errors
- [ ] No `eval`, `string concatenation`, or `template literal` SQL construction remains in engine path
