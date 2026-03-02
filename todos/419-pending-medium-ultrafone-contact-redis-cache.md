# TODO 419: Contact Lookup Redis Caching

**Repo:** Ultrafone  
**Priority:** Medium  
**Effort:** S (2-3 hours)  
**Dependencies:** None

## Description
Contact lookup happens on every inbound call. For large contact lists (thousands of contacts from HubSpot/Google), this could add latency. Cache phone→contact mappings in Redis with TTL.

## Coding Prompt
```
1. In services/contact_service.py, add Redis caching layer:
   - Key: contact:phone:{normalized_phone}
   - Value: JSON serialized contact dict
   - TTL: 300 seconds (5 min)
   
2. Cache lookup flow:
   a. Check Redis for phone number
   b. If hit: return cached contact
   c. If miss: query DB, serialize, store in Redis, return
   
3. Cache invalidation: on contact sync (google/hubspot/icloud), flush contact:phone:* keys
4. Add cache hit/miss metrics to PostHog
5. Add REDIS_CONTACT_CACHE_TTL to config/settings.py
6. Write unit tests for cache hit and miss paths
```

## Acceptance Criteria
- Contact lookup on cache hit takes <5ms (vs DB query ~50ms)
- Cache invalidates after contact sync
- Cache miss falls back to DB correctly
- Tests cover both paths
