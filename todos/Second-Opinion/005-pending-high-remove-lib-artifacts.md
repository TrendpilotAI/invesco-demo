# TODO-005: HIGH — Remove Compiled lib/ Artifacts from Git

**Priority:** HIGH
**Status:** pending
**Category:** code_quality

## Problem
`functions/lib/` contains compiled `.js`, `.d.ts`, and `.js.map` files that are checked into Git. These should be build artifacts, not source-controlled.

## Fix
1. Add `functions/lib/` to `.gitignore`
2. Remove tracked files: `git rm -r --cached functions/lib/`
3. Ensure CI/deploy builds from source (`functions/src/`)

## Impact
Compiled artifacts in Git cause merge conflicts, stale builds, and repo bloat.

## Files
- `.gitignore`
- `functions/lib/` (remove from tracking)
