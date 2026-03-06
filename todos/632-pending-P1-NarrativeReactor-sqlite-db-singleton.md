# TODO-632: Extract SQLite DB Singleton (DRY Fix)

**Repo:** NarrativeReactor  
**Priority:** P1  
**Effort:** 2 hours  
**Status:** pending

## Description
Multiple services open SQLite independently with repeated boilerplate. Extract to a shared singleton in src/lib/db.ts to prevent connection proliferation and enable centralized index management.

## Acceptance Criteria
- [ ] src/lib/db.ts exports a shared SQLite singleton with WAL mode enabled
- [ ] All services import from src/lib/db.ts instead of opening their own connections
- [ ] Migrations run once at startup, not per-service
- [ ] All existing tests still pass after refactor

## Coding Prompt
```
In /data/workspace/projects/NarrativeReactor:

1. Create src/lib/db.ts:
   import Database from 'node:sqlite';
   let _db: Database | null = null;
   export function getDb(): Database {
     if (!_db) {
       _db = new Database(process.env.SQLITE_PATH || './data/narrative.db');
       _db.exec('PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;');
       runMigrations(_db);
     }
     return _db;
   }
   - Include consolidated migrations for all tables from all services
   - Include all indexes: content_library(brand_id, created_at), campaigns(brand_id, phase), schedules(scheduled_at, status)

2. Refactor these services to use getDb():
   - src/services/contentLibrary.ts
   - src/services/campaigns.ts
   - src/services/postingScheduler.ts
   - src/services/approvalWorkflow.ts
   - Any other service with its own SQLite open

3. Run npm test to verify all 287+ tests pass
```

## Dependencies
- TODO-600 (SQLite indexes) — can merge index creation here
