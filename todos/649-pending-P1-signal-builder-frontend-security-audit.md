# TODO-649: Security Audit — Dependencies + Auth + CSP

**Repo:** signal-builder-frontend  
**Priority:** P1  
**Effort:** Small (half day)  
**Category:** Security

## Description
No recent security audit. Storybook v6 + old TypeScript likely have CVEs. Auth cookie flags should be verified. CSP headers should be added.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-frontend/:
1. Run: npm audit --json > /tmp/audit-results.json
2. Fix all critical and high severity issues
3. Check nginx.conf — add Content-Security-Policy header:
   add_header Content-Security-Policy "default-src 'self'; script-src 'self'; ..."
4. Review shared/lib/auth.ts — verify cookie settings use httpOnly, SameSite=Strict, Secure
5. Check .env.example covers all VITE_* vars used in appConfig.ts
6. Verify no secrets in source code: grep -r "password\|secret\|api_key" src/ (case-insensitive)
```

## Acceptance Criteria
- [ ] npm audit shows 0 critical/high vulns
- [ ] CSP header added to nginx.conf
- [ ] Auth cookies use httpOnly + SameSite + Secure
- [ ] No hardcoded secrets found
- [ ] .env.example is complete

## Dependencies
None
