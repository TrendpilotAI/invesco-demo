# TODO-504: Integration Tests with FastAPI TestClient

**Repo:** core-entityextraction
**Priority:** P0
**Effort:** M (1 day)
**Dependencies:** TODO-503
**Blocks:** None

## Description
Full request/response cycle tests using httpx.AsyncClient against the FastAPI app.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/tests/:

1. Create test_integration.py:
   - Use httpx.AsyncClient with app=app
   - Mock DB pool in conftest.py fixture

2. Test cases:
   a. POST /regex_entity_extraction with valid text → 200, entities returned
   b. POST /regex_entity_extraction with empty text → 422
   c. POST /regex_entity_extraction with text > 50k chars → 422
   d. POST /ml_entity_extraction with valid text → 200
   e. GET /fixed_lists → returns entity store
   f. PUT /fixed_lists → updates entities, returns success
   g. DELETE /fixed_lists → removes entities
   h. All endpoints without API key → 401
   i. Rate limiting: send 101 requests to regex endpoint → 429 on 101st

3. Add test fixtures for sample financial texts with known entities
4. Assert response schemas match Pydantic models
```

## Acceptance Criteria
- [ ] All endpoints tested for happy path and error cases
- [ ] Rate limiting verified
- [ ] Auth verified
- [ ] Tests run without external services (all mocked)
