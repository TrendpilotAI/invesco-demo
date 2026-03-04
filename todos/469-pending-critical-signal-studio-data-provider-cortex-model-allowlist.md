---
id: "469"
status: pending
priority: critical
repo: signal-studio-data-provider
title: "Fix Snowflake Cortex model string injection — add allowlist"
effort: S
dependencies: []
created: "2026-03-04"
---

## Task Description

`providers/snowflake_provider.py` lines 203 and 211 interpolate the `model` parameter directly into SQL strings for Cortex COMPLETE and EMBED calls. This is a SQL injection vector.

```python
# Line 203 — VULNERABLE
f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', %s) AS response"
# Line 211 — VULNERABLE  
f"SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('{model}', %s) AS embedding"
```

## Coding Prompt

In `providers/snowflake_provider.py`:

1. Add an allowlist constant after the imports:
```python
ALLOWED_CORTEX_MODELS: frozenset[str] = frozenset({
    "mistral-large",
    "mistral-7b", 
    "llama3-8b",
    "llama3-70b",
    "claude-3-haiku",
    "snowflake-arctic",
    "reka-flash",
    "jamba-instruct",
})
```

2. Add a validation function:
```python
def _validate_cortex_model(model: str) -> str:
    """Raise ValueError if model is not in the Cortex allowlist."""
    if model not in ALLOWED_CORTEX_MODELS:
        raise ValueError(
            f"Unsupported Cortex model: {model!r}. "
            f"Allowed: {sorted(ALLOWED_CORTEX_MODELS)}"
        )
    return model
```

3. Call it in `cortex_complete()` and `cortex_embed()` before interpolation:
```python
async def cortex_complete(self, model: str, prompt: str) -> str:
    model = _validate_cortex_model(model)
    ...

async def cortex_embed(self, model: str, text: str) -> list[float]:
    model = _validate_cortex_model(model)
    ...
```

4. Add tests in `tests/test_providers.py`:
```python
def test_cortex_rejects_unknown_model(mock_snowflake_provider):
    with pytest.raises(ValueError, match="Unsupported Cortex model"):
        asyncio.run(mock_snowflake_provider.cortex_complete("evil'model", "test"))
```

## Acceptance Criteria
- [ ] `ALLOWED_CORTEX_MODELS` frozenset defined in snowflake_provider.py
- [ ] `_validate_cortex_model()` raises ValueError for unknown models
- [ ] Both `cortex_complete` and `cortex_embed` validate model before interpolation
- [ ] Test coverage for rejection of invalid model names
- [ ] CI passes
