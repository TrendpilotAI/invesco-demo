# 213 — SQL Injection Hardening: Rewrite generateSQL() with Parameterized Queries + Whitelist Sanitizer

**Priority:** critical  
**Project:** signal-studio-templates  
**Repo:** /data/workspace/projects/signal-studio-templates/  
**Status:** pending  
**Estimated Effort:** 3h  

---

## Context

**THIS IS A HIGH RISK SECURITY VULNERABILITY.**

The `generateSQL()` function in the signal-studio-templates codebase uses naive string interpolation to build SQL queries. This creates SQL injection attack surface — any template parameter that accepts user input or external data could be exploited to exfiltrate or corrupt Invesco's financial data in the analytical Postgres database.

This must be fixed before any template is deployed to production Signal Studio.

---

## Task Description

1. Find all SQL generation code:
   ```bash
   grep -rn "generateSQL\|template literal\|\`SELECT\|\`INSERT\|\`UPDATE\|\`DELETE" src/
   ```

2. For each SQL-generating function, implement one of these approaches (in order of preference):

   **Option A — Parameterized query objects (preferred):**
   Return `{ sql: string; params: unknown[] }` tuples where user values are `$1`, `$2` placeholders. Never interpolate user data directly into SQL strings.

   **Option B — Strict whitelist sanitizer:**
   Create a `sanitizeIdentifier(value: string, allowedValues: string[]): string` function that throws if the value is not in the allowlist. Use for table names, column names, and enum-like fields that can't be parameterized.

3. Create `src/utils/sql-safety.ts` with:
   - `sanitizeIdentifier(value: string, allowedValues: readonly string[]): string`
   - `buildParameterizedQuery(template: TemplateStringsArray, ...values: unknown[]): { sql: string; params: unknown[] }`
   - Comprehensive JSDoc explaining the security model

4. Rewrite all `generateSQL()` functions (one per template) to use parameterized approach.

5. Add unit tests for the sanitizer in `src/__tests__/sql-safety.test.ts`:
   - Valid identifiers pass through
   - Invalid identifiers throw with descriptive error
   - SQL special characters are rejected
   - Injection strings like `'; DROP TABLE` are rejected

---

## Coding Prompt (Autonomous Agent)

```
You are hardening the SQL generation code in signal-studio-templates against SQL injection.

REPO: /data/workspace/projects/signal-studio-templates/

Steps:
1. Run: grep -rn "generateSQL\|template\`\|interpolat" src/ to find all SQL generation
2. Read each file that generates SQL
3. Create src/utils/sql-safety.ts with:

   export function sanitizeIdentifier(value: string, allowedValues: readonly string[]): string {
     if (!allowedValues.includes(value)) {
       throw new Error(`SQL injection guard: "${value}" is not a permitted identifier. Allowed: ${allowedValues.join(', ')}`);
     }
     // Extra defense: reject any non-alphanumeric/underscore characters
     if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(value)) {
       throw new Error(`SQL injection guard: "${value}" contains unsafe characters`);
     }
     return value;
   }

   export interface ParameterizedQuery {
     sql: string;
     params: unknown[];
   }

   export function buildQuery(strings: TemplateStringsArray, ...values: unknown[]): ParameterizedQuery {
     const params: unknown[] = [];
     const sql = strings.reduce((acc, str, i) => {
       if (i < values.length) {
         params.push(values[i]);
         return acc + str + `$${params.length}`;
       }
       return acc + str;
     }, '');
     return { sql, params };
   }

4. Rewrite EVERY generateSQL() function to use parameterized queries or sanitizeIdentifier()
   - Table names, column names → sanitizeIdentifier() with explicit allowlist
   - User-supplied values (dates, numbers, strings) → parameterized ($1, $2...)
   - Never concatenate raw user input into SQL

5. Create src/__tests__/sql-safety.test.ts with tests for:
   - sanitizeIdentifier with valid value → passes
   - sanitizeIdentifier with unknown value → throws
   - sanitizeIdentifier with SQL injection string → throws
   - buildQuery produces correct sql + params

6. Run the test suite and fix any failures
7. Report: files changed, injection vectors closed, test results
```

---

## Dependencies

- **211** (build must work first)

---

## Acceptance Criteria

- [ ] `src/utils/sql-safety.ts` exists with `sanitizeIdentifier` and `buildQuery`
- [ ] Zero raw string interpolation of user/template data into SQL strings across the entire codebase
- [ ] All `generateSQL()` functions return `ParameterizedQuery` objects (or equivalent)
- [ ] Unit tests for sql-safety.ts pass
- [ ] grep for common injection patterns finds nothing:
  ```bash
  grep -rn "WHERE.*\${" src/ # should return 0 results
  ```
- [ ] Code review: no `any` type used to bypass safety checks
