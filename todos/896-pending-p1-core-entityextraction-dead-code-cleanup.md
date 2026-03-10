# TODO-896: Remove Dead Code from main.py

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** XS (15 minutes)  
**Status:** pending

## Dead Code Items to Remove

### 1. `_locate_entities()` Function (Non-Compiled Slow Path)
Since TODO-232 introduced the compiled pattern cache (`_locate_entities_compiled`), the original `_locate_entities()` function is never called. It creates confusion about which code path runs in production.

### 2. `FixedListsUpdateRequest` and `FixedListsDeleteRequest` Pydantic Models
These models are defined but the endpoints use `await request.json()` directly:
```python
class FixedListsUpdateRequest(BaseModel):
    model_config = {"extra": "allow"}

class FixedListsDeleteRequest(BaseModel):
    entity_types_list: Optional[List[str]] = None
    all_entities: Optional[bool] = False
```
**Option A:** Remove them  
**Option B (preferred):** Wire them to the endpoints for proper Pydantic validation

### 3. Module-Level `special_characters` Extraction
The `special_characters` tuple is defined identically in two places. Extract to module-level constant.

## Coding Prompt

```
Edit /data/workspace/projects/core-entityextraction/main.py

Step 1: Remove the `_locate_entities()` function (the non-compiled slow path).
Keep `_locate_entities_compiled()` which is still used.

Step 2: Instead of deleting FixedListsUpdateRequest and FixedListsDeleteRequest,
wire them to their respective endpoints:

Change:
    @app.post("/fixed_lists")
    async def update_fixed_lists(request: Request):
        data: Dict[str, List[str]] = await request.json()
        ...

To:
    @app.post("/fixed_lists")
    async def update_fixed_lists(request: Request, req: FixedListsUpdateRequest):
        data = req.model_dump()  # properly typed
        ...

Note: FixedListsUpdateRequest uses model_config = {"extra": "allow"} so arbitrary
entity_type keys are accepted — this is correct.

For delete endpoint, use FixedListsDeleteRequest as body parameter.

Step 3: Add module-level constant:
    _SPECIAL_CHARS = ("\\", ".", "+", "*", "?", "^", "$", "(", ")", "[", "]", "{", "}", "|")

Replace both occurrences of the inline special_characters tuple with _SPECIAL_CHARS.

Run: pytest tests/ -x -q
```

## Acceptance Criteria
- [ ] `_locate_entities()` (non-compiled) is removed
- [ ] `FixedListsUpdateRequest` / `FixedListsDeleteRequest` are used by their endpoints
- [ ] `_SPECIAL_CHARS` module-level constant defined and used in both places
- [ ] All tests pass

## Dependencies
- TODO-890 (fix duplicate filter bug first, as it touches the same match_patterns area)
