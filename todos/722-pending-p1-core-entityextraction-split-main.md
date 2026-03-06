# TODO-722: Refactor main.py into modular package structure

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** 4h  
**Status:** pending

## Description
main.py is 694 lines mixing app factory, middleware, Pydantic models, entity logic, and
all endpoints. Split into a clean package structure.

## Acceptance Criteria
- `main.py` becomes a thin entry point (<50 lines)
- Endpoints split into `app/api/routes/` modules
- Pydantic models in `app/models/schemas.py`
- Extraction logic in `app/services/`
- Config/env in `app/core/config.py`
- All existing tests still pass (TODO-721)

## Coding Prompt
```
Refactor /data/workspace/projects/core-entityextraction/main.py into:

app/
  __init__.py
  core/
    config.py        — env vars, settings (Pydantic Settings)
    lifespan.py      — FastAPI lifespan (replaces @app.on_event startup)
    middleware.py    — api_key_middleware
  models/
    schemas.py       — EntityExtractionRequest, FixedListsUpdateRequest, etc.
  services/
    regex_service.py — match_patterns, _invalidate_pattern_cache
    ml_service.py    — ml_predict, _load_ml_model
    spacy_service.py — spacy_predict, _load_spacy_model
  api/
    routes/
      extraction.py  — /regex_entity_extraction, /ml_entity_extraction, /spacy_entity_extraction
      fixed_lists.py — POST/DELETE /fixed_lists
      system.py      — /health, /version
    router.py        — aggregates all routes
main.py              — app factory only

Keep backward compat: all URL paths unchanged.
```

## Dependencies
TODO-721 (tests to verify no regression)
