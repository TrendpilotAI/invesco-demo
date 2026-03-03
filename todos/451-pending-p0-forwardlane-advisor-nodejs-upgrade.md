# TODO 451 — forwardlane_advisor: Node.js Upgrade to v20 LTS

**Priority:** P0 | **Effort:** M | **Repo:** forwardlane_advisor

## Description
The forwardlane_advisor app targets Node.js >= 0.10.38 (from 2013!). This is a critical security and compatibility risk. Upgrade to Node.js 20 LTS.

## Full Coding Prompt
```
Upgrade the forwardlane_advisor Node.js application from legacy 0.10.x to Node.js 20 LTS.

Steps:
1. Update package.json engines field to "node": ">=20.0.0"
2. Update Dockerfile base image from legacy node to node:20-alpine
3. Run npm audit and fix all critical/high severity vulnerabilities
4. Update npm packages that require Node 20+:
   - Replace callback-style async code with async/await where evident
   - Test that app starts: node app.js
5. Fix any deprecation warnings from Node 20
6. Update .nvmrc or .node-version file
7. Verify Procfile and pm2.json work with new Node version

Focus on making the app boot cleanly first before addressing other issues.
```

## Acceptance Criteria
- [ ] App starts without errors on Node 20
- [ ] No critical npm audit vulnerabilities
- [ ] Dockerfile uses Node 20 base image
- [ ] package.json engines updated

## Dependencies
None — do this first

## Estimated Effort
2-3 days
