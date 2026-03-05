# TODO-603: LRU Response Cache for Content Generation — NarrativeReactor

**Priority:** P2 (Performance / Cost)
**Repo:** NarrativeReactor
**Effort:** 2 hours
**Dependencies:** TODO-599 (Pino logging)

## Problem
Identical content generation requests (same prompt + brand + format) hit AI APIs every time. Costs accumulate unnecessarily.

## Task
Add in-memory LRU cache in front of Genkit content generation flows. Cache hit → return cached result instantly.

## Acceptance Criteria
- [ ] LRU cache with max 500 entries, 5-minute TTL
- [ ] Cache key = SHA-256 hash of (brand_id + prompt + format + model)
- [ ] Cache hit logged at debug level
- [ ] Cache miss triggers normal AI call
- [ ] Cache is bypassed when `no_cache: true` passed in request
- [ ] Cache stats exposed at `/api/costs` endpoint (hits, misses, size)
- [ ] Unit tests for cache behavior

## Agent Prompt
```
In /data/workspace/projects/NarrativeReactor:
1. Run: yarn add lru-cache
2. Create src/lib/contentCache.ts:
   import { LRUCache } from 'lru-cache';
   import crypto from 'crypto';
   const cache = new LRUCache({ max: 500, ttl: 5 * 60 * 1000 });
   export function getCacheKey(brandId, prompt, format, model): string {
     return crypto.createHash('sha256').update(JSON.stringify({brandId, prompt, format, model})).digest('hex');
   }
   export { cache };
3. In src/flows/content-generation.ts, wrap the main generation logic:
   - Check cache before AI call
   - Store result in cache after AI call
   - Log cache hit/miss with logger
4. Add cache stats to getCostSummary() in src/services/costTracker.ts
5. Write tests in src/__tests__/lib/contentCache.test.ts
6. Run: npm test
```
