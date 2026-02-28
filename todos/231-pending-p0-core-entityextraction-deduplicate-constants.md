# 231 — Deduplicate Entity Type Constants

**Repo:** core-entityextraction  
**Priority:** P0 (DRY)  
**Effort:** 30 minutes  
**Dependencies:** 230 (remove dead code first)

## Description
Entity type strings (ENTITY_CITY, ENTITY_TICKER, etc.) are defined identically in both `main.py` (lines ~30-46) and `constants/entities.py`. main.py should import from constants/.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Remove the duplicate constant definitions (lines ~30-46):
   # DELETE these lines:
   ENTITY_CITY = "City"
   ENTITY_CLIENT_FIRM = "ClientFirm"
   ... (all 17 ENTITY_* definitions)

2. Add import at top of main.py:
   from constants.entities import (
       ENTITY_CITY, ENTITY_CLIENT_FIRM, ENTITY_COMPANY, ENTITY_COUNTRY,
       ENTITY_CURRENCY_PAIR, ENTITY_ECONOMIC_INDICATOR, ENTITY_ECONOMIC_SECTOR,
       ENTITY_FIN_INSTRUMENT, ENTITY_FIN_STRATEGY, ENTITY_FUND,
       ENTITY_INTEREST_RATE, ENTITY_INVESTMENT_OBJECTIVE, ENTITY_PORTFOLIO_MANAGER,
       ENTITY_PRODUCT_NAME, ENTITY_STATE, ENTITY_STOCK_INDEX, ENTITY_TICKER,
   )

3. Verify constants/entities.py exports all 17 constants (it should already).

4. Run: python -c "import main" to verify no import errors.

5. Commit: "refactor: import entity constants from constants/entities.py (DRY)"
```

## Acceptance Criteria
- [ ] ENTITY_* constants defined only in constants/entities.py
- [ ] main.py imports them from constants/entities
- [ ] App starts without errors
- [ ] All extraction endpoints return correct entity types
