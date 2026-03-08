# TODO-728: Add entity_type allowlist validation in POST /fixed_lists

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** XS  
**Status:** pending

## Description
`POST /fixed_lists` accepts arbitrary `entity_type` strings, allowing injection of unexpected keys into the entity_store dict. An attacker could pollute the store with arbitrary type keys.

## Coding Prompt
In `/data/workspace/projects/core-entityextraction/main.py`, add allowlist validation to the fixed_lists POST/DELETE endpoints:

1. Define `VALID_ENTITY_TYPES: Set[str]` from the existing entity type constants (ENTITY_CITY, ENTITY_COMPANY, etc.)
2. In the POST /fixed_lists handler, check: `if entity_type not in VALID_ENTITY_TYPES: raise HTTPException(status_code=400, detail=f"Invalid entity_type '{entity_type}'. Valid types: {sorted(VALID_ENTITY_TYPES)}")`
3. Apply the same check to DELETE /fixed_lists
4. Add test case in tests/test_fixed_lists.py: POST with invalid entity_type returns 400

## Acceptance Criteria
- [ ] Invalid entity_type returns HTTP 400 with helpful error message
- [ ] Valid entity types still work
- [ ] Test covers the 400 case
