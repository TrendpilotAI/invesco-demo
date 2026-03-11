# TIER3-SCORE-SUMMARY.md — core-entityextraction

**Composite Score:** 7.1/10  
**Category:** Infrastructure  
**Tier:** 3

## Dimension Breakdown

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Test Coverage** | 8/10 | Comprehensive test suite with auth, health, extraction, API tests |
| **Business Value** | 8/10 | Core NLP infrastructure service for financial entity extraction |
| **Security** | 7/10 | API key auth + rate limiting, but connection leak issues noted |
| **Documentation** | 7/10 | Good README with API examples, could use more inline docs |
| **Code Quality** | 6/10 | Solid FastAPI structure but 712-line main.py shows architectural debt |
| **Architecture** | 6/10 | FastAPI foundation good but monolithic main.py needs refactoring |

## Top 3 Priority Items

1. **🟠 Refactor monolithic main.py (712 lines)**
   - Extract business logic into separate modules
   - Split entity extraction logic from HTTP handlers
   - Create proper service layer architecture

2. **🟠 Fix connection leaks in persistence.py**
   - Replace `try/except/else` with `try/finally` for connection cleanup
   - Ensure connections are properly returned to pool on exceptions
   - Files: `persistence.py` multiple functions

3. **🟡 Remove dead code and DRY violations**
   - Delete unused `_locate_entities()` slow path function
   - Remove unused Pydantic models `FixedListsUpdateRequest`/`FixedListsDeleteRequest`
   - Consolidate duplicate entity location logic

## CRITICAL Flags

None - This is a well-functioning service with technical debt rather than critical issues.

## Summary

Solid FastAPI-based NLP service with excellent test coverage and good security practices. Main issues are architectural - the 712-line main.py indicates need for better separation of concerns. Connection leak issues and dead code suggest moderate technical debt that should be addressed to maintain service reliability.