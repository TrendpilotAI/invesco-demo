# TODO-831: Delete Duplicate src/ Directory

**Repo**: signal-studio-frontend  
**Priority**: P0  
**Effort**: S (4h)  
**Status**: pending

## Description
The `src/` directory (46 TS/TSX files) duplicates `app/`, `components/`, and `lib/`. This creates confusion about which files are canonical and may cause build issues.

## Coding Prompt
```
1. Compare src/app/ with app/: diff -r app/ src/app/
2. Compare src/components/ with components/: diff -r components/ src/components/
3. Identify any files in src/ that are NOT in the primary dirs
4. Merge any unique logic into the primary directories
5. Delete src/ entirely: git rm -r src/
6. Verify build: pnpm build && pnpm lint
7. Verify no import paths reference src/: grep -r "from.*src/" app/ components/ lib/
```

## Acceptance Criteria
- `src/` directory no longer exists
- `pnpm build` passes with no errors
- No import paths reference `src/`
- All tests pass
