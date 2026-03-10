# TODO-826: Fix Optional Storage Params in SignalCases

**Repo:** signal-builder-backend  
**Priority:** HIGH  
**Effort:** S (1-2 hours)  
**Status:** pending

## Problem

`apps/signals/cases/signal.py` — `SignalCases.__init__` accepts:
```python
signal_version_storage: SignalVersionStorage = None,
signal_run_storage: SignalRunStorage = None,
```

These are `= None` defaults, meaning if the DI container fails to wire them, the app starts silently with `None` storages. Any call to `self._signal_version_storage.method()` raises `AttributeError` at runtime, NOT at startup. This is a silent failure mode.

## Fix

Remove default `None` values. Make them required params:
```python
signal_version_storage: SignalVersionStorage,
signal_run_storage: SignalRunStorage,
```

Then verify the DI container in `apps/signals/containers.py` properly wires both. Run the full test suite to confirm nothing breaks.

## Coding Prompt

```
File: apps/signals/cases/signal.py
Find SignalCases.__init__ and remove default None values from:
  - signal_version_storage: SignalVersionStorage = None  →  signal_version_storage: SignalVersionStorage
  - signal_run_storage: SignalRunStorage = None           →  signal_run_storage: SignalRunStorage

Then check apps/signals/containers.py to ensure the DI container provides both.
Add a startup check test that instantiating the container doesn't raise.
Run: pipenv run pytest apps/signals/ -v
```

## Acceptance Criteria
- `SignalCases.__init__` has no default `None` params for storage dependencies
- DI container wires both storages without error
- All existing signal tests pass
