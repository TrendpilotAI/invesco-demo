# 008 — Write Unit Tests for Easy Button Views

**Repo:** forwardlane-backend  
**Priority:** high  
**Effort:** M (4-6h)  
**Status:** pending

## Description

The `easy_button/` app has zero test coverage. This is critical new code powering the Invesco demo. All views use raw SQL via the analytical DB, so tests need to mock `connections['analytical'].cursor()`.

## Coding Prompt

Create `/data/workspace/projects/forwardlane-backend/easy_button/tests/test_views.py`:

```python
"""Tests for easy_button views. All DB calls are mocked."""
import pytest
from unittest.mock import patch, MagicMock, call
from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient

# Mock the analytical DB cursor
def make_cursor_mock(fetchone_data=None, fetchall_data=None):
    cursor = MagicMock()
    cursor.__enter__ = lambda s: s
    cursor.__exit__ = MagicMock(return_value=False)
    if fetchone_data:
        cursor.fetchone.side_effect = fetchone_data
    if fetchall_data:
        cursor.fetchall.return_value = fetchall_data
    cursor.description = [(col,) for col in (fetchall_data[0].keys() if fetchall_data else [])]
    return cursor
```

Write the following test classes:

### TestDashboardView
- `test_returns_200_with_valid_data` — mock cursor returns stats + risk + opp rows; assert response shape
- `test_handles_db_error` — mock DatabaseError; assert 503 response
- `test_handles_empty_db` — cursor returns zeros; assert valid response with zeros

### TestAdvisorListView
- `test_basic_list_returns_paginated_results`
- `test_search_filter_passes_correct_params`
- `test_segment_filter_works`
- `test_invalid_ordering_uses_default`
- `test_malicious_ordering_param_is_sanitized` — pass `ordering="'; DROP TABLE"` → should still return 200 with safe default
- `test_malicious_direction_param_is_sanitized` — pass `direction="asc; SELECT 1"` → should use default

### TestAdvisorDetailView
- `test_returns_404_for_unknown_advisor`
- `test_returns_full_detail_with_holdings_flows_signals`
- `test_handles_db_error`

### TestNLQueryView
- `test_quick_pattern_match_bypasses_llm` — send "at-risk advisors"; assert used_llm=False
- `test_llm_fallback_on_no_pattern_match` — mock _gemini_sql; assert called
- `test_kimi_fallback_when_gemini_fails` — mock Gemini to raise, mock Kimi; assert Kimi called
- `test_empty_query_returns_400`
- `test_db_error_returns_422`
- `test_sql_injection_via_query_param` — send malicious NL; assert SQL is still read-only SELECT

### TestMeetingPrepView
- `test_returns_404_for_unknown_advisor`
- `test_returns_full_meeting_prep_with_talking_points`
- `test_generates_talking_points_for_declining_aum`
- `test_handles_advisor_with_no_signals`

Use `@pytest.mark.django_db` where needed. Mock `easy_button.views.connections` for all DB calls.

Also add `easy_button/tests/__init__.py` (empty).
Update `pytest.ini` to include `easy_button` in test discovery.

## Dependencies
- 004 (SQL injection fix should be in place before writing tests for it)

## Acceptance Criteria
- [ ] All test classes exist with ≥3 test cases each
- [ ] Tests run with `python -m pytest easy_button/` without real DB
- [ ] Malicious input tests confirm injection protection works
- [ ] CI/CD pipeline runs these tests
