# TODO-891: Add GET /fixed_lists Endpoint

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** S (30 minutes)  
**Status:** pending

## Problem

There is **no way to query what entities are currently loaded** in the service. The `/fixed_lists` endpoint only supports POST (add) and DELETE. This makes it impossible to:
- Debug what tickers/funds are registered
- Build an admin UI for entity management
- Write round-trip integration tests
- Verify seed data loaded correctly on startup

## Fix

Add `GET /fixed_lists` endpoint with optional `entity_type` query parameter.

## Coding Prompt

```
Edit /data/workspace/projects/core-entityextraction/main.py

Add the following endpoint after the existing delete_fixed_lists endpoint:

@app.get("/fixed_lists")
@limiter.limit("100/minute")
async def get_fixed_lists(request: Request, entity_type: Optional[str] = None):
    """
    Returns current entities in the in-memory store.
    
    Query params:
      entity_type: (optional) return only this entity type, e.g. ?entity_type=Ticker
    
    Returns:
      {"response": {"Ticker": ["AAPL", "GOOG"], ...}, "counts": {"Ticker": 2, ...}, "total": N, "status": 200}
    """
    if entity_type is not None:
        if entity_type not in entity_store:
            raise HTTPException(status_code=422, detail=f"Unknown entity type: {entity_type}. Valid types: {sorted(entity_store.keys())}")
        data = {entity_type: sorted(entity_store[entity_type])}
    else:
        data = {et: sorted(values) for et, values in entity_store.items()}
    
    counts = {et: len(vals) for et, vals in data.items()}
    total = sum(counts.values())
    return {"response": data, "counts": counts, "total": total, "status": 200}

Also add a test file /data/workspace/projects/core-entityextraction/tests/test_get_fixed_lists.py:

import pytest
import main

@pytest.fixture(autouse=True)
def seed():
    main.entity_store["Ticker"].update(["AAPL", "GOOG"])
    main.entity_store["Country"].add("United States")
    main._invalidate_pattern_cache()

@pytest.mark.asyncio
async def test_get_all_entity_types(client, api_headers):
    resp = await client.get("/fixed_lists", headers=api_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == 200
    assert "AAPL" in body["response"]["Ticker"]
    assert body["counts"]["Ticker"] == 2

@pytest.mark.asyncio
async def test_get_single_entity_type(client, api_headers):
    resp = await client.get("/fixed_lists?entity_type=Ticker", headers=api_headers)
    assert resp.status_code == 200
    assert set(resp.json()["response"]["Ticker"]) == {"AAPL", "GOOG"}

@pytest.mark.asyncio
async def test_get_unknown_entity_type(client, api_headers):
    resp = await client.get("/fixed_lists?entity_type=UnknownType", headers=api_headers)
    assert resp.status_code == 422
```

## Acceptance Criteria
- [ ] `GET /fixed_lists` returns all entities with counts
- [ ] `GET /fixed_lists?entity_type=Ticker` returns only Ticker entities
- [ ] Unknown entity_type returns HTTP 422
- [ ] All tests pass

## Dependencies
None
