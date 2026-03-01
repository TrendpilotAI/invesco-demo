# TODO 353: Fix easy_button/models.py Schema Mismatch

**Repo:** forwardlane-backend  
**Priority:** HIGH  
**Effort:** S (1-2 hours)  
**Dependencies:** None

## Description

The Django models in `easy_button/models.py` do NOT match the actual `analytical` database schema. The models are never used (views use raw SQL), but they cause confusion and could mislead future developers.

**Mismatch examples:**
- `Advisor.id` (int) vs actual `advisor_id` (TEXT)
- `Advisor.name` vs actual `full_name`  
- `Advisor.segment` choices: Wirehouse/Independent/RIA vs actual channel: RIA/BD/Bank/Insurance
- `Holding.fund_ticker` vs actual `symbol`
- `Holding.weight` vs actual `pct_of_aum`
- `Holding.value` vs actual `aum_in_fund`

## Coding Prompt

```
You are working in /data/workspace/projects/forwardlane-backend/easy_button/models.py

Task: Update the unmanaged Django models to match the actual analytical database schema.

The actual schema (from views.py SQL queries) is:

advisors table:
  advisor_id TEXT (PK), full_name TEXT, firm_name TEXT, region TEXT,
  channel TEXT (RIA/BD/Bank/Insurance), aum_current BIGINT, aum_12m_ago BIGINT,
  client_count INT, avg_account_size BIGINT, email TEXT, phone TEXT,
  city TEXT, state TEXT, created_at TIMESTAMP, updated_at TIMESTAMP

holdings table:
  holding_id SERIAL (PK), advisor_id TEXT (FK), symbol TEXT, fund_name TEXT,
  fund_type TEXT (ETF/MF/ModelPortfolio), fund_family TEXT, aum_in_fund BIGINT,
  pct_of_aum DECIMAL, as_of_date DATE

flows table:
  flow_id SERIAL (PK), advisor_id TEXT (FK), symbol TEXT, flow_month DATE,
  net_flow BIGINT, gross_inflow BIGINT, gross_outflow BIGINT

signals table:
  signal_id SERIAL (PK), advisor_id TEXT (FK), signal_type TEXT,
  signal_score DECIMAL, signal_data JSONB, triggered_at TIMESTAMP, status TEXT

Steps:
1. Rewrite easy_button/models.py with correct field names/types
2. Mark all models as managed=False (they are in the analytical DB, not managed by Django)
3. Add appropriate db_table values and app_label = 'easy_button'
4. Add ForeignKey relationships between models with db_constraint=False (analytical DB)
5. Keep all Meta classes with managed=False

Do NOT create any migrations — these are unmanaged models.
Commit: "fix: update easy_button models to match analytical DB schema"
```

## Acceptance Criteria
- [ ] All model field names match actual column names
- [ ] No migrations created (managed=False throughout)
- [ ] Models are documented with docstrings
- [ ] Tests pass
