# Deep Research: Launching a Next-Generation RIA
## Leveraging ForwardLane, OpenFlow, and AI-Native Infrastructure

**Prepared by Honey 🍯 for Nathan Stevenson — March 7, 2026**

---

## Executive Summary

This document is the playbook for launching a **new Registered Investment Advisor** that leverages everything you've already built at ForwardLane — the NL→SQL signal engine, the 150+ model Django backend, the Invesco relationships — plus a handpicked stack of best-in-class modern wealth tech. The thesis: **most RIAs are running on 10-year-old tech. You can launch one with an AI-native operating system from day one.**

The opportunity window is ideal. SEC is proposing to raise the "small entity" AUM threshold from $25M to $1B. AI tools like Jump have raised $105M proving the market wants intelligence layers. And your ForwardLane platform already does things most RIAs dream about.

---

## Part 1: Regulatory Foundation

### SEC vs. State Registration

| Factor | State Registration | SEC Registration |
|---|---|---|
| **AUM Threshold** | Under $100M RAUM | $100M+ RAUM (mandatory at $110M) |
| **Florida** | FINRA/state via IARD | Standard SEC process |
| **Timeline** | 30-45 days | 45-day SEC review window |
| **Cost** | ~$200-500 state fees | SEC fees based on AUM |

**Recommendation:** Start with **state registration in Florida** (faster, cheaper, simpler). You can elect SEC registration if you operate in 15+ states or expect to cross $100M within 120 days.

### Required Steps

1. **Form legal entity** — LLC in Florida (or Delaware LLC with FL qualification)
2. **Create IARD account** — Investment Adviser Registration Depository
3. **Appoint CCO** — Chief Compliance Officer (can be you initially)
4. **File Form ADV** — Parts 1A, 2A (brochure), 2B (supplements), 3 (CRS)
5. **File Form U4** — For each Investment Adviser Representative
6. **Written compliance program** — Policies covering portfolio management, privacy, marketing, business continuity
7. **Cybersecurity program** — Mandatory under Reg S-P amendments (June 3, 2026 deadline for smaller RIAs)

### Key 2026 Compliance Dates
- **March 31** — Annual Form ADV amendment deadline (Dec fiscal year)
- **April 30** — Annual Part 2A delivery to clients
- **June 3** — Reg S-P cybersecurity compliance for smaller RIAs
- **October 1** — Form PF new reporting requirements effective

### Estimated Startup Costs (Regulatory)

| Item | Cost |
|---|---|
| LLC formation (FL/DE) | $500-2,000 |
| IARD registration fees | $200-500 |
| E&O Insurance | $2,000-5,000/yr |
| Compliance consultant (Form ADV prep) | $5,000-15,000 |
| Cybersecurity setup & audit | $3,000-10,000 |
| **Total regulatory startup** | **$10,700-32,500** |

---

## Part 2: The ForwardLane Advantage

### What You Already Have (That Other New RIAs Don't)

| Capability | Status | Competitive Edge |
|---|---|---|
| **NL→SQL Signal Engine** | Live, tested on Invesco schema | Most RIAs can't generate signals at all — you do it for $0.01/query |
| **150+ Django Models** | Production on Railway | Years of domain modeling already done |
| **DataScience Recommendation** | ML scores per advisor | Personalized advice at scale |
| **Signal Builder** | Graph→SQL compiler | Visual signal creation — unique in the market |
| **Invesco Relationship** | $300K account, demo live | Instant credibility + revenue |
| **Data Waterfall Pipeline** | Code complete, 7 providers | Lead enrichment that rivals dedicated platforms |
| **Honey AI Network** | 48 models, 9 cron jobs, self-healing | AI operations backbone no startup RIA has |
| **NarrativeReactor** | Building | AI-generated client narratives from signals |

### OpenFlow Integration Points

The OpenFlow workflow engine can power:
- **Client onboarding automation** — Multi-step KYC/AML flows
- **Signal-triggered alerts** — When portfolio signals fire, auto-generate advisor briefs
- **Compliance workflow** — Automated 4-eyes approval, audit trails
- **Rebalancing triggers** — Signal→decision→trade execution pipeline

---

## Part 3: The AI-Native Tech Stack

### Tier 1: Core Infrastructure (Must-Have Day 1)

#### Custodian → **Schwab or Altruist**

| | Schwab | Altruist |
|---|---|---|
| **AUM Minimum** | None | None |
| **Best For** | Credibility, breadth | Modern tech, cost |
| **Key Feature** | Advisor ProDirect (for $50-300M firms) | All-in-one digital platform |
| **Trading** | iRebal included | Built-in automated rebalancing |
| **Client Referrals** | Yes | No |
| **Cost** | No custody fees | No custody fees |

**Recommendation:** **Dual custody — Schwab (primary) + Altruist (tech-forward)**. Schwab for credibility and referrals, Altruist for clients who want a modern digital experience. Many RIAs are going multi-custodial in 2026.

#### CRM → **Lightfield + Wealthbox**

**Lightfield** (AI-native CRM):
- Founded by Keith Peiris and Henri Liriani (2020), $25M+ users from Tomes
- "CRM that runs itself" — auto-captures emails, calls, meetings
- Schema-less design, "customer memory" without manual entry
- Agentic workflows: auto-draft outreach, update pipeline, flag stalled deals
- Best for: your internal ops, founder-led selling, pipeline management

**Wealthbox** (advisor-specific CRM):
- Purpose-built for financial advisors
- Modern UI, easy onboarding
- Deep integrations with Schwab, Fidelity, Orion, MoneyGuide
- Compliance-ready activity logging
- Best for: advisor-facing workflows, compliance, industry integrations

**Why both?** Lightfield is your intelligence layer (it's where Honey and the AI agents operate). Wealthbox is your compliance-grade advisor CRM that integrates with custodians.

#### Portfolio Management → **Orion Advisor Tech**

- Unified platform: portfolio accounting, trading, reporting, billing
- Owns Redtail CRM (integrations are seamless)
- Client portal included
- Compliance tools built in
- Strong API for custom integrations (connect to your ForwardLane backend)
- Cost: ~$4,000-8,000/yr for a small firm

#### Financial Planning → **RightCapital or eMoney**

| | RightCapital | eMoney |
|---|---|---|
| **Best For** | Modern, intuitive plans | Comprehensive, enterprise |
| **Client Experience** | Excellent portal | Industry standard |
| **Cost** | ~$2,400/yr | ~$4,200/yr |
| **Integrations** | Orion, Schwab, Addepar | Envestnet ecosystem |

**Recommendation:** **RightCapital** — modern, lower cost, great client portal. Upgrade to eMoney when AUM justifies it.

---

### Tier 2: Intelligence & Enablement Layer

#### AI Meeting Assistant → **Jump**

Jump is the clear winner here:
- **27,000+ advisors**, $105M raised (Series B Feb 2026)
- AI meeting prep, note-taking, conversation summaries, follow-up drafts
- **Auto-updates CRM** after meetings
- Compliance-grade: SOC 2, configurable supervision policies
- Integrates with Salesforce, Wealthbox, Redtail, Zoom, Teams
- Saves 1-2 hours/day per advisor
- "Wealthtech Startup of the Year" (Oct 2024), "Best in Show" at WM EDGE

**This is your note-taking solution.** Jump handles meeting capture → summary → CRM update → follow-up draft in one flow. Kills the need for separate note-taking apps.

#### Financial Visualization → **Asset-Map**

- Transforms complex financial data into single-page visual maps
- Shows assets, liabilities, income, goals in one intuitive view
- Integrates with Orion, MoneyGuidePro, Morningstar, Riskalyze
- Perfect for **first meetings** — instantly builds trust and rapport
- Helps advisors spot gaps and missing info before deep planning
- Clients actually understand their finances (novel concept)

**Use case:** Every prospect meeting starts with an Asset-Map. It's the "wow moment" that differentiates you from every other RIA showing pie charts.

#### Portfolio Analytics (Complex/HNW) → **Addepar**

- Cloud-based, handles alternatives, PE, VC, real estate, trusts
- "Addison" AI: natural language portfolio queries (sound familiar? Like your NL→SQL...)
- $5T+ in assets on platform
- Open API, 100+ integrations
- SOC 3 compliant
- Best for: HNW clients with complex multi-entity structures

**When to add:** Once you have HNW clients with alternative assets. Overkill for vanilla portfolios — that's what Orion handles.

#### Sales Enablement → **Seismic**

- Leader in financial services enablement (400+ firms)
- AI-powered content management, compliance-focused
- Personalized client materials auto-generated from CRM/portfolio data
- Training, coaching, content creation in one platform
- **Merging with Highspot** (2025 announcement) — combined powerhouse

**Alternative:** If Seismic is too expensive at launch, start with **HubSpot Sales Hub** for pipeline management and graduate to Seismic when you have a team.

---

### Tier 3: Differentiation Layer (Your Moat)

This is where ForwardLane's existing tech becomes your unfair advantage:

#### NL→SQL Signal Engine (ForwardLane)
- No other RIA has natural language signal generation
- Advisors type "show me clients with >$500K in equities who haven't been contacted in 90 days" → get actionable lists
- Cost: $0.01 per query vs. hiring data analysts

#### NarrativeReactor (Building)
- AI-generated personalized client narratives from portfolio signals
- "Here's what happened in your portfolio this quarter and why it matters"
- Automated, personalized, compliant

#### Data Waterfall (Lead Enrichment)
- 7-provider enrichment pipeline
- Every prospect gets auto-enriched before first meeting
- Advisor walks in knowing the client's full financial picture

#### Honey AI Network (Backbone)
- 48 models, autonomous operations
- Daily judge swarms scoring portfolio health
- Self-healing infrastructure
- This becomes the **AI operating system** for the RIA

---

## Part 4: Complete Stack Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                          │
│  Schwab Portal │ Altruist App │ RightCapital │ Asset-Map│
└───────────┬─────────────────────────────────────────────┘
            │
┌───────────▼─────────────────────────────────────────────┐
│                  ADVISOR LAYER                           │
│  Wealthbox CRM │ Orion Portfolio │ Jump Notes │ Seismic │
└───────────┬─────────────────────────────────────────────┘
            │
┌───────────▼─────────────────────────────────────────────┐
│              INTELLIGENCE LAYER (ForwardLane)            │
│  NL→SQL Engine │ Signal Builder │ NarrativeReactor      │
│  Data Waterfall │ DataScience Recommendation Model      │
└───────────┬─────────────────────────────────────────────┘
            │
┌───────────▼─────────────────────────────────────────────┐
│               OPERATIONS LAYER                           │
│  Lightfield CRM │ Honey AI Network │ OpenFlow Workflows │
│  Django Backend │ Railway Infrastructure │ Redis/Celery  │
└─────────────────────────────────────────────────────────┘
```

---

## Part 5: Competitive Landscape

### How This RIA Is Different

| Traditional RIA | Your AI-Native RIA |
|---|---|
| Manual CRM data entry | Lightfield auto-captures everything |
| Quarterly PDF reports | Real-time NarrativeReactor briefs |
| Excel-based signals | NL→SQL in natural language |
| Generic client outreach | Data Waterfall enriched, personalized |
| Advisor-dependent insights | AI-generated recommendations 24/7 |
| One meeting prep = 2 hours | Jump + Asset-Map = 15 minutes |
| Annual compliance review | Continuous automated compliance |
| Single custodian | Multi-custodial (Schwab + Altruist) |

### Comparable Firms / Inspiration

| Firm | AUM | Differentiator | Lesson |
|---|---|---|---|
| **Ritholtz Wealth** | $5B+ | Content-led growth (blog, podcasts) | Build in public → attract assets |
| **Creative Planning** | $300B+ | Comprehensive (tax, legal, estate) | Breadth wins at scale |
| **Facet** | $3B+ | Flat-fee, tech-forward | Subscription model resonates |
| **Savvy Wealth** | Growing | AI-native from inception | Proof the AI-RIA thesis works |
| **Altruist** (custodian-turned-advisor-enabler) | — | Built tech first, then enabled advisors | Your playbook |

---

## Part 6: Revenue Model & Growth Path

### Phase 1: Launch (Months 1-6)
- **AUM Target:** $10-25M
- **Clients:** 20-50 households
- **Revenue Model:** 1% AUM fee (standard), declining at scale
- **Revenue:** $100K-250K/yr
- **Team:** Nathan + 1 operations hire + Honey
- **Focus:** Invesco conversion, ForwardLane client upsell, personal network

### Phase 2: Scale (Months 7-18)
- **AUM Target:** $50-100M
- **Clients:** 100-200 households
- **Revenue:** $500K-1M/yr
- **Add:** Addepar for HNW, Seismic for sales enablement
- **Focus:** Content marketing (NarrativeReactor-powered), referral programs

### Phase 3: Differentiate (Months 18-36)
- **AUM Target:** $100-250M
- **Revenue:** $1-2.5M/yr
- **Move to SEC registration**
- **License ForwardLane tech to other RIAs** (SaaS revenue stream)
- **Hire advisors** who want to work with the best tech stack in the industry

---

## Part 7: Additional Platforms to Evaluate

### Wealth Enablement Platforms

| Platform | What It Does | Relevance |
|---|---|---|
| **Envestnet | Tamarac** | End-to-end wealth management (reporting, rebalancing, CRM) | Alternative to Orion if you want Envestnet ecosystem |
| **Black Diamond (SS&C)** | Portfolio management & reporting for HNW | If Addepar is overkill |
| **Riskalyze (now Nitrogen)** | Risk tolerance scoring, portfolio alignment | Great for prospect conversion — quantify risk tolerance |
| **Holistiplan** | Tax planning analysis from PDF tax returns | Instant tax planning insights, differentiator in client meetings |
| **Conquest Planning** | Goals-based financial planning | Integrated into Pershing's "Wove" platform |
| **fpPathfinder** | Decision flowcharts for financial planning | Quick reference during client meetings |

### Sales Enablement Platforms (Beyond Seismic)

| Platform | Best For | Key Feature |
|---|---|---|
| **Highspot** | AI-powered content surfacing | Merging with Seismic |
| **Allego** | Revenue enablement + coaching | Digital Sales Rooms, AI roleplay |
| **Gong** | Conversation intelligence | Records/analyzes every call |
| **Showpad** | Content management + guided selling | Merged with Bigtincan |

### Note-Taking Alternatives (If Not Jump)

| Platform | Best For | Key Feature |
|---|---|---|
| **Grain** | Meeting recording + highlights | AI-clips key moments |
| **Fireflies.ai** | Transcription + CRM sync | Affordable, wide integrations |
| **Otter.ai** | Real-time transcription | Consumer-friendly, good mobile |
| **Copilot (Microsoft)** | Teams-native note-taking | If you're in Microsoft ecosystem |

**Recommendation:** Jump is purpose-built for wealth management. The others are generalists.

### Data & Research

| Platform | What It Does |
|---|---|
| **Morningstar** | Investment research, fund analysis |
| **YCharts** | Data visualization, client reporting |
| **Kwanti** | Monte Carlo simulations, portfolio proposals |
| **Hidden Levers** | Stress testing, scenario analysis |

---

## Part 8: Five Immediate Next Steps

### 1. Entity Formation & Registration (~2 weeks)
- Form FL LLC
- Open IARD account
- Hire compliance consultant for Form ADV
- Budget: $8-15K

### 2. Custodian Agreement (~2-4 weeks)
- Apply to Schwab (primary) — no minimums, use Advisor ProDirect
- Apply to Altruist (secondary) — no minimums, digital-first
- Both can run in parallel

### 3. Core Tech Setup (~2 weeks)
- Wealthbox CRM (advisor layer)
- Lightfield (intelligence layer)
- Orion or Altruist built-in portfolio management
- Jump (meeting intelligence)
- RightCapital (financial planning)
- Asset-Map (client visualization)

### 4. ForwardLane Integration (~ongoing)
- Connect NL→SQL engine to Orion portfolio data
- Build Signal→Alert→Advisor Brief pipeline via OpenFlow
- Connect Data Waterfall to Wealthbox for prospect enrichment
- Deploy NarrativeReactor for automated client communications

### 5. First Clients (~Month 1-2)
- Convert Invesco relationship into anchor client
- Personal network outreach
- ForwardLane existing client upsell
- Content strategy powered by NarrativeReactor

---

## Part 9: Risk Factors

| Risk | Mitigation |
|---|---|
| **Regulatory complexity** | Hire compliance consultant, use Orion compliance tools |
| **AUM too low to be profitable** | Flat-fee model as supplement (like Facet), license tech as SaaS |
| **Over-engineering the tech stack** | Launch with Tier 1 only, add Tier 2/3 based on AUM milestones |
| **Key person risk (Nathan)** | Document everything, Honey maintains continuity, hire early |
| **Custodian concentration** | Multi-custodial from day 1 |
| **Cybersecurity breach** | SOC 2 infrastructure, Railway private networking, Reg S-P compliance |

---

## Appendix: Estimated Annual Tech Costs

| Tool | Annual Cost | Tier |
|---|---|---|
| Wealthbox CRM | $1,800 | 1 |
| Orion Advisor Tech | $5,000 | 1 |
| RightCapital | $2,400 | 1 |
| Jump | $3,600 | 1 |
| Asset-Map | $1,800 | 1 |
| Lightfield | $2,400 | 2 |
| Schwab custody | $0 | 1 |
| Altruist custody | $0 | 1 |
| Railway (ForwardLane infra) | $3,600 | 3 |
| **Subtotal (Launch)** | **~$20,600/yr** |
| Addepar (add at $50M+) | $15,000+ | 2 |
| Seismic (add with team) | $12,000+ | 2 |
| Nitrogen/Riskalyze | $5,000 | 2 |
| **Full stack** | **~$52,600/yr** |

This is remarkably lean for an RIA tech stack. Most established RIAs spend $50-100K/yr on worse technology.

---

---

## Part 10: ForwardLane Platform → RIA Operations Mapping

This section maps every major ForwardLane capability to a specific RIA operational function — showing exactly how the existing platform replaces or augments tools other RIAs have to buy separately.

### Client Acquisition & Onboarding

| RIA Need | ForwardLane Capability | What It Replaces |
|---|---|---|
| **Prospect enrichment** | Data Waterfall Pipeline (7 providers, cost-priority waterfall, Redis+DB caching) | LeadIQ ($500/mo), ZoomInfo ($15K/yr) |
| **Prospect scoring** | DataScienceRecommendation model — ML scores by advisor affinity | Manual qualification |
| **Lead routing** | Client-advisor matching via `UserClient` + `OrganizationTeam` models | CRM lead assignment rules |
| **Onboarding workflow** | OpenFlow + Pipeline Engine (`PipelineService`, `PipelineServiceBinding`) | DocuSign workflows, manual checklists |
| **KYC data capture** | Content Ingestion pipeline → entity extraction → auto-populate client records | Manual data entry |

### Portfolio Intelligence (The Core Moat)

| RIA Need | ForwardLane Capability | What It Replaces |
|---|---|---|
| **Portfolio monitoring** | 150+ models: `Holding`, `FinancialAccount`, `Transaction`, `AssetsUnderManagement`, `HoldingsAggregation`, `TransactionsAggregation` | Orion reporting ($5K/yr) |
| **Signal generation** | NL→SQL engine: "clients with >$500K equities not contacted in 90 days" → executable query at $0.01 | Data analysts ($80K+/yr) |
| **Visual signal building** | Signal Builder frontend — drag-and-drop graph nodes → SQL | Nothing comparable exists |
| **Signal library** | Templates marketplace — reusable signals across the org | Custom queries rebuilt every time |
| **Market data overlay** | Morningstar integration (ETFs, mutual funds, SMAs, UITs), `SectorPerformance`, `EquitiesCorpAction` | Morningstar Direct ($15K/yr) — you already have the data models |
| **Product matching** | `Product`, `Fund`, `Instrument`, `ApprovedInstrument` + Business Rules engine | Manual product due diligence |

### Advisor Productivity

| RIA Need | ForwardLane Capability | What It Replaces |
|---|---|---|
| **Next Best Action** | `NBAction` + `BusinessRule` + `DataScienceRecommendation` → "Call this client because [reason], suggest [action]" | Salesforce Einstein ($$$), manual prioritization |
| **Meeting prep** | Client ranking engine (`ClientRankingHistory`) + portfolio summary (`AdvisorPortfolioSummary`) + signal alerts → auto-generated brief | 2 hours of manual prep per meeting |
| **Client prioritization** | Client Ranking Engine — scores every client by: AUM, activity recency, churn risk, opportunity signals | Gut feeling |
| **Document intelligence** | Content Ingestion → NER → Topic Modeling → Document Ranking → per-advisor relevance scoring | Reading every research note manually |
| **Auto-summarization** | `DocumentMetaSummarization` — AI summaries of market commentary, product updates | Analyst teams |
| **Activity tracking** | `CrmActivity`, `CrmCallNote`, `CrmEmail`, `CrmNote`, `UserBehavior`, `AdvisorWebpageVisit` | CRM manual logging |
| **Easy Button (Salesforce)** | One-click actions embedded in Salesforce — meeting prep, client brief, signal check | Context-switching between 5 tools |

### Client Communication & Reporting

| RIA Need | ForwardLane Capability | What It Replaces |
|---|---|---|
| **Personalized narratives** | NarrativeReactor (building) — AI-generated client briefs from portfolio signals | Generic quarterly letters |
| **Campaign management** | `Campaign`, `ClientCampaign` models — track outreach, measure response | Mailchimp/HubSpot ($500/mo) |
| **Client segmentation** | `ClientSegment`, `Segmentation` models — dynamic cohorts based on any signal | Static CRM tags |
| **Churn prediction** | `Churn` model — ML-powered risk scoring | Surprise client departures |
| **Feedback loops** | `Feedback`, `LikedNBA` — track what advisors actually use, improve recommendations | No feedback → no improvement |

### Compliance & Risk

| RIA Need | ForwardLane Capability | What It Replaces |
|---|---|---|
| **Audit trail** | `audit/` module in Signal Builder — every action logged with HMAC-signed webhooks | Separate compliance software ($3-5K/yr) |
| **Access control** | `AccessGuardianCustomGroup/Permission/PermissionsSet` — granular RBAC | Basic CRM permissions |
| **Business rule enforcement** | `BusinessRule`, `BusinessRuleCollection`, `BusinessRuleParameter` — codified compliance rules | Manual compliance review |
| **Data source governance** | `DataSource`, `DataSourceLocation`, `DataSourceOrganizationBinding` — track every data origin | Spreadsheets |
| **Login/behavior auditing** | `LoginHistory`, `UserAuditHistory`, `UserBehavior` | SEC exam scramble |

### Multi-Tenant Architecture (Scale to Multiple RIAs)

| Capability | How It Works |
|---|---|
| **Organization isolation** | `Organization`, `OrganizationPreferences`, `OrganizationRegion` — each RIA is a tenant |
| **Per-org schema config** | `schema_builder/` in Signal Builder — each org can have different data schemas |
| **Per-org data sources** | `DataSourceOrganizationBinding` — data sources bound per tenant |
| **Per-org business rules** | `BusinessRuleOrganizationBinding` — rules customized per org |
| **Per-org import jobs** | `OrganizationImportJobBinding` — separate ETL per tenant |
| **Per-org job configs** | `OrganizationJobConfig` — batch job settings per org |

**This is crucial.** The platform is already built for multi-tenancy. You can run your own RIA as one org and license the platform to other RIAs as separate orgs — all on the same infrastructure.

---

### The Cost Replacement Math

| What Other RIAs Pay For | Annual Cost | ForwardLane Equivalent |
|---|---|---|
| Orion portfolio management | $5,000-8,000 | Built-in (150+ portfolio models) |
| Morningstar Direct | $15,000 | Data models already integrated |
| Data enrichment (ZoomInfo/LeadIQ) | $6,000-15,000 | Data Waterfall Pipeline |
| Salesforce Einstein analytics | $25,000+ | DataScienceRecommendation + NBA |
| Compliance software | $3,000-5,000 | Audit module + Access Guardian |
| Data analyst(s) | $80,000-120,000 | NL→SQL engine ($0.01/query) |
| Document summarization service | $5,000-10,000 | Content Ingestion + Summarization |
| Client communication platform | $2,000-6,000 | NarrativeReactor + Campaign models |
| **Total replaced** | **$141,000-189,000/yr** | **Already built** |

The platform you already own replaces **~$150K/yr in software costs** that a typical RIA would have to buy. And it does things (NL→SQL, visual signal building, ML-powered NBA) that no amount of money can buy off the shelf.

---

### Integration Architecture: ForwardLane + External RIA Stack

```
┌─────────────────────────────────────────────────────────────┐
│              EXTERNAL (Buy/License)                          │
│                                                             │
│  Schwab/Altruist  ←→  Custodian data sync                  │
│  Jump             ←→  Meeting notes → CRM sync             │
│  Asset-Map        ←→  Portfolio visualization               │
│  RightCapital     ←→  Financial planning models             │
│  Wealthbox        ←→  Advisor-facing CRM                   │
│  Lightfield       ←→  AI-native ops CRM                    │
└─────────────┬───────────────────────────────────────────────┘
              │  APIs / Webhooks / Data Sync
┌─────────────▼───────────────────────────────────────────────┐
│           FORWARDLANE INTELLIGENCE LAYER                     │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ OpenFlow     │  │ Signal       │  │ Data Waterfall    │  │
│  │ Orchestrator │  │ Engine       │  │ Enrichment        │  │
│  │              │  │ (NL→SQL)     │  │ (7 providers)     │  │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────────┘  │
│         │                │                  │               │
│  ┌──────▼──────────────────▼──────────────────▼──────────┐  │
│  │              Django Backend (150+ Models)              │  │
│  │  Portfolio │ Ranking │ NBA │ ML │ Documents │ CRM     │  │
│  └──────┬────────────────────────────────────────────────┘  │
│         │                                                   │
│  ┌──────▼────────────────────────────────────────────────┐  │
│  │         Signal Studio (Next.js 15 Frontend)           │  │
│  │  Signal Builder │ Easy Button │ Agent │ Analytics     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          Honey AI Network (Backbone)                   │  │
│  │  48 models │ 9 cron jobs │ Judge swarms │ Self-heal   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Key Integration Flows

**1. New Prospect → Client**
```
Lead captured in Lightfield
  → Data Waterfall enriches (7 providers)
  → ML model scores advisor fit
  → Routed to best advisor in Wealthbox
  → Asset-Map generated for first meeting
  → Jump captures meeting notes
  → Notes → CRM → ForwardLane client record created
  → Onboarding workflow triggered via OpenFlow
  → Custodian account opened (Schwab/Altruist API)
```

**2. Ongoing Client Intelligence**
```
Custodian data syncs nightly
  → Holdings/transactions update in ForwardLane
  → Signal Engine scans for triggers
  → "Client X: equity concentration >40%, hasn't rebalanced in 6 months"
  → NBA generated: "Call Client X, recommend diversification"
  → Easy Button surfaces in advisor's Salesforce
  → Advisor clicks → pre-built meeting prep brief
  → Jump captures the call
  → NarrativeReactor generates follow-up summary
  → Sent to client via campaign engine
```

**3. Quarterly Review Automation**
```
Signal Engine: "Generate Q1 portfolio reviews for all clients"
  → NarrativeReactor creates personalized narratives per client
  → Document Ranking surfaces relevant market commentary
  → RightCapital financial plan updated
  → Advisor reviews in Signal Studio
  → One-click send to all clients
  → Activity logged, compliance trail created
```

**4. Platform-as-a-Service (License to Other RIAs)**
```
New RIA signs up
  → New Organization tenant created
  → Schema Builder configures their data model
  → Data sources connected per org
  → Business rules customized
  → Their advisors get Signal Studio + Easy Button
  → You earn SaaS revenue while they get best-in-class tech
```

---

*This document is a living research brief. Updated as new information emerges.*
*Saved to: `/data/workspace/docs/ria-deep-research.md`*
