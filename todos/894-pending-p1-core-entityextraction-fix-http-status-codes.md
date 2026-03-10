# TODO-894: Fix HTTP Status Code Inconsistency

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** S (30 minutes)  
**Status:** pending

## Problem

All error paths across extraction and fixed_list endpoints return `HTTP 200` with an error status embedded in the JSON body:
```json
HTTP 200
{"response": "Something went wrong.", "status": 400}
```

This is incorrect and breaks:
- CloudWatch/Datadog/Prometheus error rate metrics (count these as successes)
- Standard HTTP client error handling
- API client libraries that check HTTP status
- OpenAPI/Swagger documentation

## Fix

Return proper HTTP status codes. Use `raise HTTPException(...)` or `return JSONResponse(..., status_code=4xx)`.

## Coding Prompt

```
Edit /data/workspace/projects/core-entityextraction/main.py

For each of the following locations, fix the HTTP status code:

1. regex_entity_extraction — exception handler:
   BEFORE: return JSONResponse(content={"response": str(exc), "status": 400}, status_code=200)
   AFTER:  raise HTTPException(status_code=500, detail=str(exc))

2. ml_entity_extraction — model not found:
   BEFORE: return JSONResponse(content={"response": "ML Model not found", "status": 404}, status_code=200)
   AFTER:  raise HTTPException(status_code=503, detail="ML model not available")

3. ml_entity_extraction — exception handler:
   BEFORE: return JSONResponse(content={"response": str(exc), "status": 400}, status_code=200)
   AFTER:  raise HTTPException(status_code=500, detail=str(exc))

4. spacy_entity_extraction — model not found:
   BEFORE: return JSONResponse(content={"response": "Spacy Model not found", "status": 404}, status_code=200)
   AFTER:  raise HTTPException(status_code=503, detail="spaCy model not available")

5. spacy_entity_extraction — exception handler:
   BEFORE: return JSONResponse(content={"response": str(exc), "status": 400}, status_code=200)
   AFTER:  raise HTTPException(status_code=500, detail=str(exc))

6. update_fixed_lists — exception handler:
   BEFORE: return JSONResponse(content={"response": "Something went wrong.", "status": 400}, status_code=200)
   AFTER:  raise HTTPException(status_code=500, detail="Failed to update fixed lists")

7. delete_fixed_lists — validation errors:
   BEFORE: return JSONResponse(content={"response": "You should determine entity types...", "status": 400}, status_code=200)
   AFTER:  raise HTTPException(status_code=400, detail="You must specify entity_types_list or all_entities=true")

Keep success responses as {"response": ..., "status": 200} for backward compatibility with existing clients.
Keep the body format for 400/500 errors as {"detail": "..."} which is FastAPI standard.

After changes, update test_ml_extraction.py assertions:
- "model not found" now returns HTTP 503, not 200
- Exception paths return HTTP 500, not 200

Run: pytest tests/ -x -q
```

## Acceptance Criteria
- [ ] Error responses return appropriate HTTP status codes (400, 422, 500, 503)
- [ ] Success responses still return HTTP 200
- [ ] Tests updated to match new status codes
- [ ] All tests pass

## Dependencies
- TODO-892 (ML tests need updating when this is applied)
