# Lightfield AI CRM — Deep Dive Research
*Research date: March 2026 | Compiled by Freya (GTM & Analysis)*

---

## Overview

Lightfield is an **AI-native CRM** that emerged from the ashes of Tome — the presentation tool that amassed 25M+ users before its founders pivoted. This heritage gives Lightfield credibility: the team knows how to build viral, user-friendly software at scale. It positions itself as the antithesis of traditional CRMs like Salesforce and HubSpot — the "zero-entry CRM" where data capture happens automatically and intelligence is baked in from day one.

**Tagline:** *"Complete customer memory. Zero manual data entry."*

---

## Who Built It

- **Founded:** ~2024 by the team behind Tome (presentation AI that raised $43M, reached 25M users)
- **Founders:** Previously built Tome, a heavily-funded AI presentation tool
- **Positioning:** Built specifically for the problems the Tome team experienced in their own founder-led sales motion
- **Funding:** Notably quiet about funding announcements — unusual for a startup in this space
- **Target:** Startups, founder-led sales, small B2B revenue teams (2-25 people)

---

## Core Features

### 1. Zero-Entry CRM (The Big Idea)
- Automatically ingests data from: emails, calendar events, Slack messages, meeting transcripts, support tickets
- Builds a comprehensive, searchable history for every account and contact
- Can **backfill up to 2 years of historical data** — massive advantage if migrating from another CRM
- Schema-less data model: captures everything now, evolves the structure later

### 2. Natural Language Intelligence Layer
- Ask questions in plain English: *"How has our ICP changed this quarter?"* or *"Which customers asked for this feature and why?"*
- Receives real-time answers with citations to original conversations
- Essentially NL→SQL but over your CRM data — directly relevant to Nathan's Signal Studio work
- This is conversational analytics over customer relationship data

### 3. Automated Workflow Execution
- Automates routine tasks, suggests next steps
- Updates CRM records based on conversation analysis
- Drafts personalized follow-up emails
- Summarizes conversations
- Updates pipeline stages automatically
- Identifies and re-engages dormant deals

### 4. Meeting Intelligence
- Records and transcribes all calls
- Converts transcripts to summaries and action items
- Eliminates manual note-taking
- Ensures follow-ups are timely and context-rich

### 5. Automated Data Enrichment
- Fills in missing data across the CRM
- Enriches accounts and contacts automatically
- Not clear what providers power this vs. building in-house

### 6. Personalized Bulk Outreach
- Drafts and sends personalized outreach based on past discussions with each prospect
- Leverages both structured and unstructured data
- Scales the "founder-led sales" feel to dozens of prospects simultaneously

---

## Pricing (as of early 2026)

| Plan | Price | Key Features | Limits |
|------|-------|-------------|--------|
| **Free** | $0/user/mo (forever) | Essential features, no credit card needed | Limited records/events |
| **Startup** | $36/user/mo (monthly) | Call intelligence, automated enrichment, unlimited agent queries, configurable data model | 10K records, 1K workflow events/mo |
| **Pro** | $99/user/mo (annual) | Advanced permissions, higher limits, white-glove migration, dedicated CSM | 50K records, 10K workflow events/mo |
| **Enterprise** | Custom | Min 50 user licenses | Custom limits |

**Key pricing notes:**
- Paid plans require purchasing **at least 5 user licenses** (minimum commitment)
- Startup plan includes a **dedicated Slack channel for support** — great for small teams
- Pro plan includes white-glove migration — helpful if switching from HubSpot

**For Nathan's team (2-5 people):**
- Startup: 5 licenses × $36 = **$180/mo** (minimum)
- Pro: 5 licenses × $99 = **$495/mo** annual

---

## AI Capabilities — What It Actually Does

### What Works Well:
1. **Auto-capture** is genuinely differentiated — no other CRM does this as cleanly for small teams
2. **NL querying over your CRM data** — directly addresses the "I can't find context fast enough" problem
3. **Deal revival** — detecting dormant deals and prompting re-engagement (users report 50% faster deal closure)
4. **Context preservation** — full conversation history means anyone on the team can pick up a deal without briefing

### What's Limited / Unknown:
1. No clear documentation on what enrichment providers power the data fill
2. Integrations are still limited: Notion, Linear, Granola, Outlook confirmed — broader ecosystem TBD
3. Workflow automation is relatively early vs. HubSpot Professional
4. Limited customization vs. Attio or Salesforce

---

## Integration Capabilities

**Confirmed integrations (as of early 2026):**
- Email (Gmail, Outlook)
- Calendar (Google Cal, Outlook Cal)
- Slack (messages auto-ingested)
- Notion
- Linear
- Granola (meeting notes)
- Plans for 50+ tool integrations

**Notably absent (as of research date):**
- Salesforce sync
- HubSpot migration (except white-glove on Pro)
- Native LinkedIn
- Zapier / n8n webhooks (unclear)
- Custom API (unclear if available on Startup tier)

---

## Reviews & User Feedback

### Positive:
- "Turns hours of manual logging into instant insights" — described as game-changer for startups
- "50% faster deal closure rate" reported by some users (auto-capture + deal revival)
- "Complete customer memory" praised — captures everything from Slack to support tickets
- Natural language querying described as genuinely magical vs. pre-built report hell
- Founding team background from Tome gives confidence in execution quality

### Negative / Concerns:
- **Unusually quiet about funding** — no typical startup announcements; raises questions about longevity
- Support is email-only (no live chat) on lower tiers
- Video onboarding guides for workflow building are sparse
- Some AI summaries need manual tweaking for niche contexts
- **5-user minimum on paid plans** — expensive for solo operator or 2-person team
- Integration ecosystem is still building — not mature enough for complex GTM stacks

---

## How It Compares to Traditional CRMs

| Dimension | Lightfield | HubSpot Free | Attio | Salesforce |
|-----------|-----------|--------------|-------|------------|
| Data entry | Zero (auto) | Manual | Semi-auto | Heavy manual |
| AI depth | Native, core | Bolt-on (Breeze) | Native, configurable | Add-on (Einstein) |
| Setup time | ~1 hour | 1-2 days | Half day | Weeks |
| Customization | Low-medium | Medium (free is limited) | High | Very high |
| Price (small team) | $180/mo min | Free | ~$145/mo (3 users) | $240/mo+ |
| Maturity | Early (2024) | Very mature | Medium (2023) | Very mature |

---

## Target Market & Positioning

- **Primary:** Founder-led sales teams (2-10 people), early-stage B2B startups
- **Secondary:** Small revenue teams (5-25) at seed/Series A/B companies
- **NOT for:** Enterprise, high-customization needs, large sales orgs
- **Key differentiator from HubSpot:** Zero data entry vs. HubSpot's manual logging requirement
- **Key differentiator from Attio:** Less flexible/customizable but much more automated
- **Key differentiator from Salesforce:** Radically simpler, no admin needed

---

## Verdict for Nathan's Use Case

**Fit Score: 7/10**

**Why it fits:**
- Zero-entry CRM means the team's CRM data actually stays current (huge problem with HubSpot Free)
- NL querying of customer data is directly complementary to Signal Studio's NL→SQL approach
- Auto-capture from Slack is relevant given Signal Studio is Slack-connected
- Startup tier at $36/user/mo is reasonable if team grows to 5+

**Why it might not fit:**
- 5-user minimum = $180/mo minimum even for a 2-person team
- Integration ecosystem is immature vs. n8n automation needs
- No clear API documentation for connecting to the Data Waterfall pipeline
- Quiet funding story = some longevity risk for a mission-critical tool
- Customization is limited — may not accommodate SignalHaus's complex deal tracking needs

**Bottom line:** Lightfield is the most compelling "CRM you'll actually use" option for founder-led sales. The auto-capture and NL intelligence features are genuinely differentiated. The risks are ecosystem maturity and longevity. Worth a free trial before any commitment.
