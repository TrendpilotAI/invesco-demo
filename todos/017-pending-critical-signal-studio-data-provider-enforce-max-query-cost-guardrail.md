---
status: pending
priority: p1
issue_id: "017"
tags: [python, snowflake, cost-control, signal-studio-data-provider]
dependencies: ["016"]
---

# Enforce max_query_cost Guardrail in SnowflakeProvider

## Problem Statement

`OrgConfig` defines `max_query_cost: float = 1.0` (Snowflake credits) but `SnowflakeProvider` never checks this value. The `_total_credits` counter is correctly incremented per query, but there is no enforcement: an org can burn unlimited Snowflake credits through Signal Studio. For enterprise clients like Invesco who are cost-sensitive, this is a contractual risk and could result in large unexpected bills.

## Findings

**Config defines the field:**
```python
class OrgConfig(BaseModel):
    ...
    max_query_cost: float = 1.0  # Snowflake credits
```

**Provider tracks credits but never checks:**
```python
# In execute_query():
cost = elapsed / 60_000  # very rough
self._total_credits += cost
# ← NO check against self._config.max_query_cost
```

**Impact:**
- An org can execute thousands of queries, accumulating unlimited credits
- No alerting, no soft cap, no hard cap
- Billing disputes with enterprise clients who expect spend guardrails
- The feature is documented (via config field) but is a hollow promise

## Proposed Solutions

### Option A: Hard Cap — Raise Exception When Limit Exceeded
```python
if self._total_credits + cost > self._config.max_query_cost:
    raise QueryCostExceededError(
        f"Query would exceed max_query_cost of {self._config.max_query_cost} credits "
        f"(current: {self._total_credits:.4f})"
    )
```

### Option B: Soft Cap — Warn and Log, Don't Raise
Log a warning when 80% of budget is consumed, raise at 100%.

### Option C: Per-Query Cap — Check Before Executing
Estimate cost before execution using `EXPLAIN` or query metadata, raise if projected cost exceeds per-query limit.

### Recommended: Option A + Pre-query total check
Check cumulative credits before executing. Raise `QueryCostExceededError` (a new exception class) when limit would be exceeded. Add a `reset_cost_tracking()` method to allow periodic resets (e.g., per billing cycle).

## Acceptance Criteria

- [ ] New exception class `QueryCostExceededError` defined in `providers/base.py` or `exceptions.py`
- [ ] `execute_query()` raises `QueryCostExceededError` when `_total_credits + cost > max_query_cost`
- [ ] `reset_cost_tracking()` method resets `_total_credits` to 0.0
- [ ] Test `test_max_query_cost_raises_when_exceeded` verifies exception is raised
- [ ] Test `test_max_query_cost_not_raised_when_under_limit` verifies normal operation
- [ ] Test `test_reset_cost_tracking` verifies counter resets to 0
- [ ] Exception message includes current credit usage and configured limit
- [ ] Warning logged at 80% budget consumption

## Coding Prompt

```
TASK: Enforce max_query_cost guardrail in SnowflakeProvider in signal-studio-data-provider.

REPO: /data/workspace/projects/signal-studio-data-provider/

FILES TO MODIFY:
  - providers/base.py (add QueryCostExceededError)
  - providers/snowflake_provider.py
  - tests/test_providers.py

CHANGES:

1. In providers/base.py, add exception class:
   class QueryCostExceededError(Exception):
       """Raised when a query would exceed the org's configured max_query_cost."""
       pass

2. In SnowflakeProvider.execute_query(), add check AFTER cost calculation:
   cost = elapsed / 60_000
   if self._total_credits + cost > self._config.max_query_cost:
       raise QueryCostExceededError(
           f"Query cost {cost:.6f} credits would exceed limit "
           f"{self._config.max_query_cost} credits "
           f"(accumulated: {self._total_credits:.6f})"
       )
   self._total_credits += cost

3. Add warning at 80% threshold (before raising):
   if self._total_credits >= self._config.max_query_cost * 0.8:
       import logging
       logging.getLogger(__name__).warning(
           "SnowflakeProvider: %s has used %.1f%% of max_query_cost budget",
           self._config.org_id,
           (self._total_credits / self._config.max_query_cost) * 100
       )

4. Add reset method:
   def reset_cost_tracking(self) -> None:
       self._total_credits = 0.0

5. Add tests:
   - test_max_query_cost_raises: set max_query_cost=0.001, run query with mocked 
     elapsed=100000ms (100s), verify QueryCostExceededError raised
   - test_max_query_cost_not_raised: set high limit, verify normal execution
   - test_reset_cost_tracking: accumulate credits, call reset, verify 0.0
   - test_cost_warning_at_80_pct: mock logger, verify warning emitted at threshold

IMPORTANT: Import QueryCostExceededError in __init__.py for public access.
```

## Dependencies

- `["016"]` — fix param bug first so tests run correctly

## Estimated Effort

S (hours)

## Work Log

### 2026-02-26 — Initial triage

**By:** Planning Agent

**Actions:**
- Confirmed max_query_cost is defined in OrgConfig but never enforced in SnowflakeProvider
- Identified _total_credits is tracked correctly, just needs comparison logic
- Designed exception class approach for clean error handling by callers

**Learnings:**
- The cost estimate (elapsed/60000) is very rough (assumes XS warehouse); long-term should use Snowflake's QUERY_HISTORY table for actual credit consumption
- A reset mechanism is needed for per-billing-period caps (monthly, weekly)
