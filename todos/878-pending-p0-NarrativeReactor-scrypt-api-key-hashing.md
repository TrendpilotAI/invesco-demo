# TODO-878: Replace SHA-256 with scrypt for API Key Hashing

**Repo**: NarrativeReactor  
**Priority**: P0 — Critical Security  
**Effort**: 3 hours  
**Status**: Pending  

## Problem

`src/services/tenants.ts` uses SHA-256 to hash API keys before storing in SQLite:

```typescript
export function hashApiKey(rawKey: string): string {
  return crypto.createHash('sha256').update(rawKey).digest('hex');
}
```

SHA-256 is cryptographically fast — an attacker with access to the DB can brute-force API keys at billions of attempts per second using GPUs. scrypt (or argon2) is memory-hard, making brute-force infeasible.

## Solution

Migrate to `crypto.scrypt()` (Node.js built-in, no new dependencies):

```typescript
const SCRYPT_PARAMS = { N: 16384, r: 8, p: 1 } as const;
const KEY_LENGTH = 64;

export async function hashApiKey(rawKey: string): Promise<string> {
  const salt = crypto.randomBytes(16);
  const hash = await new Promise<Buffer>((resolve, reject) => {
    crypto.scrypt(rawKey, salt, KEY_LENGTH, SCRYPT_PARAMS, (err, key) =>
      err ? reject(err) : resolve(key)
    );
  });
  return `scrypt:${salt.toString('hex')}:${hash.toString('hex')}`;
}

export async function verifyApiKey(rawKey: string, storedHash: string): Promise<boolean> {
  if (storedHash.startsWith('scrypt:')) {
    // New format
    const [, saltHex, hashHex] = storedHash.split(':');
    const salt = Buffer.from(saltHex, 'hex');
    const expected = Buffer.from(hashHex, 'hex');
    const actual = await new Promise<Buffer>((resolve, reject) => {
      crypto.scrypt(rawKey, salt, KEY_LENGTH, SCRYPT_PARAMS, (err, key) =>
        err ? reject(err) : resolve(key)
      );
    });
    return crypto.timingSafeEqual(expected, actual);
  } else {
    // Legacy SHA-256 format — verify and schedule rehash
    const legacyHash = crypto.createHash('sha256').update(rawKey).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(legacyHash), Buffer.from(storedHash));
  }
}
```

## Migration Strategy

1. Add `verifyApiKey()` async function
2. Update `validateApiKey()` in tenants.ts to use `verifyApiKey()` (make async)
3. On successful legacy SHA-256 auth, automatically rehash with scrypt (`rehashOnLogin`)
4. After 30 days, remove legacy SHA-256 branch
5. Update `rotateApiKey()` to use new `hashApiKey()` immediately

## DB Schema Change

```sql
ALTER TABLE tenants ADD COLUMN api_key_hash_v2 TEXT;
-- After migration, drop api_key_hash, rename api_key_hash_v2 to api_key_hash
```

## Files to Change

- `src/services/tenants.ts` — replace hashApiKey, add verifyApiKey, update validateApiKey
- `src/lib/db.ts` — add migration for api_key_hash_v2 column
- `src/__tests__/` — update tests to handle async hashing

## Acceptance Criteria

- [ ] `hashApiKey()` is async and uses scrypt with salt
- [ ] `verifyApiKey()` handles both legacy SHA-256 and new scrypt format
- [ ] Existing tenants auto-rehash on next successful login
- [ ] All tests updated and passing
- [ ] No new npm dependencies added (uses built-in `crypto.scrypt`)
