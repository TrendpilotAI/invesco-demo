# TODO-356: Comprehensive Tests for schema_builder + analytical_db
**Project:** signal-builder-backend  
**Priority:** P0  
**Effort:** M (3–4 days)  
**Status:** pending  
**Created:** 2026-03-01

---

## Description

`apps/schema_builder/` and `apps/analytical_db/` are identified as HIGH risk modules with no visible test coverage. `schema_builder` handles core logic for building database schemas from signal definitions; `analytical_db` manages connections and query execution against the analytical PostgreSQL database. Both are complex, critical paths with zero safety net.

---

## Full Autonomous Coding Prompt

```
You are working on the signal-builder-backend FastAPI service at /data/workspace/projects/signal-builder-backend/.

TASK: Add comprehensive test coverage (>80%) for apps/schema_builder/ and apps/analytical_db/.

STEP 1 — Explore the modules:
```
find apps/schema_builder/ -name "*.py" | head -30
find apps/analytical_db/ -name "*.py" | head -30
cat apps/schema_builder/__init__.py 2>/dev/null || echo "no init"
ls -la apps/schema_builder/
ls -la apps/analytical_db/
```

STEP 2 — Read key files to understand the architecture:
```
# Read all Python files in schema_builder
for f in $(find apps/schema_builder -name "*.py" -not -name "__init__.py"); do
    echo "=== $f ==="; cat "$f"; echo
done

# Read all Python files in analytical_db
for f in $(find apps/analytical_db -name "*.py" -not -name "__init__.py"); do
    echo "=== $f ==="; cat "$f"; echo
done
```

STEP 3 — Check existing test structure for patterns to follow:
```
find apps/ -name "test_*.py" -o -name "*_test.py" | head -10
cat apps/signals/tests/test_create_signal_case.py  # or similar existing test
```

STEP 4 — Create test directory structure:
```
mkdir -p apps/schema_builder/tests
touch apps/schema_builder/tests/__init__.py
mkdir -p apps/analytical_db/tests  
touch apps/analytical_db/tests/__init__.py
```

STEP 5 — Create schema_builder tests at `apps/schema_builder/tests/test_schema_builder.py`.

Based on what you find in the module, write tests covering:

**Schema validation tests:**
```python
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Test valid schema construction
def test_build_schema_with_valid_signal():
    """Valid signal definition produces correct schema."""
    # Use whatever SchemaBuilder class/function exists
    # Create minimal valid signal fixture
    # Assert schema has expected tables/columns/types

# Test edge cases
def test_build_schema_empty_signal():
    """Empty or minimal signal produces valid empty schema."""
    ...

def test_build_schema_with_all_field_types():
    """All supported field types are handled correctly."""
    ...

def test_build_schema_with_nested_groups():
    """Nested group structures in signal produce correct schema."""
    ...

# Test error conditions
def test_build_schema_invalid_field_type_raises():
    """Invalid field type raises SchemaBuilderError (not silent failure)."""
    ...

def test_build_schema_duplicate_column_names():
    """Duplicate column names are handled (deduplicated or error)."""
    ...

def test_build_schema_with_special_characters_in_names():
    """Field names with special characters are sanitized."""
    ...
```

STEP 6 — Create analytical_db tests at `apps/analytical_db/tests/test_analytical_db.py`.

Mock all DB connections — tests must not require a real database:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
import asyncio

# Mock the DB connection throughout
@pytest.fixture
def mock_db_connection():
    conn = AsyncMock()
    conn.execute = AsyncMock(return_value=MagicMock(fetchall=lambda: []))
    conn.close = AsyncMock()
    return conn

@pytest.fixture  
def mock_db_pool(mock_db_connection):
    pool = AsyncMock()
    pool.acquire = AsyncMock(return_value=mock_db_connection)
    pool.__aenter__ = AsyncMock(return_value=mock_db_connection)
    pool.__aexit__ = AsyncMock(return_value=None)
    return pool

# Test connection management
@pytest.mark.asyncio
async def test_get_connection_returns_connection(mock_db_pool):
    """DB connection is acquired from pool correctly."""
    ...

@pytest.mark.asyncio
async def test_connection_released_after_use(mock_db_pool):
    """Connection is always released back to pool, even on error."""
    ...

@pytest.mark.asyncio
async def test_connection_released_on_exception(mock_db_pool):
    """Connection released even when query raises exception."""
    ...

# Test query execution
@pytest.mark.asyncio
async def test_execute_query_returns_results(mock_db_connection):
    """Query execution returns properly formatted results."""
    mock_db_connection.execute.return_value = MagicMock(
        fetchall=lambda: [{"col": "val"}]
    )
    ...

@pytest.mark.asyncio
async def test_execute_query_with_parameters(mock_db_connection):
    """Parameterized queries pass parameters correctly."""
    ...

@pytest.mark.asyncio
async def test_execute_invalid_sql_raises(mock_db_connection):
    """Invalid SQL surfaces as an appropriate exception."""
    from asyncpg import PostgresSyntaxError
    mock_db_connection.execute.side_effect = PostgresSyntaxError("syntax error")
    ...

# Test sync cases (from analytical_db_sync_cases.py)
@pytest.mark.asyncio
async def test_sync_creates_schema_if_not_exists():
    """Sync operation creates schema when it doesn't exist."""
    ...

@pytest.mark.asyncio  
async def test_sync_updates_existing_schema():
    """Sync operation updates schema when signal changes."""
    ...

@pytest.mark.asyncio
async def test_sync_handles_connection_failure_gracefully():
    """Connection failure during sync raises appropriate error."""
    ...

# Test prepare_query_service (has a known potential bug on line 67)
def test_prepare_query_does_not_delete_data_unexpectedly():
    """Regression test for TODO: might be a bug in cleanup query at line 67."""
    # Test that the cleanup query only affects expected rows
    ...
```

STEP 7 — Run coverage for these modules:
```
cd /data/workspace/projects/signal-builder-backend
pipenv run pytest apps/schema_builder/tests/ apps/analytical_db/tests/ -v \
    --cov=apps/schema_builder --cov=apps/analytical_db \
    --cov-report=term-missing \
    --cov-report=html:htmlcov/
```

STEP 8 — Iterate until >80% coverage on both modules:
```
# Check coverage report
pipenv run pytest apps/schema_builder/ apps/analytical_db/ \
    --cov=apps/schema_builder --cov=apps/analytical_db \
    --cov-fail-under=80
```
Add more tests for any uncovered branches shown in the report.

STEP 9 — Add conftest.py fixtures for reuse:
```
cat > apps/schema_builder/tests/conftest.py << 'EOF'
import pytest

@pytest.fixture
def minimal_signal():
    """Minimal valid signal for schema tests."""
    return {
        "id": 1,
        "name": "Test Signal",
        "nodes": [],
        "edges": []
    }

@pytest.fixture
def full_signal():
    """Signal with all field types."""
    # Build from real signal structure observed in the codebase
    ...
EOF
```

STEP 10 — Run full test suite to ensure no regressions:
```
pipenv run pytest -v
```
```

---

## Dependencies

- Pydantic v2 migration (TODO-352) should ideally be done first so tests are written for v2
- No hard blockers — can write tests in v1 style and migrate later

---

## Effort Estimate

**3–4 days** — Exploration of undocumented modules takes time. Writing meaningful tests (not just coverage padding) for complex schema-building logic requires deep understanding of the domain.

---

## Acceptance Criteria

- [ ] `apps/schema_builder/tests/test_schema_builder.py` exists with ≥15 test cases
- [ ] `apps/analytical_db/tests/test_analytical_db.py` exists with ≥15 test cases
- [ ] Coverage on `apps/schema_builder/` ≥ 80% (`--cov-fail-under=80` passes)
- [ ] Coverage on `apps/analytical_db/` ≥ 80% (`--cov-fail-under=80` passes)
- [ ] All DB connections in tests are mocked — tests pass without a real database
- [ ] Tests cover: happy path, edge cases, error conditions, exception handling
- [ ] Regression test for potential bug in `prepare_query_service.py:67`
- [ ] All existing tests still pass after adding new tests
- [ ] `conftest.py` with shared fixtures in place
