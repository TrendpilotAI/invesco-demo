# Signal-Based List Building — GTM Playbook Extraction
> Extracted for ForwardLane/SignalHaus GTM machine | 2026-03-10
> Source: Notion playbook + Salesmotion + HeyReach + GTM Signal Studio + Starnus

---

## 🎯 TL;DR — What Matters for Us

Signal-based selling is **THE** modern outbound paradigm. It replaces static list-blasting with trigger-driven outreach that achieves **25-40% reply rates** vs 1-5% for cold. The playbook aligns PERFECTLY with what Signal Studio should be doing for ForwardLane clients.

**Our edge:** We already have the NL→SQL engine, the data waterfall enrichment pipeline, and the AI infrastructure. We can build signal detection + action orchestration that most companies cobble together from 5-10 vendors.

---

## 📊 The Numbers That Matter

| Metric | Cold Outbound | Signal-Based |
|--------|--------------|--------------|
| Reply rate | 1-5% | 25-40% |
| Win rate (past champions) | 19% | 37% |
| Conversion rate vs cold | 1x | 3x |
| Deal size (signal-sourced) | baseline | +54% |
| Sales cycle (signal-sourced) | baseline | -12% shorter |
| Budget spent by new execs in first 100 days | — | 70% |
| First-to-contact win rate multiplier | 1x | 5x |

**Key stat:** 84% of B2B buyers have already selected a preferred vendor before they talk to a sales rep (6sense 2025). Speed to signal = competitive moat.

---

## 🏗️ The Signal Hierarchy (Priority Order)

### Tier 1: Highest Converting (Act within 24-72h)
1. **Past Champion Job Change** — 37% win rate, 3x conversion, 114% higher win rates
2. **New Executive Hire (First 100 Days)** — 2.5x higher conversion in first 3 months, 70% of budget spent early
3. **Leadership Change at Pipeline Account** — 5x more likely to win if first to contact

### Tier 2: High Converting (Act within 1 week)
4. **Funding Round / IPO Filing** — Budget unlocked, growth targets set
5. **Technology Stack Change** — Active workflow disruption = buying window

### Tier 3: Supporting Signals (Layer on top)
6. **Hiring Surge** — Directional indicator of growth/investment areas
7. **Website Visit (High-Intent Pages)** — Pricing, comparison, demo pages
8. **Content Engagement** — Whitepapers, webinars, case studies
9. **Product Usage Changes** — First-party expansion/contraction signals

---

## 🔢 Signal Scoring Model

| Signal Type | Points | Example |
|-------------|--------|---------|
| Past champion job change | 10 | Former buyer starts at new company |
| New exec hire (ICP title) | 8 | VP of Sales hired at target |
| Funding/IPO | 7 | Series C announcement |
| Competitor tech removal | 7 | Dropped a rival tool |
| Hiring surge in buyer dept | 5 | 3+ open roles in sales/rev ops |
| Website visit (high-intent) | 4 | Pricing or comparison page |
| Content engagement | 2 | Downloaded whitepaper |

**Action Thresholds:**
- **15+ points** → Immediate AE-led personalized outreach
- **10-14 points** → Priority outreach within 48 hours
- **5-9 points** → Add to nurture sequence with signal-specific messaging
- **Below 5** → Monitor only

---

## 📋 The 5 Signal Plays (Copy-Paste Ready)

### Play 1: Past Champion Job Change
- **Signal:** Former customer/champion starts new role
- **Owner:** AE who held original relationship
- **Channel:** LinkedIn connection + personal email
- **Timing:** Within 72 hours
- **Message:** Congratulate move, reference past success, offer to replicate. No pitch.

### Play 2: New Executive Hire
- **Signal:** VP+ hire at target ICP account
- **Owner:** AE assigned to account
- **Channel:** Email first, LinkedIn second
- **Timing:** Week 2-4 of tenure (let them settle, catch before budget committed)
- **Message:** Reference challenge predecessor faced, share relevant case study, propose 20-min intro

### Play 3: Leadership Change at Pipeline Account
- **Signal:** C-suite/VP change at account with open opportunity
- **Owner:** Current opportunity owner
- **Channel:** Call existing contact + separate outreach to new leader
- **Timing:** Same day
- **Message:** To existing: "How does this affect priorities?" To new leader: Reference initiative in progress

### Play 4: Funding Round
- **Signal:** Series B+, IPO filing, significant debt raise
- **Owner:** AE covering segment
- **Channel:** Email referencing growth plans from announcement
- **Timing:** Within 1 week (before vendor flood)
- **Message:** Connect announced growth goals to specific problem you solve

### Play 5: Tech Stack Change
- **Signal:** Competitor removal, new complementary tech, contract renewal timing
- **Owner:** AE/SDR for competitive displacement
- **Channel:** Email referencing specific tech change
- **Timing:** Within 48 hours
- **Message:** "Noticed you moved off [competitor]. Teams that make that switch usually run into [specific problem]"

---

## 🔄 Signal Stacking — The Multiplier

Single signals are weak. **Stacked signals** are where the magic happens.

**Example stack (22 points = immediate action):**
- New VP of Sales hired (past champion) → +10
- Series B extension closed → +7
- 2 SDR Manager roles posted → +5

**This tells a story:** Company in transition, actively evaluating, budget authority shifting, known champion in the seat.

### For Signal Studio: Build Compound Signal Detection
- Each signal alone = nurture
- 2+ signals stacking on same account = priority
- 3+ signals with champion match = IMMEDIATE action

---

## 🏃 Implementation: Crawl-Walk-Run

### Crawl (Weeks 1-4): Tiger Team
- 2-3 best reps
- ONE signal type (past champion job changes)
- Shared Slack channel for alerts
- Tracking spreadsheet
- Weekly review of response rates
- **Goal:** Proof of concept, not scale

### Walk (Months 2-3): Expand
- Add signal types: new exec hires + funding rounds
- Train next cohort using validated plays
- Start tracking: meetings/signal type, pipeline/play, signal-to-opportunity conversion

### Run (Months 4-6): Automate
- Auto-routing signals to right rep
- Pre-populated templates for 60-second personalization
- Multi-touch cross-channel sequences
- Signal-to-revenue attribution dashboards
- **Critical:** Automate the PROCESS, never the PERSONALIZATION

---

## 🏗️ Three-Layer GTM Funnel (HeyReach Model)

### Layer 1: ICP + Signal Enhancement
- Start with ICP → layer signals on top
- Higher volume, moderate urgency
- **Channel:** Email at scale + LinkedIn support
- **Signals:** Hiring, funding, expansion, industry shifts

### Layer 2: Intent-First Signals
- Signal PRECEDES ICP validation
- Behavioral movement indicates emerging interest
- **Channel:** Email + LinkedIn, timing-sensitive
- **Signals:** Content engagement, ad interaction, competitive research, relevant hiring

### Layer 3: First-Party / Inbound
- Highest urgency, lowest volume
- Requires direct sales engagement
- **Channel:** Direct sales outreach, immediate
- **Signals:** Pricing page visits, CRM reactivation, product usage changes, trial signups

---

## 🤖 How This Maps to Our Stack

### What We Already Have
1. **NL→SQL Engine** — Can query signal data with natural language
2. **Data Waterfall Enrichment** — 7-provider cascade (Hunter → FindyMail → Icypeas → QuickEnrich → Forager → Wiza → LeadIQ)
3. **Signal Studio Platform** — Next.js frontend + Django backend
4. **Celery Workers** — Async batch processing
5. **Redis** — Real-time caching layer

### What We Need to Build

#### Signal Detection Layer
- **Job change monitoring** — Track ICP contacts across LinkedIn/Apollo/ZoomInfo
- **Funding event ingestion** — Crunchbase/PitchBook API feeds
- **Tech stack monitoring** — BuiltWith/Wappalyzer integration
- **Hiring signal scraper** — Career page monitoring + job board APIs
- **Website visitor identification** — Clearbit Reveal / RB2B / Leadfeeder equivalent

#### Signal Scoring Engine
- Implement the point-based scoring model above
- Compound signal detection (same account, multiple signals)
- Decay function (signals lose value over time — funding 30 days, job change 90 days)
- ICP fit multiplier on top of signal score

#### Action Orchestration
- Auto-route signals to correct play based on type + score
- Generate messaging tips with AI (reference specific signals in templates)
- Multi-channel sequencing (email → LinkedIn → phone)
- SLA tracking (time from signal detection to outreach)

#### Measurement Dashboard
- Signal-to-outreach speed
- Reply rates by signal type
- Meetings booked per signal type
- Pipeline generated per play
- Signal-to-revenue attribution
- Win rates by signal type vs cold baseline

---

## 🎯 Replicable Patterns for ForwardLane Clients

### For Invesco (Wealth Management)
**Relevant signals:**
- Advisor job changes (past users moving firms)
- New branch managers/team leads (first 100 days)
- Firm technology transitions (new CRM/planning tool adoption)
- Regulatory changes driving tool adoption
- Retirement wave signals (advisor succession planning)

### For Any ForwardLane Client
**The pitch:** "We don't just give you data — we give you a signal-based GTM engine that tells you WHO to contact, WHEN to contact them, and WHAT to say, based on real-time buying signals."

This is the Signal Studio value prop distilled.

---

## ⚠️ Common Mistakes to Avoid

1. **Drowning in signals without prioritization** — Use scoring model, not everything is urgent
2. **Generic outreach that ignores the signal** — If message doesn't reference the trigger, you wasted it
3. **Skipping research** — 15 minutes of research turns warm lead into booked meeting
4. **Automating too early** — Validate manually first, then scale
5. **Treating signals as solo sport** — Must be shared system, not individual rep habits
6. **Not tracking signal decay** — Signals lose value fast. First mover wins 5x more often

---

## 📘 The 11 Signal Playbooks (From Notion Source)

The original Notion playbook contains **11 complete, copy-paste-ready signal plays** with specific tools, SOPs, and email templates. Full raw extraction at `notion-playbook-raw.md`.

### 1. Intent-Based Hiring Signals
- **Target:** Companies posting roles indicating budget allocation
- **Window:** 72 hours after posting
- **Stack:** Apify (scrape job boards) → n8n (orchestrate) → Conigma (enrich) → Icypeas (emails) → Instantly (sequences)
- **SOP:** Daily Apify scrape at 6AM → filter 11-200 employees → enrich in Conigma (domain, decision maker, email, tech stack, ICP score) → push to sequencer
- **Template:** Reference the specific hiring role, connect to the problem it implies

### 2. Anonymous Visitor Identification
- **Target:** Website visitors who don't fill forms
- **Key Insight:** "Someone on your pricing page at 2pm Tuesday isn't browsing — they're evaluating"
- **Tools & Pricing:**
  - RB2B ($199/mo) — US visitor ID
  - Leadpipe ($149/mo) — Multi-geo
  - Snitcher (€79/mo) — EU-focused
  - Warmly ($700/mo) — All-in-one
  - Vector ($250/mo) — Signal layer
- **SOP:** Install pixel → webhook to Conigma (filter: pricing/demo/features pages, >30s, >10 employees) → enrich → route by page behavior (pricing=high intent, case study=social proof, features=education)
- **Templates:** Page-specific — pricing visitors get "what's driving the research?", case study visitors get "facing something similar?"

### 3. LinkedIn Engagement Capture
- **Target:** People engaging with relevant content
- **Key Insight:** "Someone who likes a post about outbound deliverability at 9am IS thinking about outbound deliverability"
- **Stack:** Trigify (monitor) → Conigma (enrich) → Prosp (LinkedIn outreach)
- **SOP:** Find 10-15 creators posting to your ICP → monitor with Trigify (50+ reactions trigger) → filter commenters by ICP → segment: commenters (highest intent, direct outreach) vs reactors (softer approach)
- **LinkedIn Sequence:** Day 1: visit profile + like post + connect → Day 3: DM with context → Day 4: voice note → Day 7: resource drop → Day 10: casual bump

### 4. Post Commenter Extraction
- **Target:** People commenting on specific viral posts
- **Focus:** Creating viral lead magnets with scroll-stopping hooks + value props + killer CTAs
- **Two approaches:** 300+ comments (automated) vs <300 comments (semi-manual)

### 5. Tech Stack Qualification
- **Target:** Companies using (or missing) specific technologies
- **Key Insight:** Tech stack reveals budget, sophistication, and pain points
- **Tools:** BuiltWith (website scanning), Wappalyzer (browser extension), HG Insights (enterprise), Slintel (tech + intent)
- **SOP:** Define must-have tech (e.g., Salesforce) + must-not-have (e.g., competitor tools) → build company list → enrich contacts → personalize by tech context
- **Templates:** "Missing tech" angle vs "competitor tech" angle — reference their stack intelligently

### 6. Funding Event Triggers
- **Target:** Companies that just raised capital
- **Tools:** Crunchbase Pro ($49/mo), PitchBook (enterprise), Dealroom (€399/mo EU), Fundz ($29/mo real-time)
- **SOP:** Daily Crunchbase alerts (>$1M, your verticals) → n8n automation → Conigma enrichment → add "days since funding" variable
- **Template:** Congratulate, connect growth goals to specific problem, offer 60-second Loom

### 7. Local Business Discovery
- **Target:** Brick-and-mortar in specific geographies
- **Key Insight:** "Local businesses get 1/10th the cold email volume of SaaS companies"
- **Stack:** Apify Google Maps Scraper → Conigma → Icypeas
- **SOP:** Scrape Google Maps (200/query) → filter (has website, >3.5 stars, not chains) → enrich owner/email → segment by review count
- **Template:** Reference their Google review count as social proof

### 8. Competitor Audience Mining
- **Target:** People following or engaging with competitors
- **Key Insight:** "Already in-market, already understand the category"
- **Tools:** Phantombuster/Scrapeli (follower extraction), Trigify (engagement), BuiltWith (customer ID)
- **SOP:** List 5-10 competitors → extract LinkedIn followers → filter out competitor employees → filter by ICP → differentiated messaging
- **Template:** "Noticed you follow [competitor] — are you using them or still evaluating?"

### 9. Sales Navigator Power Filtering
- **Target:** LinkedIn users at inflection points
- **Key Insight:** "Layer filters to find inflection points — job changes, company growth, recent activity"
- **SOP:** Video-based (filter layering technique)

### 10. G2/Review Site Intent
- **Target:** Companies actively researching on review sites
- **Key Insight:** "Someone reading G2 reviews is further along than someone who saw a LinkedIn post — they're comparing"
- **Tools:** G2 Buyer Intent, TrustRadius, Bombora, 6sense
- **SOP:** G2 Seller Dashboard → set filters → weekly export → enrich with decision makers → craft research-aware messaging
- **Alternative (no G2 profile):** Manual competitor review mining → extract reviewer companies
- **Template:** Don't say "I saw you on G2" — reference the problem they're researching

### 11. Minimal Viable Stack (3-Tool Setup)
- **Apollo** ($0-99/mo) — Lead sourcing
- **Conigma** — Enrichment + logic + AI personalization
- **Instantly** — Sending (30-50/day per inbox)
- **SOP:** Source in Apollo (11-200 headcount, ICP titles) → export to Conigma → enrich (tech stack, email verify, ICP score ≥7) → AI-generate custom first lines → push to Instantly → track weekly

---

## 🔗 Key Sources & Tools Referenced

### Signal Detection Tools
- **ZoomInfo** — Intent + technographic data
- **Clay** — Job changes, hiring, firmographic changes (GTM engineering platform)
- **Apollo** — Contact database + signal monitoring
- **Cognism** — Intent + contact data
- **G2** — Category research intent
- **BuiltWith** — Tech stack changes
- **Clearbit/Leadfeeder** — Anonymous website visitor identification
- **6sense** — Account identification + intent scoring
- **Bombora** — Third-party intent data
- **UserGems** — Past champion tracking (highest-converting signal tool)
- **Champify** — Champion tracking and scoring

### Execution Tools
- **HeyReach** — LinkedIn automation at scale
- **Salesmotion** — Account intelligence platform
- **Starnus** — AI agent for signal-based prospecting
- **Zapier/Make** — Signal-to-action automation
- **Pocus** — Signal-to-play orchestration

### Frameworks Referenced
- Pocus Crawl-Walk-Run model
- HeyReach 3-Layer Signal Funnel
- Salesmotion Signal Scoring Model
- Linear's signal play results (+30% deal size, 50% response rate, -20h/week prospecting)
