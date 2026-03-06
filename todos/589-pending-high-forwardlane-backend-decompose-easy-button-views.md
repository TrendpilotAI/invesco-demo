# TODO-589: Decompose easy_button/views.py into Sub-Modules

**Priority:** HIGH  
**Repo:** forwardlane-backend  
**Effort:** L (6h)  
**Status:** pending  

## Description

`easy_button/views.py` is 67,914 lines — one of the largest single Python files possible. It contains unrelated view logic for advisor listings, signals, meeting prep, NL→SQL, and more. This makes navigation, testing, and code review extremely difficult.

## Target Structure

```
easy_button/
  views/
    __init__.py          # Re-export all views for URL compatibility
    advisor.py           # AdvisorsListView, AdvisorDetailView
    signals.py           # SignalsView, SignalDetailView  
    meeting_prep.py      # MeetingPrepView, TalkingPointsView
    nl_query.py          # NLQueryView, _keyword_fallback, _clean_sql
    dashboard.py         # DashboardView, summary views
    helpers.py           # _dict_fetchall, _compute_status, _derive_risk_score, etc.
  llm.py                 # LLMClient (after TODO-586)
```

## Task

1. Create `easy_button/views/` directory
2. Move view classes to appropriate sub-modules
3. Move helper functions to `views/helpers.py`
4. Create `easy_button/views/__init__.py` that re-exports all views:
   ```python
   from .advisor import AdvisorsListView, AdvisorDetailView
   from .signals import SignalsView
   # etc.
   ```
5. Verify `easy_button/urls.py` imports still work (should be transparent via `__init__.py`)
6. Update test imports if needed
7. Verify all tests pass after restructure

## Acceptance Criteria

- [ ] `views.py` replaced by `views/` package
- [ ] No single sub-module exceeds 500 lines
- [ ] All URL routing still works (no 404s introduced)
- [ ] All existing tests pass
- [ ] `from easy_button.views import NLQueryView` still works

## Dependencies

- Best done after: TODO-585, TODO-586 (cleaner code to restructure)
