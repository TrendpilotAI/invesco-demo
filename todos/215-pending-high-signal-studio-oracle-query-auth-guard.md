# 215 · HIGH · signal-studio · Add Oracle query auth guard and table whitelist

## Status
pending

## Priority
high

## Project
signal-studio (`/data/workspace/projects/signal-studio/`)

## Task Description
`/api/oracle/query/route.ts` has minimal protection — it only checks that queries start with `SELECT`. Issues:

1. **No auth check** — any unauthenticated user can query the Oracle DB (partially fixed by TODO 212 middleware, but we need defense in depth)
2. **No table whitelist** — `SELECT * FROM sys.dba_users` or other sensitive system tables are permitted
3. **No query complexity limit** — unbounded JOIN chains or Cartesian products can DOS the DB
4. **`binds` parameter is unvalidated** — bind values could be exploited if Oracle driver has vulnerabilities

Additional routes to harden:
- `/api/oracle/tables/route.ts` — returns all table names, should filter to whitelist
- `/api/oracle/columns/route.ts` — should only return columns for whitelisted tables
- `/api/oracle/preview/route.ts` — preview queries need the same guards

## Dependencies
- 212 (middleware provides `x-user-id` header for auth context)

## Estimated Effort
3 hours

## Acceptance Criteria
- [ ] `lib/oracle/query-guard.ts` implements `validateOracleQuery(sql, binds)` 
- [ ] Only tables in `ORACLE_TABLE_WHITELIST` are queryable
- [ ] System tables (`sys.*`, `dba_*`, `all_*`, `v$*`) are always blocked
- [ ] Query complexity limit: max 5 JOINs, max 3 subqueries
- [ ] `/api/oracle/tables` response filtered to whitelist only
- [ ] Tests in `__tests__/lib/oracle-query-guard.test.ts`

## Coding Prompt

```
You are working in the Next.js 14 App Router project at /data/workspace/projects/signal-studio/.

TASK: Add a robust auth guard and table whitelist to all Oracle API routes.

### Step 1 — Create lib/oracle/query-guard.ts

```typescript
// lib/oracle/query-guard.ts
// Defense-in-depth for Oracle queries. 
// Middleware (TODO 212) is the primary auth layer; this is the secondary.

// Tables that users are permitted to query.
// Expand this list as new data providers are onboarded.
export const ORACLE_TABLE_WHITELIST = new Set([
  // Add actual ForwardLane/Invesco table names here
  "CLIENT_PORTFOLIOS",
  "ACCOUNT_BALANCES",
  "TRANSACTION_HISTORY",
  "CLIENT_PROFILES",
  "SIGNAL_RESULTS",
  "ADVISOR_ASSIGNMENTS",
  // Add more as needed
])

// Patterns that indicate system/privileged table access — always block
const SYSTEM_TABLE_PATTERNS = [
  /\bsys\.\w+/i,
  /\bdba_\w+/i,
  /\ball_\w+/i,
  /\bv\$\w+/i,         // Oracle V$ dynamic performance views
  /\bgv\$\w+/i,        // Global V$ views
  /\bx\$\w+/i,         // Internal Oracle tables
  /\buser_\w+/i,       // User-level dictionary views
  /information_schema/i,
]

export interface QueryValidationResult {
  valid: boolean
  error?: string
}

export function validateOracleQuery(
  sql: string,
  binds: unknown[] = []
): QueryValidationResult {
  if (!sql || typeof sql !== "string") {
    return { valid: false, error: "SQL query is required" }
  }

  const trimmed = sql.trim()

  // Only SELECT statements allowed
  if (!/^SELECT\s/i.test(trimmed)) {
    return { valid: false, error: "Only SELECT queries are permitted" }
  }

  // Block SQL comments (can be used to hide injection)
  if (/--/.test(trimmed) || /\/\*/.test(trimmed)) {
    return { valid: false, error: "SQL comments are not permitted" }
  }

  // Block multiple statements
  if (/;\s*\w/.test(trimmed)) {
    return { valid: false, error: "Multiple SQL statements are not permitted" }
  }

  // Block system table access
  for (const pattern of SYSTEM_TABLE_PATTERNS) {
    if (pattern.test(trimmed)) {
      return { valid: false, error: "Access to system tables is not permitted" }
    }
  }

  // Extract table references and validate against whitelist
  // Simple regex to find FROM and JOIN table names
  const tablePattern = /(?:FROM|JOIN)\s+([A-Z_][A-Z0-9_$#]*)/gi
  let match
  while ((match = tablePattern.exec(trimmed)) !== null) {
    const tableName = match[1].toUpperCase()
    if (!ORACLE_TABLE_WHITELIST.has(tableName)) {
      return {
        valid: false,
        error: `Table '${tableName}' is not in the permitted table list`,
      }
    }
  }

  // Complexity limits
  const joinCount = (trimmed.match(/\bJOIN\b/gi) ?? []).length
  if (joinCount > 5) {
    return { valid: false, error: "Query exceeds maximum JOIN complexity (max 5)" }
  }

  const subqueryCount = (trimmed.match(/\bSELECT\b/gi) ?? []).length - 1
  if (subqueryCount > 3) {
    return { valid: false, error: "Query exceeds maximum subquery depth (max 3)" }
  }

  // Validate binds is an array
  if (!Array.isArray(binds)) {
    return { valid: false, error: "Bind parameters must be an array" }
  }

  // Validate bind values are primitives (no objects/functions)
  for (const bind of binds) {
    if (typeof bind === "object" && bind !== null) {
      return { valid: false, error: "Bind parameters must be primitive values" }
    }
  }

  return { valid: true }
}
```

### Step 2 — Update app/api/oracle/query/route.ts

```typescript
import { validateOracleQuery } from "@/lib/oracle/query-guard"

export async function POST(req: NextRequest) {
  // Defense in depth: verify auth header even if middleware is in place
  const userId = req.headers.get("x-user-id")
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  const { sql, binds = [] } = await req.json()

  // Replace the old basic check with the full guard
  const validation = validateOracleQuery(sql, binds)
  if (!validation.valid) {
    return NextResponse.json({ error: validation.error }, { status: 400 })
  }

  const result = await executeQuery(sql, binds)
  return NextResponse.json({
    columns: result.metaData,
    rows: result.rows,
    rowsAffected: result.rows?.length ?? 0,
  })
}
```

### Step 3 — Update app/api/oracle/tables/route.ts

Filter returned tables to the whitelist:
```typescript
import { ORACLE_TABLE_WHITELIST } from "@/lib/oracle/query-guard"

// In the GET/POST handler, filter results:
const allTables = await getOracleTables()
const permittedTables = allTables.filter(t => 
  ORACLE_TABLE_WHITELIST.has(t.tableName?.toUpperCase())
)
return NextResponse.json({ tables: permittedTables })
```

### Step 4 — Update /api/oracle/columns and /api/oracle/preview

Apply the same auth header check and table whitelist validation.

### Step 5 — Write tests

Create `__tests__/lib/oracle-query-guard.test.ts`:
```typescript
import { validateOracleQuery, ORACLE_TABLE_WHITELIST } from "@/lib/oracle/query-guard"

describe("validateOracleQuery", () => {
  it("allows valid SELECT on whitelisted table", () => {
    const table = [...ORACLE_TABLE_WHITELIST][0]
    expect(validateOracleQuery(`SELECT * FROM ${table}`).valid).toBe(true)
  })

  it("blocks non-SELECT statements", () => {
    expect(validateOracleQuery("DROP TABLE client_portfolios").valid).toBe(false)
    expect(validateOracleQuery("INSERT INTO foo VALUES (1)").valid).toBe(false)
  })

  it("blocks system table access", () => {
    expect(validateOracleQuery("SELECT * FROM sys.dba_users").valid).toBe(false)
    expect(validateOracleQuery("SELECT * FROM v$session").valid).toBe(false)
    expect(validateOracleQuery("SELECT * FROM all_tables").valid).toBe(false)
  })

  it("blocks non-whitelisted tables", () => {
    expect(validateOracleQuery("SELECT * FROM employee_salaries").valid).toBe(false)
  })

  it("blocks SQL comments", () => {
    expect(validateOracleQuery("SELECT 1 -- comment").valid).toBe(false)
    expect(validateOracleQuery("SELECT /* comment */ 1").valid).toBe(false)
  })

  it("blocks excessive JOINs", () => {
    const table = [...ORACLE_TABLE_WHITELIST][0]
    const manyJoins = `SELECT * FROM ${table} ` + 
      Array(6).fill(`JOIN ${table} t ON t.id = 1`).join(" ")
    expect(validateOracleQuery(manyJoins).valid).toBe(false)
  })

  it("validates bind parameters", () => {
    const table = [...ORACLE_TABLE_WHITELIST][0]
    expect(validateOracleQuery(`SELECT * FROM ${table} WHERE id = :1`, [{ evil: true }]).valid).toBe(false)
    expect(validateOracleQuery(`SELECT * FROM ${table} WHERE id = :1`, [123]).valid).toBe(true)
  })
})
```

### Step 6 — Run tests
```bash
cd /data/workspace/projects/signal-studio && pnpm test __tests__/lib/oracle-query-guard.test.ts
```
```

## Related Files
- `lib/oracle/query-guard.ts` (CREATE)
- `app/api/oracle/query/route.ts` (MODIFY)
- `app/api/oracle/tables/route.ts` (MODIFY)
- `app/api/oracle/columns/route.ts` (MODIFY)
- `app/api/oracle/preview/route.ts` (MODIFY)
- `__tests__/lib/oracle-query-guard.test.ts` (CREATE)
