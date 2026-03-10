# TODO-890: Fix Duplicate Filter Block Bug in match_patterns()

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** XS (5 minutes)  
**Status:** pending

## Problem

`match_patterns()` in `main.py` applies the `include_entity_types` entity filter **twice** — once against `compiled_patterns` and again against `all_patterns`. The second application is redundant (idempotent in normal use) but:
- Wastes CPU on every request when filtering is used
- Creates a maintenance hazard if either block is modified independently
- Indicates unclear code flow

**Exact location — `main.py` `match_patterns()` function:**
```python
# First block (correct):
if isinstance(include_entity_types, bool):
    if entity_types_list is None:
        entity_types_list = []
    if include_entity_types:
        all_patterns = {k: v for k, v in compiled_patterns.items() if k in entity_types_list}
    else:
        all_patterns = {k: v for k, v in compiled_patterns.items() if k not in entity_types_list}

# SECOND BLOCK — DUPLICATE, REMOVE THIS:
if isinstance(include_entity_types, bool):
    if entity_types_list is None:
        entity_types_list = []
    if include_entity_types:
        all_patterns = {k: v for k, v in all_patterns.items() if k in entity_types_list}
    else:
        all_patterns = {k: v for k, v in all_patterns.items() if k not in entity_types_list}
```

## Fix

Remove the second `if isinstance(include_entity_types, bool):` block entirely from `match_patterns()`.

## Coding Prompt

```
Edit /data/workspace/projects/core-entityextraction/main.py

In the `match_patterns()` function, find the second occurrence of the block:
    if isinstance(include_entity_types, bool):
        if entity_types_list is None:
            entity_types_list = []
        if include_entity_types:
            all_patterns = {k: v for k, v in all_patterns.items() if k in entity_types_list}
        else:
            all_patterns = {k: v for k, v in all_patterns.items() if k not in entity_types_list}

Delete this second block entirely. The first block (which filters `compiled_patterns` into `all_patterns`) should remain.

After the fix, run: pytest tests/ -x -q
```

## Acceptance Criteria
- [ ] `match_patterns()` has exactly ONE `include_entity_types` filter block
- [ ] All existing tests pass
- [ ] `test_filter_include_entity_types` test in `test_regex_extraction.py` still passes

## Dependencies
None
