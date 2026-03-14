# SCORE SUMMARY — core-entityextraction

**Composite Score:** 6.6/10  
**Category:** CORE (ForwardLane production infrastructure)  
**Last Scored:** 2026-03-14

## Dimension Breakdown

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Code Quality** | 6/10 | 712-line monolithic main.py, duplicate filter bug, dead code, DRY violations |
| **Test Coverage** | 5/10 | ~45% estimated. Auth/health/regex covered. Zero ML/spaCy/persistence tests |
| **Security** | 7/10 | API key auth + rate limiting. Connection leak risk. No input allowlist validation |
| **Documentation** | 7/10 | Good README with API examples. BRAINSTORM/PLAN/AUDIT all current. Inline docs sparse |
| **Architecture** | 6/10 | Solid FastAPI foundation but monolithic. Sync DB in async app. No service layer split |
| **Business Value** | 8/10 | Core NLP pipeline for ForwardLane. Revenue-critical infrastructure |

## CRITICAL Issues (4)

1. 🔴 **Connection leak in persistence.py** — `try/except/else` pattern leaks connections on edge-case exceptions. Pool exhaustion under load.
2. 🔴 **Duplicate filter block bug** — `match_patterns()` applies entity type filter twice. Maintenance hazard.
3. 🔴 **Zero ML/spaCy test coverage** — Two of three extraction endpoints have no tests.
4. 🔴 **No GET /fixed_lists endpoint** — Cannot query loaded entities. Blocks debugging and admin UI.

## Priority Breakdown

| Priority | Count | Key Items |
|----------|-------|-----------|
| P0 | 4 | Connection leak, filter bug, ML tests, GET endpoint |
| P1 | 8 | HTTP status codes, asyncpg, dead code, rate limits, persistence tests, CORS, metrics, CI |
| P2 | 11 | Split main.py, combined endpoint, confidence scores, batch, stats, MacroEvent, Redis, model versioning, async loading, request ID, property tests |

## Recommended Sprint Plan

- **Sprint 1 (1-2 days):** Fix all 4 P0 bugs
- **Sprint 2 (1-2 days):** Test coverage + dead code cleanup
- **Sprint 3 (2-3 days):** asyncpg migration + architecture split
- **Sprint 4 (ongoing):** New features (combined endpoint, metrics, MacroEvent)

## Scoring Rationale

Revenue potential (7): Core infrastructure, not directly revenue-generating but enables revenue features.  
Strategic value (9): Critical pipeline component for ForwardLane's AI products.  
Completeness (7): Working in production with known bugs. All three extraction modes functional.  
Urgency (5): No immediate deadline pressure, but P0 bugs should be fixed soon.  
Effort remaining (7): Most P0/P1 fixes are small. Bigger items (asyncpg, split) are M effort.
