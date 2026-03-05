# TODO-618: Fix Duplicate Entity Type Filter Bug in match_patterns()

**Repo:** core-entityextraction  
**Priority:** P0 (Bug)  
**Effort:** S (~10 min)  
**Status:** pending

## Problem
In `main.py`, the `match_patterns()` function applies the `entity_types_list` filter block **twice** — lines ~210-220 repeat the same if/elif logic. The second application is a no-op (the dict is already filtered) but adds confusion and unnecessary iteration overhead.

## Coding Prompt
```
Edit /data/workspace/projects/core-entityextraction/main.py

In match_patterns(), find the duplicate filter block:

    # Filter entity types as requested
    all_patterns = compiled_patterns
    if isinstance(include_entity_types, bool):
        if entity_types_list is None:
            entity_types_list = []
        if include_entity_types:
            all_patterns = {k: v for k, v in compiled_patterns.items() if k in entity_types_list}
        else:
            all_patterns = {k: v for k, v in compiled_patterns.items() if k not in entity_types_list}

    if isinstance(include_entity_types, bool):   # <--- DUPLICATE STARTS HERE
        if entity_types_list is None:
            entity_types_list = []
        if include_entity_types:
            all_patterns = {k: v for k, v in all_patterns.items() if k in entity_types_list}
        else:
            all_patterns = {k: v for k, v in all_patterns.items() if k not in entity_types_list}

Delete the second if isinstance(...) block entirely.
```

## Acceptance Criteria
- [ ] Only one filter block remains in match_patterns()
- [ ] Tests pass (or manual verification: filtering with include_entity_types=True still works)
- [ ] No regression in entity extraction behavior

## Dependencies
None
