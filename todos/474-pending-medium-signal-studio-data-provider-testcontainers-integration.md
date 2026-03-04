---
id: "474"
status: pending
priority: medium
repo: signal-studio-data-provider
title: "Add testcontainers-based integration tests for Supabase/Oracle providers"
effort: L
dependencies: ["472", "471"]
created: "2026-03-04"
---

## Task Description

All tests are mock-based. Real provider behavior (asyncpg connection pool exhaustion, Oracle parameter binding quirks, actual SQL execution) is untested. Add integration tests using `testcontainers-python`.

## Coding Prompt

1. Add to `pyproject.toml` dev dependencies:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21", 
    "pytest-mock>=3.0",
    "testcontainers[postgres]>=4.0",
    "hypothesis>=6.0",
]
```

2. Create `tests/integration/conftest.py`:
```python
import pytest
import asyncio
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg

@pytest.fixture
async def supabase_provider(postgres_container):
    from signal_studio_data_provider.config import OrgConfig, SupabaseConfig
    from signal_studio_data_provider.providers.supabase_provider import SupabaseProvider
    
    config = OrgConfig(
        org_id="test-org",
        data_tier="self-serve",
        supabase=SupabaseConfig(
            database_url=postgres_container.get_connection_url().replace("postgresql://", "postgresql://")
        )
    )
    provider = SupabaseProvider(config)
    yield provider
    await provider.close()
```

3. Create `tests/integration/test_supabase_integration.py`:
```python
import pytest

@pytest.mark.integration
@pytest.mark.asyncio
async def test_execute_query_returns_results(supabase_provider):
    result = await supabase_provider.execute_query("SELECT 1 AS value")
    assert result.row_count == 1
    assert result.rows[0]["value"] == 1

@pytest.mark.integration
@pytest.mark.asyncio
async def test_test_connection(supabase_provider):
    assert await supabase_provider.test_connection() is True

@pytest.mark.integration
@pytest.mark.asyncio
async def test_write_back_and_read(supabase_provider):
    # Create table, write rows, read back
    await supabase_provider.execute_query(
        "CREATE TABLE IF NOT EXISTS test_scores (id INT, score FLOAT)"
    )
    count = await supabase_provider.write_back(
        "test_scores", [{"id": 1, "score": 0.95}], "test-org"
    )
    assert count == 1
    result = await supabase_provider.execute_query("SELECT * FROM test_scores")
    assert result.row_count == 1

@pytest.mark.integration
@pytest.mark.asyncio
async def test_max_rows_guard(supabase_provider):
    """Ensure row cap is applied for large tables."""
    # Insert 200 rows, cap at 100
    supabase_provider._config.max_query_rows = 100
    # ... seed data and verify result.row_count <= 100
```

4. Add `pytest.ini` marker:
```ini
[pytest]
markers =
    integration: marks tests requiring real database containers (deselect with -m "not integration")
```

5. Update `.github/workflows/ci.yml` to run integration tests as a separate job with `services: postgres`.

## Acceptance Criteria
- [ ] `testcontainers[postgres]` in dev dependencies
- [ ] `tests/integration/` directory with conftest and test files
- [ ] At minimum: test_connection, execute_query, write_back integration tests
- [ ] `@pytest.mark.integration` marker used throughout
- [ ] CI job runs integration tests separately
- [ ] All integration tests pass in CI
