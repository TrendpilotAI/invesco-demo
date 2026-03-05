# 233 — Add Pytest Test Suite

**Repo:** core-entityextraction  
**Priority:** P1 (Reliability)  
**Effort:** 1 day  
**Dependencies:** 230, 231

## Description
Zero tests exist. Add comprehensive pytest suite covering pattern matcher logic, exclude rules, API endpoints, and persistence functions.

## Coding Prompt
```
Create /data/workspace/projects/core-entityextraction/tests/ directory with:

1. tests/conftest.py:
   - FastAPI TestClient fixture
   - Seed entity_store with test data
   - Mock Postgres (monkeypatch persistence functions to no-op)

2. tests/test_pattern_matcher.py — Unit tests:
   - test_replace_rule_dash: entity "State-of-the-art" matches "State of the art"
   - test_replace_rule_ampersand: entity "AT&T" matches "AT and T"
   - test_case_insensitive: "apple" entity matches "Apple" in text
   - test_case_sensitive_ticker: "AAPL" matches but not "aapl"
   - test_exclude_start_of_sentence: ticker at start of sentence excluded
   - test_exclude_share_class: "A" ticker excluded when followed by "shares"
   - test_exclude_between_uppercase: ticker excluded between two uppercase words
   - test_match_positions: correct start/end positions returned
   - test_empty_entity_store: returns empty list

3. tests/test_api.py — Integration tests via TestClient:
   - test_health_returns_ok
   - test_version_returns_string
   - test_regex_extraction_finds_seeded_entity
   - test_regex_extraction_empty_text
   - test_fixed_lists_add_entities
   - test_fixed_lists_add_returns_count
   - test_fixed_lists_delete_by_type
   - test_fixed_lists_delete_all
   - test_ml_extraction_model_not_found (when model absent)

4. tests/test_persistence.py — Persistence tests (using mock):
   - test_init_db_without_database_url_returns_false
   - test_save_entities_without_pool_returns_zero
   - test_load_all_without_pool_returns_zero

5. requirements-dev.txt:
   pytest>=8.0.0
   pytest-asyncio>=0.23.0
   httpx>=0.27.0
   pytest-mock>=3.12.0

6. pytest.ini or pyproject.toml [tool.pytest.ini_options]:
   testpaths = ["tests"]
   asyncio_mode = "auto"
```

## Acceptance Criteria
- [ ] `pytest tests/` runs with 0 failures
- [ ] At minimum 20 test cases
- [ ] Pattern matcher edge cases covered (all ReplaceRules, all ExcludeRules)
- [ ] All API endpoints have at least one happy path test
- [ ] Tests run without a real Postgres connection (mocked)
- [ ] Tests run in < 10 seconds
