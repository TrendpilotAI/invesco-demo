# TODO: Trendpilot — Migrate File-Based Storage to Supabase

**Priority:** P0 — Production blocker  
**Repo:** /data/workspace/projects/Trendpilot/  
**Effort:** 3-4 days  
**Dependencies:** Supabase project exists (ycisqlzzsimtlqfabmns), schema migration file at supabase/migrations/

## Description
The entire Trendpilot backend runs on file-based JSON storage (`data/aggregations.json`, `data/subscribers.json`, etc.). The Supabase client is wired but NOT used by any service. This is a production blocker — file storage has no concurrency safety, unbounded growth, and won't survive a Railway restart.

## Coding Prompt (Autonomous Execution)
```
Migrate all in-memory/file-based stores in /data/workspace/projects/Trendpilot/ to Supabase:

1. Update src/services/storage/index.ts:
   - Replace fs.readFileSync/writeFileSync with supabaseAdmin calls
   - store() → INSERT into aggregations table
   - getLatest() → SELECT ... ORDER BY created_at DESC LIMIT 1
   - getHistory(limit) → SELECT ... ORDER BY created_at DESC LIMIT n

2. Update src/services/email/digest.ts SubscriberStore:
   - Replace in-memory array with Supabase subscribers table
   - addSubscriber() → UPSERT
   - getSubscribers() → SELECT WHERE active=true

3. Update src/services/profiles/index.ts ProfileStore:
   - Replace Map with Supabase user_profiles table

4. Update src/services/tenants/index.ts TenantStore:
   - Replace Map with Supabase tenants table

5. Update src/services/teams/index.ts TeamStore:
   - Replace Map with Supabase teams table

6. Update src/services/theming/index.ts ThemeStore:
   - Replace Map with Supabase themes table

7. Verify supabase/migrations/20260218000000_initial_schema.sql has all required tables.
   Add missing tables if needed with a new migration file.

8. Update all tests to use Supabase test client (or mock supabaseAdmin).

9. Add database indexes:
   - topics(created_at DESC)
   - newsletters(tenant_id, created_at DESC)  
   - subscribers(email) UNIQUE
   - aggregations(created_at DESC)

Supabase project: ycisqlzzsimtlqfabmns
Connection info in TOOLS.md under Supabase section.
```

## Acceptance Criteria
- [ ] No fs.readFileSync/writeFileSync calls in production code paths
- [ ] All CRUD operations go through supabaseAdmin
- [ ] Existing 423 tests still pass (with Supabase mocked or test DB)
- [ ] Data persists across Railway restarts
- [ ] Indexes created for query-heavy columns
