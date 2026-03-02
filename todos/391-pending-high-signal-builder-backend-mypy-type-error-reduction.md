# TODO-391: Reduce mypy Type Errors (307 → 0)

**Repo:** signal-builder-backend  
**Priority:** High  
**Status:** Pending  
**Created:** 2026-03-02  

## Description

After Pydantic v2 migration, mypy reports 307 type errors across apps/ and core/.
Top categories: `no-any-return` (52), `assignment` (47), `arg-type` (42), `attr-defined` (33), `name-defined` (32).
CI currently documents but doesn't block on mypy failures. This is technical debt that risks type regressions.

## Dependencies
- TODO-352: Pydantic v2 migration (partially done — types need cleanup)

## Execution Prompt

```
You are fixing mypy type errors in signal-builder-backend at /data/workspace/projects/signal-builder-backend/.

Current state: 307 mypy errors. Run `mypy apps/ core/ --ignore-missing-imports` to see them.

Approach:
1. Start with the highest-count categories:
   - `no-any-return` (52): Add explicit return types to functions returning Any
   - `assignment` (47): Fix type mismatches in variable assignments  
   - `arg-type` (42): Fix incorrect argument types in function calls
   - `attr-defined` (33): Fix undefined attribute access (often Optional chains)
   - `name-defined` (32): Fix undefined names (missing imports or typos)

2. For each fix:
   - Add explicit type annotations rather than suppressing with `# type: ignore`
   - Use `Optional[X]` instead of `X | None` for consistency with Python 3.11
   - Use `cast()` only when truly necessary
   - Prefer `assert isinstance(x, X)` to narrow types in business logic

3. Run mypy after each module to confirm fixes
4. Update CI threshold in mypy.ini: reduce `--allow-error-count` as errors decrease
5. Target: < 50 errors after first pass, 0 after second pass

Acceptance: `mypy apps/ core/` exits with 0 errors or CI threshold ≤ 10.
```

## Effort Estimate
- M (2-4 hours of focused work)

## Acceptance Criteria
- [ ] mypy exits with ≤ 10 errors
- [ ] CI mypy step blocks on new type regressions
- [ ] No new `# type: ignore` comments added without justification comment
