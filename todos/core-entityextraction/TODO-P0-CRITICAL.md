# core-entityextraction — P0 CRITICAL TODOs

> Generated: 2026-03-14 | Source: AUDIT.md + code review

## 🔴 TODO-890: Fix Duplicate Filter Block in `match_patterns()`
**File:** `main.py`  
**Severity:** P0 — Bug  
**Effort:** XS (5 min)  
**Description:** The `include_entity_types` filtering block is applied TWICE in `match_patterns()`. The second block is identical and redundant. Currently idempotent but a maintenance hazard — if either block is modified independently, behavior diverges silently.  
**Fix:** Remove the second `if isinstance(include_entity_types, bool):` block entirely.

---

## 🔴 TODO-893: Fix Connection Leak in persistence.py
**File:** `persistence.py`  
**Severity:** P0 — Bug  
**Effort:** XS (15 min)  
**Description:** Multiple functions (`load_all`, `save_entities`, `delete_entities`) use `try/except/else` with `_put_conn(conn)` in the `else` clause. If an exception occurs after the `try` succeeds but before `else` runs, the connection is never returned to the pool, causing connection pool exhaustion under load.  
**Fix:** Move `_put_conn(conn)` to a `finally` block to unconditionally return connections.

---

## 🔴 TODO-892: Add ML/spaCy Integration Tests
**File:** `tests/`  
**Severity:** P0 — Quality  
**Effort:** M (2h)  
**Description:** Zero tests exist for `/ml_entity_extraction` and `/spacy_entity_extraction` endpoints (note: `test_ml_extraction.py` exists at 256 lines but needs verification of actual coverage). Need:
- Test endpoint returns 404 when model not loaded (mock `_ml_nlp = None`)
- Test with known financial sentences against nermodel3
- Test `entity_types_list` filtering for ML results
- Test `include_entity_types=False` exclusion
- Test spaCy endpoint with `ENABLE_SPACY_ENTITY_EXTRACTION` toggle

---

## 🔴 TODO-891: Add GET /fixed_lists Endpoint
**File:** `main.py`  
**Severity:** P0 — Feature  
**Effort:** S (30 min)  
**Description:** No way to query what entities are currently loaded. Essential for debugging, admin UIs, and integration tests that verify load state.  
**API:**
```
GET /fixed_lists → all entity types with counts
GET /fixed_lists?entity_type=Ticker → {"Ticker": ["AAPL", ...], "count": N}
```
