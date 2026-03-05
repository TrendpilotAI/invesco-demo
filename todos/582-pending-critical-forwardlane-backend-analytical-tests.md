# TODO-582: Add Tests for analytical/ App

**Priority:** CRITICAL
**Repo:** forwardlane-backend
**Effort:** M (4h)
**Status:** pending

## Problem
`analytical/` has zero test coverage. All 5 endpoints (dashboard, advisors list, advisor detail, signals, easy-button) are completely untested. This is the core Invesco demo layer.

## Fix

Create `analytical/tests/__init__.py` and `analytical/tests/test_views.py`:

```python
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse

class MockCursor:
    def __init__(self, rows, description=None):
        self._rows = rows
        self.description = description or [('col',)]
    def execute(self, sql, params=None): pass
    def fetchone(self): return self._rows[0] if self._rows else None
    def fetchall(self): return self._rows
    def __enter__(self): return self
    def __exit__(self, *a): pass

DASHBOARD_ROW = {'total_advisors': 100, 'total_aum': 5000000, 'avg_aum': 50000, 'total_aum_change_12m': 100000}

class DashboardViewTest(TestCase):
    @patch('analytical.views.connections')
    def test_dashboard_returns_200(self, mock_conns):
        # Mock the cursor to return expected data
        mock_cursor = MockCursor([DASHBOARD_ROW], [('total_advisors',), ('total_aum',), ('avg_aum',), ('total_aum_change_12m',)])
        mock_conns.__getitem__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        c = Client()
        resp = c.get('/api/analytics/dashboard/')
        self.assertEqual(resp.status_code, 200)

    def test_dashboard_missing_db_returns_503(self):
        # Without mock, should handle connection error gracefully
        pass

# Similar tests for AdvisorsListView, AdvisorDetailView, SignalsView, EasyButtonView
```

## Files
- `analytical/tests/__init__.py` (create)
- `analytical/tests/test_views.py` (create)

## Acceptance Criteria
- [ ] All 5 analytical views have at least one happy-path test
- [ ] DB errors return 503 (test the error path)
- [ ] Tests run in CI via `tox`
- [ ] `tox.ini` includes `analytical` in pylint/bandit scope

## Dependencies
- TODO-581 (fix psycopg2 pooling first — tests will be easier to mock)
