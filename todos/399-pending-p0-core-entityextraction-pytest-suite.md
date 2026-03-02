# TODO-399: Add Pytest Test Suite

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** M (1-2 days)  
**Status:** pending

## Description
Zero tests exist for this production NLP service. Any code change could silently break extraction accuracy or API compatibility.

## Coding Prompt
```
Create a complete test suite for /data/workspace/projects/core-entityextraction/:

1. Create requirements-dev.txt:
   pytest>=8.0
   pytest-asyncio>=0.23
   httpx>=0.27
   pytest-mock>=3.12
   coverage>=7.4

2. Create tests/conftest.py:
   - AsyncClient fixture for the FastAPI app
   - Mock entity_store fixture with sample data (5-10 entities per type)
   - Mock persistence module (stub init_db, load_all, save_entities, delete_entities)
   - Set ENTITY_EXTRACTION_API_KEY env var for tests

3. Create tests/test_pattern_matching.py:
   - test_locate_entities_basic: simple ticker "AAPL" found in text
   - test_locate_entities_case_insensitive: "apple" matches "Apple" for non-ticker types
   - test_locate_entities_case_sensitive_ticker: "aapl" does NOT match ticker (uppercase only)
   - test_exclude_rule_start_of_sentence: ticker at start of sentence excluded
   - test_exclude_rule_share_class: ticker followed by "shares" excluded
   - test_replace_rule_dash: entity "Goldman-Sachs" matches "Goldman Sachs" via Dash rule
   - test_replace_rule_ampersand: "AT&T" matches "AT and T"
   - test_match_patterns_returns_list: match_patterns(["text"]) returns list of dicts
   - test_match_patterns_entity_type_filter_include: include_entity_types=True filters correctly
   - test_match_patterns_entity_type_filter_exclude: include_entity_types=False excludes correctly

4. Create tests/test_api.py:
   - test_health: GET /health → {"status": "ok"}
   - test_version: GET /version → string
   - test_regex_extraction_valid: POST /regex_entity_extraction with seeded entity returns match
   - test_regex_extraction_no_match: text with no seeded entities returns empty list
   - test_regex_extraction_requires_api_key: missing key → 401
   - test_regex_extraction_valid_key: valid key → 200
   - test_regex_extraction_rate_limit: mock slowapi to return 429, assert handled correctly
   - test_ml_extraction_model_not_loaded: _ml_nlp=None → 404 response
   - test_fixed_lists_add: POST /fixed_lists adds entities, returns count
   - test_fixed_lists_delete_by_type: DELETE /fixed_lists with entity_types_list
   - test_fixed_lists_delete_all: DELETE /fixed_lists with all_entities=true
   - test_fixed_lists_empty_body: DELETE /fixed_lists with no body → 400

5. Create tests/test_auth.py:
   - test_health_no_auth_required: /health accessible without key
   - test_invalid_key_rejected: X-API-Key: "wrong" → 401
   - test_multiple_valid_keys: comma-separated keys, both accepted
   - test_no_key_configured_passthrough: ENTITY_EXTRACTION_API_KEY unset → all requests pass

6. Add Makefile targets:
   test: pytest tests/ -v --cov=. --cov-report=term-missing
   test-ci: pytest tests/ --cov=. --cov-fail-under=60

7. Update bitbucket-pipelines.yml to run pytest before deploy
```

## Dependencies
- TODO-396 (remove dead files, cleaner import surface)

## Acceptance Criteria
- `pytest tests/` passes with 0 failures
- Coverage ≥ 60% on main.py
- Tests run in < 30 seconds
- No real Postgres or ML model required (all mocked)
