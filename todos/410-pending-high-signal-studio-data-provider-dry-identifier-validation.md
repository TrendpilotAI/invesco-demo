# TODO 410 — DRY: Deduplicate Identifier Validation Across Providers

**Repo:** signal-studio-data-provider  
**Priority:** High  
**Effort:** Small (0.25 days)  
**Status:** pending

## Description
`_SAFE_IDENTIFIER_RE` regex and `_validate_identifier()` function are copy-pasted verbatim in:
- `providers/snowflake_provider.py:7-13`
- `providers/supabase_provider.py:7-13`
- `providers/oracle_provider.py:7-13`

Classic DRY violation. If the regex needs updating for a new attack vector, must update 3 files.

## Task
1. Move to `providers/base.py`:
```python
import re

_SAFE_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

def validate_identifier(name: str) -> str:
    """Raise ValueError if name is not a safe SQL identifier."""
    if not _SAFE_IDENTIFIER_RE.match(name):
        raise ValueError(f"Unsafe SQL identifier: {name!r}")
    return name
```

2. Remove duplicate definitions from all three providers
3. Update imports: `from .base import validate_identifier`

## Acceptance Criteria
- [ ] Single definition in `providers/base.py`
- [ ] All providers import from base
- [ ] Tests pass unchanged

## Dependencies
TODO 407 (custom exceptions — IdentifierValidationError might replace ValueError here)
