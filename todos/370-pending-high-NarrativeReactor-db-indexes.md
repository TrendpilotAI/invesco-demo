# 370 — Add DB Indexes for content_drafts/campaigns/workflows Tables

## Task Description
`src/lib/db.ts` creates 5+ SQLite tables with zero indexes. The scheduler worker polls `scheduled_posts` every 60 seconds and several API endpoints query by `status`. Without indexes, these are full table scans that degrade as data grows.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

Open `src/lib/db.ts` and add the following indexes to the migration block (after table CREATE statements):

```sql
CREATE INDEX IF NOT EXISTS idx_content_drafts_status ON content_drafts(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);
CREATE INDEX IF NOT EXISTS idx_scheduled_posts_scheduled_at ON scheduled_posts(scheduled_at, status);
CREATE INDEX IF NOT EXISTS idx_scheduled_posts_status ON scheduled_posts(status);
```

Steps:
1. Read `src/lib/db.ts` fully to understand the migration structure
2. Find where table CREATE statements are executed
3. Add index creation statements immediately after their corresponding table creation
4. Use `CREATE INDEX IF NOT EXISTS` so they are idempotent (safe to run on existing DBs)
5. Also check if `agent_messages` table exists — if so, add: `CREATE INDEX IF NOT EXISTS idx_agent_messages_timestamp ON agent_messages(timestamp);`
6. Run `npm test` to confirm all 287+ tests still pass
7. Grep for any queries that benefit: `grep -rn "WHERE status\|WHERE scheduled_at" src/` and verify they now hit indexed columns

Do NOT add indexes to columns that are never queried (don't over-index).

## Dependencies
None

## Estimated Effort
S

## Acceptance Criteria
- [ ] Indexes added to `content_drafts(status)`, `campaigns(status)`, `workflows(status)`
- [ ] Index added to `scheduled_posts(scheduled_at, status)` for scheduler worker
- [ ] All uses of `CREATE INDEX` use `IF NOT EXISTS` (idempotent)
- [ ] All existing tests pass after change
- [ ] No new DB connection errors or migration failures
