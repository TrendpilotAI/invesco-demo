# TODO 430 — Add SQLite Indexes to NarrativeReactor

**Priority:** HIGH  
**Repo:** NarrativeReactor  
**Effort:** 1 hour  
**Status:** pending

## Description
NarrativeReactor's SQLite tables lack indexes on high-frequency query columns. This causes full table scans on common operations like scheduler polling, campaign filtering, and content library queries.

## Task

Add the following indexes to `src/lib/db.ts` in the initialization block:

```sql
CREATE INDEX IF NOT EXISTS idx_content_drafts_created_at ON content_drafts(created_at);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_agent_messages_campaign_id ON agent_messages(campaign_id);
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);
```

Also pin Genkit wildcard dependencies in `package.json`:
- Change `"genkit": "*"` → `"genkit": "^1.x.x"` (use latest stable)
- Change `"@genkit-ai/google-genai": "*"` → specific version
- Change `"@genkit-ai/vertexai": "*"` → specific version
- Change `"@genkit-ai/firebase": "*"` → specific version
- Change `"@genkit-ai/dotprompt": "*"` → specific version

## Acceptance Criteria
- [ ] All 4 indexes exist in db.ts initialization
- [ ] No wildcard `"*"` versions in package.json
- [ ] `npm run build` passes
- [ ] `npm test` passes

## Dependencies
None — standalone improvement.
