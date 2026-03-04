# TODO-503: Create pytest Unit Test Suite

**Repo:** core-entityextraction
**Priority:** P0
**Effort:** M (1 day)
**Dependencies:** None
**Blocks:** TODO-504 (integration tests build on this)

## Description
Zero test coverage is a critical risk. Create comprehensive unit tests for pattern matching, entity extraction, and persistence layer.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Create tests/ directory with conftest.py, __init__.py
2. Add pytest, pytest-cov, pytest-asyncio to requirements.txt

3. tests/test_pattern_matcher.py:
   - Test match_patterns() with known financial entities (tickers, company names, dates)
   - Test ExcludeRules filtering
   - Test ReplaceRule substitutions
   - Test edge cases: empty text, special characters, unicode
   - Test all 17 entity types have working patterns

4. tests/test_entity_extraction.py:
   - Test regex extraction endpoint logic with sample financial text
   - Test ML extraction endpoint logic (mock spaCy model)
   - Test max_length=50000 validation
   - Test empty/null input handling

5. tests/test_persistence.py:
   - Mock asyncpg pool (or psycopg2 pool if TODO-501 not done yet)
   - Test init_db creates tables
   - Test upsert_entities inserts and updates
   - Test delete_entities removes correctly
   - Test load_entities returns expected format

6. tests/test_auth.py:
   - Test valid API key passes
   - Test invalid API key returns 401
   - Test missing API key returns 401
   - Test comma-separated key rotation

7. Add pytest.ini or pyproject.toml with:
   [tool.pytest.ini_options]
   asyncio_mode = "auto"
   
8. Target: 70%+ coverage on first pass
```

## Acceptance Criteria
- [ ] `pytest --cov` runs and passes
- [ ] Coverage ≥ 70%
- [ ] All 17 entity types have at least one test
- [ ] Auth tests cover valid/invalid/missing keys
- [ ] Persistence tests use mocks (no real DB needed)
