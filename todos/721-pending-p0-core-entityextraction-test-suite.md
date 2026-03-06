# TODO-721: Add pytest test suite

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** 1d  
**Status:** pending

## Description
Zero test coverage. A production financial NLP service with no tests is high-risk.
Need unit + integration tests covering all endpoints and the extraction logic.

## Acceptance Criteria
- `pytest tests/` passes with >70% coverage
- Tests cover: /health, /version, /regex_entity_extraction, /ml_entity_extraction, /fixed_lists CRUD
- Persistence layer tested with mocked psycopg2
- Regex extraction tested with 20+ financial entity fixture sentences
- CI stage added to bitbucket-pipelines.yml

## Coding Prompt
```
Create a pytest test suite at /data/workspace/projects/core-entityextraction/tests/:

1. tests/conftest.py — AsyncClient fixture using httpx + FastAPI test app; mock DATABASE_URL
2. tests/test_health.py — GET /health and GET /version
3. tests/test_regex_extraction.py — POST /regex_entity_extraction with 20 financial sentences
   covering entities: Company, Fund, Country, CurrencyPair, EconomicIndicator
4. tests/test_fixed_lists.py — POST /fixed_lists (add), GET /regex_entity_extraction (verify),
   DELETE /fixed_lists (remove), verify gone
5. tests/test_auth.py — missing key returns 401, valid key passes, /health bypasses auth
6. tests/test_persistence.py — mock psycopg2 pool, verify save_entities and load_all called correctly

Add pytest and httpx to requirements.txt (dev section or requirements-dev.txt).
Add test step to bitbucket-pipelines.yml:
  - step:
      name: Test
      image: python:3.11
      script:
        - pip install -r requirements.txt -r requirements-dev.txt
        - pytest tests/ --tb=short
```

## Dependencies
None
