# TODO-511: Refactor main.py God File

**Repo:** core-entityextraction
**Priority:** P2
**Effort:** M (4-6h)
**Dependencies:** TODO-503 (tests first, so refactor doesn't break things)
**Blocks:** None

## Description
609-line main.py mixes routing, business logic, pattern matching, and ML loading. Extract into clean modules.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Create routers/ directory:
   - routers/__init__.py
   - routers/extraction.py — regex and ML extraction endpoints
   - routers/entities.py — fixed_lists CRUD endpoints
   - routers/health.py — health check endpoint

2. Create services/ (or rename existing):
   - services/pattern_matcher.py — _build_entity_patterns, match_patterns, ExcludeRules, ReplaceRule
   - services/ml_predictor.py — spaCy model loading, spacy_predict
   - services/entity_store.py — in-memory entity store management

3. Keep main.py minimal:
   - App init, middleware, router includes, startup/shutdown events
   - Target: <50 lines

4. Update all imports
5. Run tests to verify no regressions
```

## Acceptance Criteria
- [ ] main.py < 50 lines
- [ ] All business logic in services/
- [ ] All routes in routers/
- [ ] All existing tests pass
- [ ] No behavior changes
