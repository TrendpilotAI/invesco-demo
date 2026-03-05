# TODO #429 — Use Railway URL for IT Security Demo (Security Headers)

**Priority:** P0
**Repo:** invesco-retention
**Effort:** XS (15 min)
**Status:** PENDING

## Problem
`next.config.ts` defines security headers (X-Frame-Options, X-Content-Type-Options, etc.) but these are **silently ignored** for `output: 'export'` (static builds). GitHub Pages does NOT send these headers.

## Impact
If Invesco IT security team reviews the demo URL and runs a header check, it will appear no security headers are set — credibility risk.

## Fix
Use the Railway/Docker deployment URL instead of GitHub Pages for any IT security discussion. The nginx.conf in demo-app/ correctly sets headers when served via Docker/Railway.

## Steps
1. Deploy to Railway if not already live (DEPLOY_INSTRUCTIONS.md has instructions)
2. Verify headers using: `curl -I https://<railway-url>/` — confirm X-Frame-Options present
3. Update DEPLOYED_URL.txt with Railway URL as "security-compliant URL"
4. Use Railway URL in the IT Security one-pager (#335)

## Acceptance Criteria
- [ ] Railway URL returns proper security headers
- [ ] IT security one-pager (#335) uses Railway URL

## Agent Prompt
```
Deploy invesco-retention demo-app to Railway via Docker.
File: /data/workspace/projects/invesco-retention/demo-app/Dockerfile
Instructions: /data/workspace/projects/invesco-retention/DEPLOY_INSTRUCTIONS.md

After deploying, run: curl -I <url> and confirm these headers are present:
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin

Update /data/workspace/projects/invesco-retention/DEPLOYED_URL.txt with the Railway URL.
```
