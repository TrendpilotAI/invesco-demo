# 483 — Resolve Dual State Management: Jotai v1 → v2 or Remove

**Priority:** P2  
**Repo:** signal-builder-frontend  
**Effort:** Medium (1-2 days)  
**Dependencies:** None

## Task Description
The app uses both Redux Toolkit (RTK) and Jotai v1 for state management. This creates cognitive overhead and bundle bloat. Either upgrade Jotai to v2 (breaking changes in atom API) or migrate all Jotai atoms to RTK slices and remove the dependency entirely.

## Coding Prompt
```
Audit and resolve dual state management in /data/workspace/projects/signal-builder-frontend/.

Step 1 — Audit Jotai usage:
  grep -r "atom\|useAtom\|useAtomValue" src/ --include="*.ts" --include="*.tsx" -l

Step 2 — Decide approach:
  If <10 files use Jotai → migrate to RTK and remove jotai package
  If >10 files use Jotai → upgrade to jotai v2 (breaking: atom() import, Provider optional)

Step 3A — If migrating to RTK:
  - Convert each atom to a slice or selector
  - Replace useAtom(xAtom) with useSelector(selectX) + useDispatch()
  - Remove jotai from package.json
  - Run yarn typecheck

Step 3B — If upgrading to jotai v2:
  yarn upgrade jotai@latest
  - Update imports: atom from 'jotai' (unchanged)
  - Update Provider usage (now optional)
  - Update atomWithStorage if used
  - Test all pages that use atoms

Step 4 — Document the state management convention in README.md:
  "Redux Toolkit for server state and global app state.
   [Jotai for local component trees / OR removed — all state in RTK]"
```

## Acceptance Criteria
- [ ] Single state management approach documented
- [ ] Either jotai removed OR upgraded to v2
- [ ] yarn typecheck passes
- [ ] All existing tests pass
- [ ] README updated with state management convention
