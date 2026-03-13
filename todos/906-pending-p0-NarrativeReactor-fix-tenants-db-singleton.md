# TODO: Migrate tenants.ts to Use DB Singleton (Fix Lock Contention)

## Priority: P0
## Repo: NarrativeReactor

### Problem
tenants.ts creates a direct better-sqlite3 connection instead of using the WAL singleton from db.ts. This bypasses WAL mode and causes SQLite lock contention under concurrent load, leading to "database is locked" errors in production.

### Action Items
- Refactor tenants.ts to import and use the singleton DB instance from db.ts
- Remove the direct `new Database(DB_PATH)` instantiation in tenants.ts
- Run concurrency test to verify no lock contention: simultaneous tenant read + content write
- Verify WAL mode is consistently applied across all DB access paths
- Add integration test for concurrent DB access

### Impact
- Eliminates production database lock errors under load
- Required before any multi-tenant customer onboarding
- Prevents data corruption risk

### References
- AUDIT.md critical issues
- src/db.ts, src/tenants.ts
