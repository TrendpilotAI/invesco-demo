# 236 · P0 · Trendpilot — Wire Supabase as Primary Data Store

## Status
pending

## Priority
P0 — nothing ships without persistent data

## Description
Replace all file-based / in-memory storage in `src/api/index.ts` with calls to `src/services/db.ts` (already implemented Supabase CRUD layer). The Express API currently imports `TrendStorage`, `SubscriberStore`, and `ProfileStore` which store data in memory or local JSON files. These must be replaced with `db.ts` functions that use the Supabase Postgres backend.

The Supabase project is already provisioned (`ycisqlzzsimtlqfabmns`). The `db.ts` module already has full CRUD for: `newsletters`, `sections`, `subscribers`, `topics`, `engagements`, `click_events`, `templates`, `lists`.

## Dependencies
- Supabase project `ycisqlzzsimtlqfabmns` must be reachable
- `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` env vars set
- Run `npm run db:gen-types` to regenerate `src/lib/database.types.ts` from live schema

## Estimated Effort
1–2 days

## Coding Prompt

```
You are working on the Trendpilot project at /data/workspace/projects/Trendpilot/.

TASK: Replace file-based storage with Supabase in the Express API.

CONTEXT:
- `src/api/index.ts` imports TrendStorage, SubscriberStore, ProfileStore — all in-memory/file-based
- `src/services/db.ts` has a complete Supabase CRUD layer (newsletters, subscribers, topics, etc.)
- `src/lib/supabase.ts` should export supabaseAdmin using SUPABASE_SERVICE_ROLE_KEY

STEPS:

1. Verify/create `src/lib/supabase.ts`:
   ```ts
   import { createClient } from '@supabase/supabase-js';
   import type { Database } from './database.types.js';

   export const supabase = createClient<Database>(
     process.env.SUPABASE_URL!,
     process.env.SUPABASE_ANON_KEY!
   );

   export const supabaseAdmin = createClient<Database>(
     process.env.SUPABASE_URL!,
     process.env.SUPABASE_SERVICE_ROLE_KEY!,
     { auth: { autoRefreshToken: false, persistSession: false } }
   );
   ```

2. In `src/api/index.ts`, replace storage dependencies:
   - Remove: `TrendStorage`, `SubscriberStore`, `ProfileStore` imports and instantiation
   - Add: `import * as db from '@/services/db.js';`
   - Replace all `storage.getTopics()` → `db.topics.list()`
   - Replace all `storage.saveTopics(topics)` → `db.topics.bulkCreate(topics)`
   - Replace all `subscriberStore.add(email)` → `db.subscribers.create({ email, status: 'active', subscribed_at: new Date().toISOString() })`
   - Replace all `subscriberStore.list()` → `db.subscribers.list()`
   - Replace newsletter creation → `db.newsletters.create(data)`
   - Replace newsletter retrieval → `db.newsletters.findById(id)` or `db.newsletters.list()`

3. Update the health check endpoint to verify Supabase connectivity:
   ```ts
   app.get('/health', async (req, res) => {
     try {
       await db.subscribers.count();
       res.json({ status: 'ok', db: 'supabase' });
     } catch (e) {
       res.status(503).json({ status: 'error', db: String(e) });
     }
   });
   ```

4. Run the existing Vitest test suite. Adapt tests that relied on TrendStorage to either:
   a) Mock `db.ts` module functions using `vi.mock('@/services/db.js', ...)`
   b) Or point to a Supabase test environment

5. Verify: `curl http://localhost:3001/health` returns `{ status: 'ok', db: 'supabase' }`

6. Verify: POST /subscribers with an email persists to Supabase subscribers table.
```

## Acceptance Criteria
- [ ] `src/api/index.ts` has zero imports from `TrendStorage`, `SubscriberStore`, `ProfileStore`
- [ ] All CRUD operations use `src/services/db.ts`
- [ ] `GET /health` returns `{ status: 'ok', db: 'supabase' }`
- [ ] Adding a subscriber via API persists to Supabase table (verify in Supabase dashboard)
- [ ] Existing test suite passes (with mocked or real Supabase DB)
- [ ] No TypeScript errors (`tsc --noEmit`)
