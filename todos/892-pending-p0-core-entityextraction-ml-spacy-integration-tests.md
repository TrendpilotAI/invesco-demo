# TODO-892: Add ML and spaCy NER Integration Tests

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** M (2 hours)  
**Status:** pending

## Problem

There are **zero tests** for `/ml_entity_extraction` and `/spacy_entity_extraction` endpoints. This means:
- ML model failures go undetected in CI
- Entity type filtering behavior is untested for NER paths
- Regression risk is high when nermodel3 is retrained

## Fix

Create `tests/test_ml_extraction.py` and `tests/test_spacy_extraction.py` with comprehensive tests for both endpoints.

## Coding Prompt

```
Create /data/workspace/projects/core-entityextraction/tests/test_ml_extraction.py:

"""
Tests for POST /ml_entity_extraction endpoint.
Uses two strategies:
1. Mocked _ml_nlp=None to test "model not loaded" path
2. Real nermodel3 predictions on known financial sentences (if model available)
"""

import pytest
from unittest.mock import patch, MagicMock
import main


@pytest.mark.asyncio
async def test_ml_returns_404_when_model_not_loaded(client, api_headers):
    """When ML model is None, endpoint returns model-not-found response."""
    with patch.object(main, "_ml_nlp", None):
        resp = await client.post(
            "/ml_entity_extraction",
            json={"text": "Apple announced earnings."},
            headers=api_headers,
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == 404
    assert "not found" in body["response"].lower()


@pytest.mark.asyncio
async def test_ml_with_mock_model(client, api_headers):
    """Mock the spaCy model to return predictable entities."""
    mock_ent = MagicMock()
    mock_ent.label_ = "ORG"
    mock_ent.text = "Apple"
    mock_ent.start_char = 0
    mock_ent.end_char = 5
    
    mock_doc = MagicMock()
    mock_doc.ents = [mock_ent]
    
    mock_nlp = MagicMock(return_value=mock_doc)
    
    with patch.object(main, "_ml_nlp", mock_nlp):
        resp = await client.post(
            "/ml_entity_extraction",
            json={"text": "Apple announced earnings."},
            headers=api_headers,
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == 200
    entities = body["response"]
    assert len(entities) == 1
    assert entities[0]["type"] == "ORG"
    assert entities[0]["value"] == "Apple"
    assert entities[0]["startPosition"] == 0
    assert entities[0]["endPosition"] == 5


@pytest.mark.asyncio
async def test_ml_entity_type_filter_include(client, api_headers):
    """include_entity_types=True filters to only requested types."""
    mock_ents = [
        MagicMock(label_="ORG", text="Apple", start_char=0, end_char=5),
        MagicMock(label_="GPE", text="US", start_char=20, end_char=22),
    ]
    mock_doc = MagicMock()
    mock_doc.ents = mock_ents
    mock_nlp = MagicMock(return_value=mock_doc)
    
    with patch.object(main, "_ml_nlp", mock_nlp):
        resp = await client.post(
            "/ml_entity_extraction",
            json={
                "text": "Apple is based in the US.",
                "include_entity_types": True,
                "entity_types_list": ["ORG"],
            },
            headers=api_headers,
        )
    assert resp.status_code == 200
    types = {e["type"] for e in resp.json()["response"]}
    assert types == {"ORG"}


@pytest.mark.asyncio
async def test_ml_entity_type_filter_exclude(client, api_headers):
    """include_entity_types=False excludes the specified types."""
    mock_ents = [
        MagicMock(label_="ORG", text="Apple", start_char=0, end_char=5),
        MagicMock(label_="GPE", text="US", start_char=20, end_char=22),
    ]
    mock_doc = MagicMock()
    mock_doc.ents = mock_ents
    mock_nlp = MagicMock(return_value=mock_doc)
    
    with patch.object(main, "_ml_nlp", mock_nlp):
        resp = await client.post(
            "/ml_entity_extraction",
            json={
                "text": "Apple is based in the US.",
                "include_entity_types": False,
                "entity_types_list": ["GPE"],
            },
            headers=api_headers,
        )
    assert resp.status_code == 200
    types = {e["type"] for e in resp.json()["response"]}
    assert "GPE" not in types


@pytest.mark.asyncio
async def test_ml_response_structure(client, api_headers):
    """All response items have required keys with correct types."""
    mock_ent = MagicMock()
    mock_ent.label_ = "ORG"
    mock_ent.text = "Goldman Sachs"
    mock_ent.start_char = 0
    mock_ent.end_char = 13
    mock_doc = MagicMock()
    mock_doc.ents = [mock_ent]
    mock_nlp = MagicMock(return_value=mock_doc)
    
    with patch.object(main, "_ml_nlp", mock_nlp):
        resp = await client.post(
            "/ml_entity_extraction",
            json={"text": "Goldman Sachs raised rates."},
            headers=api_headers,
        )
    for item in resp.json()["response"]:
        assert "type" in item
        assert "value" in item
        assert "startPosition" in item
        assert "endPosition" in item
        assert isinstance(item["startPosition"], int)
        assert isinstance(item["endPosition"], int)


Also create /data/workspace/projects/core-entityextraction/tests/test_spacy_extraction.py with equivalent tests for /spacy_entity_extraction. Include:
- Test that endpoint returns 404 when ENABLE_SPACY_ENTITY_EXTRACTION is not set
- Test with mocked _spacy_nlp returning entities
- Test that SPACY_EXCLUDED_ENTITY_TYPES (CARDINAL, DATE, etc.) are filtered out
- Test entity_types_list include/exclude filtering
- Test response structure

Run: pytest tests/test_ml_extraction.py tests/test_spacy_extraction.py -v
```

## Acceptance Criteria
- [ ] `test_ml_extraction.py` with 5+ tests passing
- [ ] `test_spacy_extraction.py` with 5+ tests passing
- [ ] Tests for model-not-loaded path
- [ ] Tests for entity type filtering (include and exclude)
- [ ] Tests for response structure validation
- [ ] SPACY_EXCLUDED_ENTITY_TYPES filtering verified

## Dependencies
- None (uses mocking, no real model required for most tests)
