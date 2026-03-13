# TODO: Add Helmet Middleware and Harden HTTP Security Headers

## Priority: P0
## Repo: NarrativeReactor

### Problem
Missing helmet middleware means the API is vulnerable to XSS, clickjacking, MIME sniffing attacks, and other common web vulnerabilities.

### Action Items
- Install and configure `helmet` npm package in Express app
- Configure CSP policy appropriate for the API (strict for API, permissive only what dashboard needs)
- Add HSTS header for HTTPS enforcement
- Add X-Frame-Options: DENY
- Add X-Content-Type-Options: nosniff
- Add referrer-policy
- Pin wildcard genkit dependencies to specific versions to prevent breaking changes
- Add security headers test to CI pipeline

### Impact
- Closes multiple well-known attack vectors
- Required for SOC2/enterprise customer security reviews
- Low effort, high impact

### References
- AUDIT.md security section
- TODO-879 (helmet-middleware)
- TODO-604 (pin-wildcard-genkit-deps)
