# TODO-398: Cache Compiled Regex Patterns (Performance)

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** S (2 hours)  
**Status:** pending

## Description
`match_patterns()` calls `_build_entity_patterns()` for all 17 entity types on every single request. With thousands of entities, this re-iterates sets and concatenates strings from scratch every time. No compiled `re.Pattern` objects are cached.

Estimated improvement: 20-50x speedup on large entity stores.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Add module-level pattern cache and version counter:
   _pattern_cache: Dict[str, re.Pattern] = {}
   _store_version: int = 0

2. Create a function build_all_pattern_cache() that:
   - Iterates ENTITY_OPTIONS
   - Calls _build_entity_patterns() for each entity type
   - Compiles the joined regex: re.compile(r"(?:^|\W)(" + joined + r")(?:$|\W)", flags)
   - Stores in _pattern_cache[entity_type]
   - Called at startup (after entity store is loaded) and after every /fixed_lists write

3. Modify match_patterns() to use _pattern_cache instead of calling _build_entity_patterns + re.compile inline

4. In /fixed_lists POST and DELETE handlers, after updating entity_store, call:
   global _store_version
   _store_version += 1
   build_all_pattern_cache()

5. Add _pattern_cache to the startup_event() after persistence.load_all() completes

6. Add a simple benchmark test to verify improvement:
   import time; t=time.time(); [match_patterns(["test text"]) for _ in range(100)]; print(time.time()-t)
```

## Dependencies
None

## Acceptance Criteria
- Pattern cache populated at startup
- Cache invalidated on /fixed_lists writes
- No regression in extraction results
- Measurable speedup on repeated calls
