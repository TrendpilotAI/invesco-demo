# TODO-725: Add batch extraction endpoint

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** 2h  
**Status:** pending

## Description
ForwardLane backend likely needs to extract entities from many texts at once (e.g. news feed,
document batch). A batch endpoint avoids N serial HTTP calls.

## Acceptance Criteria
- `POST /batch_regex_entity_extraction` accepts `{"texts": ["...", "..."], ...}`
- Returns `{"results": [{text: ..., entities: ...}, ...], "status": 200}`
- Max 100 texts per batch (configurable via env)
- Rate limit: 20/minute per API key

## Coding Prompt
```
Add to /data/workspace/projects/core-entityextraction/main.py:

class BatchExtractionRequest(BaseModel):
    texts: List[str] = pydantic.Field(max_items=100)
    include_entity_types: Optional[bool] = None
    entity_types_list: Optional[List[str]] = None

@app.post("/batch_regex_entity_extraction")
@limiter.limit("20/minute")
async def batch_regex_entity_extraction(request: Request, req: BatchExtractionRequest):
    results = []
    for text in req.texts:
        result = match_patterns([text], req.include_entity_types, req.entity_types_list)
        results.append({"text": text[:100], "entities": result})
    return {"response": results, "status": 200, "count": len(results)}

Add test in tests/test_regex_extraction.py for batch endpoint.
```

## Dependencies
None
