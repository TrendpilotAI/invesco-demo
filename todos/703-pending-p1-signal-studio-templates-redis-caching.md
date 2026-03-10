---
id: 703
status: pending
repo: signal-studio-templates
priority: P1
effort: M
created: 2026-03-10
---

# TODO 703 — Redis Caching Layer for TemplateEngine

**Repo:** signal-studio-templates  
**Priority:** P1 — High-value templates execute expensive queries on every call  
**Effort:** M (1 day)

## Problem

Every API call to `POST /templates/:id/execute` re-executes the full SQL query. Expensive aggregation queries (territory-pulse, best-shots-on-goal, regional-benchmark, concentration-risk) run repeatedly for the same parameters. At Invesco scale with 100+ advisors querying the same templates, this is a serious performance bottleneck.

## Solution

Add an optional Redis cache layer with configurable TTL per template.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates:

1. pnpm add ioredis

2. Create engine/cache-provider.ts:
   
   export interface CacheProvider {
     get(key: string): Promise<string | null>;
     set(key: string, value: string, ttlSeconds: number): Promise<void>;
     invalidate(key: string): Promise<void>;
     invalidatePattern(pattern: string): Promise<void>;
   }
   
   export class NoCacheProvider implements CacheProvider {
     async get() { return null; }
     async set() {}
     async invalidate() {}
     async invalidatePattern() {}
   }
   
   export class RedisCacheProvider implements CacheProvider {
     private client: Redis;
     constructor(redisUrl: string) {
       this.client = new Redis(redisUrl);
     }
     async get(key: string) { return this.client.get(key); }
     async set(key, value, ttlSeconds) { await this.client.setex(key, ttlSeconds, value); }
     async invalidate(key) { await this.client.del(key); }
     async invalidatePattern(pattern) {
       const keys = await this.client.keys(pattern);
       if (keys.length) await this.client.del(...keys);
     }
   }

3. Update TemplateEngine constructor to accept optional cache:
   constructor(
     private dataProvider: DataProvider,
     private aiProvider?: AIProvider,
     private cache?: CacheProvider,  // defaults to NoCacheProvider
   ) {
     this.cache = cache ?? new NoCacheProvider();
   }

4. Add caching to execute():
   - Cache key: `sst:v1:${templateId}:${sha256(JSON.stringify(sortedParams))}`
   - Before SQL execution: check cache. If hit, parse and return cached ExecutionResult
   - After SQL execution: store rows + rowCount in cache with TTL
   - Default TTL: 300 seconds (5 minutes)
   - Template-level TTL override: add optional `cacheMinutes?: number` field to SignalTemplate schema
   - If includeTalkingPoints=true, NEVER cache (AI responses should be fresh)
   - Cache key includes templateId + hash of sorted parameters (not talking points)

5. Add cache hash utility using Node.js built-in crypto (no new deps):
   import { createHash } from 'crypto';
   const hashParams = (params: Record<string, any>) =>
     createHash('sha256')
       .update(JSON.stringify(Object.keys(params).sort().reduce((acc, k) => ({ ...acc, [k]: params[k] }), {})))
       .digest('hex')
       .slice(0, 16);

6. Environment variables:
   - REDIS_URL: Redis connection URL (optional; cache disabled if not set)
   
7. Factory helper in index.ts exports:
   export function createTemplateEngine(opts?: {
     redisUrl?: string;
     openaiKey?: string;
   }): TemplateEngine {
     const cache = opts?.redisUrl ? new RedisCacheProvider(opts.redisUrl) : undefined;
     const aiProvider = opts?.openaiKey ? new OpenAIAIProvider(opts.openaiKey) : undefined;
     return new TemplateEngine(new MockDataProvider(), aiProvider, cache);
   }

8. Add tests in __tests__/engine/cache-provider.test.ts:
   - NoCacheProvider always returns null from get()
   - RedisCacheProvider requires a running Redis (skip if REDIS_URL not set)
   - Cache hit returns same data as original execution
   - includeTalkingPoints=true bypasses cache
```

## Files

- `engine/cache-provider.ts` (new)
- `engine/template-engine.ts` (add cache integration)
- `schema/signal-template.ts` (add `cacheMinutes?: number` field)
- `index.ts` (add `createTemplateEngine` factory)
- `__tests__/engine/cache-provider.test.ts` (new)
- `package.json` (add ioredis)

## Acceptance Criteria

- Cache is optional (NoCacheProvider default, no Redis required)
- First call: cache miss, executes SQL
- Second call (same params): cache hit, skips SQL
- includeTalkingPoints=true: always executes SQL (no cache)
- TTL configurable per template via `cacheMinutes` field

## Dependencies

- Pairs with: TODO-700 (PostgresDataProvider — Redis becomes important at real scale)
- See also: TODO-321 (redis-caching-template-versioning)
