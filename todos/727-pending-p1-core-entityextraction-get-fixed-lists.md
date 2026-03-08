# TODO-727: Add GET /fixed_lists endpoint

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** XS  
**Status:** pending

## Description
Currently there is no way to query what entities exist in the store without a direct DB client. This makes admin tooling and debugging production entity mismatches impossible via the API.

## Coding Prompt
Add `GET /fixed_lists` endpoint to `/data/workspace/projects/core-entityextraction/main.py`:

1. Add `GET /fixed_lists` with optional query param `?entity_type=Ticker`
2. If `entity_type` provided: return `{"entity_type": "Ticker", "entities": [...], "count": N}`
3. If no `entity_type`: return all entity types with counts `{"entities": {"Ticker": [...], "Fund": [...], ...}}`
4. Require X-API-Key auth (same middleware as other endpoints)
5. Add rate limit: 200/minute
6. Add test in `tests/test_fixed_lists.py` covering both query modes

## Acceptance Criteria
- [ ] GET /fixed_lists returns full entity store
- [ ] GET /fixed_lists?entity_type=Ticker filters correctly
- [ ] Returns 401 without valid X-API-Key
- [ ] Swagger docs show the endpoint
- [ ] Tests pass
