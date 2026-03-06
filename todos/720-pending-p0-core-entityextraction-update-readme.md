# TODO-720: Update README for FastAPI/Python 3.11

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** 1h  
**Status:** pending

## Description
The README still documents the old Flask/Python 3.6 setup. New developers and CI systems
that rely on README instructions will get incorrect setup steps.

## Acceptance Criteria
- README documents FastAPI + Python 3.11 setup
- Docker Compose and bare-metal (venv) instructions are accurate
- Environment variables documented (DATABASE_URL, ENTITY_EXTRACTION_API_KEY, etc.)
- API endpoint list with example curl commands
- spaCy model download instructions included

## Coding Prompt
```
Update /data/workspace/projects/core-entityextraction/README.md to reflect the current
FastAPI + Python 3.11 + spaCy 3.7 stack. Remove all Flask/Python 3.6 references.
Include:
1. Prerequisites: Python 3.11, Docker, Docker Compose
2. Environment variables: DATABASE_URL, ENTITY_EXTRACTION_API_KEY, ENABLE_SPACY_ENTITY_EXTRACTION, REVISION_VERSION
3. Docker Compose quick start
4. Bare-metal venv setup (pip install -r requirements.txt, uvicorn main:app)
5. API overview: GET /health, GET /version, POST /regex_entity_extraction, POST /ml_entity_extraction, POST /spacy_entity_extraction, POST /fixed_lists, DELETE /fixed_lists
6. Example curl requests for each endpoint
7. Rate limits (100/min regex, 60/min ML)
8. Training: brief note on train_ml.py
```

## Dependencies
None
