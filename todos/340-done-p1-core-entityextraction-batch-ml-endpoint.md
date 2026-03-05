# 340 — Add Batch ML/spaCy Entity Extraction Endpoints

**Repo:** core-entityextraction  
**Priority:** P1 (Feature/Performance)  
**Effort:** 2 hours

## Problem
Callers processing N documents must make N sequential API calls. This is the primary throughput bottleneck for ForwardLane's document analysis pipeline.

## Solution
Add batch endpoints:

```python
class BatchEntityExtractionRequest(BaseModel):
    texts: List[str] = Field(..., max_items=100, description="Up to 100 texts")
    include_entity_types: Optional[bool] = None
    entity_types_list: Optional[List[str]] = None

@app.post("/batch_regex_entity_extraction")
async def batch_regex(req: BatchEntityExtractionRequest):
    import asyncio
    results = await asyncio.gather(*[
        asyncio.to_thread(match_patterns, [text], req.include_entity_types, req.entity_types_list)
        for text in req.texts
    ])
    return {"response": [{"text_index": i, "entities": r} for i, r in enumerate(results)], "status": 200}

@app.post("/batch_ml_entity_extraction")  
async def batch_ml(req: BatchEntityExtractionRequest):
    # spaCy nlp.pipe() is optimized for batch processing
    if _ml_nlp is None:
        raise HTTPException(404, "ML model not loaded")
    docs = list(_ml_nlp.pipe(req.texts))
    results = [extract_entities_from_doc(doc) for doc in docs]
    return {"response": results, "status": 200}
```

Note: `nlp.pipe()` is significantly faster than calling `nlp()` per text.

## Dependencies
- TODO-337 (input validation) should be applied to batch too

## Acceptance Criteria
- [ ] Batch regex endpoint accepts up to 100 texts
- [ ] Batch ML endpoint uses `nlp.pipe()` for efficiency
- [ ] Returns per-text results with text_index
- [ ] Integration tests with 1, 10, 100 texts
- [ ] Rate limiting applied per batch (not per text)
