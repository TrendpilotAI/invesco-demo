# TODO-620: Add Redis Response Caching for Entity Extraction

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** M (~3-4 hours)  
**Status:** pending

## Problem
Identical text is re-processed on every request. ML NER inference is expensive (~50-200ms). News headlines and standard financial texts recur frequently.

## Coding Prompt
```
Add Redis caching to /data/workspace/projects/core-entityextraction/main.py:

1. Add to requirements.txt:
   redis>=5.0.0

2. Add env var: REDIS_URL (optional — cache disabled if not set)

3. Create cache module or add cache logic to main.py:
   import hashlib, json
   import redis as redis_lib
   
   _redis_client = None
   
   def _get_redis():
       global _redis_client
       if _redis_client is None:
           redis_url = os.environ.get("REDIS_URL")
           if redis_url:
               _redis_client = redis_lib.from_url(redis_url, decode_responses=True)
       return _redis_client
   
   def _cache_key(prefix: str, text: str, include_entity_types, entity_types_list) -> str:
       payload = f"{prefix}:{text}:{include_entity_types}:{sorted(entity_types_list or [])}"
       return "ee:" + hashlib.sha256(payload.encode()).hexdigest()
   
   CACHE_TTL = int(os.environ.get("CACHE_TTL_SECONDS", 60))

4. Wrap regex_entity_extraction and ml_entity_extraction endpoints:
   - Check cache before processing
   - Store result in cache on miss
   - Add X-Cache: HIT|MISS response header

5. Invalidate cache on fixed_lists POST/DELETE:
   # After _invalidate_pattern_cache(), also flush Redis ee:* keys
   r = _get_redis()
   if r:
       keys = r.keys("ee:*")
       if keys: r.delete(*keys)
```

## Acceptance Criteria
- [ ] REDIS_URL env var controls cache enable/disable
- [ ] Identical requests return cached results with X-Cache: HIT
- [ ] Cache invalidated when entity lists change
- [ ] TTL configurable via CACHE_TTL_SECONDS (default 60s)
- [ ] No crash if Redis is unavailable (graceful fallback)

## Dependencies
- Runs independently; optionally after asyncpg migration
