# TODO 105 — Add 5 Complex-Tier Templates (P2)

**Repo:** signal-studio-templates  
**Priority:** P2  
**Effort:** M (2-3 days)  
**Status:** pending

---

## Autonomous Coding Prompt

```
Add 5 new "advanced" complexity templates to /data/workspace/projects/signal-studio-templates/

Use existing templates as reference for structure (see dormant-relationships.ts for pattern).
Follow the SignalTemplate schema in schema/signal-template.ts exactly.

TEMPLATES TO CREATE:

1. templates/sales-intelligence/aum-velocity-tracker.ts
   id: "aum-velocity-tracker"
   name: "AUM Velocity Tracker"
   description: "Advisors with accelerating or decelerating AUM over rolling periods. Spot momentum before it peaks or reverses."
   complexity: "advanced"
   requiredDataSources: ["holdings", "crm", "transactions"]
   Parameters: period_days (90), territory_id (optional), velocity_threshold (10 = ±10% change)
   SQL: Compare AUM at t-0 vs t-period_days vs t-2*period_days, calculate velocity and acceleration

2. templates/meeting-prep/portfolio-overlap-analyzer.ts
   id: "portfolio-overlap-analyzer"
   name: "Portfolio Overlap Analyzer"
   description: "How much does this advisor's book overlap with our product lineup? Find whitespace for new allocations."
   complexity: "advanced"
   requiredDataSources: ["holdings", "product-catalog"]
   Parameters: advisor_id (required), min_position_value (100000)
   SQL: LEFT JOIN advisor holdings against product catalog, compute overlap percentage by asset class

3. templates/risk-compliance/multi-advisor-risk-dashboard.ts
   id: "multi-advisor-risk-dashboard"
   name: "Multi-Advisor Risk Dashboard"
   description: "Aggregate risk metrics across an entire territory or book of business. Spot systemic risk patterns."
   complexity: "advanced"
   requiredDataSources: ["holdings", "crm", "compliance"]
   Parameters: territory_id (optional), risk_threshold (0.15), min_aum (1000000)

4. templates/product-marketing/product-correlation-matrix.ts
   id: "product-correlation-matrix"
   name: "Product Correlation Matrix"
   description: "Which products are bought together? Find the strongest co-purchase signals for cross-sell."
   complexity: "advanced"
   requiredDataSources: ["transactions", "holdings", "product-catalog"]
   Parameters: product_id (required), lookback_months (12), min_correlation_count (5)

5. templates/management/territory-heat-map.ts
   id: "territory-heat-map"
   name: "Territory Heat Map"
   description: "Visual breakdown of revenue, activity, and pipeline health by territory. Spot underperforming regions."
   complexity: "advanced"
   requiredDataSources: ["crm", "holdings", "pipeline", "interactions"]
   Parameters: period_days (90), metric (select: aum|revenue|activity|pipeline)

After creating templates, add them to templates/index.ts exports.
Update __tests__/templates.test.ts to expect 25 templates (not 20).
Run pnpm test to verify.
```

## Acceptance Criteria
- [ ] 5 new advanced templates created
- [ ] All follow SignalTemplate schema exactly (id, name, description, sqlTemplate, outputSchema, etc.)
- [ ] Added to templates/index.ts
- [ ] Test updated and passing (25 templates)
- [ ] exampleOutput included for each template

## Dependencies
- TODO 100 (fix quoted params before writing new templates — use correct pattern)
