# 10 Signal Ideas for Invesco Wholesalers

## 1. AUM Decline Alert
**Query:** Advisors with >15% YoY decline in Invesco AUM
**Trigger:** Weekly
**Action:** Personal outreach to understand concerns
**Data:** invesco_mf_book_data.invesco_current_assets vs prior year

## 2. Cross-Sell Opportunity (ETF → MF)
**Query:** High MF AUM but zero ETF holdings
**Trigger:** Monthly
**Action:** Introduce ETF solutions
**Data:** invesco_mf_book_data + invesco_etf_book_data

## 3. Defend Revenue Risk
**Query:** High defend_aum_m + declining trend
**Trigger:** Daily
**Action:** Urgent retention call
**Data:** customers_invesco_datasciencerecommendation.defend_aum_m

## 4. RIA Conversion Ready
**Query:** Independent advisors with high ria_opportunity_score
**Trigger:** Weekly
**Action:** RIA partnership pitch
**Data:** customers_invesco_datasciencerecommendation.ria_opportunity_score

## 5. Competitive Takeover
**Query:** Invesco AUM down but MSWM total stable = money going to competitors
**Trigger:** Weekly
**Action:** Competitive analysis call
**Data:** invesco_mf_book_data (Invesco vs MSWM comparison)

## 6. Dormant Account
**Query:** No CRM activity in 90+ days but significant AUM
**Trigger:** Weekly
**Action:** Re-engagement campaign
**Data:** t_crm_notes.date + t_holdings.amount

## 7. High Engagement, Low Penetration
**Query:** Many CRM interactions but low AUM share of wallet
**Trigger:** Monthly
**Action:** Deepen relationship
**Data:** t_crm_notes + invesco_mf_book_data

## 8. Product Concentration Risk
**Query:** >80% AUM in single product/fund
**Trigger:** Monthly
**Action:** Diversification conversation
**Data:** t_holdings by instrument_id

## 9. Transaction Trend Reversal
**Query:** Switched from net selling to net buying
**Trigger:** Daily
**Action:** Capitalize on momentum
**Data:** t_transactions (buy vs sell over time)

## 10. Segment-Specific Opportunity
**Query:** Advisors in "Wirehouse" segment with "High" opportunity_score
**Trigger:** Weekly
**Action:** Segment-specific pitch
**Data:** t_clients.segment + customers_invesco_datasciencerecommendation
