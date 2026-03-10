# TODO-833: Fix PasswordUpdateRequest.validate_password_complexity() — Add @field_validator

**Repo:** signal-studio-auth
**Priority:** P1 (High)
**Effort:** 30 minutes
**Status:** pending
**Dependencies:** None
**Created:** 2026-03-10

## Problem

`routes/auth_routes.py` line ~296 defines `PasswordUpdateRequest` with a `validate_password_complexity()` classmethod, but it's missing the `@field_validator("new_password")` decorator. This means:

1. The validator is **never called** by Pydantic — it's just a dead method
2. The `/update-password` route (lines ~508-515) has **duplicate inline validation** that does the same checks manually with `HTTPException(status_code=422, ...)`
3. If anyone constructs `PasswordUpdateRequest(new_password="weak")` directly, no validation occurs

## Files to Change

- `routes/auth_routes.py`:
  - Add `@field_validator("new_password")` decorator to `validate_password_complexity()` (line ~296)
  - Add `field_validator` to the pydantic import (line ~31)
  - Remove the 4 inline validation checks in `/update-password` route (lines ~508-515)

## Coding Prompt

```
Open /data/workspace/projects/signal-studio-auth/routes/auth_routes.py

1. Add field_validator to the pydantic import:
   Change: from pydantic import BaseModel, ConfigDict, EmailStr
   To:     from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

2. Add the decorator to validate_password_complexity (around line 296):
   Change:
       @classmethod
       def validate_password_complexity(cls, v: str) -> str:
   To:
       @field_validator("new_password")
       @classmethod
       def validate_password_complexity(cls, v: str) -> str:

3. In the /update-password route handler, remove the duplicate inline checks.
   Delete these lines (approximately 508-515):
       password = body.new_password
       if len(password) < 8:
           raise HTTPException(status_code=422, detail="Password must be at least 8 characters")
       if not any(c.isupper() for c in password):
           raise HTTPException(status_code=422, detail="Password must contain at least one uppercase letter")
       if not any(c.islower() for c in password):
           raise HTTPException(status_code=422, detail="Password must contain at least one lowercase letter")
       if not any(c.isdigit() for c in password):
           raise HTTPException(status_code=422, detail="Password must contain at least one number")

   Replace with just:
       password = body.new_password
   (Pydantic will validate on model construction before the route handler runs)

4. Update tests: PasswordUpdateRequest(new_password="weak") should now raise ValidationError.
   Add a quick test in tests/test_password_reset.py or a new test file:

   def test_password_complexity_validation():
       from pydantic import ValidationError
       import pytest
       from routes.auth_routes import PasswordUpdateRequest
       
       with pytest.raises(ValidationError):
           PasswordUpdateRequest(new_password="weak")
       with pytest.raises(ValidationError):
           PasswordUpdateRequest(new_password="alllowercase1")
       with pytest.raises(ValidationError):
           PasswordUpdateRequest(new_password="ALLUPPERCASE1")
       with pytest.raises(ValidationError):
           PasswordUpdateRequest(new_password="NoDigitsHere")
       # Valid password should work
       valid = PasswordUpdateRequest(new_password="ValidPass1")
       assert valid.new_password == "ValidPass1"

Run: cd /data/workspace/projects/signal-studio-auth && python -m pytest -v
```

## Acceptance Criteria

- [ ] `@field_validator("new_password")` decorator is on `validate_password_complexity()`
- [ ] `PasswordUpdateRequest(new_password="weak")` raises `ValidationError`
- [ ] Inline validation in `/update-password` route is removed (DRY)
- [ ] Route still returns 422 for weak passwords (Pydantic raises → FastAPI returns 422)
- [ ] All existing tests pass
- [ ] New unit test validates the 4 complexity rules + a valid password
