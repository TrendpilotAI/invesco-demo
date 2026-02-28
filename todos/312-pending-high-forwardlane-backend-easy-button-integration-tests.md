# TODO-312: Easy Button Integration Tests — forwardlane-backend

**Priority:** HIGH  
**Effort:** M  
**Repo:** forwardlane-backend  
**Status:** pending

## Description
The easy_button endpoints (NL→SQL, MeetingPrepView, etc.) back the Invesco enterprise demo. Only `test_clean_sql.py` exists. Full integration tests are needed for demo readiness.

## Autonomous Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/easy_button/tests/:
1. Create test_views.py with Django test client / DRF APIClient
2. Write tests for:
   a. NLQueryView — happy path (valid SQL returned), rate limit (429 after threshold), SQL injection blocked (dangerous keywords → 400)
   b. MeetingPrepView — Gemini success path (mock), Kimi fallback (mock Gemini fail), static fallback (mock both fail), Redis cache hit (second call returns cached)
   c. EasyButtonPermission — blocks when EASY_BUTTON_ENABLED env not set, allows when set
3. Use pytest fixtures + pytest-django; mock external LLM calls with unittest.mock.patch
4. Target: 80%+ branch coverage on easy_button/views.py
5. Add to tox.ini testpaths if not already included
6. Run: python -m pytest easy_button/tests/ -v and fix failures
```

## Acceptance Criteria
- [ ] All new tests pass in CI
- [ ] NL→SQL happy path, injection block, and rate limit covered
- [ ] MeetingPrep all three fallback paths tested
- [ ] EasyButtonPermission gating tested

## Dependencies
- TODO-311 (Django 4.2 compat) should be done first
