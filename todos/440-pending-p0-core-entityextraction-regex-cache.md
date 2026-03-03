# TODO-440: Cache compiled regex patterns to eliminate per-request recompilation

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** S (2h)  
**Status:** pending

## Problem
`_build_entity_patterns()` in main.py is called on every extraction request, rebuilding regex patterns from the entity store each time. This is O(n) overhead where n = entity count, estimated 30-50ms wasted per request.

## Task
Compile regex patterns once at startup and cache them; invalidate on entity store update.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Add module-level cache dict:
   _pattern_cache: Dict[str, Tuple[List[str], Dict]] = {}
   _pattern_cache_version: int = 0

2. Wrap _build_entity_patterns() with cache check:
   def _get_entity_patterns(entity_type: str, options: Dict):
       cache_key = f"{entity_type}:{hash(frozenset(options.items()))}"
       if cache_key not in _pattern_cache:
           _pattern_cache[cache_key] = _build_entity_patterns(entity_type, options)
       return _pattern_cache[cache_key]

3. After entity_store is modified (in update_fixed_lists, delete_fixed_lists),
   call _invalidate_pattern_cache() which clears _pattern_cache

4. At startup (after entity store loaded), pre-warm the cache by calling
   _get_entity_patterns() for all entity types with default options

5. Add cache stats to /health endpoint: pattern_cache_size, pattern_cache_hits
```

## Acceptance Criteria
- [ ] Pattern cache populated at startup
- [ ] Cache invalidated on entity store update
- [ ] Benchmark shows >25ms improvement on repeated extraction requests
- [ ] No regressions in extraction accuracy
