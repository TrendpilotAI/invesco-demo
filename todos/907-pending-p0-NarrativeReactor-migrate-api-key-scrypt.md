# TODO: Migrate API Key Hashing from SHA-256 to scrypt

## Priority: P0
## Repo: NarrativeReactor

### Problem
API keys are hashed using SHA-256, which is fast and vulnerable to brute-force/rainbow table attacks. Should use a memory-hard function (scrypt or bcrypt) for key storage.

### Action Items
- Replace SHA-256 hashing with Node.js built-in `crypto.scrypt()` with salt
- Implement seamless migration: on API key verification, check if hash is SHA-256 format, if so verify and re-hash with scrypt
- Update key generation endpoint to use scrypt from day one
- Add test coverage for both hash formats during migration period
- Document key rotation procedure

### Impact
- Eliminates brute-force attack vector on API keys
- Required for enterprise/compliance customers
- Industry-standard security practice

### References
- AUDIT.md security section (item: scrypt migration)
- TODO-878 (scrypt-api-key-hashing)
