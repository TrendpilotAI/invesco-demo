# TODO-619: Add Entity Confidence Scores to API Response

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** M (~2-4 hours)  
**Status:** pending

## Problem
Entity extraction returns binary results — entity found or not. ForwardLane downstream consumers have no signal on extraction quality to filter noise.

## Task Description
Add `confidence` field (0.0–1.0) to each extracted entity result.

## Coding Prompt
```
Edit /data/workspace/projects/core-entityextraction/main.py to add confidence scores:

1. For regex matching in match_patterns() / _locate_entities_compiled():
   - Exact match in entity_store: confidence = 1.0
   - Case-folded match: confidence = 0.9
   - Replace-rule expanded match (dash removed, etc.): confidence = 0.75
   - Track which expansion was used when adding to patterns list in _build_entity_patterns()
   
   Simplest approach: add a parallel dict mapping pattern → confidence score
   in _build_compiled_patterns(). Return (pattern_string, confidence) tuples.

2. For ML NER in ml_predict():
   - spaCy Doc.ents don't expose confidence by default in v3
   - Use the NER pipe's beam scores if available: nlp.get_pipe("ner")
   - Fallback: confidence = 0.85 for all ML entities (known model)

3. For spacy_predict():
   - Use same fallback: confidence = 0.80

4. Update response format:
   BEFORE: {"type": "Ticker", "value": "AAPL", "startPosition": 5, "endPosition": 9}
   AFTER:  {"type": "Ticker", "value": "AAPL", "startPosition": 5, "endPosition": 9, "confidence": 1.0, "source": "regex"}
   
   Add "source" field: "regex" | "ml" | "spacy"

5. Update Swagger descriptions in swagger_descriptions/ to document new fields.
```

## Acceptance Criteria
- [ ] All entity results include `confidence` (float 0.0-1.0) and `source` ("regex"|"ml"|"spacy") fields
- [ ] Regex exact matches return confidence >= 0.9
- [ ] ML predictions return confidence with source="ml"
- [ ] Swagger docs updated
- [ ] Backward compatible (new fields added, none removed)

## Dependencies
- TODO-503 (pytest suite) — test new fields after implementation
