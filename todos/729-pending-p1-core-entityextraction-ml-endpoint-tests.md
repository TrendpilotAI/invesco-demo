# TODO-729: Add ML extraction endpoint tests

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** M  
**Status:** pending

## Description
`test_regex_extraction.py` has comprehensive coverage but there are zero tests for `/ml_entity_extraction` or `/spacy_entity_extraction`. CI gives false confidence.

## Coding Prompt
Create `/data/workspace/projects/core-entityextraction/tests/test_ml_extraction.py`:

1. Mock `main._ml_nlp` so tests don't require model download in CI:
   ```python
   from unittest.mock import MagicMock, patch
   mock_doc = MagicMock()
   mock_ent = MagicMock(label_="Company", text="Apple", start_char=0, end_char=5)
   mock_doc.ents = [mock_ent]
   ```
2. Test cases:
   - ML model not loaded → returns 404 with helpful message
   - Successful extraction → returns entities list with type/value fields
   - Filter by entity_type → only matching types returned
   - Empty text → returns empty list
   - Text exceeds max_length=50000 → returns 422
   - No X-API-Key → returns 401
3. Create `tests/test_spacy_extraction.py` with similar structure (mock `main._spacy_nlp`)
4. Add `--cov=. --cov-report=term-missing` to pytest.ini and set `--cov-fail-under=60`

## Acceptance Criteria
- [ ] ML endpoint has >= 6 test cases
- [ ] spaCy endpoint has >= 4 test cases
- [ ] Tests run without downloading ML models
- [ ] Coverage >= 60% reported in CI
- [ ] `pytest tests/ -v` passes
