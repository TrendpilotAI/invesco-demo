# TODO 100 — Fix SQL Quoted Placeholder Bug (P0 CRITICAL)

**Repo:** signal-studio-templates  
**Priority:** P0 — Ship today  
**Effort:** S (2-4 hours)  
**Status:** pending

---

## Problem

`parameterizeLegacyTemplate` replaces `{{key}}` with `$N` positional params, but SQL templates wrap placeholders in single quotes: `'{{territory_id}}'`. After replacement: `'$1'` — a literal string, not a param. All optional filters silently no-op. INTERVAL queries throw runtime errors.

**30+ affected locations across 15 files.**

---

## Autonomous Coding Prompt

```
Fix the SQL quoted placeholder bug in /data/workspace/projects/signal-studio-templates/.

PROBLEM: SQL templates use '{{key}}' with surrounding quotes. After parameterizeLegacyTemplate
runs, this becomes '$1' (literal string), not a bound parameter. All optional filters
(territory_id, advisor_id, product_id, etc.) silently return wrong results.

STEPS:

1. In each template file below, find every occurrence of '{{key}}' (with quotes) and
   remove the surrounding single quotes so the placeholder is unquoted: {{key}}.
   
   Files to fix:
   - templates/sales-intelligence/dormant-relationships.ts (line 38)
   - templates/sales-intelligence/territory-pulse.ts (lines 32, 38, 45, 53)
   - templates/sales-intelligence/best-shots-on-goal.ts (line 45)
   - templates/sales-intelligence/product-fit-scorer.ts (lines 28, 52)
   - templates/meeting-prep/meeting-brief.ts (line 64)
   - templates/meeting-prep/recent-activity-digest.ts (lines 35, 42)
   - templates/meeting-prep/competitive-landscape.ts (lines 42, 44, 45)
   - templates/meeting-prep/relationship-health.ts (line 46)
   - templates/risk-compliance/concentration-risk.ts (line 40)
   - templates/risk-compliance/suitability-check.ts (lines 41, 43)
   - templates/risk-compliance/risk-drift-alert.ts (lines 39, 40)
   - templates/risk-compliance/rmd-life-events.ts (line 48)
   - templates/management/pipeline-health.ts (lines 37, 38)
   - templates/management/wholesaler-scorecard.ts (line 48)
   - templates/management/regional-benchmark.ts (line 66)
   - templates/product-marketing/competitive-displacement.ts (lines 50, 51, 56)
   - templates/product-marketing/product-adoption-tracker.ts (lines 40, 55, 56)
   - templates/product-marketing/campaign-target-list.ts (lines 41-47, 53)
   - templates/product-marketing/cross-sell-recommender.ts (line 27)

2. Fix INTERVAL syntax. Change:
   INTERVAL '{{period_days}} days'  →  ({{period_days}} || ' days')::interval
   INTERVAL '{{days}} days'         →  ({{days}} || ' days')::interval
   INTERVAL '{{lookback_months}} months' → ({{lookback_months}} || ' months')::interval
   INTERVAL '1 {{period}}'          →  ({{period}})::text (use DATE_TRUNC with the param directly)
   
   Note: after parameterization, these become ($1 || ' days')::interval which is valid PG.

3. Add a regression test in __tests__/sql-safety.test.ts:
   - Test that generateSQL() for dormant-relationships with territory_id='TX' produces
     SQL with '$1' as a positional param (not literal string '$1' inside quotes)
   - Test that the params array contains 'TX', not '$1'

4. Run: cd /data/workspace/projects/signal-studio-templates && pnpm test
   All tests must pass.

5. Run: pnpm typecheck
   Must pass with no errors.
```

---

## Acceptance Criteria
- [ ] No `'{{` pattern exists in any template SQL string
- [ ] All `INTERVAL '{{` patterns fixed to use cast approach
- [ ] Regression test added and passes
- [ ] `pnpm test` passes
- [ ] `pnpm typecheck` passes

## Dependencies
None — this is a standalone fix.
