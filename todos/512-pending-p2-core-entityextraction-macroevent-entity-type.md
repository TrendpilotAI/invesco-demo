# TODO-512: Add MacroEvent Entity Type

**Repo:** core-entityextraction
**Priority:** P2
**Effort:** M (1 day)
**Dependencies:** None
**Blocks:** None

## Description
Add new entity type `MacroEvent` for Fed meetings, earnings calls, elections, etc. Seed from financial calendar.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Add MacroEvent to entity type enum/constants
2. Create seeds/macro_events.json with initial events:
   - FOMC meetings, Fed rate decisions
   - Major earnings seasons (Q1-Q4)
   - US elections, economic data releases (CPI, NFP, GDP)
   - Global events (ECB meetings, BOJ decisions)

3. Add regex patterns for MacroEvent matching:
   - Date-associated event names
   - Abbreviated forms ("FOMC", "NFP", "CPI")

4. Update entity store to load MacroEvent seeds on startup
5. Add tests for MacroEvent extraction
6. Update API docs with new entity type
```

## Acceptance Criteria
- [ ] MacroEvent recognized as 18th entity type
- [ ] Seed data includes major financial calendar events
- [ ] Tests verify extraction of macro events from sample text
- [ ] API docs updated
