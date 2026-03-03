# Distribution Intelligence — Generic Demo Mapping

## From Invesco-Specific → Any Asset Manager

The Invesco implementation is the reference architecture. Here's how every signal maps to a generic, white-label version any asset manager can deploy.

---

## The 10 Signals — Generic Version

### 1. Upsell Opportunity (Score 1-10)
**Invesco:** `upsell_opportunity_score` — Advisors already buying Invesco who could buy more. Predicted net sale amount + strategy recommendations.

**Generic:** "Your advisor bought $X in the last 3 months and has capacity for $Y more in these strategies: [fund recommendations]"

**Data required:** Trailing 3-6 month net sales per advisor, product holdings, capacity model
**ML model:** Regression on historical purchase patterns → predicted additional net sale

---

### 2. Cross-Sell / Takeover Opportunity (Score 1-10)
**Invesco:** `cross_sell_opportunity_score` — Competitor AUM the advisor holds that could shift to Invesco strategies.

**Generic:** "Your advisor has $X in competitor [Category] strategies. Takeover opportunity: $Y across [recommended funds]"

**Data required:** Advisor book composition (your products vs. competitor products), category-level AUM
**ML model:** Category affinity + competitive displacement probability

---

### 3. Strategic Opportunity (Score 1-10)
**Invesco:** `strategic_opportunity_score` — Advisor is the target audience for specific strategic initiatives (new fund launches, thematic pushes).

**Generic:** "This advisor matches your target profile for [Campaign/Product Launch]. Strategy fit: [list of aligned strategies]"

**Data required:** Advisor segment, investment style, client demographics → campaign targeting criteria
**ML model:** Audience clustering + strategy-advisor fit scoring

---

### 4. Defend Revenue / Assets at Risk (Score 1-10)
**Invesco:** `defend_revenue_opportunity_score` — AUM at risk of leaving with fund-level detail.

**Generic:** "ALERT: $X AUM at risk across [funds]. Recommend defensive action on [specific positions]"

**Data required:** AUM trend (declining), redemption patterns, competitive inflows
**ML model:** Attrition prediction + fund-level risk scoring

---

### 5. Distressed AUM (Score 1-10)
**Invesco:** `distressed_aum_score` — AUM that eroded from peak. Shows peak asset, current asset, % drop, eroded amount, and fund-level detail.

**Generic:** "Advisor's AUM dropped X% from peak ($Y → $Z). $W eroded across [funds]. Recovery potential: [recommendations]"

**Data required:** Historical AUM time series, peak detection
**ML model:** Trend analysis + recovery probability

---

### 6. Buying Pattern Change (Score 1-10)
**Invesco:** `buying_pattern_change_score` — Shifts in model usage, concentration, ETF allocation.

**Generic:** "Behavioral shift detected: Advisor moved from [old pattern] → [new pattern]. Implications: [actionable insight]"

**Data required:** Time-series behavioral features (model portfolio usage, product concentration, vehicle mix)
**ML model:** Change-point detection + behavioral clustering

---

### 7. Rising Stars ⭐ (Score 4-10)
**Invesco:** Trailing 12-month gross sales increase $100K-$5M+. Scored by magnitude.

**Generic:** "RISING STAR: Advisor increased purchases by $X over trailing 12 months. MF: +$Y, ETF: +$Z"

**Score matrix (directly reusable):**
| Score | Sales Increase |
|-------|---------------|
| 4 | $100K - $250K |
| 5 | $250K - $500K |
| 6 | $500K - $750K |
| 7 | $750K - $1M |
| 8 | $1M - $2.5M |
| 9 | $2.5M - $5M |
| 10 | $5M+ |

**Data required:** Trailing 12-month buy amounts, year-over-year comparison
**ML model:** Simple rules-based (no ML needed — direct calculation)

---

### 8. Fallen Angels 👼 (Score 4-10)
**Invesco:** Trailing 12-month gross sales DECREASE $100K-$5M+. Same score matrix, inverted.

**Generic:** "FALLEN ANGEL: Advisor decreased purchases by $X over trailing 12 months. Engagement urgently needed."

**Data required:** Same as Rising Stars, opposite direction
**ML model:** Rules-based (inverse of Rising Stars matrix)

---

### 9. RIA Opportunity (Score 1-10)
**Invesco:** `ria_opportunity_score` — For RIA channel: custodian, total AUM, vehicle types, greenspace tickers.

**Generic:** "RIA Intelligence: [Firm] has $X AUM at [Custodian]. Currently using [vehicle types]. Greenspace opportunity in [product categories/tickers you offer but they don't hold]"

**Data required:** RIA 13F filings, ADV data, custodian relationships, product holdings
**ML model:** Greenspace analysis (your catalog minus their holdings = opportunity)

---

### 10. Overall Opportunity Score (Composite)
**Invesco:** `opportunity_score` — Weighted composite of all signals above.

**Generic:** Single number (1-10) summarizing total opportunity. Drives the call queue / daily priority list for wholesalers.

**Weighting (configurable per client):**
- Upsell: 20%
- Cross-sell: 20%
- Rising Star: 15%
- Defend: 15%
- Strategic: 10%
- RIA: 10%
- Buying Pattern: 5%
- Distressed: 5%

---

## Data Integration — What Each Client Needs to Provide

### Minimum Viable (4-6 week deployment)
| Data | Format | Signals Enabled |
|------|--------|----------------|
| Advisor book data (positions/AUM by advisor) | CSV/SFTP monthly | Upsell, Cross-sell, Defend, Distressed |
| Trailing sales data (buys/sells by advisor, monthly) | CSV/SFTP monthly | Rising Stars, Fallen Angels |
| Product catalog (your funds/strategies) | One-time CSV | Strategic, Cross-sell |

### Full Deployment (8-12 week)
| Data | Format | Signals Enabled |
|------|--------|----------------|
| All above + | | |
| RIA 13F/ADV data (we can source) | API/bulk | RIA Opportunity |
| CRM/engagement data | API | Buying Pattern Change |
| Campaign targeting criteria | Config | Strategic Opportunity |
| Competitor product mapping | One-time | Cross-sell precision |

### Morgan Stanley–Level (Invesco reference)
| Data | Signals |
|------|---------|
| MF Book Data (50+ columns per advisor) | Full MF ranking + category AUM |
| ETF Book Data (50+ columns) | Full ETF ranking |
| SMA Book Data (UMA, fiduciary, consulting) | SMA opportunity |
| UIT Book Data (prior year + current) | UIT trend analysis |
| Rank Data (Invesco % of book, FA book rank) | Competitive positioning |
| DataScienceRecommendation (ML output, 40+ fields) | All 10 signals |

---

## Demo Script — "Distribution Intelligence in 5 Minutes"

### Screen 1: Wholesaler Dashboard
> "Good morning. Your territory has 847 advisors. Here are today's top 10 priorities."

Show ranked list: Advisor name, firm, composite score, top signal icon (🌟⚠️💰🎯)

### Screen 2: Rising Star Deep-Dive
> "Sarah Chen at Raymond James — Score 9/10. Her MF purchases are up $3.2M trailing 12 months. She's your hottest advisor."

Show: trend chart, fund-level breakdown, recommended talking points

### Screen 3: Fallen Angel Alert
> "Mark Williams at UBS — Score 8/10 Fallen Angel. ETF purchases down $1.8M. He was a top-10 advisor last year."

Show: decline chart, at-risk funds, suggested defensive actions, competitor analysis

### Screen 4: Cross-Sell Opportunity
> "Jennifer Park at Merrill — Score 7/10 Takeover. She has $4.2M in competitor fixed income strategies. Your [Fund X] has outperformed by 180bps. Here's the pitch."

Show: competitor displacement analysis, fund comparison, one-click email template

### Screen 5: RIA Greenspace
> "Apex Wealth Management — Score 8/10. $340M AUM, uses Schwab as custodian, heavy in equities. Zero allocation to your alternatives suite. Greenspace: $15-25M potential."

Show: RIA profile, current holdings, gap analysis, recommended products

### Screen 6: One-Click Actions
> "For each advisor, you can: Generate meeting prep brief | Send personalized email | Log call notes | Set follow-up reminder"

**Craig Lieb quote (Invesco):** "I want easy buttons for my wholesalers. One click to prep for a meeting. One click to send the right content."

---

## Pricing Model (Suggested)

| Tier | Signals | Advisors | Annual Price |
|------|---------|----------|-------------|
| **Starter** | Rising Stars + Fallen Angels + Overall Score | Up to 5,000 | $150K/yr |
| **Professional** | All 10 signals | Up to 25,000 | $300K/yr |
| **Enterprise** | All signals + custom models + API access | Unlimited | $500K+/yr |

*Invesco is at ~Professional tier ($300K). Expanding to Enterprise with NL→SQL and custom signals.*

---

## Implementation Timeline

| Week | Milestone |
|------|-----------|
| 1-2 | Data integration kickoff; schema mapping |
| 3-4 | Data pipeline live; Rising Stars + Fallen Angels scoring |
| 5-6 | Full 10-signal scoring; QA with client distribution team |
| 7-8 | UI deployment; wholesaler training; soft launch |
| 9-12 | Full rollout; custom model tuning; NL→SQL enablement |

---

## Key Differentiators vs. Generic CRM/BI

1. **Book data native** — We don't do generic "intent signals." We ingest actual position-level data and score opportunities from real AUM.
2. **10 ML-driven signals** — Not dashboards. Not reports. Actionable scores that drive the daily call queue.
3. **Proven at $2.2T AUM scale** — Live with Invesco's Morgan Stanley channel. 200+ columns, 22 tables, 30+ business rules.
4. **4-6 week deployment** — Not a 12-month integration project. We map to your data fast.
5. **NL→SQL** — Your distribution head can ask "show me all rising stars in the Southeast with >$1M increase" in plain English.
