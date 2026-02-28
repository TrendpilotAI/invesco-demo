# 234 · P1 · signal-builder-frontend · Dependency Security Audit + Quick Wins

## Status
pending

## Priority
P1 — react-scripts 5.0.1 has known CVEs; `uuidv4` deprecated; multiple stale packages

## Description
Multiple dependencies are flagged with CVEs or are deprecated. This task performs a full audit and fixes the quick wins (deprecated packages, easy upgrades) while scoping the larger CRA → Vite migration separately.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Run full audit and document findings
cd /data/workspace/projects/signal-builder-frontend
yarn audit 2>&1 | tee /tmp/audit-results.txt
npx npm-check-updates --format group 2>&1 | head -80

Step 2: Replace deprecated `uuidv4` with `uuid`
1. yarn remove uuidv4
2. yarn add uuid
3. yarn add -D @types/uuid
4. Find all usages: grep -rn "from 'uuidv4'\|require('uuidv4')" src/
5. Replace each:
   // Before: import { uuidv4 } from 'uuidv4';
   // After:  import { v4 as uuidv4 } from 'uuid';
6. Verify: yarn typecheck

Step 3: Remove/replace `compose-function` (last updated 2016)
1. Find usages: grep -rn "compose-function\|from 'compose-function'" src/
2. Replace with inline implementation or lodash/flowRight:
   // Option A (inline, zero-dep):
   const compose = <T>(...fns: Array<(arg: T) => T>) => (x: T) => fns.reduceRight((v, f) => f(v), x);
3. yarn remove compose-function

Step 4: Check jotai usage scope
grep -rn "from 'jotai'" src/ --include="*.ts" --include="*.tsx"
If ≤ 5 usages: plan to migrate to RTK (create separate TODO)
If unused: yarn remove jotai

Step 5: Pin react-scripts CVE workarounds via package.json resolutions
Add to package.json:
```json
"resolutions": {
  "nth-check": "^2.1.1",
  "postcss": "^8.4.31",
  "loader-utils": "^3.2.1"
}
```
Run: yarn install

Step 6: Add yarn audit to CI (see TODO 232)
If not already done, add to bitbucket-pipelines.yml security step:
  - yarn audit --level high

Step 7: Create upgrade tracking document
Write to /data/workspace/projects/signal-builder-frontend/DEPS-UPGRADE-PLAN.md:
- react-scripts → Vite (Major effort, own TODO)
- TypeScript 4.4 → 5.x (Medium effort, own TODO)
- Storybook 6 → 8 (Medium effort, dev-only)
- jotai 1 → 2 (if actively used)
- RTK 1.9 → 2.x (Medium effort, breaking changes)
- tanstack/react-query 4 → 5 (Medium, API changes)

Commit: "deps: replace uuidv4 with uuid, remove compose-function, pin CVE resolutions"
```

## Dependencies
- None (can run immediately)

## Effort Estimate
S (4–8 hours)

## Acceptance Criteria
- [ ] `uuidv4` removed from package.json
- [ ] `uuid` package added and all imports updated
- [ ] `compose-function` removed or confirmed not used
- [ ] CVE resolutions pinned in package.json
- [ ] `yarn audit --level high` returns no high/critical findings (or documented exceptions)
- [ ] `DEPS-UPGRADE-PLAN.md` created with upgrade roadmap
- [ ] `yarn build` and `yarn test` both pass
