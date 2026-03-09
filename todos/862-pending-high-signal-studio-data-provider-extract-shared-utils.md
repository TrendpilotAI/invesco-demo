# TODO-862: Extract _validate_identifier and build_schema_info to Shared Utils

**Repo:** signal-studio-data-provider  
**Priority:** High  
**Effort:** S (1 hour)  
**Status:** pending  
**Depends on:** None

## Problem
`_validate_identifier` is duplicated in `providers/snowflake_provider.py` and `providers/supabase_provider.py`.
`get_schema()` assembly pattern duplicated across all 3 providers.

## Fix
Create `providers/_utils.py`:
```python
import re
_SAFE_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

def validate_identifier(name: str) -> str:
    if not _SAFE_IDENTIFIER_RE.match(name):
        raise ValueError(f"Unsafe SQL identifier: {name!r}")
    return name
```

Remove duplicates from snowflake + supabase providers; import from `_utils`.

## Acceptance Criteria
- [ ] Single `validate_identifier` in `providers/_utils.py`
- [ ] snowflake + supabase providers import from `_utils`
- [ ] All existing tests still pass
