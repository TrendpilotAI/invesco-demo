# TODO-509: Entity Confidence Scores

**Repo:** core-entityextraction
**Priority:** P1
**Effort:** M (4-8h)
**Dependencies:** None
**Blocks:** None

## Description
Return normalized confidence scores (0.0-1.0) alongside each extracted entity. Regex: compute from match specificity + frequency. ML/spaCy: use model probability directly.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Update response Pydantic models to include confidence field:
   class ExtractedEntity(BaseModel):
       text: str
       type: str
       start: int
       end: int
       confidence: float = Field(ge=0.0, le=1.0)

2. For regex extraction:
   - Exact match in entity store → 1.0
   - Partial/fuzzy match → 0.7-0.9 based on match length ratio
   - Pattern-only match (no store validation) → 0.5
   - Add frequency bonus: entities seen more often in store get +0.1

3. For ML/spaCy extraction:
   - Use ent._.score or model probability directly
   - Normalize to 0.0-1.0 range

4. Update all response schemas and API docs
5. Add tests for confidence scoring logic
```

## Acceptance Criteria
- [ ] Every extracted entity includes a confidence score
- [ ] Scores are normalized 0.0-1.0
- [ ] Regex and ML have appropriate scoring strategies
- [ ] API documentation updated
- [ ] Tests cover confidence computation
