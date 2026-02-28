# 225 · NarrativeReactor · Redis Caching Layer

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Created:** 2026-02-27

---

## Task Description

NarrativeReactor makes expensive LLM API calls (Gemini, Claude, Vertex) repeatedly for the same inputs. There's no caching layer. Add Redis-backed caching for: flow results, brand profiles, trend data, and social performance metrics. Use Railway Redis (already provisioned in TOOLS.md).

---

## Coding Prompt (agent-executable)

```
Working in /data/workspace/projects/NarrativeReactor/:

1. Install: npm i ioredis @types/ioredis

2. Create src/lib/cache.ts:
   - Connect to REDIS_URL env var (fallback: no-op cache if not set)
   - export async function cacheGet<T>(key: string): Promise<T | null>
   - export async function cacheSet<T>(key: string, value: T, ttlSeconds: number): Promise<void>
   - export async function cacheDelete(key: string): Promise<void>
   - export function cacheKey(...parts: string[]): string  // namespaced: "nr:v1:{parts.join(':')}"
   - Add cache stats: hits, misses, errors (in-memory counters)

3. Integrate caching into high-value services:
   a. src/services/brandManager.ts — cache brand profiles for 1 hour (key: nr:v1:brand:{brandId})
   b. src/services/hashtagDiscovery.ts — cache hashtag results for 6 hours
   c. src/services/performanceTracker.ts — cache social metrics for 15 minutes
   d. src/services/trendpilotBridge.ts — cache trend data for 30 minutes
   e. src/flows/content-generation.ts — cache generated content by input hash for 24 hours

4. Add GET /api/cache/stats endpoint (admin scope required):
   - Returns: { hits, misses, hitRate, uptime }

5. Add GET /api/cache/flush endpoint (admin scope required):
   - Flushes all nr:v1:* keys

6. Create src/__tests__/lib/cache.test.ts with mock Redis tests

7. Add REDIS_URL to .env.example

REDIS_URL (external): redis://default:n0cCnXT!P~Deqag~_R-ycmL30-4Jx79E@trolley.proxy.rlwy.net:11973
```

---

## Dependencies

- 224 (auth improvements — for cache admin endpoints)

## Effort Estimate

5–6 hours

## Acceptance Criteria

- [ ] Cache module gracefully degrades if Redis unavailable (no-op fallback)
- [ ] Brand profiles cached and retrieved correctly
- [ ] Cache stats endpoint returns accurate hit/miss data
- [ ] Test suite passes with mock Redis
- [ ] Measurable latency improvement on repeated calls (< 10ms vs 2000ms+)
