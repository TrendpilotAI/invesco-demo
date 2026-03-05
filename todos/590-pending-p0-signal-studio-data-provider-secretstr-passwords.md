# TODO 590 — Use SecretStr for all passwords and API keys

**Repo:** signal-studio-data-provider  
**Priority:** P0 (Security)  
**Effort:** XS (1-2 hours)  
**Dependencies:** None

## Task Description
All password/key fields in `config.py` are plain `str`, meaning they appear in `repr()` output and can be accidentally logged. Replace with `pydantic.SecretStr`.

## Files to Change
- `/data/workspace/projects/signal-studio-data-provider/config.py`

## Changes Required
```python
from pydantic import BaseModel, Field, SecretStr

class SnowflakeConfig(BaseModel):
    password: SecretStr = Field(repr=False)  # change str → SecretStr

class SupabaseConfig(BaseModel):
    anon_key: SecretStr = Field(repr=False)
    service_role_key: SecretStr = Field(repr=False)
    database_url: SecretStr = Field(repr=False)

class OracleConfig(BaseModel):
    password: SecretStr = Field(repr=False)
```

Then update all provider usages that call `.password` to `.password.get_secret_value()`.

## Autonomous Agent Prompt
```
In /data/workspace/projects/signal-studio-data-provider/config.py, change all password/key fields from `str` to `pydantic.SecretStr`:
- SnowflakeConfig.password
- SupabaseConfig.anon_key, service_role_key, database_url  
- OracleConfig.password

Then search all files in providers/ for usages of these fields and update them to call `.get_secret_value()` where needed (e.g., when passing to DB connectors).

Update tests in tests/ to use `.get_secret_value()` where they compare secret values.

Run `pytest tests/` to verify all tests pass.
```

## Acceptance Criteria
- [ ] All password/key config fields are `SecretStr`
- [ ] `repr(config)` does not show secret values (shows `'**********'`)
- [ ] All providers extract secrets via `.get_secret_value()` before passing to connectors
- [ ] `pytest tests/` passes green
