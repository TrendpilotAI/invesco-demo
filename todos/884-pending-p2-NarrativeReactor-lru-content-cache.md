# TODO-884: Add LRU Cache for AI Content Generation

**Repo**: NarrativeReactor  
**Priority**: P2 — Cost Optimization  
**Effort**: 2 hours  
**Status**: Pending  

## Problem

Every identical content generation request (same prompt + brand) hits AI APIs at full cost. In production with multiple tenants generating similar content (e.g., daily social posts for same brand), this wastes 30-50% of AI budget.

## Solution

Add an in-memory LRU cache with TTL in `src/flows/content-generation.ts`:

```typescript
// src/lib/contentCache.ts (new file)
import crypto from 'crypto';

interface CacheEntry {
  result: unknown;
  expiresAt: number;
}

const cache = new Map<string, CacheEntry>();
const MAX_ENTRIES = 500;
const TTL_MS = 5 * 60 * 1000; // 5 minutes

export function getCacheKey(prompt: string, brandId: string, contentType: string): string {
  return crypto.createHash('sha256')
    .update(`${brandId}:${contentType}:${prompt}`)
    .digest('hex');
}

export function getFromCache(key: string): unknown | null {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expiresAt) {
    cache.delete(key);
    return null;
  }
  return entry.result;
}

export function setInCache(key: string, result: unknown): void {
  // Evict oldest if at capacity
  if (cache.size >= MAX_ENTRIES) {
    const firstKey = cache.keys().next().value;
    if (firstKey) cache.delete(firstKey);
  }
  cache.set(key, { result, expiresAt: Date.now() + TTL_MS });
}

export function getCacheStats() {
  return { size: cache.size, maxEntries: MAX_ENTRIES };
}
```

Usage in `src/flows/content-generation.ts`:
```typescript
import { getCacheKey, getFromCache, setInCache } from '../lib/contentCache';

// In content generation flow:
const cacheKey = getCacheKey(input.prompt, input.brandId, input.contentType);
const cached = getFromCache(cacheKey);
if (cached) {
  return cached;  // Cache hit — no AI API call
}
const result = await generateWithAI(input);  // Cache miss
setInCache(cacheKey, result);
return result;
```

Add cache stats to cost endpoint:
```typescript
// GET /api/costs — already exists, add cache stats
{ ...costSummary, cacheStats: getCacheStats() }
```

## Files to Change

- `src/lib/contentCache.ts` — new LRU cache module
- `src/flows/content-generation.ts` — wrap generation with cache check
- `src/index.ts` — expose cache stats in /api/costs

## Acceptance Criteria

- [ ] Cache returns identical response for same prompt+brand within 5 minutes
- [ ] Cache evicts entries after TTL
- [ ] Cache doesn't exceed 500 entries (LRU eviction)
- [ ] Cache stats visible in /api/costs endpoint
- [ ] Tests mock cache to verify it's called correctly
- [ ] No AI API call made on cache hit (verified via mock spy)
