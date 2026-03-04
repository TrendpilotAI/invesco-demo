---
id: "472"
status: pending
priority: high
repo: signal-studio-data-provider
title: "DRY: Extract _validate_identifier to shared _utils.py"
effort: XS
dependencies: []
created: "2026-03-04"
---

## Task Description

`_SAFE_IDENTIFIER_RE` and `_validate_identifier()` are copy-pasted identically across `supabase_provider.py`, `oracle_provider.py`, and likely `snowflake_provider.py`. Any bug fix must be applied in 3 places.

## Coding Prompt

1. Create `providers/_utils.py`:
```python
"""Shared utilities for DataProvider implementations."""
from __future__ import annotations
import re

_SAFE_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def validate_identifier(name: str) -> str:
    """Raise ValueError if *name* is not a safe SQL identifier.
    
    Allows: letters, digits, underscores. Must start with letter or underscore.
    Rejects: spaces, quotes, hyphens, SQL keywords embedded in names.
    """
    if not _SAFE_IDENTIFIER_RE.match(name):
        raise ValueError(f"Unsafe SQL identifier: {name!r}")
    return name
```

2. In each provider file, replace the local definition with an import:
```python
# Remove the local _SAFE_IDENTIFIER_RE and _validate_identifier
# Add:
from ._utils import validate_identifier
```

3. Update all call sites: `_validate_identifier(x)` → `validate_identifier(x)`

4. Verify all existing tests still pass (no behavior change).

## Acceptance Criteria
- [ ] `providers/_utils.py` created with `validate_identifier()`
- [ ] All 3 provider files import from `_utils` instead of defining locally
- [ ] No remaining local `_validate_identifier` or `_SAFE_IDENTIFIER_RE` definitions in provider files
- [ ] CI passes
