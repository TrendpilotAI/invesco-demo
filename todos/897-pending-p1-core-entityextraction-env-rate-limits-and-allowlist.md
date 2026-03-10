# TODO-897: Env-Based Rate Limits + entity_types_list Allowlist Validation

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** XS (20 minutes)  
**Status:** pending

## Problems

### 1. Rate Limits Hardcoded (ignores documented env vars)
The README documents `RATE_LIMIT_REGEX` and `RATE_LIMIT_ML` env vars, but the code has hardcoded values:
```python
@limiter.limit("100/minute")   # ignores RATE_LIMIT_REGEX
@limiter.limit("60/minute")    # ignores RATE_LIMIT_ML
```

### 2. entity_types_list Not Validated
Unknown entity types in `entity_types_list` silently produce no results — no error message. A typo like `"Tiker"` returns empty silently.

## Fix

### Rate Limits
```python
@limiter.limit(os.environ.get("RATE_LIMIT_REGEX", "100/minute"))
async def regex_entity_extraction(...):

@limiter.limit(os.environ.get("RATE_LIMIT_ML", "60/minute"))
async def ml_entity_extraction(...):

@limiter.limit(os.environ.get("RATE_LIMIT_SPACY", "60/minute"))
async def spacy_entity_extraction(...):
```

### Allowlist Validation
Add to `EntityExtractionRequest` validator:
```python
from pydantic import model_validator

class EntityExtractionRequest(BaseModel):
    text: str = pydantic.Field(max_length=50_000)
    include_entity_types: Optional[bool] = None
    entity_types_list: Optional[List[str]] = None
    
    @model_validator(mode='after')
    def validate_entity_types(self):
        if self.entity_types_list:
            from main import ENTITY_OPTIONS
            unknown = set(self.entity_types_list) - set(ENTITY_OPTIONS.keys())
            if unknown:
                raise ValueError(f"Unknown entity types: {sorted(unknown)}. Valid: {sorted(ENTITY_OPTIONS.keys())}")
        return self
```

## Coding Prompt

```
Edit /data/workspace/projects/core-entityextraction/main.py

1. Update the three rate limit decorators:
   @limiter.limit("100/minute") on regex_entity_extraction → @limiter.limit(os.environ.get("RATE_LIMIT_REGEX", "100/minute"))
   @limiter.limit("60/minute") on ml_entity_extraction → @limiter.limit(os.environ.get("RATE_LIMIT_ML", "60/minute"))
   @limiter.limit("60/minute") on spacy_entity_extraction → @limiter.limit(os.environ.get("RATE_LIMIT_SPACY", "60/minute"))

2. Add a Pydantic model_validator to EntityExtractionRequest that validates 
   entity_types_list values against ENTITY_OPTIONS.keys() when provided.
   Unknown types should raise ValueError with a clear message listing valid types.

3. Add a test to test_regex_extraction.py:
   async def test_unknown_entity_type_returns_422(client, api_headers):
       resp = await client.post(
           "/regex_entity_extraction",
           json={"text": "test", "include_entity_types": True, "entity_types_list": ["UnknownType"]},
           headers=api_headers,
       )
       assert resp.status_code == 422

Run: pytest tests/ -x -q
```

## Acceptance Criteria
- [ ] Rate limits read from env vars with defaults
- [ ] Unknown entity types return HTTP 422 with clear error
- [ ] Test for 422 on unknown entity type
- [ ] All existing tests pass

## Dependencies
None
