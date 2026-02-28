# 237 · P0 · Trendpilot — Connect Real NewsAPI, Reddit, RSS APIs

## Status
pending

## Priority
P0 — platform has no real content without live data

## Description
The aggregator source files (`news-api.ts`, `reddit.ts`, `rss.ts`) already exist and make real HTTP calls, but they degrade silently to empty arrays without API keys. This task:
1. Ensures API keys are loaded from env vars and validated at startup
2. Adds proper error handling, retry logic, and rate limit awareness
3. Persists fetched topics to Supabase (`db.topics.bulkCreate`) via the aggregator pipeline
4. Schedules automatic runs via the existing cron scheduler

## Dependencies
- TODO #236 (Supabase data store) must be complete
- `NEWS_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` env vars
- Optional: RSS feed URLs configured in env or Supabase config table

## Estimated Effort
1 day

## Coding Prompt

```
You are working on the Trendpilot project at /data/workspace/projects/Trendpilot/.

TASK: Wire real API integrations for NewsAPI, Reddit, and RSS — persisting results to Supabase.

FILES TO MODIFY:
- src/services/aggregator/sources/news-api.ts
- src/services/aggregator/sources/reddit.ts
- src/services/aggregator/sources/rss.ts
- src/services/aggregator/index.ts
- src/lib/config.ts (or create it)

STEP 1 — Config validation at startup:
Create/update `src/lib/config.ts`:
```ts
export const config = {
  newsApi: {
    key: process.env.NEWS_API_KEY ?? '',
    enabled: Boolean(process.env.NEWS_API_KEY),
  },
  reddit: {
    clientId: process.env.REDDIT_CLIENT_ID ?? '',
    clientSecret: process.env.REDDIT_CLIENT_SECRET ?? '',
    username: process.env.REDDIT_USERNAME ?? '',
    password: process.env.REDDIT_PASSWORD ?? '',
    enabled: Boolean(process.env.REDDIT_CLIENT_ID && process.env.REDDIT_CLIENT_SECRET),
  },
  rss: {
    feeds: (process.env.RSS_FEEDS ?? '').split(',').filter(Boolean),
    enabled: Boolean(process.env.RSS_FEEDS),
  },
};
```

STEP 2 — NewsAPI (`src/services/aggregator/sources/news-api.ts`):
- If `!config.newsApi.enabled`, log warning and return []
- Add retry logic (3 attempts with exponential backoff) using a simple `withRetry` helper
- Parse all categories: technology, business, science, health
- Deduplicate by URL before returning
- Log how many topics were fetched

STEP 3 — Reddit (`src/services/aggregator/sources/reddit.ts`):
- Implement OAuth2 app-only auth (POST https://www.reddit.com/api/v1/access_token with Basic auth)
- Cache the access token in memory (expires in 1 hour)
- Fetch top posts from r/technology, r/worldnews, r/business, r/science (limit 25 each)
- Map to Topic shape: { id: `reddit-${post.id}`, title, url, source: 'reddit', publishedAt }
- Handle 429 rate limits: back off and retry after `Retry-After` header seconds

STEP 4 — RSS (`src/services/aggregator/sources/rss.ts`):
- Use `fast-xml-parser` or built-in fetch to parse RSS/Atom feeds
- Default feeds: TechCrunch, Hacker News, BBC News (add as env RSS_FEEDS or hardcode defaults)
- Install if needed: `npm install fast-xml-parser`

STEP 5 — Aggregator orchestrator (`src/services/aggregator/index.ts`):
```ts
import * as db from '@/services/db.js';

export async function runAggregation(): Promise<void> {
  const [newsTopics, redditTopics, rssTopics] = await Promise.allSettled([
    fetchNewsTopics(),
    fetchRedditTopics(),
    fetchRSSTopics(),
  ]);
  
  const all = [newsTopics, redditTopics, rssTopics]
    .filter(r => r.status === 'fulfilled')
    .flatMap(r => (r as PromiseFulfilledResult<Topic[]>).value);
  
  // Deduplicate by URL
  const unique = deduplicateTopics(all);
  
  // Persist to Supabase
  if (unique.length > 0) {
    await db.topics.bulkCreate(unique.map(t => ({
      id: t.id,
      title: t.title,
      url: t.url,
      source: t.source,
      published_at: t.publishedAt,
      tags: t.tags ?? [],
    })));
  }
  
  console.log(`[aggregator] Fetched ${unique.length} unique topics`);
}
```

STEP 6 — Schedule in API startup:
In `src/api/index.ts`, add:
```ts
import cron from 'node-cron';
import { runAggregation } from '@/services/aggregator/index.js';

// Run every hour
cron.schedule('0 * * * *', () => runAggregation().catch(console.error));
// Run once on startup
runAggregation().catch(console.error);
```

STEP 7 — Test:
- `POST /api/aggregate/run` endpoint (admin-only) that triggers `runAggregation()` manually
- Verify topics appear in Supabase topics table after calling endpoint
```

## Acceptance Criteria
- [ ] `NEWS_API_KEY` set → real articles appear in `/api/topics`
- [ ] `REDDIT_CLIENT_*` set → Reddit posts appear in topics
- [ ] Topics are persisted to Supabase `topics` table (verify in dashboard)
- [ ] Missing API keys log a warning but don't crash the server
- [ ] Rate limit errors are caught and don't crash the aggregation run
- [ ] `POST /api/aggregate/run` (admin auth) triggers a run and returns count of topics fetched
