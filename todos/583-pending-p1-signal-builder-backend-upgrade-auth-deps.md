# TODO-583: Upgrade python-jose → PyJWT, passlib → argon2-cffi

**Priority:** P1 (High Security)
**Repo:** signal-builder-backend
**Effort:** S (2-4 hours)
**Status:** Pending

## Problem
- `python-jose==3.3.0` has known CVEs (algorithm confusion attacks)
- `passlib==1.7.4` is unmaintained since 2020

## Task
1. Replace python-jose with PyJWT (actively maintained, simpler API)
2. Replace passlib password hashing with argon2-cffi directly
3. Update all imports and usage
4. Ensure all auth tests pass

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend/:

1. pipenv install PyJWT[crypto] argon2-cffi
2. pipenv uninstall python-jose passlib
3. Find all imports: grep -r "from jose\|import jose\|from passlib\|import passlib" apps/ core/
4. Replace jose token creation/validation with PyJWT equivalents:
   jose.jwt.encode() → jwt.encode()
   jose.jwt.decode() → jwt.decode()
5. Replace passlib CryptContext with argon2:
   from argon2 import PasswordHasher
   ph = PasswordHasher()
   ph.hash(password), ph.verify(hash, password)
6. Run full test suite: pipenv run pytest tests/ -x
7. Run pip-audit to confirm CVEs resolved
```

## Acceptance Criteria
- [ ] python-jose removed from Pipfile
- [ ] passlib removed from Pipfile
- [ ] All auth flows work with new libraries
- [ ] pip-audit reports no known CVEs for auth deps
- [ ] All 666+ tests pass
