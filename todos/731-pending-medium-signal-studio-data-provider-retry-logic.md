# TODO 731: Retry Logic with Exponential Backoff

**Repo:** signal-studio-data-provider  
**Priority:** MEDIUM  
**Effort:** S (half day)  
**Dependencies:** None

## Description
No retry on transient failures. Add `tenacity`-based exponential backoff to all provider `execute_query` and `test_connection` methods. Retry on: network errors, connection timeouts, warehouse restart signals.

## Acceptance Criteria
- [ ] `tenacity` added to dependencies in `pyproject.toml`
- [ ] `@retry_transient` decorator applies to `execute_query`, `get_schema`, `get_tables`, `get_columns`
- [ ] Retry config: max 3 attempts, exponential backoff 1s/2s/4s with jitter
- [ ] Provider-specific transient exceptions mapped (Snowflake: `OperationalError`, asyncpg: `ConnectionFailureError`, Oracle: `DatabaseError` with ORA-03113/ORA-12541)
- [ ] Non-retryable errors (auth failures, SQL syntax) propagate immediately
- [ ] Tests verify retry behavior with mock failures

## Coding Prompt
```python
# providers/retry.py
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import asyncpg

TRANSIENT_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
    asyncpg.TooManyConnectionsError,
    asyncpg.ConnectionFailureError,
)

retry_transient = retry(
    retry=retry_if_exception_type(TRANSIENT_EXCEPTIONS),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    reraise=True,
)

# Apply in providers:
class SnowflakeProvider:
    @retry_transient
    async def execute_query(self, sql, params=None):
        ...
```
