# Executive Summary: AI CRM Research
*March 2026 | Freya (GTM & Analysis) | For Nathan Stevenson / ForwardLane & SignalHaus*

---

## The Bottom Line (Read This First)

**You don't need to buy Lightfield. You need to connect what you already have.**

Signal Studio (NL→SQL), Data Waterfall (enrichment), n8n (automation), and Railway (infra) are already in place. The missing piece is a CRM that's **API-first, PostgreSQL-native, and deployable on Railway** — so all three can talk to each other. That CRM is **Twenty CRM** (open-source, 40K GitHub stars, official Railway template, $0 licensing cost).

Add **Apollo.io** ($49/user/mo) for intent signals and buying alerts, and you have a GTM intelligence stack that rivals $2,000/mo SaaS tools at ~$440/mo total.

---

## The Three Options (Ranked)

### 🥇 Option 1: The Hybrid Build (Recommended)
**Twenty CRM (self-hosted) + Apollo.io + Signal Studio integration**
- Monthly cost (3 users): ~$440/mo
- Data ownership: 100%
- Signal Studio integration: Native (PostgreSQL → PostgreSQL)
- Setup time: 3-4 weeks
- Scalability: Unlimited users, cost stays flat

### 🥈 Option 2: Best SaaS
**Attio Pro + Apollo.io**
- Monthly cost (3 users): ~$354/mo
- Data ownership: Vendor-controlled
- Signal Studio integration: Good (webhooks)
- Setup time: 1 week
- AI out-of-box: Yes

### 🥉 Option 3: Stay HubSpot
**HubSpot Professional + Apollo.io**
- Monthly cost (3 users): ~$447/mo
- Data ownership: HubSpot-controlled
- Signal Studio integration: OK (webhooks)
- Setup time: 2-3 days
- Risk: Growing cost, manual data entry persists

---

## Lightfield: What It Is and Why We're Watching It

Lightfield is a genuinely impressive AI-native CRM built by the Tome team. Key features:
- **Zero-entry CRM**: Auto-captures email, calendar, Slack, meetings — no manual logging
- **NL querying**: Ask natural language questions about your deals/customers
- **Deal revival**: Auto-detects dormant deals and prompts re-engagement
- **Startup tier**: $36/user/mo but **5-user minimum = $180/mo** even for a 2-person team

**Why we're not recommending it now:**
1. 5-user minimum is expensive for a 2-5 person team
2. Integration ecosystem is immature (limited API documentation)
3. Quiet funding story = longevity risk
4. You can replicate its NL querying using Signal Studio + Twenty CRM (which you already have most of)

**Revisit:** When the team reaches 5+ users and the ecosystem matures (6-12 months).

---

## The AI CRM Landscape at a Glance

| Category | Winner | Why |
|----------|--------|-----|
| Best AI-Native SaaS CRM | **Attio** | Best API, AI attributes, GraphQL, flexible data model |
| Best Zero-Entry CRM | **Lightfield** | Auto-capture from all channels is genuinely magical |
| Best Open-Source CRM | **Twenty CRM** | 40K GitHub stars, Railway template, modern stack |
| Best Signal Intelligence | **Apollo.io** | Best value: database + intent signals + sequences |
| Best Enrichment Platform | **Clay** | 150+ providers, Claygent AI, but expensive |
| Best Enterprise CRM | **Salesforce** | Most powerful but wildly overpriced for this stage |
| Best PLG Signal Tool | **Pocus** | Product usage signals, but requires PLG motion |
| Worst Fit (overkill) | **Salesforce / Unify** | Way too expensive, enterprise-focused |

---

## Critical Gaps in Current Stack

1. **No auto-capture**: HubSpot Free requires manual updates → data is perpetually stale
2. **No signal intelligence**: No alerts for funding, job changes, website visits, G2 reviews
3. **Fragmented context**: Deal info lives in Slack, Drive, HubSpot, Asana — never unified
4. **No AI outreach**: Data Waterfall enrichment isn't connected to personalized outreach
5. **Motion + Asana overlap**: Tool sprawl causing context switching and wasted time
6. **No pipeline analytics**: Can't answer "what's working?" without manual spreadsheet analysis

**The most expensive gap** (by opportunity cost): Missing buying signals = missing perfect moments to engage = potentially $50K+ in lost deals per year.

---

## The Secret Weapon Nobody's Discussing

Signal Studio already does NL→SQL over business data. **If CRM data lives in PostgreSQL (which Twenty CRM uses), then Signal Studio can answer sales questions immediately:**

- *"Which accounts went dark in the last 14 days?"*
- *"Show me all companies in our ICP with open deals over $100K"*
- *"Which leads from this quarter's enrichment are at Series B companies in fintech?"*

This is Lightfield's core AI value proposition — but Nathan already has 80% of the infrastructure to build it. The 20% gap is deploying Twenty CRM and syncing its database to Signal Studio.

---

## Immediate Actions (Next 7 Days)

1. **Sign up for Apollo.io Basic** ($49/user/mo) — get intent signals immediately, regardless of CRM decision
2. **Deploy Twenty CRM on Railway** using the one-click template — takes 30 minutes
3. **Export HubSpot contacts** to CSV and import into Twenty
4. **Test Signal Studio** with a query against a small sample of deal data to validate the NL→SQL approach

---

## Open-Source CRM Rankings for Self-Hosting

| Rank | Tool | GitHub Stars | Railway Template | PostgreSQL | Nathan Fit |
|------|------|-------------|-----------------|------------|-----------|
| 1 | Twenty CRM | 40K | ✅ Official | ✅ | ⭐⭐⭐⭐⭐ |
| 2 | Odoo Community | 40K | ✅ Official | ✅ | ⭐⭐⭐ |
| 3 | ERPNext | 23K | ✅ Official | ⚡ | ⭐⭐ |
| 4 | Huly | 18K | Via Docker | ❌ (MongoDB) | ⭐⭐⭐ |
| 5 | SuiteCRM | 5.3K | Via Docker | ❌ (MySQL) | ⭐⭐ |
| 6 | EspoCRM | 2.8K | Via Docker | ❌ (MySQL) | ⭐⭐ |

---

## Files in This Research Package

| File | Contents |
|------|---------|
| `executive-summary.md` | This file — top-line findings |
| `lightfield-ai-deep-dive.md` | Everything on Lightfield |
| `ai-crm-landscape.md` | All AI CRMs compared in depth |
| `opensource-crm-landscape.md` | All open-source options in depth |
| `comparison-matrix.md` | Side-by-side feature/cost matrix |
| `gap-analysis.md` | What we're missing with current stack |
| `recommendation.md` | Final recommendation with architecture |
| `tool-pricing.md` | Detailed pricing for all options |

---

*Research completed March 2026 | Total tools researched: 25+ | Sources: G2, Capterra, GitHub, pricing pages, reviews, technical documentation*
