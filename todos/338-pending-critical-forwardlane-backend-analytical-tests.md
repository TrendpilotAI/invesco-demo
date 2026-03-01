# 338 — Add Test Suite for analytical/ Views

**Priority:** CRITICAL
**Repo:** forwardlane-backend
**Effort:** M (3-4 hours)
**Category:** Testing

## Description
`analytical/views.py` (560 lines, 5 endpoints serving Invesco advisor data) has ZERO tests.
This is the highest-risk untest code in the codebase — it touches financial data and is the
core of the Invesco demo.

## Endpoints to Test
1. `GET /api/v1/analytical/advisors/` — list advisors
2. `GET /api/v1/analytical/advisors/<id>/` — advisor detail
3. `GET /api/v1/analytical/advisors/<id>/holdings/` — holdings breakdown
4. `GET /api/v1/analytical/advisors/<id>/flows/` — AUM flows
5. `GET /api/v1/analytical/dashboard/` — top-level stats

## Test Cases to Write

### `analytical/tests/test_advisor_views.py`
```python
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.urls import reverse

class TestAdvisorListView(TestCase):
    @patch('analytical.views._analytical_cursor')  # after psycopg2 fix
    def test_returns_200_with_advisor_list(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [...]
        response = self.client.get('/api/v1/analytical/advisors/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('advisors', response.json())

    @override_settings(DEMO_ENV='')
    def test_auth_required_when_demo_mode_off(self):
        response = self.client.get('/api/v1/analytical/advisors/')
        self.assertEqual(response.status_code, 403)

    @patch('analytical.views._analytical_cursor')
    def test_db_error_returns_503(self, mock_cursor):
        mock_cursor.side_effect = Exception("DB connection failed")
        response = self.client.get('/api/v1/analytical/advisors/')
        self.assertIn(response.status_code, [500, 503])
```

## Files to Create
- `analytical/tests/__init__.py`
- `analytical/tests/test_advisor_views.py`

## Dependencies
- TODO-336 (fix psycopg2 connections first — makes mocking much easier)

## Acceptance Criteria
- [ ] `analytical/tests/` directory created with `__init__.py`
- [ ] All 5 endpoints have at least: 200 test, 403 test (demo off), error test
- [ ] `pytest analytical/` passes in CI
- [ ] `analytical` added to pylint scope in `tox.ini`
