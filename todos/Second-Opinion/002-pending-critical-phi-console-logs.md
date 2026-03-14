# TODO: Remove PHI-Adjacent console.log Statements

- **Project:** Second-Opinion
- **Priority:** CRITICAL
- **Status:** pending
- **Category:** Security / HIPAA
- **Effort:** S (1-2 hours)
- **Created:** 2026-03-14

## Description
12 `console.log` statements found across components. Any log near medical data processing could leak Protected Health Information (PHI) to browser console, violating HIPAA.

## Action Items
1. Run: `grep -rn "console\." components/ hooks/ --include="*.tsx" --include="*.ts"`
2. Audit each instance — if near analysis/patient/medical data, remove or sanitize
3. Add ESLint rule `no-console: warn` to prevent future additions
4. Consider structured logger that auto-redacts PHI fields
5. Verify service worker cache exclusions are comprehensive

## Detection
```bash
grep -rn "console\." components/ --include="*.tsx" --include="*.ts"
# 12 instances found
```
