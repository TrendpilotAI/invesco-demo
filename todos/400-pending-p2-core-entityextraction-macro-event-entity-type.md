# TODO-400: Add MacroEvent Entity Type

**Repo:** core-entityextraction  
**Priority:** P2  
**Effort:** S (2-3 hours)  
**Status:** pending

## Description
The current 17 entity types are missing macro financial events (FOMC meetings, CPI releases, NFP reports) which are critical signals in ForwardLane's advisor intelligence product.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Add to constants/entities.py:
   ENTITY_MACRO_EVENT = "MacroEvent"

2. Add ENTITY_MACRO_EVENT to main.py entity_store init dict

3. Add to ENTITY_OPTIONS in main.py:
   ENTITY_MACRO_EVENT: {"replace_rules": [ReplaceRule.Dash, ReplaceRule.Dot]},

4. Add seed data in seeds/fixed_lists/ for MacroEvent:
   macro_events = [
     "FOMC", "Fed meeting", "Federal Reserve meeting", "rate decision",
     "CPI", "Consumer Price Index", "PCE", "Personal Consumption Expenditures",
     "NFP", "non-farm payroll", "jobs report", "unemployment rate",
     "Jackson Hole", "OPEC", "earnings season", "GDP", "retail sales",
     "Treasury auction", "debt ceiling", "fiscal cliff", "taper tantrum"
   ]

5. Update schema.sql to include MacroEvent if entity types are schema-constrained

6. Add tests/test_macro_event.py:
   - test_fomc_extracted: "The FOMC raised rates" → MacroEvent match
   - test_nfp_extracted: "NFP came in below expectations" → MacroEvent match
   - test_macro_event_in_fixed_lists: add via /fixed_lists, extract via /regex_entity_extraction
```

## Dependencies
- TODO-399 (test suite)

## Acceptance Criteria
- MacroEvent appears in /fixed_lists CRUD operations
- Seed data loads correctly at startup
- At least 20 macro event patterns recognized
- Tests pass
