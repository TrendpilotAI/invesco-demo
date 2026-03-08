# Security Audit — express-rate-limit CVE

**CVE/GHSA:** GHSA-46wh-pxpv-q5gq  
**Severity:** HIGH (devDependency only — no production exposure)  
**Path:** `shadcn → @modelcontextprotocol/sdk → express-rate-limit >=8.2.0 <8.2.2`  
**Issue:** IPv4-mapped IPv6 addresses bypass per-client rate limiting  

## Fix Applied
- `package.json` includes `pnpm.overrides` and `overrides` pinning `express-rate-limit` to `^8.2.2`
- This forces the fixed version regardless of what shadcn's transitive dep resolves to
- Dev-only risk — the demo-app is a static Next.js export with no server-side rate limiting in production

## Verification
Run `pnpm audit` after `pnpm install` — should show 0 HIGH/CRITICAL vulnerabilities.
