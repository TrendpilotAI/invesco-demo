# TODO 407 — Custom Exception Hierarchy for signal-studio-data-provider

**Repo:** signal-studio-data-provider  
**Priority:** High (P1)  
**Effort:** Small (0.5 days)  
**Status:** pending

## Description
All providers raise generic `ValueError`/`RuntimeError`. Callers cannot catch specific error types for proper handling (e.g., retry on ConnectionError vs fail-fast on QueryError).

## Task
Add a custom exception hierarchy in `providers/base.py`:

```python
class DataProviderError(Exception):
    """Base exception for all DataProvider errors."""

class ProviderConnectionError(DataProviderError):
    """Raised when a connection cannot be established or is lost."""

class ProviderQueryError(DataProviderError):
    """Raised when a query fails to execute."""

class ProviderSchemaError(DataProviderError):
    """Raised when schema introspection fails."""

class BudgetExceededError(DataProviderError):
    """Raised when a query would exceed org budget limits."""

class IdentifierValidationError(DataProviderError):
    """Raised when a table/column name fails safe-identifier validation."""
```

Then update all providers to raise these specific types instead of `ValueError`/`RuntimeError`.

## Acceptance Criteria
- [ ] Custom exceptions defined in `providers/base.py`
- [ ] All providers updated to use specific exceptions
- [ ] Tests updated to catch specific exception types
- [ ] `__all__` in `__init__.py` exports exception types

## Dependencies
None (foundational change)
