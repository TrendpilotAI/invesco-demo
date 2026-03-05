# TODO-609: Extract Oracle Connection Singleton

**Repo:** signal-studio-frontend  
**Priority:** P1 (Maintainability)  
**Effort:** S (3-5 hours)  
**Status:** pending

## Description

Oracle `oracledb` initialization and connection pool setup is duplicated in `lib/oracle-service.ts`, `lib/oracle-vector-service.ts`, and `lib/oracleml-service.ts`. Each file initializes Instant Client independently, which can cause conflicts. Extract to a shared singleton.

## Acceptance Criteria
- [ ] `lib/oracle/connection.ts` exports `getConnection()` and `getPool()` singletons
- [ ] Instant Client init called exactly once across all Oracle services
- [ ] All three oracle service files refactored to use the shared connection module
- [ ] No functional regression in Oracle connect, query, vector, OML features

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend:

1. Create lib/oracle/connection.ts with:
   - initializeInstantClient() called once via module-level singleton
   - getPool(): returns the shared oracledb pool (creates if not exists)
   - getConnection(): gets a connection from the pool
   - closePool(): for cleanup

2. Refactor lib/oracle-service.ts to import from lib/oracle/connection.ts
3. Refactor lib/oracle-vector-service.ts similarly  
4. Refactor lib/oracleml-service.ts similarly
5. Update any barrel exports in lib/index.ts

Test: run npm run dev and verify /oracle-connect page still connects
```

## Dependencies
- None
