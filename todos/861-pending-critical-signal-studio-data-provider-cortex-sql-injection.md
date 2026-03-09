# TODO-861: Fix Cortex SQL Injection in SnowflakeProvider

**Repo:** signal-studio-data-provider  
**Priority:** CRITICAL 🔴  
**Effort:** S (< 1 hour)  
**Status:** pending

## Problem
`providers/snowflake_provider.py` — `cortex_complete()` and `cortex_embed()` interpolate the `model` parameter directly into SQL f-strings:

```python
f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', %s) AS response"
f"SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('{model}', %s) AS embedding"
```

An attacker controlling `model` can inject arbitrary SQL.

## Fix
Add a whitelist validator in `providers/snowflake_provider.py`:

```python
_CORTEX_MODELS = frozenset({
    "llama3-8b", "llama3-70b", "mistral-7b", "mixtral-8x7b",
    "snowflake-arctic", "reka-flash", "reka-core"
})

def _validate_cortex_model(model: str) -> str:
    if model not in _CORTEX_MODELS:
        raise ValueError(f"Unknown Cortex model: {model!r}")
    return model
```

Call before interpolating. Add test in `tests/test_security.py`.

## Acceptance Criteria
- [ ] `cortex_complete()` and `cortex_embed()` validate model name against whitelist
- [ ] Test: invalid model raises `ValueError`
- [ ] Test: SQL injection payload in model name raises `ValueError`
