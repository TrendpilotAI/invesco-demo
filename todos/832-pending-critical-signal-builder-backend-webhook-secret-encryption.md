# TODO-832: Webhook Secret Encryption at Rest

**Repo:** signal-builder-backend  
**Priority:** CRITICAL  
**Effort:** M (1-2 days)  
**Status:** pending

## Problem

`apps/webhooks/models/webhook.py:16`:
```python
secret: Mapped[str | None] = mapped_column(String(255))
```

Webhook signing secrets are stored as **plaintext** in PostgreSQL. If the database is compromised, all HMAC signing secrets are exposed — attackers can forge webhook payloads that look authentic to all consumers.

## Solution

Use app-level encryption (AES-256-GCM via `cryptography` library) to encrypt webhook secrets before storing. The encryption key lives in `settings.WEBHOOK_SECRET_ENCRYPTION_KEY` (env var), not in the database.

**Why NOT argon2 hash:** HMAC signing requires the actual secret value (can't hash it). We need reversible encryption, not one-way hashing.

## Coding Prompt

```bash
# Add to Pipfile:
cryptography = ">=42.0.0"
```

```python
# core/encryption.py (new file):
import base64, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def get_encryption_key() -> bytes:
    key_b64 = settings.WEBHOOK_SECRET_ENCRYPTION_KEY
    return base64.b64decode(key_b64)

def encrypt_secret(plaintext: str) -> str:
    """Encrypt a webhook secret for storage. Returns base64(nonce + ciphertext)."""
    key = get_encryption_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce + ciphertext).decode()

def decrypt_secret(encrypted: str) -> str:
    """Decrypt a stored webhook secret. Returns plaintext."""
    key = get_encryption_key()
    aesgcm = AESGCM(key)
    data = base64.b64decode(encrypted)
    nonce, ciphertext = data[:12], data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode()
```

```python
# apps/webhooks/cases/webhook.py — use encrypt/decrypt:
from core.encryption import encrypt_secret, decrypt_secret

# On create:
secret_encrypted = encrypt_secret(raw_secret)
# On sign:
raw_secret = decrypt_secret(webhook.secret)
```

```python
# Migration: encrypt existing plaintext secrets
# scripts/migrate_webhook_secrets.py
```

Add `WEBHOOK_SECRET_ENCRYPTION_KEY` to `.env.example` with generation instructions:
```bash
python3 -c "import os,base64; print(base64.b64encode(os.urandom(32)).decode())"
```

## Acceptance Criteria
- New webhook secrets are stored encrypted in DB
- HMAC signing decrypts secret before use — existing functionality unchanged
- Migration script encrypts all existing plaintext secrets
- `WEBHOOK_SECRET_ENCRYPTION_KEY` required at startup; app fails loudly if missing
- Tests verify encrypt→decrypt roundtrip
- Audit log records secret rotation events
