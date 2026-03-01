# TODO-360: Update Jest to Fix glob HIGH CVE

**Priority:** P2
**Effort:** S
**Repo:** signal-studio
**Status:** pending

## Description
`jest > @jest/core > @jest/reporters > glob@10.x` has a HIGH CVE (command injection risk). Updating jest to latest pulls in patched glob@>=10.5.0.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Check current jest version: cat package.json | grep '"jest"'

2. Run npm audit to see current vulnerabilities:
   pnpm audit 2>&1 | head -50

3. Update jest and related packages:
   pnpm update jest @types/jest jest-environment-jsdom ts-jest --latest

4. Run test suite to verify nothing broke:
   pnpm test:ci 2>&1 | tail -20

5. Run pnpm audit again to confirm CVE resolved

6. Commit: "fix(deps): update jest to patch glob HIGH CVE in dependency chain"
```

## Dependencies
None

## Acceptance Criteria
- `pnpm audit` shows no HIGH or CRITICAL severity issues related to jest/glob
- All existing tests still pass
- `pnpm test:ci` exits 0
