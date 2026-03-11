# Polsia — Business Model Deep Dive
**Research Date:** March 10, 2026

---

## Revenue Model Overview

Polsia operates a **hybrid subscription + revenue share** model. Ben explicitly does NOT want to be a "token reseller" (charging for AI compute usage). Instead:

### Tier 1: Subscription
- **Price:** ~$47–$50/month per user
- **Ben's framing:** "Breaking even — I want the most people possible to experience the product"
- **Intent:** Mass adoption over margin — land-grab strategy
- **What you get:** One "company instance" with full agent stack running autonomously

### Tier 2: Revenue Share (The Big Bet)
- **Rate:** 20% of revenue generated on platform
- **Ben's framing:** "Sounds like an App Store fee. It's expensive, but I make it cheap to get in."
- **Mechanic:** Polsia processes transactions via Stripe Connect — automatically captures the 20% before paying out to the company owner
- **The upside bet:** If Polsia's companies make real money, Ben makes real money — aligned incentives
- **Current reality:** Most companies appear to be early-stage or non-revenue (templates), so the 20% revenue share generates minimal income today

---

## ARR Math

### What's Claimed:
- "1.5M ARR" (Solo Founders podcast, ~March 3, 2026)
- "$3.1M+ ARR run rate" (as of March 2026 per search results)
- "1,500 companies" → grew to 3,300+ companies by March 10, 2026

### What the Math Suggests:
- If 3,300 companies × $50/month × 12 = **$1.98M ARR** from subscriptions alone
- At an earlier 1,500 companies × $50 × 12 = **$900K ARR** from subscriptions
- The "$1.5M ARR" claim (~February/March 2026) likely includes some revenue share income on top of subscriptions
- The "$3.1M ARR run rate" likely includes growth since the podcast + more revenue share

### Reddit's Critique:
> "I sold $60 worth of subscriptions in the first 30 minutes, that's over $1M ARR!"  
> — u/al2o3cr

This is a fair shot at the *"2 weeks"* framing. The "2 weeks" may mean "2 weeks after going viral" — during which a spike of signups could have extrapolated to a large annualized number. Silicon Valley founders routinely do this.

---

## Operating Costs

Ben disclosed in the "Agents at Work" podcast (full transcript retrieved):

| Cost | Amount/Month |
|------|--------------|
| Claude Opus Max subscriptions (×3) | ~$600 |
| OpenAI Codex Max | ~$200 |
| Hosting/infrastructure (Render, Neon) | Minimal (usage-based) |
| Ben's salary | Undisclosed (likely SF-level) |
| Office | $0 (works from hacker house) |
| **Total AI tool costs** | **~$800/month** |

**Key advantage:** Received credits from Google Cloud, Anthropic, and OpenAI for building on their platforms. This significantly reduces LLM API costs for the company instances.

**Funding:** Raised a **pre-seed round** (amount not disclosed). Given the low burn, this pre-seed could be significant runway — possibly 2+ years.

---

## How Companies Sign Up

1. **User registers** at polsia.com (~$50/month subscription)
2. **Idea input:** Either user provides a business idea OR clicks "Surprise Me" (AI researches the user and proposes an idea)
3. **Provisioning:** Polsia spins up:
   - Web server instance (Render)
   - PostgreSQL database (Neon)
   - GitHub repository
   - Email address
   - Stripe account (via Stripe Connect)
   - Meta Ads account
4. **Agent activation:** Orchestrated agent system begins running daily cycles
5. **User touchpoints:** User receives daily email updates from their "AI CEO" summarizing what was done
6. **Chat interface:** User can chat with their AI co-founder within the app to give direction
7. **Escalation:** If agents can't handle something (feature not built, permission needed), they escalate to Ben (currently) or email chain

---

## Payment Infrastructure

- **Platform billing:** Stripe for subscription payments (~$50/month)
- **Company revenue:** Stripe Connect for each company instance — Polsia takes 20% at the transaction level
- **Ad spend:** Meta CAPI integration for conversion tracking on Meta Ads campaigns
- **Daily ad budget:** Charged directly to user's account (they fund their own ad spend on top of subscription)

---

## Industries / Company Types Being Built

Based on the public subdomains observed (polsia.app):

| Company | Domain | Type | Status |
|---------|--------|------|--------|
| LeakProof | leakproof.polsia.app | Unknown (home repair?) | Empty template |
| CoPropilot | copropilot.polsia.app | Property management? | Empty template |
| PawPulse | pawpulse.polsia.app | Pet services | Empty template |
| Registra | registra.polsia.app | Registration/forms | Empty template |

**Pattern:** The AI is generating consumer-facing B2C apps in various niches. These appear to be early-stage MVPs that haven't yet reached revenue stage. The "company builder" model creates a lot of companies, but most are in the "built landing page, haven't acquired customers yet" phase.

**What types of companies work best:**
- Based on Ben's description: online businesses, not physical
- Strong in: SaaS, subscription apps, e-commerce, digital services
- The Meta Ads integration suggests digital marketing-heavy consumer businesses
- Cold outreach integration (with Hunter.io-style email database) suggests B2B plays too

---

## Onboarding Flow

1. **Sign up** at polsia.com
2. **Input idea** or use "Surprise Me" (AI researches your background)
3. **Get provisioned:** Full tech stack within minutes
4. **Receive daily AI CEO email:** What's being worked on, what's been shipped
5. **Chat interface:** Direct message your AI co-founder for direction
6. **Guide optionally:** 80% runs on autopilot; user provides the 20% vision/guidance
7. **Revenue:** If companies earn money, Polsia takes 20% automatically via Stripe Connect

---

## The "Incubator" Positioning

Ben explicitly calls Polsia an "incubator" rather than SaaS. This is deliberate:
- Traditional SaaS: charge for access to tools, user builds with them
- Polsia: the AI DOES the building AND charges a revenue share when it works
- This creates **aligned incentives** — Ben profits only when users succeed
- Similar model to: App Store (30% cut), Kickstarter (5% cut), YC (7% equity)
- Key difference from YC: Polsia provides the execution, not just funding + advice

---

## Future Business Model Evolution (from podcast)

Ben envisions:
1. **Full autonomy** — platform builds itself, reduces Ben's involvement to near zero
2. **Self-improving platform** — agent feature requests from the agent fleet, not just human users
3. **Expanded revenue share model** — as companies mature and generate real revenue, the 20% becomes substantial
4. **Potential institutional revenue** — the pre-seed raise suggests investors see a larger opportunity

---

## Financial Projections (Our Estimate)

If the 3,300 company count is real and most are paying $50/month:
- **Subscription ARR:** $3,300 × $50 × 12 = **$1.98M/year**
- **Revenue share ARR:** Unknown, likely small (<$500K) given most companies are early-stage
- **Total ARR estimate:** ~$2-3M — consistent with "$3.1M run rate" claim
- **Margin:** Extremely high (only ~$800/month in known direct costs + salary)

This is a legitimate, growing business — even if the individual company quality is low.
