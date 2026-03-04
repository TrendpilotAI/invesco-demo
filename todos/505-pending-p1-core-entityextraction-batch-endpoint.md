# TODO-505: Batch/Bulk Extraction Endpoint

**Repo:** core-entityextraction
**Priority:** P1
**Effort:** S (2-4h)
**Dependencies:** TODO-501 (asyncpg for true async parallelism)
**Blocks:** None

## Description
Add `POST /batch_regex_entity_extraction` accepting an array of texts (up to 100) for parallel processing. Critical for ForwardLane's document pipeline.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Create Pydantic model:
   class BatchExtractionRequest(BaseModel):
       texts: List[str] = Field(..., max_length=100)
       # each text still limited to 50k chars

2. Add endpoint POST /batch_regex_entity_extraction:
   - Accept BatchExtractionRequest
   - Process texts in parallel with asyncio.gather
   - Return array of results matching input order
   - Rate limit: 20/min (heavier than single)
   - Same API key auth as other endpoints

3. Add corresponding batch ML endpoint: POST /batch_ml_entity_extraction

4. Handle partial failures: if one text fails, return error for that index, success for others
```

## Acceptance Criteria
- [ ] Batch endpoint accepts up to 100 texts
- [ ] Results maintain input order
- [ ] Partial failures handled gracefully
- [ ] Rate limited appropriately
- [ ] Tests added for batch endpoint
