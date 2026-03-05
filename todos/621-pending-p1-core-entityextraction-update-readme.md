# TODO-621: Rewrite README.md for FastAPI/Python 3.11

**Repo:** core-entityextraction  
**Priority:** P1 (Quick Fix)  
**Effort:** S (~30 min)  
**Status:** pending

## Problem
README.md still references Flask, Python 3.6.5, SQLite, and `python -u -m flask run`. The service was completely rewritten to FastAPI + Python 3.11 + Postgres.

## Coding Prompt
```
Rewrite /data/workspace/projects/core-entityextraction/README.md:

# Entity Extraction Service v2.0.0

## Overview
FastAPI microservice for financial entity extraction. Supports 17 entity types including Ticker, Company, Fund, Country, CurrencyPair via:
- Regex pattern matching (compiled, cached)  
- ML NER (custom spaCy nermodel3)
- Standard spaCy NER (optional)

## Quick Start (Docker)
cp .env.example .env  # set DATABASE_URL, ENTITY_EXTRACTION_API_KEY
docker-compose up

Service available at http://localhost:5001
Swagger UI: http://localhost:5001/docs

## Environment Variables
- DATABASE_URL — Postgres connection string (optional; in-memory if unset)
- ENTITY_EXTRACTION_API_KEY — comma-separated API keys for zero-downtime rotation
- ENABLE_SPACY_ENTITY_EXTRACTION — set to "true" to enable standard spaCy NER
- SPACY_MODEL — spaCy model name (default: en_core_web_sm)
- REVISION_VERSION — injected by CI for version endpoint
- DB_POOL_MIN / DB_POOL_MAX — Postgres pool size (default: 2/10)
- REDIS_URL — optional Redis for response caching
- CACHE_TTL_SECONDS — cache TTL (default: 60)

## Local Dev (Virtualenv)
python -m venv env && source env/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload --port 5001

## API Endpoints
POST /regex_entity_extraction — regex-based extraction (100/min rate limit)
POST /ml_entity_extraction — ML NER extraction (60/min rate limit)  
POST /spacy_entity_extraction — standard spaCy NER (60/min, requires ENABLE_SPACY)
POST /fixed_lists — add entities to store
DELETE /fixed_lists — remove entities from store
GET /health — health check
GET /version — version string

## Authentication
All endpoints (except /health) require X-API-Key header matching ENTITY_EXTRACTION_API_KEY.
```

## Acceptance Criteria
- [ ] No Flask/SQLite/Python 3.6 references remain
- [ ] All env vars documented
- [ ] API endpoints documented with rate limits
- [ ] Docker and local dev instructions accurate
