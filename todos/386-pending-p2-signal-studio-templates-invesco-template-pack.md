# TODO 386: Signal Studio Templates — Invesco-Specific Template Pack

**Priority:** P2  
**Repo:** signal-studio-templates  
**Effort:** L (3-5 days)  
**Status:** pending

---

## Description

Add 5 Invesco-specific signal templates that go beyond the generic 20 templates and directly address Invesco's distribution and sales workflows. These templates are the highest direct revenue value feature — they make Signal Studio uniquely valuable to Invesco and strengthen the contract renewal case.

## Why This Matters

The current 20 templates are generic financial advisor templates. Invesco's key value prop is that Signal Studio "knows" their fund family, product catalog, and distribution model. Custom templates make this concrete.

## Coding Prompt (Autonomous Execution)

```
Add 5 new templates to /data/workspace/projects/signal-studio-templates/templates/invesco/:

1. invesco-fund-performance.ts
   - SQL: join advisor holdings against Invesco fund catalog, compare YTD performance vs benchmark
   - Parameters: fund_family (select), period (select: YTD/1Y/3Y/5Y), min_aum
   - Output: advisor_name, fund_name, aum, ytd_return, benchmark_return, vs_benchmark, outperformance_flag
   - Talking points: "Fund X outperformed benchmark by Y% — strong retention talking point"

2. invesco-redemption-risk.ts
   - SQL: score advisors by redemption likelihood (underperformance + no recent contact + market downturn)
   - Parameters: risk_threshold (number 0-100), lookback_days
   - Output: advisor_name, aum_at_risk, risk_score, last_contact_days, fund_performance_delta, recommended_action
   - Talking points: "High risk — schedule call within 48 hours, lead with performance recovery narrative"

3. invesco-flows-summary.ts
   - SQL: aggregate net flows by territory, product line, and time period
   - Parameters: period (select: WTD/MTD/QTD/YTD), territory_id, product_line
   - Output: territory_name, product_line, gross_inflows, gross_outflows, net_flows, vs_prior_period_pct
   - Talking points: Management-ready summary of flow trends

4. invesco-competitive-wins.ts
   - SQL: identify advisors who moved assets from competitor funds into Invesco in last N days
   - Parameters: lookback_days, min_amount
   - Output: advisor_name, from_fund_family, to_invesco_fund, amount_moved, date, relationship_tenure_years
   - Talking points: "Congratulate and deepen relationship — ask for referrals"

5. invesco-distribution-readiness.ts
   - SQL: monthly distribution schedule for Invesco funds + advisor notification status
   - Parameters: month (date), fund_family, min_distribution_amount
   - Output: fund_name, ex_date, distribution_amount_per_share, advisor_count, notified_count, pending_contact
   - Talking points: "Distribution coming on [date] — proactive client communication opportunity"

Create /data/workspace/projects/signal-studio-templates/templates/invesco/index.ts to export all 5.
Update /data/workspace/projects/signal-studio-templates/templates/index.ts to include invesco templates.
Add integration tests in __tests__/invesco-templates.test.ts.
```

## Dependencies
- TODO 100 (SQL injection fix) should be completed first
- Uses same SignalTemplate schema as existing templates

## Acceptance Criteria
- [ ] 5 new template files created under `templates/invesco/`
- [ ] All templates exported from `templates/index.ts`
- [ ] All templates pass `TemplateEngine.validateParameters()` with valid params
- [ ] SQL output contains no `{{variable}}` placeholders after generation
- [ ] Tests added for each template
- [ ] README updated with Invesco template section
