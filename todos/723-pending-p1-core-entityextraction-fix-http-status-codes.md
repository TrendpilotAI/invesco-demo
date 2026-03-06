# TODO-723: Fix HTTP status code semantics

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** 2h  
**Status:** pending

## Description
Multiple endpoints return HTTP 200 with a `"status": 4xx` field inside the body.
This breaks standard HTTP clients, monitoring tools, and load balancers that check
status codes. Proper HTTP semantics required.

## Acceptance Criteria
- 400 errors return HTTP 400
- 404 (model not found) returns HTTP 404
- 401 (unauthorized) already correct ✅
- Body format: `{"detail": "...", "status": 4xx}` using FastAPI HTTPException pattern

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py, fix all endpoints that
return `JSONResponse(content={..., "status": 400}, status_code=200)`:

1. /regex_entity_extraction — exception path → HTTP 400
2. /ml_entity_extraction — exception path → HTTP 400; model not found → HTTP 404
3. /spacy_entity_extraction — same as ML
4. POST /fixed_lists — exception → HTTP 400; no new entities → HTTP 200 (keep)
5. DELETE /fixed_lists — "no types to delete" → HTTP 400; exception → HTTP 500

Use FastAPI's raise HTTPException(status_code=4xx, detail="...") pattern.
Keep the "status" field in the response body for backward compat with existing clients:
  return JSONResponse({"detail": msg, "status": 400}, status_code=400)
```

## Dependencies
TODO-721 (tests will catch regression)
