# core-entityextraction — P2 NICE-TO-HAVE TODOs
> Updated: 2026-03-15 | Scored by Honey 🍯

## 🚀 [FEATURE] Multi-Tenancy Foundation
- API Key → Tenant mapping in Postgres (replace single static key)
- Per-tenant entity stores (scoped `/fixed_lists`)
- Tenant usage analytics (`extraction_events` table)
- **Effort:** M-L | **Status:** ❌ PENDING

## 🚀 [FEATURE] Entity Versioning
- Version-stamped entity stores with `effective_from` timestamps
- Entity changelog API for compliance audit trails
- Reproducible extraction via optional `entity_store_version` param
- **Effort:** M | **Status:** ❌ PENDING

## 🚀 [FEATURE] Entity Normalization / Canonicalization
- Map "Goldman Sachs" / "Goldman" / "GS" → canonical form
- Tickers → exchange symbol, funds → ISIN/CUSIP
- **Effort:** M | **Status:** ❌ PENDING

## 🚀 [FEATURE] Extraction Explainability
- Return match_source (pattern vs ml_model), confidence, context_window
- `explain=true` query param for verbose mode
- **Effort:** M | **Status:** ❌ PENDING

## 🚀 [FEATURE] Macro Event Entity Type
- Add `MACRO_EVENT` for FOMC meetings, CPI releases, earnings dates
- Temporal context extraction: "Q3 earnings" → `{temporal: "Q3_2026"}`
- **Effort:** S | **Status:** ❌ PENDING

## 🧪 [QUALITY] Golden Dataset Regression Tests
- Curate 50-100 financial text samples with known-correct annotations
- Run as regression suite on every PR, alert on F1 drop > 2%
- **Effort:** M | **Status:** ❌ PENDING

## 🛠️ [DEVOPS] Docker Multi-stage Build
- Current Dockerfile likely installs dev deps in prod. Add multi-stage: spaCy model download → slim runtime.
- **Effort:** S | **Status:** ❌ PENDING

## 🔒 [SECURITY] Dependency Vulnerability Scan
- Add `pip-audit` to CI pipeline
- **Effort:** XS | **Status:** ❌ PENDING

## 🔒 [SECURITY] Verify docker/.env not committed with real secrets
- Check if `docker/.env` contains real credentials. Add to `.gitignore` if needed.
- **Effort:** XS | **Status:** ❌ PENDING

## ⚡ [PERFORMANCE] Redis Pattern Cache for Multi-Instance
- Replace in-process pattern cache with Redis for shared invalidation across Railway instances
- **Effort:** M | **Status:** ❌ PENDING

## ⚡ [PERFORMANCE] spaCy Pipeline Optimization
- Disable unused pipeline components (`parser`, `lemmatizer`) for pure NER tasks
- Use `nlp.select_pipes(enable=["ner"])` for 2-3x speed improvement
- **Effort:** XS | **Status:** ❌ PENDING

## 🚀 [FEATURE] Extraction Feedback Loop
- `POST /feedback` endpoint for correction capture
- Feeds retraining data flywheel
- **Effort:** L | **Status:** ❌ PENDING

## 🚀 [FEATURE] LLM Fallback for Low-Confidence Entities
- When ML confidence < threshold, fall back to GPT-4o structured extraction
- Cache results in Redis, log fallback rates to guide retraining
- **Effort:** L | **Status:** ❌ PENDING
