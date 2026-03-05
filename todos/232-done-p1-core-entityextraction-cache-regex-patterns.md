# 232 — Cache Compiled Regex Patterns

**Repo:** core-entityextraction  
**Priority:** P1 (Performance)  
**Effort:** 4 hours  
**Dependencies:** 231

## Description
`match_patterns()` calls `_build_entity_patterns()` for all 17 entity types on every extraction request. This rebuilds pattern lists from the entity store and calls `re.compile()` on a potentially huge joined pattern string. Cache the compiled patterns, invalidated only when the entity store changes.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Add module-level pattern cache:
   _pattern_cache: Dict[str, Tuple[re.Pattern, Dict]] = {}
   _cache_dirty: bool = True

2. Add cache invalidation helper:
   def _invalidate_pattern_cache():
       global _cache_dirty
       _cache_dirty = True

3. Add cache build function:
   def _ensure_pattern_cache():
       global _pattern_cache, _cache_dirty
       if not _cache_dirty:
           return
       new_cache = {}
       for entity_type, opts in ENTITY_OPTIONS.items():
           values, options = _build_entity_patterns(entity_type, dict(opts))
           if not values:
               continue
           # Build and compile the regex
           special_chars = ("\\", ".", "+", "*", "?", "^", "$", "(", ")", "[", "]", "{", "}", "|")
           def clean(v):
               return functools.reduce(lambda m, ch: m.replace(ch, f"\\{ch}"), special_chars, v)
           cleaned = [clean(v) for v in values]
           joined = "|".join(cleaned)
           flags = [] if options.get("case_sensitive") else [re.IGNORECASE]
           try:
               compiled = re.compile(r"(?:^|\W)(" + joined + r")(?:$|\W)", *flags)
               new_cache[entity_type] = (compiled, options)
           except re.error as e:
               LOGGER.error("Failed to compile pattern for %s: %s", entity_type, e)
       _pattern_cache = new_cache
       _cache_dirty = False
       LOGGER.info("Pattern cache rebuilt: %d entity types", len(_pattern_cache))

4. Update match_patterns() to use cache:
   def match_patterns(...):
       _ensure_pattern_cache()
       # Use _pattern_cache[entity_type] instead of calling _build_entity_patterns

5. Update _locate_entities() signature to accept pre-compiled pattern instead of values list.

6. Call _invalidate_pattern_cache() in:
   - update_fixed_lists() after modifying entity_store
   - delete_fixed_lists() after clearing entity_store
   - startup_event() after load_all()
```

## Acceptance Criteria
- [ ] Pattern cache built once on startup, not per-request
- [ ] Cache invalidated on every /fixed_lists write or delete
- [ ] Extraction results identical to pre-cache behavior
- [ ] 10x+ reduction in CPU time for extraction on loaded entity store
- [ ] Thread-safe (use threading.Lock if needed)
