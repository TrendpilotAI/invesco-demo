# TODO-404: Pydantic v2 Migration

**Repo:** signal-studio-auth  
**Priority:** HIGH  
**Effort:** S (2-3 hours)  
**Dependencies:** None

## Problem
`requirements.txt` pins `pydantic>=1.10.0` which allows Pydantic v1. Pydantic v2 is a major rewrite with 5-50x better validation performance and is the standard going forward. The `_compat.py` middleware shims suggest v1/v2 compatibility issues.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-auth/:

1. Update requirements.txt: `pydantic>=2.0.0`

2. Update all Pydantic models in routes/auth_routes.py:
   - Replace `.dict(by_alias=True)` with `.model_dump(by_alias=True)`
   - Update any `class Config` → `model_config = ConfigDict(...)`
   - Add `from pydantic import ConfigDict` imports

3. Update middleware/_compat.py:
   - Ensure AnonymousUser and User classes use Pydantic v2 syntax
   - Add `model_config = ConfigDict(populate_by_name=True)`

4. Add typed response models for all routes:
   - `LoginResponse(access_token, refresh_token, token_type, expires_in, user)`
   - `SignupResponse(user, session)`
   - `UserResponse(user_id, email, username, organization)`

5. Run pytest and fix any v1→v2 breakage

6. Update minimum Python version to 3.11 in pyproject.toml if it exists
```

## Acceptance Criteria
- [ ] `pydantic>=2.0.0` in requirements.txt
- [ ] All tests pass with Pydantic v2
- [ ] Response models added to all routes
- [ ] No deprecation warnings from Pydantic
