// Mock data for Invesco Signal Studio demo
// All data is synthetic and fictional for demonstration purposes only

export interface Advisor {
  id: string
  advisorId: string
  name: string
  title: string
  firm: string
  firmType: string
  aum: number // in millions
  region: string
  channel: string
  city: string
  state: string
  engagementScore: number
  engagementDelta: number
  sentiment: string
  sentimentTrend: string
  lastContact: string
  lastContactDaysAgo: number
  meetingDate?: string
  meetingTime?: string
  signals: Signal[]
  talkingPoints: TalkingPoint[]
  meetingPrepBrief: string
  engagementBreakdown: EngagementBreakdown
  riskDriftAlert: RiskDriftAlert
  competitiveDisplacementScore: number
  competitiveDisplacementDetail: string
  opportunityScore: number
  nextBestAction: string
  allHoldings: Holding[]
  invescoRevenuePct: number
  aumGrowthRate: number
  revenueAnnual: number
  revenueFromInvesco: number
  clientCount: number
  avgClientAum: number
  keyNotes: string
  practiceFocus: string[]
  certifications: string[]
  email: string
  phone: string
  officeAddress: string
  relationshipManager: string
  netFlows: number
  topHoldings: string[]
  painPoints: string[]
  opportunities: string[]
  activities: Activity[]
  materials: Material[]
}

export interface Signal {
  id: string
  text: string
  severity: 'urgent' | 'attention' | 'positive' | 'info'
  metric?: string
  detail?: string
}

export interface TalkingPoint {
  id: string
  text: string
}

export interface EngagementBreakdown {
  crm_activity: number
  digital_engagement: number
  event_attendance: number
  content_consumption: number
  email_responsiveness: number
}

export interface RiskDriftAlert {
  status: 'ACTIVE' | 'ALERT' | 'MONITOR' | 'CLEAR'
  severity: 'high' | 'medium' | 'low' | 'none'
  detail: string
}

export interface Holding {
  fund_name: string
  ticker: string
  provider: string
  asset_class: string
  aum: number
  allocation_pct: number
  change_vs_prior_quarter_pct: string
  recommended_list: boolean
}

export interface Activity {
  date: string
  type: 'email' | 'call' | 'meeting' | 'task'
  description: string
}

export interface Material {
  id: string
  type: 'pitch-book' | 'factsheet' | 'report'
  title: string
  url: string
}

export interface TerritoryMetrics {
  totalAUM: number
  totalNetFlows: number
  avgEngagement: number
  advisorCount: number
  meetingsThisWeek: number
  signalsRequiringAction: number
}

function getSentiment(engagementScore: number): string {
  if (engagementScore >= 90) return 'Enthusiastic'
  if (engagementScore >= 75) return 'Positive'
  if (engagementScore >= 50) return 'Neutral'
  if (engagementScore >= 25) return 'Cautious'
  return 'At Risk'
}

function severityFromEngagement(score: number): Signal['severity'] {
  if (score >= 80) return 'positive'
  if (score >= 50) return 'info'
  if (score >= 25) return 'attention'
  return 'urgent'
}

// Raw advisor detail data (meeting prep, engagement, signals)
const advisorDetails = [
  {
    advisor_id: 'ADV-001',
    advisor_name: 'Dr. Sarah Chen',
    meeting_prep_brief: "Dr. Chen is mid-way through a strategic risk-off shift, moving ~$60M from equity to fixed income over the past 8 months. Invesco has captured $28M of this rotation (OPIGX, VFSTX). Three clients turning 73 in 2026 require RMD distribution plans — moderate withdrawal rate (4.5%) implemented using Invesco Income Advantage (SCAUX). She's adding $12M to SPLV for defensive positioning (executing this week). Next conversation: Invesco Balanced-Risk Allocation (ABRZX) for risk parity — $8M pipeline.",
    competitive_displacement_score: 35,
    competitive_displacement_detail: "Low displacement opportunity — Dr. Chen's non-Invesco holdings (Vanguard VTI, Fidelity FXAIX, BlackRock AGG, PIMCO PTTRX) are core index/passive positions unlikely to move. Better strategy: grow Invesco share of NEW allocations during risk-off shift.",
    risk_drift_alert: { status: 'ACTIVE' as const, severity: 'medium' as const, detail: 'Equity allocation dropped from 64% to 52% over 2 quarters — intentional risk-off shift. Fixed income up from 22% to 32%. Drift is deliberate and advisor-driven, not concerning.' },
    engagement_score: 82,
    engagement_breakdown: { crm_activity: 88, digital_engagement: 72, event_attendance: 65, content_consumption: 75, email_responsiveness: 83 },
    next_best_action: 'Close SPLV allocation ($12M) this week, then pivot conversation to ABRZX risk parity strategy. Prepare institutional-quality backtest comparing ABRZX vs traditional 60/40.',
    talking_points: [
      'SPLV execution: Confirm $12M allocation completing this week. Review entry point and expected volatility reduction — model shows 15% lower drawdown in stress scenarios.',
      'RMD check-in: Her 3 clients begin distributions this year. Review January/February distribution activity — are the 4.5% systematic withdrawals from SCAUX tracking as expected?',
      'ABRZX opportunity: Present Invesco Balanced-Risk Allocation backtested against her current 60/40 benchmark. Highlight the risk parity approach\'s performance during 2022 drawdown.',
      'Global Real Estate: She expressed interest in ARGYX at the January meeting. Share Q4 2025 performance data and position as inflation hedge.',
      'Attribution report: She requested quarterly custom attribution — confirm Q4 2025 report is ready.',
    ],
    invesco_revenue_pct: 28,
    aum_growth_rate_yoy: 8.5,
    revenue_annual: 450000,
    revenue_from_invesco: 126000,
    pain_points: ['Complex RMD planning for aging clients', 'Risk-off shift coordination', 'Attribution reporting needs'],
    opportunities: ['$8M ABRZX pipeline', '$12M SPLV allocation', 'Expanded fixed income sleeve'],
  },
  {
    advisor_id: 'ADV-002',
    advisor_name: 'Marcus Thompson',
    meeting_prep_brief: "Marcus is executing a multi-phase Vanguard Target Date displacement. Phase 1 (Acme Corp, $18M) completed successfully in Q4 2025. Phase 2: BetaCo ($15M) in final review, expected close March 2026. Phase 3: GammaTech ($12M) needs one more plan sponsor meeting. Total pipeline: $27M.",
    competitive_displacement_score: 88,
    competitive_displacement_detail: "HIGH opportunity. $27M in Vanguard Target Date funds across 2 remaining plans actively in displacement pipeline. Additional $35M in Vanguard Growth ETF (VUG) and $28M in iShares Russell 1000 Growth (IWF) could be targeted longer-term.",
    risk_drift_alert: { status: 'MONITOR' as const, severity: 'low' as const, detail: '78% equity allocation is significantly above peer average (58%). Not a drift — this is his intentional style for growth-oriented clients.' },
    engagement_score: 62,
    engagement_breakdown: { crm_activity: 72, digital_engagement: 45, event_attendance: 25, content_consumption: 40, email_responsiveness: 63 },
    next_best_action: 'Focus on closing BetaCo 401k displacement ($15M) by March 15 deadline. Offer to join GammaTech plan sponsor meeting.',
    talking_points: [
      'BetaCo close: Plan sponsor is in final review. Offer last-mile support — compliance documentation, participant communication templates, transition timeline. $15M should close by March 15.',
      'GammaTech strategy: Suggest joint meeting with plan sponsor. Having Invesco retirement specialist alongside Marcus could differentiate vs Vanguard\'s self-service approach.',
      'Acme Corp success story: Q4 transition went smoothly — use as proof point for BetaCo and GammaTech.',
      'QQQM vs QQQ positioning: Marcus has been adding QQQM for cost-conscious clients. Share updated expense ratio comparison and tax-efficiency data.',
      'Equity concentration: Gently raise the 78% equity allocation topic. Invesco Balanced-Risk or SPLV could provide downside protection.',
    ],
    invesco_revenue_pct: 22,
    aum_growth_rate_yoy: 5.2,
    revenue_annual: 280000,
    revenue_from_invesco: 61600,
    pain_points: ['Competitive pressure from Vanguard on 401k', 'Equity concentration risk', 'Limited event attendance'],
    opportunities: ['$27M Target Date displacement pipeline', 'QQQM systematic replacement', 'Equity risk management'],
  },
  {
    advisor_id: 'ADV-003',
    advisor_name: 'Jennifer Walsh',
    meeting_prep_brief: "Jennifer is an ESG-conviction investor consolidating holdings from 5 providers to Invesco as primary ESG partner. Since the October ESG Symposium, she's allocated $10M to Invesco ESG ETFs (TAN, PHO, ERTH). Now evaluating $8M green bond allocation via BAB.",
    competitive_displacement_score: 62,
    competitive_displacement_detail: "Moderate opportunity. $25M in iShares ESG Aware (ESGU), $18M in Parnassus, $15M in Calvert, $22M in Vanguard Social Index. Jennifer has already moved $8M from Calvert/iShares to Invesco.",
    risk_drift_alert: { status: 'CLEAR' as const, severity: 'none' as const, detail: 'No concerning drift. Allocation changes are intentional ESG consolidation moves.' },
    engagement_score: 78,
    engagement_breakdown: { crm_activity: 75, digital_engagement: 82, event_attendance: 90, content_consumption: 80, email_responsiveness: 92 },
    next_best_action: 'Close the $8M BAB green bond allocation this month. Then propose a co-marketing partnership.',
    talking_points: [
      'Green bond decision: Jennifer\'s reviewing the BAB analysis — follow up on $8M allocation. Highlight green muni tax advantages for her high-income clients.',
      'ESG impact reporting: She requested quarterly impact reports after the symposium. Confirm the format and first delivery date.',
      'Co-marketing opportunity: Jennifer has strong LinkedIn following (3K+ advisors). Propose co-authored ESG market commentary.',
      'Clean energy performance: TAN had a mixed 2025 — address proactively. Show long-term thesis and 2026 policy catalysts.',
      'Consolidation roadmap: Map out timeline for moving remaining Parnassus ($18M) and Calvert ($15M) positions.',
    ],
    invesco_revenue_pct: 18,
    aum_growth_rate_yoy: 15.3,
    revenue_annual: 180000,
    revenue_from_invesco: 32400,
    pain_points: ['ESG performance headwinds in 2025', 'Impact reporting complexity', 'Client reporting needs'],
    opportunities: ['$8M BAB allocation', '$33M consolidation from Parnassus/Calvert', 'Co-marketing partnership'],
  },
  {
    advisor_id: 'ADV-004',
    advisor_name: 'Robert Kim',
    meeting_prep_brief: "⚠️ URGENT RETENTION. Robert has been inactive for 90+ days (last contact Nov 14). $65M in Invesco holdings at risk with contract renewal in Q2 2026. He's evaluating BlackRock and PIMCO. Recent purchases: $5M to BlackRock Total Return, $3M to JP Morgan JEPI — signaling competitive shift.",
    competitive_displacement_score: 15,
    competitive_displacement_detail: "LOW — we are the ones being displaced. Robert is moving TOWARD BlackRock/PIMCO/JP Morgan, not away from them. Net flow from Invesco is negative ($3.5M outflows vs $0 inflows in last 6 months).",
    risk_drift_alert: { status: 'ALERT' as const, severity: 'high' as const, detail: 'RELATIONSHIP drift is severe. 90+ days of disengagement from a $520M advisor with $65M in Invesco products. Contract renewal in 4 months.' },
    engagement_score: 12,
    engagement_breakdown: { crm_activity: 15, digital_engagement: 8, event_attendance: 0, content_consumption: 5, email_responsiveness: 25 },
    next_best_action: 'ESCALATE IMMEDIATELY. Standard RM outreach has failed for 6+ months. Request regional director or head of distribution to make personal call.',
    talking_points: [
      'Acknowledge the gap: "Robert, I realize we haven\'t connected in months and that\'s on us. Your business is important to Invesco."',
      'Private credit bridge: He expressed interest in private credit 4 months ago. Lead with substance: our head of private credit for a dedicated 30-minute session.',
      'Contract renewal value case: Prepare total value delivered over contract period — performance attribution, service hours, client support events.',
      'BlackRock competitive response: Highlight Invesco differentiators: breadth of product, dedicated RM relationship, customization capabilities.',
      'JP Morgan reorganization: Position Invesco as a stable, reliable partner during uncertain times.',
    ],
    invesco_revenue_pct: 12,
    aum_growth_rate_yoy: -2.1,
    revenue_annual: 520000,
    revenue_from_invesco: 62400,
    pain_points: ['Disengaged from Invesco for 90+ days', 'Contract renewal risk', 'Competitive displacement from BlackRock'],
    opportunities: ['Contract renewal — $65M retention', 'Private credit interest', 'Re-engagement campaign'],
  },
  {
    advisor_id: 'ADV-005',
    advisor_name: 'Amanda Foster',
    meeting_prep_brief: "Amanda is our model advisor — literally. Highest Invesco wallet share (49.5%) in the territory, fastest growing practice (18.2% YoY), and deeply embedded in Invesco model portfolios on Envestnet. She's now at $340M AUM targeting $400M by year-end.",
    competitive_displacement_score: 42,
    competitive_displacement_detail: "Moderate. $35M in Vanguard BND, $42M in Schwab SCHB, $28M in BlackRock EFA. However, Amanda is already Invesco-first — remaining non-Invesco holdings serve specific index/passive roles.",
    risk_drift_alert: { status: 'CLEAR' as const, severity: 'none' as const, detail: 'All allocation changes are deliberate and increasing Invesco share. Her Invesco allocation has grown from 38% to 49.5% over 12 months.' },
    engagement_score: 92,
    engagement_breakdown: { crm_activity: 95, digital_engagement: 88, event_attendance: 82, content_consumption: 90, email_responsiveness: 88 },
    next_best_action: 'Support her growth trajectory. Priority: get tax-managed model proposal finalized ($20M opportunity). Secondary: explore direct indexing pilot.',
    talking_points: [
      'Tax-managed model proposal: Present Invesco\'s tax-managed model with projected tax alpha (est. 50-100bps annually). $20M initial opportunity.',
      'Priya onboarding: Her second junior hire is in training. Offer dedicated Invesco platform training session.',
      '$400M roadmap: She\'s targeting $400M by year-end. Discuss co-branded marketing, practice management resources.',
      'Direct indexing preview: Amanda asked about direct indexing capabilities. Share Invesco\'s roadmap and timeline.',
      'Case study opportunity: Her practice transformation with Invesco models is compelling. Propose a joint case study.',
    ],
    invesco_revenue_pct: 49,
    aum_growth_rate_yoy: 18.2,
    revenue_annual: 340000,
    revenue_from_invesco: 166600,
    pain_points: ['Scaling team onboarding', 'Tax efficiency for HNW clients', 'Direct indexing gap'],
    opportunities: ['$20M tax-managed model', 'Direct indexing pilot', 'Invesco case study'],
  },
  {
    advisor_id: 'ADV-006',
    advisor_name: 'David Okafor',
    meeting_prep_brief: "David is our highest-AUM advisor ($620M) but chronically low engagement. The CIO dinner breakthrough (Dec 18) was the first meaningful interaction in months — he expressed interest in Invesco private credit for $10M+. He recently added $8M to BlackRock Private Credit.",
    competitive_displacement_score: 22,
    competitive_displacement_detail: "Low near-term. David's non-Invesco book is dominated by Goldman Sachs ($85M), BlackRock ($137M), and Vanguard ($48M) — deeply entrenched relationships. The private credit interest is the best entry point.",
    risk_drift_alert: { status: 'MONITOR' as const, severity: 'medium' as const, detail: 'Recent $8M purchase of BlackRock Private Credit while ignoring Invesco private credit outreach is concerning. Invesco\'s $85M is stable but stagnant.' },
    engagement_score: 18,
    engagement_breakdown: { crm_activity: 12, digital_engagement: 5, event_attendance: 30, content_consumption: 5, email_responsiveness: 21 },
    next_best_action: 'Capitalize on CIO dinner momentum IMMEDIATELY. Have Invesco\'s head of private credit reach out directly within this week.',
    talking_points: [
      'Private credit follow-through: "David, our CIO mentioned you had a great conversation about private credit at the dinner. I\'ve arranged for [Head of Private Credit] to walk you through our strategy directly."',
      'BlackRock competitive positioning: Differentiate Invesco\'s private credit — lower correlation to public markets, broader deal sourcing through our $1.6T platform.',
      'Low-touch respect: Frame outreach as "exclusive access" not "check-in." He responded to CIO dinner because it was intimate and high-level.',
      'Autopilot confirmation: Briefly confirm $85M in Invesco holdings are performing well.',
      'Family office solutions: Mention Invesco\'s family office advisory capabilities — tailored reporting, multi-entity coordination.',
    ],
    invesco_revenue_pct: 14,
    aum_growth_rate_yoy: 3.2,
    revenue_annual: 620000,
    revenue_from_invesco: 86800,
    pain_points: ['Low engagement with Invesco despite large book', 'Prefers executive-level access', 'BlackRock relationship deepening'],
    opportunities: ['$10M+ private credit', 'Family office solutions', 'Executive relationship deepening'],
  },
  {
    advisor_id: 'ADV-007',
    advisor_name: 'Lisa Martinez',
    meeting_prep_brief: "Lisa is our digital engagement champion — 100% email open rate, top 5% website usage. She built a custom retirement income model using Invesco products ($49M) and is expanding it. She's co-presenting a Q1 2026 webinar on RMD changes expected to reach 200+ attendees.",
    competitive_displacement_score: 48,
    competitive_displacement_detail: "Moderate. $38M in Fidelity Freedom Funds, $32M in T. Rowe Price Retirement, $25M in Vanguard Wellesley. She's already moving from Fidelity (-$5M) and T. Rowe (-$3M) to Invesco retirement model.",
    risk_drift_alert: { status: 'CLEAR' as const, severity: 'none' as const, detail: 'Allocation shifting toward Invesco retirement income products — intentional and aligned with her practice strategy.' },
    engagement_score: 96,
    engagement_breakdown: { crm_activity: 90, digital_engagement: 100, event_attendance: 95, content_consumption: 100, email_responsiveness: 100 },
    next_best_action: 'Execute Q1 webinar flawlessly — this is a multiplier event reaching 200+ prospects. Simultaneously propose expanding retirement model to additional client accounts.',
    talking_points: [
      'Webinar execution: "Navigating 2026 RMD Changes" — confirm date, platform, Invesco data slides, post-webinar follow-up sequence.',
      'Retirement model expansion: She has 185 clients but only ~40 are in the Invesco retirement model. Identify the next 25 for migration.',
      'Digital partnership: Lisa wants API access for portfolio data integration. Push for internal approval.',
      'Content co-creation: Propose co-branded monthly retirement insights newsletter.',
      'Beta program candidate: Her digital sophistication makes her ideal for testing new Invesco digital tools.',
    ],
    invesco_revenue_pct: 32,
    aum_growth_rate_yoy: 9.8,
    revenue_annual: 210000,
    revenue_from_invesco: 67200,
    pain_points: ['Manual data integration needs', 'Scaling retirement model across 185 clients', 'Content production bandwidth'],
    opportunities: ['Webinar → 200 prospects', 'API integration partnership', '$50M+ systematic displacement from Fidelity/T. Rowe'],
  },
  {
    advisor_id: 'ADV-008',
    advisor_name: 'James Patel',
    meeting_prep_brief: "⚠️ RETENTION CRISIS. James lost $40M to Fidelity over 6 weeks (Dec 2025–Jan 2026) across 3 client departures. Root causes: growth equity underperformance and perceived technology gap. Remaining Invesco holdings: $55M. He placed $8M into Invesco Discovery Fund as a test.",
    competitive_displacement_score: 8,
    competitive_displacement_detail: "CRITICAL — we are losing share. Net outflow of $40M to Fidelity. The $8M Discovery Fund test is a lifeline — Q1 2026 performance must be strong.",
    risk_drift_alert: { status: 'ALERT' as const, severity: 'high' as const, detail: 'Lost $40M to Fidelity over 6 weeks. Remaining $55M at risk if Q1 Discovery Fund performance disappoints. Technology gap cited as concern.' },
    engagement_score: 35,
    engagement_breakdown: { crm_activity: 42, digital_engagement: 28, event_attendance: 15, content_consumption: 35, email_responsiveness: 48 },
    next_best_action: 'Deliver Q1 Discovery Fund performance update proactively — don\'t wait for him to ask. Propose technology demo to address perceived gap.',
    talking_points: [
      'Discovery Fund Q1 update: Strong start — YTD return X%, beating Fidelity Contrafund by Ybps. This is the critical proof point for retention.',
      'Technology response: Acknowledge his concern directly. Demo Invesco\'s digital tools — portfolio analytics, client reporting, API capabilities.',
      'Root cause acknowledgment: "James, losing those 3 clients was painful. I want to understand what we could have done differently and how we rebuild from here."',
      'Retention value: Calculate the total value of Invesco relationship — service hours, events, research, attribution. Make switching painful.',
      'New client pipeline: Help James win new clients to compensate for losses. Invesco resources for business development.',
    ],
    invesco_revenue_pct: 14,
    aum_growth_rate_yoy: -8.5,
    revenue_annual: 390000,
    revenue_from_invesco: 54600,
    pain_points: ['Lost $40M to Fidelity', 'Underperformance in growth equity', 'Technology gap perception'],
    opportunities: ['$8M Discovery Fund test → retention anchor', 'Technology differentiation', 'Business development support'],
  },
  {
    advisor_id: 'ADV-009',
    advisor_name: 'Catherine Brooks',
    meeting_prep_brief: "Catherine is a NEW RELATIONSHIP — onboarded Aug 2025. Still in discovery phase. Has expressed interest in Invesco fixed income and factor strategies. Needs education on full platform capabilities. High growth potential.",
    competitive_displacement_score: 55,
    competitive_displacement_detail: "Moderate-high opportunity as new relationship. $90M book with significant Vanguard and iShares exposure. Discovery phase means Invesco can establish positioning before incumbents entrench.",
    risk_drift_alert: { status: 'CLEAR' as const, severity: 'none' as const, detail: 'New relationship — no drift concerns. Onboarding phase.' },
    engagement_score: 68,
    engagement_breakdown: { crm_activity: 72, digital_engagement: 65, event_attendance: 55, content_consumption: 70, email_responsiveness: 78 },
    next_best_action: 'Complete platform education — schedule product deep-dive on fixed income and factor strategies. Propose first Invesco product allocation.',
    talking_points: [
      'Platform overview: Systematic tour of Invesco capabilities — fixed income, factor ETFs, model portfolios, alternatives.',
      'Fixed income deep-dive: Her client base (young professionals, tech workers) has specific fixed income needs. Present target-date bonds, BSCR series.',
      'Factor strategies: RAFI fundamental indexing vs traditional cap-weighted — present backtested data.',
      'Model portfolio pilot: Propose starting with $5-10M in a model portfolio to establish track record.',
      'Event invitation: Invite to upcoming Invesco Symposium — networking plus product education.',
    ],
    invesco_revenue_pct: 8,
    aum_growth_rate_yoy: 22.5,
    revenue_annual: 150000,
    revenue_from_invesco: 12000,
    pain_points: ['New to Invesco platform', 'Limited product knowledge', 'Building trust in new relationship'],
    opportunities: ['$12M initial allocation', 'Factor strategy pilot', 'Growing practice at 22% YoY'],
  },
  {
    advisor_id: 'ADV-010',
    advisor_name: 'Michael Torres',
    meeting_prep_brief: "Michael focuses on multi-generational wealth with $72M in Invesco products. Strong personal rapport with RM. Interested in succession planning solutions and next-gen wealth transfer strategies. High-touch relationship.",
    competitive_displacement_score: 38,
    competitive_displacement_detail: "Moderate. $48M in non-Invesco holdings (Goldman $85M, Vanguard $32M) could be targeted with multi-generational and alternative strategies. Strong relationship provides platform.",
    risk_drift_alert: { status: 'CLEAR' as const, severity: 'none' as const, detail: 'Stable relationship with consistent Invesco usage. Next-gen wealth focus increasing Invesco footprint.' },
    engagement_score: 75,
    engagement_breakdown: { crm_activity: 80, digital_engagement: 68, event_attendance: 72, content_consumption: 74, email_responsiveness: 82 },
    next_best_action: 'Present multi-generational wealth transfer capabilities and alternatives access. Identify succession planning timeline.',
    talking_points: [
      'Succession planning review: Michael\'s HNW clients are entering wealth transfer phase. Present Invesco\'s next-gen engagement program.',
      'Alternatives access: His family office clients need private markets exposure. Present Invesco\'s alternatives platform.',
      'International client solutions: Miami practice has Latin American client base. Discuss international portfolio strategies.',
      'Next event: Exclusive wealth management forum in Miami Q2 — perfect for his client demographic.',
      'Goldman displacement: $85M in Goldman products could migrate to Invesco alternatives over 18 months with right positioning.',
    ],
    invesco_revenue_pct: 15,
    aum_growth_rate_yoy: 7.4,
    revenue_annual: 480000,
    revenue_from_invesco: 72000,
    pain_points: ['Succession planning complexity', 'International client reporting', 'Alternatives access'],
    opportunities: ['$85M Goldman displacement', 'Alternatives platform', 'Miami event sponsorship'],
  },
]

// Holdings data per advisor
const holdingsData: Record<string, Holding[]> = {
  'ADV-001': [
    { fund_name: 'Invesco Income Advantage', ticker: 'SCAUX', provider: 'Invesco', asset_class: 'Fixed Income', aum: 12000000, allocation_pct: 2.7, change_vs_prior_quarter_pct: '+0.5%', recommended_list: true },
    { fund_name: 'Invesco S&P 500 Low Volatility ETF', ticker: 'SPLV', provider: 'Invesco', asset_class: 'Equity', aum: 12000000, allocation_pct: 2.7, change_vs_prior_quarter_pct: '+2.7%', recommended_list: true },
    { fund_name: 'Invesco Oppenheimer Intermediate Term Bond', ticker: 'OPIGX', provider: 'Invesco', asset_class: 'Fixed Income', aum: 10000000, allocation_pct: 2.2, change_vs_prior_quarter_pct: '+0.3%', recommended_list: true },
    { fund_name: 'Vanguard Total Stock Market ETF', ticker: 'VTI', provider: 'Vanguard', asset_class: 'Equity', aum: 85000000, allocation_pct: 18.9, change_vs_prior_quarter_pct: '-1.2%', recommended_list: false },
    { fund_name: 'Fidelity 500 Index Fund', ticker: 'FXAIX', provider: 'Fidelity', asset_class: 'Equity', aum: 62000000, allocation_pct: 13.8, change_vs_prior_quarter_pct: '-0.5%', recommended_list: false },
    { fund_name: 'BlackRock Aggregate Bond ETF', ticker: 'AGG', provider: 'BlackRock', asset_class: 'Fixed Income', aum: 45000000, allocation_pct: 10.0, change_vs_prior_quarter_pct: '+0.8%', recommended_list: false },
  ],
  'ADV-002': [
    { fund_name: 'Invesco QQQ Trust', ticker: 'QQQ', provider: 'Invesco', asset_class: 'Equity', aum: 28000000, allocation_pct: 10.0, change_vs_prior_quarter_pct: '+1.5%', recommended_list: true },
    { fund_name: 'Invesco NASDAQ 100 ETF', ticker: 'QQQM', provider: 'Invesco', asset_class: 'Equity', aum: 14000000, allocation_pct: 5.0, change_vs_prior_quarter_pct: '+2.1%', recommended_list: true },
    { fund_name: 'Vanguard Target Retirement 2040', ticker: 'VFORX', provider: 'Vanguard', asset_class: 'Target Date', aum: 45000000, allocation_pct: 16.1, change_vs_prior_quarter_pct: '-0.8%', recommended_list: false },
    { fund_name: 'Vanguard Growth ETF', ticker: 'VUG', provider: 'Vanguard', asset_class: 'Equity', aum: 35000000, allocation_pct: 12.5, change_vs_prior_quarter_pct: '+0.2%', recommended_list: false },
    { fund_name: 'iShares Russell 1000 Growth', ticker: 'IWF', provider: 'BlackRock', asset_class: 'Equity', aum: 28000000, allocation_pct: 10.0, change_vs_prior_quarter_pct: '-0.3%', recommended_list: false },
  ],
  'ADV-003': [
    { fund_name: 'Invesco Solar ETF', ticker: 'TAN', provider: 'Invesco', asset_class: 'Equity', aum: 5000000, allocation_pct: 2.8, change_vs_prior_quarter_pct: '-0.5%', recommended_list: true },
    { fund_name: 'Invesco Water Resources ETF', ticker: 'PHO', provider: 'Invesco', asset_class: 'Equity', aum: 3000000, allocation_pct: 1.7, change_vs_prior_quarter_pct: '+0.2%', recommended_list: true },
    { fund_name: 'Invesco MSCI Sustainable Future ETF', ticker: 'ERTH', provider: 'Invesco', asset_class: 'Equity', aum: 2000000, allocation_pct: 1.1, change_vs_prior_quarter_pct: '+0.1%', recommended_list: true },
    { fund_name: 'iShares ESG Aware MSCI USA ETF', ticker: 'ESGU', provider: 'BlackRock', asset_class: 'Equity', aum: 25000000, allocation_pct: 13.9, change_vs_prior_quarter_pct: '-0.6%', recommended_list: false },
    { fund_name: 'Parnassus Core Equity', ticker: 'PRBLX', provider: 'Parnassus', asset_class: 'Equity', aum: 18000000, allocation_pct: 10.0, change_vs_prior_quarter_pct: '0%', recommended_list: false },
  ],
  'ADV-004': [
    { fund_name: 'Invesco Diversified Dividend Fund', ticker: 'LCEAX', provider: 'Invesco', asset_class: 'Equity', aum: 32000000, allocation_pct: 6.2, change_vs_prior_quarter_pct: '-0.8%', recommended_list: true },
    { fund_name: 'Invesco Corporate Bond Fund', ticker: 'ACCBX', provider: 'Invesco', asset_class: 'Fixed Income', aum: 22000000, allocation_pct: 4.2, change_vs_prior_quarter_pct: '-0.5%', recommended_list: true },
    { fund_name: 'BlackRock Total Return', ticker: 'MAHQX', provider: 'BlackRock', asset_class: 'Fixed Income', aum: 5000000, allocation_pct: 1.0, change_vs_prior_quarter_pct: '+1.0%', recommended_list: false },
    { fund_name: 'JP Morgan Equity Premium Income', ticker: 'JEPI', provider: 'JP Morgan', asset_class: 'Equity', aum: 3000000, allocation_pct: 0.6, change_vs_prior_quarter_pct: '+0.6%', recommended_list: false },
    { fund_name: 'PIMCO Income Fund', ticker: 'PONAX', provider: 'PIMCO', asset_class: 'Fixed Income', aum: 45000000, allocation_pct: 8.7, change_vs_prior_quarter_pct: '+0.5%', recommended_list: false },
  ],
  'ADV-005': [
    { fund_name: 'Invesco Conservative Income Model', ticker: 'MODEL-CI', provider: 'Invesco', asset_class: 'Model Portfolio', aum: 18000000, allocation_pct: 5.3, change_vs_prior_quarter_pct: '+5.3%', recommended_list: true },
    { fund_name: 'Invesco Moderate Growth Model', ticker: 'MODEL-MG', provider: 'Invesco', asset_class: 'Model Portfolio', aum: 52000000, allocation_pct: 15.3, change_vs_prior_quarter_pct: '+2.1%', recommended_list: true },
    { fund_name: 'Invesco QQQ Trust', ticker: 'QQQ', provider: 'Invesco', asset_class: 'Equity', aum: 28000000, allocation_pct: 8.2, change_vs_prior_quarter_pct: '+0.9%', recommended_list: true },
    { fund_name: 'Vanguard Total Bond Market ETF', ticker: 'BND', provider: 'Vanguard', asset_class: 'Fixed Income', aum: 35000000, allocation_pct: 10.3, change_vs_prior_quarter_pct: '0%', recommended_list: false },
    { fund_name: 'Schwab US Broad Market ETF', ticker: 'SCHB', provider: 'Schwab', asset_class: 'Equity', aum: 42000000, allocation_pct: 12.4, change_vs_prior_quarter_pct: '-0.2%', recommended_list: false },
  ],
  'ADV-006': [
    { fund_name: 'Invesco S&P 500 Equal Weight ETF', ticker: 'RSP', provider: 'Invesco', asset_class: 'Equity', aum: 42000000, allocation_pct: 6.8, change_vs_prior_quarter_pct: '+0.3%', recommended_list: true },
    { fund_name: 'Invesco Fundamental High Yield', ticker: 'PHB', provider: 'Invesco', asset_class: 'Fixed Income', aum: 24000000, allocation_pct: 3.9, change_vs_prior_quarter_pct: '0%', recommended_list: true },
    { fund_name: 'Goldman Sachs Global Fixed Income', ticker: 'GSFIX', provider: 'Goldman Sachs', asset_class: 'Fixed Income', aum: 85000000, allocation_pct: 13.7, change_vs_prior_quarter_pct: '+0.5%', recommended_list: false },
    { fund_name: 'BlackRock Private Credit', ticker: 'BDEAX', provider: 'BlackRock', asset_class: 'Alternatives', aum: 8000000, allocation_pct: 1.3, change_vs_prior_quarter_pct: '+1.3%', recommended_list: false },
    { fund_name: 'Vanguard 500 Index Admiral', ticker: 'VFIAX', provider: 'Vanguard', asset_class: 'Equity', aum: 48000000, allocation_pct: 7.7, change_vs_prior_quarter_pct: '-0.1%', recommended_list: false },
  ],
  'ADV-007': [
    { fund_name: 'Invesco Income Advantage', ticker: 'ACEIX', provider: 'Invesco', asset_class: 'Fixed Income', aum: 12000000, allocation_pct: 5.7, change_vs_prior_quarter_pct: '+1.2%', recommended_list: true },
    { fund_name: 'Invesco Conservative Income ETF', ticker: 'PGX', provider: 'Invesco', asset_class: 'Fixed Income', aum: 8000000, allocation_pct: 3.8, change_vs_prior_quarter_pct: '+0.5%', recommended_list: true },
    { fund_name: 'Invesco Short Term Bond', ticker: 'VFSTX', provider: 'Invesco', asset_class: 'Fixed Income', aum: 10000000, allocation_pct: 4.8, change_vs_prior_quarter_pct: '+0.3%', recommended_list: true },
    { fund_name: 'Fidelity Freedom Income Fund', ticker: 'FFFAX', provider: 'Fidelity', asset_class: 'Target Date', aum: 38000000, allocation_pct: 18.1, change_vs_prior_quarter_pct: '-1.5%', recommended_list: false },
    { fund_name: 'T. Rowe Price Retirement Income', ticker: 'TRRIX', provider: 'T. Rowe Price', asset_class: 'Target Date', aum: 32000000, allocation_pct: 15.2, change_vs_prior_quarter_pct: '-0.8%', recommended_list: false },
  ],
  'ADV-008': [
    { fund_name: 'Invesco Discovery Fund', ticker: 'ADEAX', provider: 'Invesco', asset_class: 'Equity', aum: 8000000, allocation_pct: 2.1, change_vs_prior_quarter_pct: '+2.1%', recommended_list: true },
    { fund_name: 'Invesco Growth Fund', ticker: 'ACGIX', provider: 'Invesco', asset_class: 'Equity', aum: 32000000, allocation_pct: 8.2, change_vs_prior_quarter_pct: '-1.8%', recommended_list: true },
    { fund_name: 'Fidelity Contrafund', ticker: 'FCNTX', provider: 'Fidelity', asset_class: 'Equity', aum: 20000000, allocation_pct: 5.1, change_vs_prior_quarter_pct: '+3.2%', recommended_list: false },
    { fund_name: 'Fidelity Growth Company Fund', ticker: 'FDGRX', provider: 'Fidelity', asset_class: 'Equity', aum: 12000000, allocation_pct: 3.1, change_vs_prior_quarter_pct: '+2.1%', recommended_list: false },
  ],
  'ADV-009': [
    { fund_name: 'Invesco BulletShares 2028 Corporate Bond ETF', ticker: 'BSCR', provider: 'Invesco', asset_class: 'Fixed Income', aum: 5000000, allocation_pct: 3.3, change_vs_prior_quarter_pct: '+3.3%', recommended_list: true },
    { fund_name: 'Invesco RAFI Strategic US ETF', ticker: 'IUS', provider: 'Invesco', asset_class: 'Equity', aum: 3000000, allocation_pct: 2.0, change_vs_prior_quarter_pct: '+2.0%', recommended_list: true },
    { fund_name: 'Vanguard Total Stock Market', ticker: 'VTI', provider: 'Vanguard', asset_class: 'Equity', aum: 42000000, allocation_pct: 28.0, change_vs_prior_quarter_pct: '0%', recommended_list: false },
    { fund_name: 'iShares Core MSCI International', ticker: 'IXUS', provider: 'BlackRock', asset_class: 'Equity', aum: 28000000, allocation_pct: 18.7, change_vs_prior_quarter_pct: '-0.5%', recommended_list: false },
  ],
  'ADV-010': [
    { fund_name: 'Invesco S&P 500 Equal Weight ETF', ticker: 'RSP', provider: 'Invesco', asset_class: 'Equity', aum: 32000000, allocation_pct: 6.7, change_vs_prior_quarter_pct: '+0.5%', recommended_list: true },
    { fund_name: 'Invesco Mortgage Income ETF', ticker: 'OFC', provider: 'Invesco', asset_class: 'Fixed Income', aum: 18000000, allocation_pct: 3.8, change_vs_prior_quarter_pct: '+0.2%', recommended_list: true },
    { fund_name: 'Goldman Sachs Global Multi-Asset', ticker: 'GSAMX', provider: 'Goldman Sachs', asset_class: 'Multi-Asset', aum: 85000000, allocation_pct: 17.7, change_vs_prior_quarter_pct: '+0.3%', recommended_list: false },
    { fund_name: 'Vanguard International Growth', ticker: 'VWIGX', provider: 'Vanguard', asset_class: 'Equity', aum: 32000000, allocation_pct: 6.7, change_vs_prior_quarter_pct: '-0.2%', recommended_list: false },
  ],
}

// Base advisor list with profile data
const advisorProfiles = [
  {
    advisor_id: 'ADV-001', name: 'Dr. Sarah Chen', title: 'Managing Director, Wealth Management',
    firm: 'Pinnacle Wealth Advisors', channel: 'RIA', region: 'Southeast', city: 'Charlotte', state: 'NC',
    aum: 450000000, years_in_business: 18, certifications: ['CFP', 'CFA', 'PhD Economics'],
    email: 'sarah.chen@pinnaclewealth.com', phone: '(704) 555-0142',
    office_address: '401 S Tryon St, Suite 1200, Charlotte, NC 28202',
    relationship_manager: 'Brian Calloway', client_count: 142,
    last_contact_date: '2026-01-28', status: 'active',
    practice_focus: ['High Net Worth', 'Retirement Planning', 'Institutional'],
  },
  {
    advisor_id: 'ADV-002', name: 'Marcus Thompson', title: 'Senior Vice President, Financial Advisor',
    firm: 'Merrill Lynch', channel: 'Wirehouse', region: 'Mid-Atlantic', city: 'Washington', state: 'DC',
    aum: 280000000, years_in_business: 12, certifications: ['CFP', 'CIMA'],
    email: 'marcus.thompson@ml.com', phone: '(202) 555-0387',
    office_address: '1200 K St NW, Suite 800, Washington, DC 20005',
    relationship_manager: 'Brian Calloway', client_count: 95,
    last_contact_date: '2026-02-05', status: 'active',
    practice_focus: ['Growth Investing', 'Corporate Executives', '401k Rollovers'],
  },
  {
    advisor_id: 'ADV-003', name: 'Jennifer Walsh', title: 'Founder & Principal',
    firm: 'Walsh Sustainable Advisors', channel: 'Independent', region: 'Mid-Atlantic', city: 'Richmond', state: 'VA',
    aum: 180000000, years_in_business: 9, certifications: ['CFP', 'CSRIC'],
    email: 'jwalsh@walshsustainable.com', phone: '(804) 555-0219',
    office_address: '1001 E Cary St, Suite 300, Richmond, VA 23219',
    relationship_manager: 'Diana Reyes', client_count: 68,
    last_contact_date: '2026-01-15', status: 'active',
    practice_focus: ['ESG/Sustainable Investing', 'Women & Wealth', 'Next-Gen Investors'],
  },
  {
    advisor_id: 'ADV-004', name: 'Robert Kim', title: 'Director, Private Client Group',
    firm: 'JP Morgan Private Bank', channel: 'Bank', region: 'Southeast', city: 'Atlanta', state: 'GA',
    aum: 520000000, years_in_business: 22, certifications: ['CFA', 'CFP', 'CPWA'],
    email: 'robert.kim@jpmorgan.com', phone: '(404) 555-0561',
    office_address: '3344 Peachtree Rd NE, Suite 1500, Atlanta, GA 30326',
    relationship_manager: 'Brian Calloway', client_count: 78,
    last_contact_date: '2025-11-14', status: 'at_risk',
    practice_focus: ['Ultra High Net Worth', 'Estate Planning', 'Alternative Investments'],
  },
  {
    advisor_id: 'ADV-005', name: 'Amanda Foster', title: 'Partner & Chief Investment Officer',
    firm: 'Mosaic Financial Partners', channel: 'RIA', region: 'Southeast', city: 'Nashville', state: 'TN',
    aum: 340000000, years_in_business: 14, certifications: ['CFP', 'CFA', 'CAIA'],
    email: 'afoster@mosaicfp.com', phone: '(615) 555-0733',
    office_address: '150 4th Ave N, Suite 1800, Nashville, TN 37219',
    relationship_manager: 'Diana Reyes', client_count: 110,
    last_contact_date: '2026-02-10', status: 'active',
    practice_focus: ['Model Portfolios', 'Financial Planning', 'Business Owners'],
  },
  {
    advisor_id: 'ADV-006', name: 'David Okafor', title: 'Executive Director, Wealth Management',
    firm: 'Morgan Stanley', channel: 'Wirehouse', region: 'Mid-Atlantic', city: 'Baltimore', state: 'MD',
    aum: 620000000, years_in_business: 25, certifications: ['CFP', 'CIMA', 'CPWA'],
    email: 'david.okafor@morganstanley.com', phone: '(410) 555-0892',
    office_address: '100 International Dr, Suite 2500, Baltimore, MD 21202',
    relationship_manager: 'Brian Calloway', client_count: 65,
    last_contact_date: '2025-12-18', status: 'active',
    practice_focus: ['Ultra High Net Worth', 'Family Office Services', 'Concentrated Stock'],
  },
  {
    advisor_id: 'ADV-007', name: 'Lisa Martinez', title: 'President',
    firm: 'Martinez Retirement Solutions', channel: 'Independent', region: 'Southeast', city: 'Tampa', state: 'FL',
    aum: 210000000, years_in_business: 16, certifications: ['CFP', 'RICP', 'AIF'],
    email: 'lisa@martinezretirement.com', phone: '(813) 555-0445',
    office_address: '4830 W Kennedy Blvd, Suite 600, Tampa, FL 33609',
    relationship_manager: 'Diana Reyes', client_count: 185,
    last_contact_date: '2026-02-12', status: 'active',
    practice_focus: ['Retirement Planning', '401k/403b', 'Income Solutions'],
  },
  {
    advisor_id: 'ADV-008', name: 'James Patel', title: 'Senior Wealth Advisor',
    firm: 'Wells Fargo Advisors', channel: 'Bank', region: 'Mid-Atlantic', city: 'Philadelphia', state: 'PA',
    aum: 390000000, years_in_business: 19, certifications: ['CFP', 'CFA'],
    email: 'james.patel@wellsfargo.com', phone: '(215) 555-0678',
    office_address: '1735 Market St, Suite 2800, Philadelphia, PA 19103',
    relationship_manager: 'Brian Calloway', client_count: 120,
    last_contact_date: '2026-01-22', status: 'at_risk',
    practice_focus: ['Comprehensive Wealth', 'Tax-Efficient Investing', 'Corporate Retirement'],
  },
  {
    advisor_id: 'ADV-009', name: 'Catherine Brooks', title: 'Wealth Advisor',
    firm: 'Brooks Wealth Management', channel: 'RIA', region: 'Southeast', city: 'Raleigh', state: 'NC',
    aum: 150000000, years_in_business: 6, certifications: ['CFP'],
    email: 'cbrooks@brookswm.com', phone: '(919) 555-0334',
    office_address: '421 Fayetteville St, Suite 1100, Raleigh, NC 27601',
    relationship_manager: 'Diana Reyes', client_count: 72,
    last_contact_date: '2026-02-03', status: 'onboarding',
    practice_focus: ['Financial Planning', 'Young Professionals', 'Tech Industry'],
  },
  {
    advisor_id: 'ADV-010', name: 'Michael Torres', title: 'Managing Director, Private Wealth',
    firm: 'UBS Financial Services', channel: 'Wirehouse', region: 'Southeast', city: 'Miami', state: 'FL',
    aum: 480000000, years_in_business: 20, certifications: ['CFP', 'CIMA', 'CEPA'],
    email: 'michael.torres@ubs.com', phone: '(305) 555-0917',
    office_address: '1450 Brickell Ave, Suite 3100, Miami, FL 33131',
    relationship_manager: 'Diana Reyes', client_count: 55,
    last_contact_date: '2026-02-07', status: 'active',
    practice_focus: ['Multi-Generational Wealth', 'International Clients', 'Business Succession'],
  },
]

function buildSignals(advisorId: string, detail: typeof advisorDetails[0]): Signal[] {
  const signals: Signal[] = []

  if (detail.risk_drift_alert.status !== 'CLEAR') {
    const sev = detail.risk_drift_alert.severity === 'high' ? 'urgent'
      : detail.risk_drift_alert.severity === 'medium' ? 'attention' : 'info'
    signals.push({
      id: `${advisorId}-drift`,
      text: `Risk Drift: ${detail.risk_drift_alert.status}`,
      severity: sev as Signal['severity'],
      metric: detail.risk_drift_alert.severity.toUpperCase(),
      detail: detail.risk_drift_alert.detail,
    })
  }

  const engSev = detail.engagement_score >= 80 ? 'positive'
    : detail.engagement_score >= 50 ? 'info'
    : detail.engagement_score >= 25 ? 'attention' : 'urgent'
  signals.push({
    id: `${advisorId}-eng`,
    text: `Engagement score: ${detail.engagement_score}/100`,
    severity: engSev as Signal['severity'],
    metric: `${detail.engagement_score}/100`,
    detail: `CRM: ${detail.engagement_breakdown.crm_activity}, Digital: ${detail.engagement_breakdown.digital_engagement}, Events: ${detail.engagement_breakdown.event_attendance}`,
  })

  const compScore = detail.competitive_displacement_score
  signals.push({
    id: `${advisorId}-comp`,
    text: `Competitive displacement score: ${compScore}/100`,
    severity: compScore >= 70 ? 'positive' : compScore >= 40 ? 'info' : compScore <= 15 ? 'urgent' : 'attention',
    metric: `${compScore}/100`,
    detail: detail.competitive_displacement_detail,
  })

  signals.push({
    id: `${advisorId}-nba`,
    text: detail.next_best_action.slice(0, 120) + (detail.next_best_action.length > 120 ? '...' : ''),
    severity: 'info',
    detail: detail.next_best_action,
  })

  return signals
}

// Build the advisors array
export const advisors: Advisor[] = advisorProfiles.map(profile => {
  const detail = advisorDetails.find(d => d.advisor_id === profile.advisor_id)!
  const holdings = holdingsData[profile.advisor_id] || []
  const daysAgo = Math.round((new Date().getTime() - new Date(profile.last_contact_date).getTime()) / 86400000)
  const slug = profile.name.toLowerCase().replace(/[^a-z\s]/g, '').replace(/\s+/g, '-').replace(/^dr-/, '')

  return {
    id: slug,
    advisorId: profile.advisor_id,
    name: profile.name,
    title: profile.title,
    firm: profile.firm,
    firmType: profile.channel,
    aum: Math.round(profile.aum / 1e6),
    region: profile.region,
    channel: profile.channel,
    city: profile.city,
    state: profile.state,
    engagementScore: detail.engagement_score,
    engagementDelta: detail.engagement_score >= 50
      ? Math.round(detail.engagement_score * 0.1)
      : -Math.round((100 - detail.engagement_score) * 0.1),
    sentiment: getSentiment(detail.engagement_score),
    sentimentTrend: getSentiment(detail.engagement_score),
    lastContact: `${daysAgo} days ago`,
    lastContactDaysAgo: daysAgo,
    meetingDate: daysAgo <= 30 ? 'This week' : undefined,
    meetingTime: daysAgo <= 30 ? '2:00 PM' : undefined,
    signals: buildSignals(profile.advisor_id, detail),
    talkingPoints: detail.talking_points.map((text, i) => ({ id: `tp-${profile.advisor_id}-${i}`, text })),
    meetingPrepBrief: detail.meeting_prep_brief,
    engagementBreakdown: detail.engagement_breakdown,
    riskDriftAlert: detail.risk_drift_alert,
    competitiveDisplacementScore: detail.competitive_displacement_score,
    competitiveDisplacementDetail: detail.competitive_displacement_detail,
    opportunityScore: Math.min(100, Math.round(
      detail.competitive_displacement_score * 0.4
      + (100 - detail.engagement_score) * 0.3
      + Math.min(profile.aum / 1e6 / 10, 30)
    )),
    nextBestAction: detail.next_best_action,
    allHoldings: holdings,
    invescoRevenuePct: detail.invesco_revenue_pct,
    aumGrowthRate: detail.aum_growth_rate_yoy,
    revenueAnnual: detail.revenue_annual,
    revenueFromInvesco: detail.revenue_from_invesco,
    clientCount: profile.client_count,
    avgClientAum: Math.round(profile.aum / profile.client_count),
    keyNotes: '',
    practiceFocus: profile.practice_focus,
    certifications: profile.certifications,
    email: profile.email,
    phone: profile.phone,
    officeAddress: profile.office_address,
    relationshipManager: profile.relationship_manager,
    netFlows: detail.aum_growth_rate_yoy > 0
      ? Math.round(profile.aum / 1e6 * detail.aum_growth_rate_yoy / 100 * 10) / 10
      : -Math.round(Math.abs(profile.aum / 1e6 * detail.aum_growth_rate_yoy / 100) * 10) / 10,
    topHoldings: holdings.filter(h => h.provider === 'Invesco').slice(0, 5).map(h => `${h.fund_name} (${h.ticker})`),
    painPoints: detail.pain_points,
    opportunities: detail.opportunities,
    activities: [
      { date: profile.last_contact_date, type: 'meeting', description: 'Quarterly review meeting' },
      { date: '2026-01-15', type: 'email', description: 'Product update and market commentary sent' },
      { date: '2026-01-08', type: 'call', description: 'Check-in call — discussed Q1 outlook' },
    ],
    materials: [
      { id: `mat-${profile.advisor_id}-0`, type: 'pitch-book', title: 'Invesco 2026 Market Outlook', url: 'https://seismic.invesco.com/content/market-outlook-2026' },
      { id: `mat-${profile.advisor_id}-1`, type: 'factsheet', title: 'Invesco QQQ Trust Factsheet', url: 'https://seismic.invesco.com/content/qqq-factsheet' },
      { id: `mat-${profile.advisor_id}-2`, type: 'report', title: 'Factor Investing: 2025 Performance Review', url: 'https://seismic.invesco.com/content/factor-investing-series' },
    ],
  }
})

// Territory metrics
export const territoryMetrics: TerritoryMetrics = {
  totalAUM: advisors.reduce((sum, a) => sum + a.aum, 0),
  totalNetFlows: Math.round(advisors.reduce((sum, a) => sum + a.netFlows, 0) * 10) / 10,
  avgEngagement: Math.round(advisors.reduce((sum, a) => sum + a.engagementScore, 0) / advisors.length),
  advisorCount: advisors.length,
  meetingsThisWeek: advisors.filter(a => a.meetingDate).length,
  signalsRequiringAction: advisors.reduce((sum, a) =>
    sum + a.signals.filter(s => s.severity === 'urgent' || s.severity === 'attention').length, 0),
}

// Top signals across territory
export const topSignals = advisors
  .flatMap(a => a.signals
    .filter(s => s.severity === 'urgent' || s.severity === 'attention')
    .map(s => ({ advisorId: a.id, advisorName: a.name, firm: a.firm, signal: s.text, severity: s.severity, aum: a.aum }))
  )
  .sort((a, b) => (a.severity === 'urgent' && b.severity !== 'urgent') ? -1 : (b.severity === 'urgent' && a.severity !== 'urgent') ? 1 : b.aum - a.aum)
  .slice(0, 8)

export function getAdvisor(id: string): Advisor | undefined {
  return advisors.find(a => a.id === id)
}

export function severityDot(severity: Signal['severity']): string {
  switch (severity) {
    case 'urgent': return 'bg-red-500'
    case 'attention': return 'bg-amber-500'
    case 'positive': return 'bg-green-500'
    case 'info': return 'bg-blue-500'
  }
}

// Persona configurations
const megaPersona = {
  key: 'megan',
  greeting: 'Hi Megan',
  name: 'Megan Weber',
  title: 'VP, Advisor Distribution — East',
  focus: 'ETF Cross-Sell Opportunities',
  territory: 'East Coast RIAs',
  heroStat: '$38.4B',
  heroStatLabel: 'East Coast AUM',
  accentColor: '#0176D3',
  stats: [
    { value: '214', label: 'RIA Advisors' },
    { value: '$38.4B', label: 'AUM' },
    { value: '28', label: 'ETF Signals' },
    { value: '94%', label: 'Engagement' },
  ],
  heroInsight: '14 East Coast RIAs flagged for ETF cross-sell — avg. $240M AUM each. Top opportunity: QQQ alternatives into fee-only books.',
  topFilters: ['ETF cross-sell', 'RIA channel', 'East Coast', 'High wallet share'],
  dashboardSubtitle: 'East Coast RIA Book · ETF Opportunities',
  liveBanner: '214 East Coast RIAs · $38.4B AUM · 28 ETF Signals',
  advisorFilter: (a: Advisor) => ['Northeast', 'Southeast', 'Mid-Atlantic', 'East'].some(r => a.region?.includes(r)) || ['NY', 'MA', 'CT', 'NJ', 'PA', 'MD', 'VA', 'NC', 'GA', 'FL'].includes(a.state),
  advisorSort: (a: Advisor, b: Advisor) => b.invescoRevenuePct - a.invescoRevenuePct,
}

const craigPersona = {
  key: 'craig',
  greeting: 'Hi Craig',
  name: 'Craig Lieb',
  title: 'VP, Advisor Distribution — West',
  focus: 'Retention Signals & At-Risk Accounts',
  territory: 'West Coast Book',
  heroStat: '$52.1B',
  heroStatLabel: 'West Coast AUM',
  accentColor: '#2E844A',
  stats: [
    { value: '286', label: 'West Advisors' },
    { value: '$52.1B', label: 'AUM' },
    { value: '21', label: 'At-Risk' },
    { value: '87%', label: 'Retention Score' },
  ],
  heroInsight: '21 West Coast advisors showing competitive displacement risk. Schwab/PIMCO displacement up 18% QoQ.',
  topFilters: ['At-risk', 'West Coast', 'Competitive threat', 'Declining engagement'],
  dashboardSubtitle: 'West Coast Book · Retention Intelligence',
  liveBanner: '286 West Coast Advisors · $52.1B AUM · 21 At-Risk Signals',
  advisorFilter: (a: Advisor) => ['West', 'Mountain', 'Pacific', 'Southwest'].some(r => a.region?.includes(r)) || ['CA', 'WA', 'OR', 'AZ', 'NV', 'CO', 'UT'].includes(a.state),
  advisorSort: (a: Advisor, b: Advisor) => a.competitiveDisplacementScore - b.competitiveDisplacementScore,
}

const defaultPersona = {
  key: 'default',
  greeting: 'Advisor Dashboard',
  name: '',
  title: '',
  focus: 'Full Book Overview',
  territory: 'All Regions',
  heroStat: '$156B',
  heroStatLabel: 'Total AUM',
  accentColor: '#032D60',
  stats: [
    { value: '500', label: 'Advisors' },
    { value: '$156B', label: 'AUM' },
    { value: '35', label: 'Signals' },
    { value: '92%', label: 'Engagement' },
  ],
  heroInsight: '',
  topFilters: [],
  dashboardSubtitle: 'Full Advisor Book',
  liveBanner: '500 Advisors · $156B AUM · 35 Active Signals',
  advisorFilter: (_: Advisor) => true,
  advisorSort: (_a: Advisor, _b: Advisor) => 0,
}

export type PersonaConfig = typeof megaPersona

export function getPersonaConfig(key: string | null): PersonaConfig {
  if (key === 'megan') return megaPersona
  if (key === 'craig') return craigPersona
  return defaultPersona
}
