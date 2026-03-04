# TODO-516: Entity Synonyms/Aliases Support

**Repo:** core-entityextraction
**Priority:** P2
**Effort:** L (2 days)
**Dependencies:** TODO-501 (asyncpg), TODO-511 (refactor for clean integration)
**Blocks:** None

## Description
Map entity aliases to canonical forms (e.g., "Apple Inc." → "Apple", "AAPL" → "Apple"). Store in Postgres, return canonical name with `alias_of` field.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Add aliases table to schema.sql:
   CREATE TABLE entity_aliases (
     alias TEXT PRIMARY KEY,
     canonical_name TEXT NOT NULL,
     entity_type TEXT NOT NULL,
     created_at TIMESTAMP DEFAULT NOW()
   );

2. Add CRUD endpoints:
   - POST /aliases — add alias mapping
   - GET /aliases?entity_type=X — list aliases
   - DELETE /aliases/{alias} — remove

3. Update extraction logic:
   - After entity extraction, check alias table
   - If match found, add alias_of field to response
   - Return canonical name as primary, original as alias_of

4. Add seed data for common financial aliases (ticker→company, abbreviations)
5. Cache alias lookup in Redis if TODO-510 is done
```

## Acceptance Criteria
- [ ] Alias mappings stored in Postgres
- [ ] CRUD API for alias management
- [ ] Extraction returns canonical names with alias_of field
- [ ] Tests cover alias resolution
