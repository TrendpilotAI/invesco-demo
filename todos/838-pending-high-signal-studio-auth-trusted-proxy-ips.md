# TODO-838: Fix X-Forwarded-For Spoofing — Add TRUSTED_PROXY_IPS Validation

**Repo:** signal-studio-auth
**Priority:** P1 (High)
**Effort:** 1.5 hours
**Status:** pending
**Dependencies:** None
**Created:** 2026-03-10

## Problem

`_client_ip()` in `routes/auth_routes.py` (line ~145) blindly trusts `X-Forwarded-For`:

```python
def _client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
```

An attacker can bypass rate limiting by setting `X-Forwarded-For: random-ip` on every request, getting a fresh rate limit window each time. This completely defeats the login/signup rate limits.

## Files to Change

- `routes/auth_routes.py` — Update `_client_ip()` with TRUSTED_PROXY_IPS validation
- `config/supabase_config.py` — Add TRUSTED_PROXY_IPS env var loading

## Coding Prompt

```
1. Open /data/workspace/projects/signal-studio-auth/config/supabase_config.py

Add after the existing config:

import ipaddress

# Trusted proxy IPs/CIDRs — only trust X-Forwarded-For from these sources
# Comma-separated. Railway uses 10.0.0.0/8 internal network.
_TRUSTED_PROXY_IPS_RAW = os.environ.get("TRUSTED_PROXY_IPS", "")
TRUSTED_PROXY_NETWORKS: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
if _TRUSTED_PROXY_IPS_RAW:
    for cidr in _TRUSTED_PROXY_IPS_RAW.split(","):
        cidr = cidr.strip()
        if cidr:
            try:
                TRUSTED_PROXY_NETWORKS.append(ipaddress.ip_network(cidr, strict=False))
            except ValueError:
                _logger = logging.getLogger(__name__)
                _logger.warning("Invalid CIDR in TRUSTED_PROXY_IPS: %s", cidr)

2. Open /data/workspace/projects/signal-studio-auth/routes/auth_routes.py

Replace _client_ip() with:

import ipaddress
from config.supabase_config import TRUSTED_PROXY_NETWORKS

def _client_ip(request: Request) -> str:
    """
    Extract real client IP, only trusting X-Forwarded-For from known proxies.
    
    If TRUSTED_PROXY_IPS is not configured, falls back to request.client.host
    (safe default — ignores X-Forwarded-For entirely when no proxies trusted).
    If configured, only trusts X-Forwarded-For when the direct connection
    comes from a trusted proxy IP.
    """
    direct_ip = request.client.host if request.client else "unknown"
    
    forwarded_for = request.headers.get("X-Forwarded-For")
    if not forwarded_for or not TRUSTED_PROXY_NETWORKS:
        return direct_ip
    
    # Only trust the header if the direct connection is from a trusted proxy
    try:
        direct_addr = ipaddress.ip_address(direct_ip)
        is_trusted = any(direct_addr in net for net in TRUSTED_PROXY_NETWORKS)
    except ValueError:
        return direct_ip
    
    if not is_trusted:
        return direct_ip
    
    # Rightmost untrusted IP in X-Forwarded-For chain is the real client
    # For single-proxy setups (Railway), leftmost is fine
    return forwarded_for.split(",")[0].strip()

Add tests:
- Test _client_ip with no X-Forwarded-For → returns client.host
- Test _client_ip with X-Forwarded-For but no TRUSTED_PROXY_NETWORKS → returns client.host
- Test _client_ip with X-Forwarded-For from trusted proxy → returns forwarded IP
- Test _client_ip with X-Forwarded-For from untrusted source → returns client.host

Run: cd /data/workspace/projects/signal-studio-auth && python -m pytest -v
```

## Acceptance Criteria

- [ ] `_client_ip()` only trusts `X-Forwarded-For` from IPs in `TRUSTED_PROXY_IPS`
- [ ] When `TRUSTED_PROXY_IPS` is empty, `X-Forwarded-For` is ignored entirely (safe default)
- [ ] Rate limiting works correctly with spoofed headers (attacker gets their real IP rate-limited)
- [ ] Railway deployments work by setting `TRUSTED_PROXY_IPS=10.0.0.0/8`
- [ ] Unit tests cover all trust/distrust scenarios
- [ ] All existing tests pass
