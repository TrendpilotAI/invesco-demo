# 214 · PYTEST TESTS — EASY_BUTTON AND ANALYTICAL APPS

**Repo:** forwardlane-backend  
**Priority:** P0 (zero test coverage on security-critical, unauthenticated endpoints)  
**Effort:** M (1–2 days)  
**Status:** pending

---

## Task Description

Both `easy_button/` and `analytical/` have **zero test coverage**. These apps include:
- SQL injection surface (`AdvisorListView`, `NLQueryView`)
- Security-critical SQL sanitization (`_clean_sql()` in NLQueryView)
- Public unauthenticated endpoints (fixed by TODO #211, but need test coverage)
- Complex business logic (`_derive_risk_score`, `_generate_talking_points`)
- LLM-generated SQL execution chain (Gemini → Kimi → keyword fallback)

This task creates a pytest test suite for both apps using factory fixtures and mocked
database connections (no live DB required for unit tests).

---

## Coding Prompt (Agent-Executable)

```
You are creating pytest tests for forwardlane-backend at /data/workspace/projects/forwardlane-backend/.

CONTEXT:
- easy_button/views.py: 8 view classes, 1344 lines
- analytical/views.py: 5 view classes, 560 lines
- Both apps use ANALYTICAL_DB_URL / connections['analytical']
- NLQueryView._clean_sql() is the security barrier for LLM-generated SQL
- The project uses pytest-django (check Pipfile/tox.ini for existing test config)

TASK: Create comprehensive test suites for both apps.

STEP 1 — Check existing test infrastructure:
Run: cat /data/workspace/projects/forwardlane-backend/tox.ini
Run: cat /data/workspace/projects/forwardlane-backend/pytest.ini 2>/dev/null || echo "no pytest.ini"
Run: cat /data/workspace/projects/forwardlane-backend/Pipfile | grep -A5 "dev-packages"
Understand the existing test patterns before writing new ones.

STEP 2 — Create easy_button/tests/__init__.py (empty)

STEP 3 — Create easy_button/tests/conftest.py:
"""
Shared fixtures for easy_button tests.
All DB access is mocked — no live analytical DB required.
"""
import pytest
from unittest.mock import MagicMock, patch
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(db):
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpass123')
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def mock_analytical_cursor():
    """Returns a factory for creating mock analytical DB cursors."""
    def _make_cursor(description, fetchone_result=None, fetchall_result=None):
        cursor = MagicMock()
        cursor.__enter__ = MagicMock(return_value=cursor)
        cursor.__exit__ = MagicMock(return_value=False)
        cursor.description = [(col,) for col in description]
        if fetchone_result is not None:
            cursor.fetchone.return_value = fetchone_result
        if fetchall_result is not None:
            cursor.fetchall.return_value = fetchall_result
        return cursor
    return _make_cursor


@pytest.fixture
def mock_connections(mock_analytical_cursor):
    """Patches django.db.connections to return a mock analytical cursor."""
    with patch('easy_button.views.connections') as mock_conns:
        def get_cursor(description, fetchone=None, fetchall=None):
            cur = mock_analytical_cursor(description, fetchone, fetchall)
            mock_conns.__getitem__.return_value.cursor.return_value = cur
            return cur
        mock_conns._get_cursor = get_cursor
        yield mock_conns

STEP 4 — Create easy_button/tests/test_nl_query_security.py:
"""
CRITICAL: Tests for NLQueryView._clean_sql() security sanitizer.
This is the primary barrier between LLM output and database execution.
"""
import pytest
from easy_button.views import NLQueryView


@pytest.mark.parametrize("dangerous_sql,description", [
    ("select pg_read_file('/etc/passwd')", "pg_read_file"),
    ("select * from pg_catalog.pg_shadow", "pg_shadow"),
    ("select current_setting('server_version')", "current_setting"),
    ("select 1; DROP TABLE advisors;", "statement stacking"),
    ("UPDATE advisors SET aum_current = 0", "UPDATE statement"),
    ("DELETE FROM advisors", "DELETE statement"),
    ("INSERT INTO advisors VALUES (1)", "INSERT statement"),
    ("DROP TABLE advisors", "DROP TABLE"),
    ("TRUNCATE advisors", "TRUNCATE"),
    ("CREATE TABLE evil AS SELECT 1", "CREATE TABLE"),
    ("ALTER TABLE advisors ADD COLUMN evil TEXT", "ALTER TABLE"),
    ("GRANT ALL ON advisors TO public", "GRANT"),
])
def test_clean_sql_blocks_dangerous(dangerous_sql, description):
    """_clean_sql() must raise ValueError for all dangerous patterns."""
    view = NLQueryView()
    with pytest.raises(ValueError, match=r"(?i)(dangerous|not allowed|invalid)"):
        view._clean_sql(dangerous_sql)


@pytest.mark.parametrize("safe_sql", [
    "SELECT advisor_id, full_name FROM advisors WHERE aum_current > 1000000 LIMIT 50",
    "SELECT COUNT(*) FROM advisors",
    "SELECT a.advisor_id, s.signal_type FROM advisors a JOIN signals s ON a.advisor_id = s.advisor_id LIMIT 20",
    "select advisor_id from advisors where region = 'NE' limit 10",
])
def test_clean_sql_allows_safe_queries(safe_sql):
    """_clean_sql() must not raise for legitimate SELECT queries."""
    view = NLQueryView()
    result = view._clean_sql(safe_sql)
    assert result is not None
    assert "SELECT" in result.upper() or "select" in result


def test_clean_sql_adds_limit_when_missing():
    """_clean_sql() must append LIMIT if not present."""
    view = NLQueryView()
    result = view._clean_sql("SELECT advisor_id FROM advisors")
    assert "LIMIT" in result.upper()


def test_clean_sql_enforces_max_limit():
    """_clean_sql() must cap LIMIT at a reasonable maximum."""
    view = NLQueryView()
    result = view._clean_sql("SELECT advisor_id FROM advisors LIMIT 99999")
    import re
    match = re.search(r'LIMIT\s+(\d+)', result, re.I)
    if match:
        assert int(match.group(1)) <= 500  # Some reasonable maximum


def test_clean_sql_strips_single_line_comments():
    """SQL comments should be stripped."""
    view = NLQueryView()
    result = view._clean_sql("SELECT 1 -- DROP TABLE advisors")
    assert "DROP" not in result.upper()

STEP 5 — Create easy_button/tests/test_dashboard_view.py:
"""Tests for DashboardView GET /api/v1/easy-button/dashboard/"""
import pytest
from unittest.mock import patch, MagicMock
from rest_framework import status


@pytest.fixture
def dashboard_cursor_mock():
    """Mock cursor returning KPI data."""
    cursor = MagicMock()
    cursor.__enter__ = MagicMock(return_value=cursor)
    cursor.__exit__ = MagicMock(return_value=False)
    # advisors_count, total_aum, prev_aum, avg_growth_pct
    cursor.fetchone.return_value = (150, 45_000_000_000, 42_000_000_000, 7.1)
    cursor.fetchall.return_value = [
        ('CROSS_SELL_ETF', 25),
        ('AUM_DECLINE', 18),
        ('RIA_CONVERSION', 12),
    ]
    return cursor


@patch('easy_button.views.connections')
def test_dashboard_returns_200(mock_conns, api_client, dashboard_cursor_mock):
    mock_conns.__getitem__.return_value.cursor.return_value = dashboard_cursor_mock
    response = api_client.get('/api/v1/easy-button/dashboard/')
    assert response.status_code == status.HTTP_200_OK


@patch('easy_button.views.connections')
def test_dashboard_returns_expected_keys(mock_conns, api_client, dashboard_cursor_mock):
    mock_conns.__getitem__.return_value.cursor.return_value = dashboard_cursor_mock
    response = api_client.get('/api/v1/easy-button/dashboard/')
    data = response.json()
    # Assert top-level KPI keys are present (adjust to match actual response shape)
    assert any(key in data for key in ['advisors_count', 'total_aum', 'kpis', 'signals'])

STEP 6 — Create easy_button/tests/test_nl_query_view.py:
"""Tests for NLQueryView POST /api/v1/easy-button/nl-query/"""
import pytest
from unittest.mock import patch


@patch('easy_button.views.NLQueryView._call_gemini', return_value="SELECT advisor_id FROM advisors LIMIT 10")
@patch('easy_button.views.connections')
def test_nl_query_returns_sql(mock_conns, mock_gemini, api_client):
    mock_cursor = mock_conns.__getitem__.return_value.cursor.return_value.__enter__.return_value
    mock_cursor.description = [('advisor_id',)]
    mock_cursor.fetchall.return_value = [('ADV001',)]
    
    response = api_client.post('/api/v1/easy-button/nl-query/', {'query': 'show all advisors'}, format='json')
    assert response.status_code == 200


@patch('easy_button.views.NLQueryView._call_gemini', side_effect=Exception("API timeout"))
@patch('easy_button.views.NLQueryView._call_kimi', return_value="SELECT advisor_id FROM advisors LIMIT 10")
@patch('easy_button.views.connections')
def test_nl_query_falls_back_to_kimi(mock_conns, mock_kimi, mock_gemini, api_client):
    mock_cursor = mock_conns.__getitem__.return_value.cursor.return_value.__enter__.return_value
    mock_cursor.description = [('advisor_id',)]
    mock_cursor.fetchall.return_value = []
    
    response = api_client.post('/api/v1/easy-button/nl-query/', {'query': 'show at-risk advisors'}, format='json')
    assert response.status_code == 200
    mock_kimi.assert_called_once()


def test_nl_query_requires_query_param(api_client):
    response = api_client.post('/api/v1/easy-button/nl-query/', {}, format='json')
    assert response.status_code in [400, 422]

STEP 7 — Add easy_button and analytical to tox.ini:
In tox.ini, find the pylint command line that lists apps. Add 'easy_button analytical' to that list.
Example: if it says `pylint user pipeline_engine core ...` change to `pylint user pipeline_engine core ... easy_button analytical`

STEP 8 — Run the tests to confirm they work:
Run: cd /data/workspace/projects/forwardlane-backend && python -m pytest easy_button/tests/ -v 2>&1 | head -60
Fix any import errors or missing fixtures.
```

---

## Files to Create

| File | Contents |
|------|----------|
| `easy_button/tests/__init__.py` | Empty |
| `easy_button/tests/conftest.py` | Shared fixtures (APIClient, mock cursor factory) |
| `easy_button/tests/test_nl_query_security.py` | `_clean_sql()` security tests (highest priority) |
| `easy_button/tests/test_dashboard_view.py` | DashboardView GET tests |
| `easy_button/tests/test_nl_query_view.py` | NLQueryView POST + fallback chain tests |
| `easy_button/tests/test_advisor_list_view.py` | Pagination, filters, sort whitelist |
| `easy_button/tests/test_advisor_detail_view.py` | 404 path, nested structure |
| `easy_button/tests/test_meeting_prep_view.py` | LLM mock, 404 path |
| `analytical/tests/__init__.py` | Empty |
| `analytical/tests/conftest.py` | Analytical fixtures |
| `analytical/tests/test_dashboard_view.py` | Analytical dashboard tests |

## Files to Modify

| File | Change |
|------|--------|
| `tox.ini` | Add `easy_button analytical` to pylint app list |

---

## Acceptance Criteria

- [ ] `python -m pytest easy_button/tests/ -v` passes with no errors
- [ ] `_clean_sql()` security tests cover all `_DANGEROUS_PATTERNS` entries
- [ ] All dangerous SQL patterns raise `ValueError`
- [ ] All safe SELECT queries pass `_clean_sql()`
- [ ] `DashboardView` test asserts 200 status and expected response keys
- [ ] `NLQueryView` test verifies Gemini → Kimi fallback chain works
- [ ] `NLQueryView` test verifies missing query param returns 4xx
- [ ] `easy_button` and `analytical` added to tox.ini pylint command
- [ ] No tests make live DB or API calls (all mocked)

---

## Notes

- Start with `test_nl_query_security.py` — highest risk, easiest to write
- The `_clean_sql()` patterns are in `easy_button/views.py` around line 1340–1365
- Check `_DANGEROUS_PATTERNS` list to ensure parametrize covers all entries
- After TODO #211 (auth), add auth behavior tests: token present/absent, DEMO_ENV values
