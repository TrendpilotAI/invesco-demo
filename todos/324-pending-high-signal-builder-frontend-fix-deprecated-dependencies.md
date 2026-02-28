# TODO-324: Fix Deprecated Dependencies — Signal Builder Frontend

**Priority:** P0 (High)
**Status:** Pending
**Project:** signal-builder-frontend
**Effort:** S (4 hours)
**Source:** PLAN.md → P0-002

---

## Task Description

Remove security risks from deprecated packages. Replace `uuidv4` with the native `crypto.randomUUID()` API, run a full `yarn audit` to patch high/critical CVEs, and pin `react-scripts` until the Vite migration is complete.

---

## Coding Prompt

```
You are working in the Signal Builder Frontend repo at /data/workspace/projects/signal-builder-frontend.

Fix deprecated and vulnerable dependencies:

1. Replace uuidv4:
   - Find all usages: `grep -r "uuidv4\|from 'uuid'" src/ --include="*.ts" --include="*.tsx" -l`
   - Replace every import of `uuidv4` or `uuid` with the native API:
     ```ts
     // Before
     import { v4 as uuidv4 } from 'uuid';
     const id = uuidv4();

     // After
     const id = crypto.randomUUID();
     ```
   - Remove the `uuid` / `uuidv4` package from package.json after all usages are gone:
     `yarn remove uuid uuidv4`
   - Note: crypto.randomUUID() is available in all modern browsers and Node 14.17+

2. Audit and patch CVEs:
   - Run: `yarn audit --level high`
   - For each high/critical vulnerability, check if a patched version exists
   - Use `yarn upgrade <package>@<safe-version>` for direct dependencies
   - For transitive vulnerabilities, add resolutions to package.json:
     ```json
     "resolutions": {
       "vulnerable-package": "^safe-version"
     }
     ```
   - Re-run audit until no high/critical CVEs remain (moderate is acceptable for now)

3. Pin react-scripts:
   - In package.json, change `"react-scripts": "x.x.x"` to an exact version (remove `^` or `~`)
   - This prevents accidental upgrades during the Vite migration window

4. Run `yarn build` to confirm nothing is broken.

5. Commit with message: "fix: replace uuidv4 with crypto.randomUUID, patch CVEs"
```

---

## Acceptance Criteria

- [ ] `uuidv4` / `uuid` package removed from `package.json`
- [ ] All usages replaced with `crypto.randomUUID()`
- [ ] `yarn audit --level high` returns zero high/critical vulnerabilities
- [ ] `react-scripts` pinned to exact version in `package.json`
- [ ] `yarn build` passes without errors
- [ ] `yarn test` (if tests exist) passes
