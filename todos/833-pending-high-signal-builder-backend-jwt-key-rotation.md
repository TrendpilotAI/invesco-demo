# TODO-833: JWT Key Rotation / Versioning Mechanism

**Repo:** signal-builder-backend  
**Priority:** HIGH  
**Effort:** M (2 days)  
**Status:** pending

## Problem

A single `SECRET_KEY` is used for all JWT signing (identified in AUDIT.md). If this key leaks:
1. All existing tokens are compromised (attacker can forge any token)
2. There's no way to rotate without invalidating ALL active sessions
3. The existing JTI blacklist only handles individual token revocation, not key compromise

## Solution

Implement key versioning in JWT signing:
1. JWT header includes `kid` (key ID) field
2. Settings holds `JWT_SIGNING_KEYS` dict: `{"v1": "old_key", "v2": "current_key"}`
3. New tokens always signed with current key (highest version)
4. Verification tries the `kid`-specified key, falls back to all keys
5. Key rotation = add new key to dict, bump current pointer; old tokens naturally expire

## Coding Prompt

```python
# settings/common.py changes:
JWT_SIGNING_KEYS: dict[str, str] = {}  # populated from JWT_SIGNING_KEYS_JSON env var
JWT_CURRENT_KEY_ID: str = "v1"  # which key to sign new tokens with

# Parse from env: JWT_SIGNING_KEYS_JSON='{"v1": "secret1", "v2": "secret2"}'
# If not set, fall back to SECRET_KEY as v1 for backwards compatibility

# core/auth/jwt.py changes:
import jwt

def create_access_token(data: dict, ...) -> str:
    current_kid = settings.JWT_CURRENT_KEY_ID
    current_key = settings.JWT_SIGNING_KEYS[current_kid]
    return jwt.encode(
        {**data, ...},
        current_key,
        algorithm="HS256",
        headers={"kid": current_kid}
    )

def decode_token(token: str) -> dict:
    # Get kid from unverified headers
    header = jwt.get_unverified_header(token)
    kid = header.get("kid", "v1")  # default v1 for old tokens
    key = settings.JWT_SIGNING_KEYS.get(kid)
    if not key:
        raise InvalidTokenError(f"Unknown key ID: {kid}")
    return jwt.decode(token, key, algorithms=["HS256"])
```

Add to `.env.example`:
```bash
# JWT key rotation: JSON dict of key_id -> secret
# Rotate by adding new key and updating JWT_CURRENT_KEY_ID
JWT_SIGNING_KEYS_JSON={"v1": "your-secret-key-here"}
JWT_CURRENT_KEY_ID=v1
```

## Acceptance Criteria
- New tokens include `kid` header
- Old tokens (no `kid`) still validate via backwards-compatible fallback
- Adding a new key + changing `JWT_CURRENT_KEY_ID` = zero-downtime rotation
- Old tokens continue to work until they expire
- Tests: test_jwt_key_rotation.py covering rotation + backwards compat
- Documented in README security section
