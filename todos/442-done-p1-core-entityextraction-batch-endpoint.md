# TODO-442: Add batch extraction endpoint for pipeline throughput

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** S (2-4h)  
**Status:** pending

## Problem
Current API only accepts one text at a time. ForwardLane's pipeline processes many documents — requires N sequential requests. A batch endpoint reduces latency and connection overhead by 10-100x.

## Task
Add `POST /batch_regex_entity_extraction` accepting up to 100 texts.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Add new request model:
   class BatchEntityExtractionRequest(BaseModel):
       texts: List[str] = Field(..., min_items=1, max_items=100)
       entity_types: Optional[List[str]] = None
       # Each text inherits global max_length=50_000

2. Add endpoint:
   @app.post("/batch_regex_entity_extraction")
   @limiter.limit("20/minute")  # Lower limit for batch
   async def batch_regex_entity_extraction(request: Request, req: BatchEntityExtractionRequest):
       results = []
       for text in req.texts:
           result = _run_regex_extraction(text, req.entity_types)
           results.append(result)
       return {"results": results, "count": len(results)}

3. Extract _run_regex_extraction(text, entity_types) from existing regex_entity_extraction
   so both endpoints share the same logic

4. Optional: use asyncio.gather for parallel processing if texts are independent
   (safe since entity_store is read-only during extraction)

5. Add to Swagger docs with example request/response

6. Add batch endpoint for ML too: /batch_ml_entity_extraction (same pattern)
```

## Acceptance Criteria
- [ ] POST /batch_regex_entity_extraction accepts array of texts
- [ ] Returns array of results in same order as input
- [ ] Rate limit: 20 batch requests/minute per API key
- [ ] Error in one text doesn't fail entire batch (per-item error handling)
- [ ] Swagger docs updated
