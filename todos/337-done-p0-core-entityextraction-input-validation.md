# 337 — Add Input Size Validation to EntityExtractionRequest

**Repo:** core-entityextraction  
**Priority:** P0 (Security/Stability)  
**Effort:** 30 minutes

## Problem
`EntityExtractionRequest.text: str` has no max_length constraint. A malicious caller can send MB-sized payloads causing catastrophic regex backtracking or memory exhaustion.

## Solution
Add Pydantic Field constraints to the request model in `main.py`:

```python
from pydantic import BaseModel, Field

class EntityExtractionRequest(BaseModel):
    text: str = Field(..., max_length=50_000, description="Text to extract entities from (max 50k chars)")
    include_entity_types: Optional[bool] = None
    entity_types_list: Optional[List[str]] = None
```

Also add to batch endpoint when created.

## Acceptance Criteria
- [ ] Requests with text > 50,000 chars return HTTP 422
- [ ] Pydantic validation error message is clear
- [ ] Unit test: `test_input_too_large_returns_422`
