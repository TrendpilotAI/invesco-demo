# 813 — Improve Password Strength Validation

**Repo:** signal-studio-auth  
**Priority:** P2  
**Effort:** S (1 hour)  
**Dependencies:** none

## Acceptance Criteria

- [ ] Passwords must be 8+ chars (existing)
- [ ] Must contain at least 1 uppercase, 1 lowercase, 1 number
- [ ] Common passwords rejected (check against top-1000 list)
- [ ] Clear error messages indicating what's missing
- [ ] Applied to both `/auth/signup` and `/auth/update-password`

## Coding Prompt

```
In /data/workspace/projects/signal-studio-auth/routes/auth_routes.py:

Create a password validator:

import re

COMMON_PASSWORDS = {"password", "password1", "123456", "qwerty", "letmein", "admin"}

def _validate_password(password: str) -> None:
    errors = []
    if len(password) < 8:
        errors.append("at least 8 characters")
    if not re.search(r"[A-Z]", password):
        errors.append("at least 1 uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("at least 1 lowercase letter")
    if not re.search(r"\d", password):
        errors.append("at least 1 number")
    if password.lower() in COMMON_PASSWORDS:
        errors.append("cannot be a common password")
    if errors:
        raise HTTPException(422, f"Password must contain: {', '.join(errors)}")

Call _validate_password(body.password) in signup() and _validate_password(body.new_password) in update_password().
Add tests in tests/test_auth.py.
```
