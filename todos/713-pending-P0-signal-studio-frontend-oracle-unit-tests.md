# TODO-713: Oracle Service Unit Tests

**Repo**: signal-studio-frontend  
**Priority**: P0  
**Effort**: M (1-2 days)  
**Status**: pending  
**Depends on**: TODO-711

## Description
The Oracle service layer has zero test coverage. Add comprehensive unit tests with mocked oracledb.

## Coding Prompt
```
Create unit tests for the Oracle service layer in signal-studio-frontend.

Files to create:
1. __tests__/lib/oracle/vector-service.test.ts
   - Mock oracledb module: jest.mock('oracledb', ...)
   - Test: testConnection() returns {success: true} when pool connects
   - Test: testConnection() returns {success: false} on connection error
   - Test: vectorizeSignals() calls OpenAI embeddings API for each signal
   - Test: vectorizeSignals() inserts records with bind variables
   - Test: searchSimilar() generates query embedding and calls vector_distance()
   - Test: searchSimilar() returns ranked results

2. __tests__/lib/oracle/query-builder.test.ts
   - Test: buildOracleQuery() rejects unknown tables
   - Test: buildOracleQuery() generates correct SELECT with WHERE clause
   - Test: buildOracleQuery() caps LIMIT at 10,000
   - Test: buildOracleQuery() rejects SQL injection attempts in column names
   - Test: buildOracleQuery() uses bind variables for filter values

3. __tests__/api/oracle/query.test.ts
   - Test POST /api/oracle/query: missing table → 400
   - Test POST /api/oracle/query: valid request → 200 with results
   - Test POST /api/oracle/query: Oracle error → 500

Use jest.mock() for oracledb and fetch (for OpenAI embeddings).
Use @testing-library/react for any React component tests.
```

## Acceptance Criteria
- [ ] `npm run test:lib` passes with new Oracle tests
- [ ] `npm run test:api` passes with Oracle API tests
- [ ] Coverage for lib/oracle/ > 80%
