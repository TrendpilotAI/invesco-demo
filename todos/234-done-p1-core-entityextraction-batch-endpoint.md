# 234 — Add Batch Entity Extraction Endpoint

**Repo:** core-entityextraction  
**Priority:** P1 (Value — reduces ForwardLane backend round-trips)  
**Effort:** 2 hours  
**Dependencies:** None

## Description
Current `/regex_entity_extraction` accepts a single text string. Add `/batch_entity_extraction` accepting an array of texts, returning results for each.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Add request model:
   class BatchEntityExtractionRequest(BaseModel):
       texts: List[str]
       include_entity_types: Optional[bool] = None
       entity_types_list: Optional[List[str]] = None

2. Add endpoint (with auth dependency):
   @app.post("/batch_entity_extraction", dependencies=[Depends(get_api_key)])
   async def batch_entity_extraction(req: BatchEntityExtractionRequest):
       if not req.texts:
           return {"response": [], "status": 200}
       if len(req.texts) > 100:
           raise HTTPException(status_code=400, detail="Maximum 100 texts per batch")
       try:
           result = match_patterns(req.texts, req.include_entity_types, req.entity_types_list)
       except Exception as exc:
           LOGGER.exception("Error in batch entity extraction: %s", exc)
           return JSONResponse(content={"response": str(exc), "status": 400}, status_code=200)
       return {"response": result, "status": 200}

3. Note: match_patterns() already accepts List[str] internally, so this is mostly 
   exposing the existing behavior through a proper batch endpoint.

4. Add test in tests/test_api.py:
   - test_batch_extraction_multiple_texts
   - test_batch_extraction_empty_list
   - test_batch_extraction_over_limit_returns_400
```

## Acceptance Criteria
- [ ] POST /batch_entity_extraction accepts {"texts": ["text1", "text2"]}
- [ ] Returns all matched entities across all texts with correct positions
- [ ] Enforces max 100 texts per request
- [ ] Authenticated (requires X-API-Key if API_KEY set)
- [ ] Response format matches /regex_entity_extraction
