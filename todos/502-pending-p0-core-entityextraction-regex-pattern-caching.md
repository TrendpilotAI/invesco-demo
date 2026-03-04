# TODO-502: Cache Compiled Regex Patterns

**Repo:** core-entityextraction
**Priority:** P0
**Effort:** S (2h)
**Dependencies:** None (can be done independently)
**Blocks:** None

## Description
`_build_entity_patterns()` recompiles regex patterns on every request. Cache compiled patterns keyed by entity type and options hash. Estimated 30-50ms savings per request.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Find _build_entity_patterns() function
2. Add module-level dict: _PATTERN_CACHE = {}
3. Compute a cache key from (entity_type, frozenset of entity options/values)
4. On cache hit, return compiled patterns directly
5. On cache miss, compile and store
6. Add cache invalidation: clear _PATTERN_CACHE when entity store is updated (PUT /fixed_lists endpoint)
7. Alternative: use @functools.lru_cache with appropriate key
8. Add a /debug/pattern_cache_stats endpoint (dev only) showing cache size and hit rate
```

## Acceptance Criteria
- [ ] Patterns compiled once per unique entity configuration
- [ ] Cache invalidated on entity store updates
- [ ] Measurable latency improvement on repeated requests
- [ ] No behavior change in extraction results
