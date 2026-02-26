---
status: pending
priority: p1
issue_id: "208"
tags: [security, dependencies, npm-audit, signal-builder-frontend]
dependencies: []
---

# 208 — Dependency Vulnerability Audit + Upgrade

## Problem Statement

Several dependencies are pinned at potentially outdated versions with known CVEs:
- `react-scripts: 5.0.1` — CRA 5.x has known webpack-dev-server CVEs
- `typescript: ^4.4.2` — TypeScript 4.4 is from 2021; 5.x is current
- `reactflow: ^11.5.6` — v12 was released with breaking changes
- `@reduxjs/toolkit: ^1.9.1` — v2.x is available

The `yarn audit` command has never been run in CI (no step in bitbucket-pipelines.yml), meaning CVEs may have accumulated silently.

## Findings

From `package.json`:
- `"typescript": "^4.4.2"` — Current: 5.x (major version behind)
- `"react-scripts": "5.0.1"` — CRA is effectively deprecated (Vite migration recommended long-term)
- `"@reduxjs/toolkit": "^1.9.1"` — v2.x released with improved type inference
- `"reactflow": "^11.5.6"` — v12 released
- `"storybook"` packages: all at `^6.5.x` — v7 and v8 released
- `"msw": "^2.1.5"` — v2 is current ✅
- `"axios": "^1.3.4"` — v1.x ✅

## Proposed Solutions

### Option A: Audit + fix High/Critical CVEs only (Quick win)
Run `yarn audit`, identify High/Critical findings, upgrade only those packages.
- **Pros:** Low risk, targeted
- **Effort:** S (~2-3h)
- **Risk:** Low

### Option B: Full upgrade to latest compatible versions
Run `npx npm-check-updates -u` and upgrade everything.
- **Pros:** Maximal freshness
- **Cons:** High risk of breaking changes
- **Effort:** XL
- **Risk:** High

## Recommended Action

Option A first. Document findings. Create separate TODOs for major version upgrades (RTK v2, TypeScript v5, Storybook v7).

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Audit and fix dependency vulnerabilities

1. Run yarn audit and capture output:
   cd /data/workspace/projects/signal-builder-frontend
   yarn audit --level moderate 2>&1 | tee /tmp/audit-results.txt
   cat /tmp/audit-results.txt

2. For each High or Critical vulnerability:
   a. Identify the package and the fixed version
   b. Update package.json with the patched version
   c. Run yarn install
   d. Run yarn typecheck to verify no type regressions
   e. Run yarn test --watchAll=false to verify no test regressions

3. Fix resolutions for transitive dependency CVEs in package.json:
   "resolutions": {
     "package-with-cve": "^safe-version"
   }
   (yarn supports "resolutions" field for transitive fixes)

4. Upgrade patch/minor versions for security:
   yarn upgrade --latest --pattern "@testing-library/*"
   yarn upgrade --latest --pattern "axios"
   
5. Run yarn audit again to verify High/Critical count is 0:
   yarn audit --level high

6. Add yarn audit to bitbucket-pipelines.yml as a non-blocking step:
   - step:
       name: Security Audit
       script:
         - yarn install
         - yarn audit --level high || true  # warn but don't fail initially
   
   (Use "|| true" initially; remove after all highs are resolved)

7. Document findings in a comment at the top of package.json or a SECURITY.md file:
   List: date audited, CVEs found, CVEs resolved, known acceptable risks

8. Verify the build still works:
   yarn build 2>&1 | tail -5
```

## Dependencies

None — security audit should run first.

## Estimated Effort

**Small** — 2-3 hours

## Acceptance Criteria

- [ ] `yarn audit --level high` reports 0 High or Critical vulnerabilities
- [ ] `yarn audit` step added to `bitbucket-pipelines.yml`
- [ ] `yarn typecheck` still passes after upgrades
- [ ] `yarn test --watchAll=false` still passes after upgrades
- [ ] `yarn build` still succeeds
- [ ] Audit findings are documented (SECURITY.md or package.json comment)
- [ ] Package.json `resolutions` field used for transitive CVE overrides if needed

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Identified 4 potentially outdated packages from package.json review
- Confirmed no yarn audit step exists in CI pipelines
- Recommended incremental approach (High/Critical first, then major version upgrades separately)
