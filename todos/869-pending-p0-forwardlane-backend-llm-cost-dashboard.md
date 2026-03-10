# FL-010: Multi-Tenant LLM Cost Dashboard

**Repo:** forwardlane-backend  
**Priority:** P0  
**Effort:** M (2-3 days)  
**Status:** pending

## Task Description
Add `completion_tokens` and `cost_usd` tracking to the existing LLM observability model, then surface per-tenant cost aggregates in Django admin and a client-facing API endpoint. Required for enterprise SOW transparency and internal cost management.

## Problem
We track `latency_ms` and `prompt_chars` in LLM observability, but have no visibility into:
- How many tokens each LLM call consumes
- What each call costs per provider (Gemini Flash vs Kimi)
- Per-tenant monthly LLM spend
Without this, we can't bill correctly, set quotas, or present transparent cost reports to enterprise clients.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Find the LLM observability model (likely in ai/models.py or libs/llm_client.py).
   Add fields:
   - completion_tokens = models.IntegerField(null=True, blank=True)
   - cost_usd = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
   - provider = models.CharField(max_length=50, blank=True)  # 'gemini' or 'kimi'
   Create migration.

2. Create ai/cost_tracker.py:
   # Cost constants per provider (per 1M tokens, as of 2026-03)
   PROVIDER_COSTS = {
       'gemini-flash': {'input': 0.075, 'output': 0.30},   # per 1M tokens
       'gemini-pro': {'input': 1.25, 'output': 5.00},
       'kimi': {'input': 0.15, 'output': 0.60},  # update with actual rates
   }

   def calculate_cost(provider: str, prompt_tokens: int, completion_tokens: int) -> Decimal:
       rates = PROVIDER_COSTS.get(provider, PROVIDER_COSTS['gemini-flash'])
       input_cost = (prompt_tokens / 1_000_000) * rates['input']
       output_cost = (completion_tokens / 1_000_000) * rates['output']
       return Decimal(str(input_cost + output_cost)).quantize(Decimal('0.000001'))

3. In libs/llm_client.py (or wherever LLM calls are made):
   - After each LLM response, extract completion_tokens from response metadata
   - Call calculate_cost() and save to observability model
   - Both Gemini and Kimi APIs return token counts in response body

4. Create ai/views/cost_views.py:
   - GET /api/v1/usage/costs/ — admin only
     Response: [{tenant_id, tenant_name, date, provider, total_calls, total_tokens, total_cost_usd}]
   - Filter by: tenant_id, date_from, date_to, provider
   - Aggregate using Django ORM: .values('tenant_id', 'provider', date=TruncDay('created_at')).annotate(...)

5. Add to Django admin:
   - LLMCostAdmin with columns: tenant, date, provider, calls, tokens, cost
   - Export as CSV button

6. Write tests in ai/tests/test_cost_tracker.py:
   - Test cost calculation for each provider
   - Test token extraction from mocked API responses
   - Test API endpoint returns correct aggregates

File changes:
- ai/models.py — add fields
- ai/migrations/XXXX_add_cost_fields.py — new
- ai/cost_tracker.py — new
- libs/llm_client.py — update to capture tokens and cost
- ai/views/cost_views.py — new
- ai/tests/test_cost_tracker.py — new
```

## Acceptance Criteria
- [ ] `completion_tokens` and `cost_usd` saved on every LLM call
- [ ] Both Gemini and Kimi providers tracked
- [ ] Admin view shows per-tenant, per-day cost aggregates
- [ ] API endpoint `/api/v1/usage/costs/` returns correct filtered data
- [ ] Unit tests for cost calculation pass
- [ ] Integration test mocks LLM response and verifies cost saved

## Dependencies
- None — builds on existing LLM observability model.
