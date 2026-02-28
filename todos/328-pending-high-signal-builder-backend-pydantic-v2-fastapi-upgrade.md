# Upgrade Pydantic v2 + FastAPI to Latest

**Repo:** signal-builder-backend  
**Priority:** high  
**Effort:** L (1-2 weeks)  
**Phase:** 1  
**Depends on:** TODO-316 (CVE audit baseline)

## Problem
- Pydantic 1.10.13 is EOL with known CVEs; v2 is 5-50x faster
- FastAPI 0.92 is very outdated (current: 0.115+)
- Must be done together due to tight coupling

## Task
1. Create feature branch `feat/pydantic-v2-upgrade`
2. Install pydantic v2 with `pydantic[v1]` compat shim initially
3. Update all schema files:
   - `.dict()` → `.model_dump()`
   - `.json()` → `.model_dump_json()`
   - `@validator` → `@field_validator`
   - `class Config` → `model_config = ConfigDict(...)`
4. Upgrade fastapi to 0.115+
5. Upgrade fastapi-jwt-auth (may need alternative — library unmaintained)
6. Run full test suite, fix failures
7. Remove v1 compat shim

## Acceptance Criteria
- All tests pass with pydantic v2 (no v1 shim)
- FastAPI at 0.115+
- No deprecated pydantic v1 APIs in codebase
- API response times improved (benchmark before/after)
