# TODO-713: DONE — Oracle Service Unit Tests

**Status**: done  
**Commit**: f78b2315  
**Branch**: main  

## Tests added (33 total, all passing)

### `__tests__/lib/oracle/vector-service.test.ts` (16 tests)
- `testConnection()` — success, connection error, execute error (with finally close)
- `vectorizeSignals()` — calls embeddings API, uses bind variables, commits, handles unique violations (upsert), skipExisting, records failures, empty array short-circuit, fatal error rollback
- `searchSimilar()` — generates query embedding, calls VECTOR_DISTANCE(), respects limit, closes connection on error

### `__tests__/lib/oracle/query-builder.test.ts` (12 tests)
- `validateOracleIdentifier()` — valid identifiers, SQL injection rejection
- `buildOracleQuery()` — SELECT *, columns, WHERE with bind vars, MAX_ROWS cap, unknown tables, injection in column names, unknown columns, IS NULL/IS NOT NULL, ORDER BY, disallowed operators

### `__tests__/api/oracle/query.test.ts` (5 tests)
- POST /api/oracle/query: missing table → 400, validation error → 400, valid → 200, Oracle error → 500, params forwarded correctly

## Mocking strategy
- `oracledb` and `@/lib/oracle-service` mocked at module level
- `@/lib/oracle/embeddings` mocked to avoid real OpenAI calls
- `@jest-environment node` set on API test for NextRequest/Fetch API compatibility
