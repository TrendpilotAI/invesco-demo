# TODO-588: Rate Limiting X-Forwarded-For Adversarial Tests

**Repo:** signal-builder-backend
**Priority:** P2 (Medium)
**Effort:** S (Small, ~2h)
**Status:** pending
**Created:** 2026-03-06

## Description

Slowapi rate limiting was added (TODO-353) but the X-Forwarded-For header spoofing bypass has not been tested or hardened. An attacker can rotate IPs via X-Forwarded-For headers to bypass rate limits.

## Acceptance Criteria

- [ ] Test verifies that X-Forwarded-For spoofing does NOT bypass rate limits when TRUSTED_PROXIES is configured
- [ ] Settings include a TRUSTED_PROXIES list for Railway/production
- [ ] Slowapi is configured to only trust X-Forwarded-For from trusted proxy IPs
- [ ] CI test covers: normal rate limit, spoofed header (should still be rate limited), trusted proxy header (should work correctly)

## Coding Prompt

```
In /data/workspace/projects/signal-builder-backend/:

1. In settings/common.py, add:
   TRUSTED_PROXIES: list[str] = []  # e.g. ["10.0.0.1"] for Railway reverse proxy

2. In core/__init__.py (app factory), configure slowapi key_func to use real IP:
   from slowapi.util import get_remote_address
   # override key_func to strip untrusted X-Forwarded-For headers
   # only use X-Forwarded-For if request.client.host in settings.TRUSTED_PROXIES

3. Add tests in tests/test_rate_limiting_security.py:
   - Test: exceed rate limit from same IP → 429
   - Test: rotate X-Forwarded-For headers from untrusted client → still rate limited (same real IP bucket)
   - Test: trusted proxy with X-Forwarded-For → correctly uses forwarded IP
```

## Dependencies
- TODO-353 (rate limiting) — DONE ✅
