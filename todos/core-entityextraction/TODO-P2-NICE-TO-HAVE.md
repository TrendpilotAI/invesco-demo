# core-entityextraction — P2 NICE-TO-HAVE TODOs

> Generated: 2026-03-14 | Source: BRAINSTORM.md + AUDIT.md

## 🟢 TODO-902: Split main.py into Service Modules
**File:** `main.py` (712 lines)  
**Effort:** M (3h)  
**Description:** Monolithic main.py combines entity store, pattern matching, ML services, endpoints, middleware, and models. Split into:
```
services/pattern_service.py    ← ReplaceRule, ExcludeRules, match_patterns, cache
services/ml_service.py         ← _load_ml_model, ml_predict, spacy_predict
services/entity_store.py       ← entity_store dict, entity_count
main.py                        ← FastAPI app, endpoints only (~150 lines)
```

---

## 🟢 TODO-903: Combined Extraction Endpoint
**Effort:** S  
**Description:** `/combined_entity_extraction` runs regex + ML in parallel, merges results with source tagging and deduplication by (type, value, span).

---

## 🟢 TODO-904: Entity Confidence Scores from ML NER
**Effort:** M  
**Description:** Expose per-entity confidence scores from spaCy. Regex/fixed_list results return `confidence: 1.0`.

---

## 🟢 TODO-905: Batch Extraction Endpoint
**Effort:** S  
**Description:** `POST /batch_entity_extraction` accepting `{"texts": [...], "mode": "regex|ml|spacy|combined"}`.

---

## 🟢 TODO-906: Entity Stats / Health Detail
**Effort:** XS  
**Description:** `GET /stats` returning entity counts by type, cache version, model status, DB connectivity. Useful for K8s readiness probes.

---

## 🟢 TODO-907: MacroEvent Entity Type
**Effort:** M  
**Description:** Add `MacroEvent` type (e.g., "Federal Reserve meeting", "FOMC decision"). Seeds + regex patterns.

---

## 🟢 TODO-908: Redis Entity Store Cache
**Effort:** M  
**Description:** Multi-instance deployments diverge when entities updated via one instance. Add Redis write-through with pubsub invalidation.

---

## 🟢 TODO-909: Model Versioning Strategy
**Effort:** M  
**Description:** nermodel3 baked into repo. Store models in S3/R2 by version tag, `MODEL_VERSION` env var selects at startup.

---

## 🟢 TODO-910: Async spaCy Model Loading
**Effort:** S  
**Description:** Model loading blocks startup 2-5s. Use `asyncio.get_event_loop().run_in_executor()`.

---

## 🟢 TODO-911: Request ID Middleware
**Effort:** XS  
**Description:** Add `X-Request-ID` header generation/propagation for distributed tracing.

---

## 🟢 TODO-912: Property-Based Testing (Hypothesis)
**Effort:** M  
**Description:** Use `hypothesis` to generate random financial text and verify regex patterns don't false-positive.
