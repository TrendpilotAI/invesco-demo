# 339 — Add Confidence Scores to Entity Extraction Responses

**Repo:** core-entityextraction  
**Priority:** P1 (Feature/Value)  
**Effort:** 2-3 hours

## Problem
ML and spaCy predictions return no confidence score. Callers cannot threshold or rank results. Regex matches have implicit confidence=1.0 but this isn't expressed.

## Solution
Update response structure to include `confidence` field:

```python
# For regex matches:
{"type": "Ticker", "value": "AAPL", "startPosition": 5, "endPosition": 9, "confidence": 1.0, "source": "regex"}

# For ML/spaCy matches (spaCy doesn't expose raw prob easily):
# Use ent.kb_id_ or custom scorer, or default to 0.9 for NER hits
{"type": "ORG", "value": "Goldman Sachs", "startPosition": 0, "endPosition": 13, "confidence": 0.87, "source": "spacy"}
```

For spaCy 3.x, confidence can be obtained via:
```python
# After NER, scores are in doc._.trf_data or via custom component
# Simplest: use ent.start_char/end_char span confidence from beam search
```

## Acceptance Criteria
- [ ] All three endpoints return `confidence` (float 0-1) and `source` ("regex"|"ml"|"spacy") per entity
- [ ] Regex always returns 1.0
- [ ] ML/spaCy returns best available confidence or 0.9 default
- [ ] API docs updated
- [ ] Backward compatible (new fields, no removals)
