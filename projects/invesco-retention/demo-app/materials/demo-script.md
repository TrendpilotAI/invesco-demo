# Invesco Demo Script & Narration Guide
*ForwardLane — Signal Studio for Distribution Intelligence*
*Version: 1.0 | For: Brian Kiley Demo (pre-run with Megan & Craig)*

---

## Pre-Demo Checklist
- [ ] Browser open to `https://trendpilotai.github.io/invesco-demo/`
- [ ] Reset demo state: `Cmd+Shift+R` (or click Reset button in corner)
- [ ] Screen mirroring working, resolution looks clean
- [ ] Backup recording queued in case of live failure
- [ ] `?demo=megan` URL ready for personalized variant (see Personas section)
- [ ] Mute Slack, email notifications

---

## OPENING — 2 Minutes
**"This is what your advisors see when they open Salesforce Monday morning."**

> **TONE:** Confident, unhurried. Don't rush to impress. Let the UI breathe.

**Script:**
> "Brian, I want to start by showing you something very specific. Not a slide deck, not a concept. This is what a wholesaler at Invesco would see when they open Salesforce on Monday morning.
>
> Today, your wholesalers open Salesforce and see… accounts. A list of names. Maybe some notes. Maybe some stale contact data. What they don't see — what ForwardLane gives them — is *intelligence.*
>
> Signal Studio sits inside Salesforce as a native panel. Your IT team doesn't have to rip and replace anything. It's a Salesforce-native embedded app. Your wholesalers never leave their existing workflow."

**Pause. Let them look at the interface.**

> "What I'm about to show you is a 90-day pilot vision. Twenty of your top wholesalers. Real data. Measurable AUM retention lift. Let's walk through it."

---

## SCREEN 1 — Dashboard (Territory Intelligence) — 3 Minutes

**URL/Nav:** Home dashboard — signal feed and ROI stats

> **WHAT TO CLICK:** Navigate to the Dashboard view. Point to the live signal feed.

**Script:**
> "This is the territory dashboard. Every morning, it surfaces the signals that matter most — ranked by urgency and AUM impact.
>
> See this signal here? [Point to an AUM-decline alert] This is a $47M book with a -8% AUM trend over the last quarter. That advisor hasn't been contacted in 23 days. Without ForwardLane, your wholesaler might not know about this until the quarterly review — if they notice it at all. By then, the money has moved."

**Highlight the ROI panel:**
> "Across Invesco's distribution team — 450 wholesalers, three meetings a day — ForwardLane saves 47 minutes per meeting in prep time. That's 1,048 hours *per week* your team gets back. Not in theory. In our deployments, that time goes back into client-facing activity.
>
> The 23% AUM growth number up here? That's the median lift in accounts where wholesalers used the Meeting Brief before every visit. We'll get to that."

**Key emphasis moment:**
> "The AUM-decline alert is the most important feature in this whole demo. It's not just data. It's *prioritized* data — ranked by which accounts are most likely to move assets in the next 30 days."

---

## SCREEN 2 — Meeting Brief (Salesforce Record View) — 3 Minutes

**URL/Nav:** `/salesforce?id=marcus-thompson` (or whichever advisor persona is set up)

> **WHAT TO CLICK:** Click into Marcus Thompson's contact record from the signal feed or use the advisor selector in the nav bar.

**Script:**
> "Let's click into Marcus Thompson. He's flagged with an Opportunity Score of 72 — high potential, but there's a risk signal we need to address.
>
> Watch what happens."

*[1.5 second loading animation plays — Salesforce-style shimmer]*

> "The AI is pulling from Salesforce CRM data, Marcus's holdings, his engagement history, external market signals. It synthesizes all of that in under two seconds.
>
> And this is what the wholesaler gets."

**Walk through the Meeting Brief panel:**
> "Up here — Opportunity Score. 72 out of 100. The AI says high upsell potential. Why? Marcus is currently at 31% Invesco wallet share with $47M AUM. The model sees he's been actively growing his equity allocation, and there's a new Invesco fund that aligns directly with his practice focus.
>
> Below that — Meeting Prep & Talking Points. This is AI-generated, personalized for this advisor, for this meeting. Not a generic script. Specific to Marcus, today.
>
> And the Key Signals carousel — swipe through these. [Click through 2-3 cards] AUM decline. Competitive product flag. Engagement drop. Risk drift.
>
> Notice we're still inside Salesforce the entire time. The breadcrumb up top. Contacts tab is selected. The 'Log to SF' button — if the wholesaler wants to create a follow-up task, one click. It writes back to Salesforce natively."

**The moment that lands:**
> "Before ForwardLane, a wholesaler spent 45 minutes the night before a meeting pulling this together manually. Now it's two seconds. And it's better."

---

## SCREEN 3 — Signal Builder (Signal Studio) — 2 Minutes

**URL/Nav:** `/create` or Signal Studio tab

> **WHAT TO CLICK:** Show the Signal Builder interface. Point to the "Revenue Defense" signal.

**Script:**
> "This is where your strategy team lives. Signal Builder.
>
> Your analysts and product managers can define custom signals without writing a single line of code. Let me show you the 'Revenue Defense' signal — this is a template we built specifically for Invesco's use case.
>
> [Point to the signal definition] It's watching for three conditions: AUM decline greater than 5% quarter over quarter, last wholesaler contact more than 14 days ago, *and* the advisor holds a competing fund in the same category as your flagged product. When all three are true — the signal fires. That advisor surfaces to the top of the dashboard. The wholesaler gets the alert before the money moves.
>
> Invesco's team would own this. You'd build signals for tax season, for market volatility events, for your product launch cycles. Your strategy team becomes the intelligence layer."

---

## SCREEN 4 — Easy Button (Natural Language Query) — 2 Minutes

**URL/Nav:** Easy Button / NL→SQL interface (if available in demo)

> **WHAT TO TYPE:** "Who are my at-risk advisors with QQQ exposure?"

**Script:**
> "Last feature. We call this the Easy Button.
>
> Your regional managers, your head of distribution — they shouldn't need a data analyst to answer business questions. Watch this."

*[Type query: "Who are my at-risk advisors with QQQ exposure?"]*

> "Plain English. No SQL. No BI tool. Just a question.
>
> And here's the answer — ranked advisors with QQQ holdings, flagged as at-risk, with the relevant signals surfaced. This runs against your actual Snowflake data warehouse. The output is actionable: name, AUM, last contact, risk score.
>
> Your head of distribution can pull a call list in 10 seconds."

---

## CLOSING — Pilot Proposal — 3 Minutes

**Script:**
> "So here's what we're proposing.
>
> A 90-day pilot. 20 of your highest-AUM wholesalers. Real Invesco data — we connect to your Salesforce instance and your data warehouse. No rip-and-replace. No lengthy IT project. We've done this in 30 days.
>
> The success metric is simple: **AUM retention lift in pilot accounts vs. control group.** We measure it. You own the data. At 90 days, you know whether it works.
>
> The math: Invesco manages north of $1.5 trillion. If ForwardLane improves retention by even 0.1% in the accounts touched by your wholesalers — that's $1.5 billion in protected AUM. At your average fee rate, that's tens of millions in revenue that doesn't walk out the door.
>
> We're asking for 20 advisors. 90 days. A committed exec sponsor — ideally you, Brian — and 30 minutes a month with the pilot wholesalers to collect feedback.
>
> We want to earn the full rollout. This pilot is how."

**Close:**
> "What questions do you have? And more importantly — what would make you say yes to a 90-day pilot today?"

---

## OBJECTION HANDLING

### Objection: "IT Security / Data Privacy"
> **Them:** "How does this handle our advisor data? We're highly regulated."
>
> **You:** "Great question — this comes up in every financial services deal. ForwardLane is SOC 2 Type II certified. Data never leaves your Salesforce org or your data warehouse. We don't store advisor data on our servers — the AI runs against your data in your environment. It's the same security model as Salesforce itself. Your IT team will want to see our security architecture doc — I'll send that over today."

### Objection: "Integration Complexity"
> **Them:** "We've tried to integrate tools like this before. It takes 18 months."
>
> **You:** "We've heard that from every enterprise we talk to. Here's the difference: we've built the Salesforce connector. It's pre-built. Your Salesforce admin enables it, maps a few fields, and it's live. The Snowflake connector is the same — we've done this with two other asset managers in the last 12 months. The 30-day estimate is based on real deployments, not optimism."

### Objection: "We Already Have Salesforce Einstein / Native AI"
> **Them:** "Salesforce already has AI baked in. Why do we need ForwardLane?"
>
> **You:** "Einstein is a general-purpose layer. It doesn't know that an advisor with declining AUM in a QQQ position is about to move to a competitor — unless someone built that domain logic. We bring the distribution intelligence domain model. The signals, the risk frameworks, the asset management context — that's what's proprietary. Einstein is the plumbing. We're the intelligence."

### Objection: "Why Not Build This In-House?"
> **Them:** "Our data science team could build this."
>
> **You:** "They probably could. In 18-24 months, with a $3-4M investment in engineering and ongoing maintenance. And then they'd need to keep up with AI model improvements. ForwardLane gives you a production-grade system, maintained and improved, for $300K a year. The question is: what's the highest-value use of your internal engineering team?"

### Objection: "Budget Isn't There Right Now"
> **Them:** "We're mid-budget cycle, this isn't in the plan."
>
> **You:** "That's exactly why we're proposing a pilot — not a full-year commitment. We can structure the 90-day pilot as a proof-of-concept spend that sits in a different budget bucket. If it shows the numbers, it earns its own line item for next cycle. Brian, would it help if I worked with your finance team on how to structure this?"

---

## DEMO PERSONAS

### `?demo=megan` — Megan's View
**Character:** Head of Distribution / Strategy Lead
**Pain points focus:**
- Retention intelligence — which accounts are at risk before it's too late
- Wholesaler productivity — quality of client interactions, not just volume
- Proving ROI of distribution investment to CFO

**What to emphasize:** AUM-decline alerts, territory dashboard, the pilot ROI math. Megan cares about outcomes, not features.

**Talking point for Megan:**
> "Megan, you told us that your biggest challenge isn't finding new advisors — it's keeping the ones you have from moving assets when the market gets volatile. That's exactly what this dashboard is built for."

---

### `?demo=craig` — Craig's View
**Character:** Technology / Operations Lead (or skeptic in the room)
**Pain points focus:**
- Integration complexity — doesn't trust vendor timelines
- Data governance — who owns what, where does data go
- Support model — who do they call when something breaks

**What to emphasize:** Native Salesforce architecture, security posture, Ten Decoders support model, the "30-day implementation" proof points.

**Talking point for Craig:**
> "Craig, I want to be specific about what the integration looks like on your side. There are three connectors: Salesforce CRM, your data warehouse, and optionally Seismic for materials. We've built all three. Your team's job is to grant access and map fields. We handle the rest. I'll follow up with our security architecture deck and implementation scope document."

---

## BACKUP PLAN (If Live Demo Fails)

1. **Primary fallback:** Pre-recorded screen capture video of full demo flow (request from Nathan)
2. **Secondary fallback:** Slide deck with annotated screenshots of each screen
3. **Recovery command:** `Cmd+Shift+R` to reset demo state; hard reload (`Cmd+Shift+R` in browser) to clear state
4. **Humor recovery line:** *"This is actually a great sign — our clients' IT environments are messier than a controlled demo. We know how to handle it."*

---

## KEY PHRASES THAT LAND

| Phrase | When to use |
|--------|-------------|
| *"Before the money moves"* | When discussing AUM-decline alerts |
| *"Native Salesforce — never leave your workflow"* | Addressing integration anxiety |
| *"1,048 hours a week saved"* | ROI moment on dashboard |
| *"You own the data"* | Data privacy objection |
| *"Earn the full rollout"* | Closing the pilot ask |
| *"What's the highest-value use of your engineers?"* | Build-vs-buy objection |

---

## TIMING SUMMARY

| Section | Time | Key Moment |
|---------|------|------------|
| Opening | 2 min | "This is what your advisors see Monday morning" |
| Dashboard | 3 min | AUM-decline alert, ROI stats |
| Meeting Brief | 3 min | AI-generated brief, Salesforce chrome |
| Signal Builder | 2 min | Revenue Defense signal, custom signal creation |
| Easy Button | 2 min | NL→SQL, QQQ query |
| Pilot Close | 3 min | 20 advisors, 90 days, AUM retention metric |
| **Total** | **15 min** | + Q&A |

---

*Last updated: 2026-03-08 | Owner: Nathan Stevenson | ForwardLane Confidential*
