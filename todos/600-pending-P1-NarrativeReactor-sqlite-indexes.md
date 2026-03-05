# TODO-600: SQLite Indexes — NarrativeReactor

**Priority:** P1 (Performance)
**Repo:** NarrativeReactor
**Effort:** 1 hour
**Dependencies:** None

## Problem
Content library, campaigns, and schedules tables lack indexes on commonly queried columns. Will degrade significantly as data grows.

## Task
Add a migration that creates indexes on all hot query paths.

## Acceptance Criteria
- [ ] Index on `content_library(brand_id, created_at)`
- [ ] Index on `schedules(scheduled_at, status)`
- [ ] Index on `campaigns(brand_id, phase)`
- [ ] Migration runs idempotently on startup (IF NOT EXISTS)
- [ ] EXPLAIN QUERY PLAN shows index usage for common queries

## Agent Prompt
```
In /data/workspace/projects/NarrativeReactor/src/lib/db.ts (or wherever SQLite is initialized):
1. Find the database initialization / schema creation code
2. Add after existing CREATE TABLE statements:
   CREATE INDEX IF NOT EXISTS idx_content_brand_created ON content_library(brand_id, created_at);
   CREATE INDEX IF NOT EXISTS idx_schedules_time_status ON schedules(scheduled_at, status);
   CREATE INDEX IF NOT EXISTS idx_campaigns_brand_phase ON campaigns(brand_id, phase);
3. Also enable WAL mode: db.pragma('journal_mode = WAL');
4. Run: npm test to verify tests pass
5. Add a test that verifies PRAGMA index_list returns these indexes
```
