# TODO 452 — forwardlane_advisor: Security Audit & CVE Remediation

**Priority:** P0 | **Effort:** M | **Repo:** forwardlane_advisor

## Description
All npm dependencies are from 2016-2017 with multiple known CVEs. Conduct full security audit and fix critical vulnerabilities.

## Full Coding Prompt
```
Perform security audit and remediation for forwardlane_advisor.

1. Run: npm audit --json > /tmp/audit-report.json
2. Fix all critical and high severity vulnerabilities:
   - bcryptjs: upgrade to latest
   - express: upgrade from ~4.12.3 to ^4.21
   - passport: upgrade from ^0.3.0 to ^0.7
   - libxmljs: upgrade from 0.18.0 to latest (XXE vulnerabilities)
   - sequelize: assess upgrade path from v3
   - cookie-session: upgrade from alpha version
   - express-session: upgrade from ^1.11.3

3. Secrets management audit:
   - Ensure all *.sample config files are in .gitignore
   - Verify no credentials in git history: git log --all -S 'password' --oneline
   - Add .env.example template
   - Document required environment variables

4. CORS & headers review:
   - Verify helmet.js configuration in app.js
   - Add explicit CORS configuration restricting origins
   - Ensure CSP headers are set

5. Session security:
   - Set secure: true, httpOnly: true, sameSite: 'strict' on sessions
   - Generate strong session secret from environment variable

Document all findings in SECURITY-FIXES.md
```

## Acceptance Criteria
- [ ] Zero critical npm audit vulnerabilities
- [ ] No secrets in config files tracked by git
- [ ] Session cookies have secure flags
- [ ] CORS properly configured
- [ ] SECURITY-FIXES.md documents all changes

## Dependencies
- TODO 451 (Node.js upgrade first)

## Estimated Effort
3-4 days
