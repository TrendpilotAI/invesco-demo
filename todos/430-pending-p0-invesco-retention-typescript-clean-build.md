# TODO #430 — Verify TypeScript Clean Build Before Demo

**Priority:** P0
**Repo:** invesco-retention
**Effort:** XS (10 min)
**Status:** PENDING

## Problem
TypeScript version 5.9.3 with React 19 and Next 16 — very new versions that may have type compatibility edge cases. Zero type errors = zero surprise crashes during demo.

## Steps
```bash
cd /data/workspace/projects/invesco-retention/demo-app
npm run build
# Should exit 0 with no type errors
```

If errors found, fix them immediately.

## Acceptance Criteria
- [ ] `npm run build` exits 0 with no errors
- [ ] All 4 static pages generated: index.html, dashboard.html, salesforce.html, create.html, mobile.html

## Agent Prompt
```
cd /data/workspace/projects/invesco-retention/demo-app
npm run build 2>&1

If any errors, fix them in the relevant .tsx file.
Report the build output and confirm success.
```
