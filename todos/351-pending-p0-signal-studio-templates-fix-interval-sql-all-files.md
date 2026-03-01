# TODO 351: Fix SQL INTERVAL Pattern Across All 7 Template Files

**Repo:** signal-studio-templates  
**Priority:** P0 (Security + Correctness)  
**Effort:** S (2-3 hours)  
**Status:** pending

---

## Problem

17 occurrences across 7 template files use `INTERVAL '{{variable}} days'` which becomes `INTERVAL '$1 days'` after parameterization — **invalid PostgreSQL** that causes runtime crashes or potential SQL injection via future string-substitution code paths.

## Files to Fix

1. `templates/risk-compliance/risk-drift-alert.ts` line 39
2. `templates/risk-compliance/rmd-life-events.ts` line 46
3. `templates/management/wholesaler-scorecard.ts` lines 30, 31, 33, 40, 46
4. `templates/management/regional-benchmark.ts` lines 33, 38, 39
5. `templates/meeting-prep/meeting-brief.ts` lines 56, 62
6. `templates/meeting-prep/recent-activity-digest.ts` lines 36, 43
7. `templates/sales-intelligence/territory-pulse.ts` line 23

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates/, fix all INTERVAL SQL injection patterns.

For each file listed above, replace the pattern:
  INTERVAL '{{variable}} days'
with:
  ($N * INTERVAL '1 day')
where $N is the correct parameter index for that variable.

For month-based intervals in product-adoption-tracker.ts:
  INTERVAL '{{lookback_months}} months'
replace with:
  ($N * INTERVAL '1 month')

After fixing:
1. Run: cd /data/workspace/projects/signal-studio-templates && npx tsc --noEmit
2. Run: npm test
3. Verify no remaining INTERVAL patterns: grep -rn "INTERVAL '\\\$" templates/
```

## Acceptance Criteria

- [ ] Zero occurrences of `INTERVAL '$` in compiled output
- [ ] All templates pass TypeScript compilation
- [ ] All existing tests pass
- [ ] grep for `INTERVAL '{{` returns zero results

## Dependencies

None — standalone fix.
