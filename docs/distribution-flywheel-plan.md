# Distribution Flywheel Plan
## Nathan Stevenson → ForwardLane / SignalHaus / Trendpilot

**Created:** 2026-03-03
**Goal:** Build a self-reinforcing content distribution engine that compounds Nathan's personal brand, drives inbound for ForwardLane/Signal Studio, and launches Trendpilot as a standalone SaaS.

**North Star Metric:** 10,000 newsletter subscribers within 6 months. Every subscriber is owned distribution that no algorithm can take away.

---

## Phase 1: Engine Online (Week 1-2)
*Get NarrativeReactor deployed and generating content.*

### NarrativeReactor Deployment
- [ ] Audit current codebase — verify all 32 services compile and tests pass
- [ ] Create Railway service for NarrativeReactor (Express API)
- [ ] Configure environment variables (Gemini, Claude, Fal.ai, Webhook keys)
- [ ] Set up SQLite persistent volume on Railway
- [ ] Deploy and verify health endpoint responds
- [ ] Verify Postiz is fully configured (https://postiz-production-6189.up.railway.app)
- [ ] Connect social accounts in Postiz (LinkedIn, Twitter/X, any others)
- [ ] Wire NarrativeReactor → Postiz integration (API or Blotato as fallback)
- [ ] Test end-to-end: prompt → content generation → Postiz scheduling → publish

### Nathan's Brand Voice Profile
- [ ] Collect 10-20 examples of Nathan's existing writing (LinkedIn posts, emails, presentations)
- [ ] Create brand voice profile in NarrativeReactor (tone, vocabulary, banned phrases, style rules)
- [ ] Generate 5 test posts and have Nathan grade them (A/B/C/D)
- [ ] Iterate voice profile until Nathan rates output B+ or better
- [ ] Document voice profile settings for reproducibility

### Deliverable
NarrativeReactor is live on Railway, generating content that sounds like Nathan, and can publish to LinkedIn/Twitter via Blotato.

---

## Phase 2: Trend Intelligence (Week 2-3)
*Get Trendpilot feeding topics into the content engine.*

### Trendpilot Deployment
- [ ] Wire Supabase credentials and verify DB connection
- [ ] Run Prisma migrations against production Supabase
- [ ] Create Railway service for Trendpilot
- [ ] Configure environment variables (Supabase, API keys)
- [ ] Deploy and verify health endpoint + trend discovery running
- [ ] Test: Trendpilot surfaces 10 trending fintech/wealth mgmt topics

### The Bridge (Trendpilot → NarrativeReactor)
- [ ] Define bridge API contract (Trendpilot POST trending topics → NarrativeReactor ingests)
- [ ] Implement bridge endpoint on NarrativeReactor side (`/api/ingest/trends`)
- [ ] Implement bridge caller on Trendpilot side (cron or webhook on new trend detection)
- [ ] Test end-to-end: trend detected → content draft generated → queued for review
- [ ] Add Railway private networking between services (*.railway.internal)

### Content Pipeline Automation
- [ ] Set up daily cron: Trendpilot discovers top 3 fintech trends each morning
- [ ] NarrativeReactor auto-generates draft posts for each trend
- [ ] Drafts land in a review queue (SQLite content library)
- [ ] Nathan reviews via API/dashboard — approve, edit, or reject
- [ ] Approved posts push to Postiz with optimal time scheduling
- [ ] Postiz handles cross-platform publishing (LinkedIn, Twitter/X, etc.)
- [ ] Use Postiz analytics to track per-post performance

### Deliverable
Every morning Nathan wakes up to 3 draft posts about trending fintech topics, written in his voice. Review takes 15 minutes. Posts go live automatically.

---

## Phase 3: Newsletter Launch (Week 3-4)
*Start building the owned audience asset.*

### Newsletter Infrastructure
- [ ] Wire SendGrid credentials in Trendpilot
- [ ] Design newsletter template (clean, text-forward — not corporate)
- [ ] Set up signup landing page (could be simple Trendpilot dashboard page or standalone)
- [ ] Configure double opt-in and unsubscribe flows
- [ ] Test deliverability (SPF, DKIM, DMARC for sending domain)

### First Newsletter
- [ ] Curate first issue: 1 original insight from Nathan + 3 trend summaries from Trendpilot
- [ ] Format: "What I'm seeing in fintech this week" — personal, opinionated, short
- [ ] Send to initial list (personal contacts, LinkedIn connections who engage, existing clients)
- [ ] Set up weekly cadence (every Tuesday or Thursday morning)

### Growth Mechanics
- [ ] Add newsletter CTA to every LinkedIn post ("I write about this weekly → [link]")
- [ ] Add newsletter CTA to Nathan's LinkedIn profile/banner
- [ ] Add newsletter CTA to ForwardLane email signatures
- [ ] Create a "best of" thread every month linking to past newsletter insights
- [ ] Track: open rate, click rate, reply rate, unsubscribe rate, subscriber growth

### Deliverable
Weekly newsletter shipping. Subscriber count growing. Every post Nathan publishes drives signups to the owned list.

---

## Phase 4: Amplification (Week 4-6)
*Pour gasoline on the organic fire.*

### Content Multiplication
- [ ] Every newsletter issue → 3-5 LinkedIn posts (NarrativeReactor reformats automatically)
- [ ] Every LinkedIn post that performs well → Twitter thread version
- [ ] Every month → 1 long-form article (LinkedIn article or blog) from best-performing content
- [ ] All variants scheduled through Postiz (single calendar view across all platforms)
- [ ] Pull Postiz engagement analytics back into NarrativeReactor
- [ ] Feed engagement data back into trend scoring (Trendpilot weights topics by past performance)

### Paid Amplification (Only After Organic Proves Out)
- [ ] Identify top 3 performing organic posts per month
- [ ] Boost those posts only ($50-100/post to start) — warm audience amplification
- [ ] Track CAC difference: boosted post with existing engagement vs cold ad
- [ ] Document the multiplier effect (this becomes a case study for Trendpilot marketing)

### Thought Leadership Positioning
- [ ] Identify 3-5 fintech podcasts for Nathan to guest on (NarrativeReactor generates talking points)
- [ ] Publish 1 contrarian take per month ("most wealth managers are wrong about X")
- [ ] Engage with other fintech voices on LinkedIn (comment strategy, not just posting)
- [ ] Track: inbound leads attributable to content (ask "how did you find us?" on every call)

### Deliverable
Content machine running at full speed. Multiple formats, cross-platform, engagement-driven topic selection. First paid amplification tests showing multiplier effect.

---

## Phase 5: Trendpilot SaaS Launch (Week 6-10)
*Turn the internal tool into a product.*

### Product Readiness
- [ ] Wire Stripe payments (subscription tiers already designed in Phase 5 specs)
- [ ] Implement auth middleware (Supabase auth)
- [ ] Polish dashboard UI (trend discovery + newsletter builder + analytics)
- [ ] Set up API key management for programmatic access
- [ ] Rate limiting and usage tracking per tier
- [ ] Landing page at trendpilot.ai (benefits, pricing, signup)

### Launch Distribution (Eating Our Own Cooking)
- [ ] Nathan announces Trendpilot in newsletter ("here's the tool I've been using to find every topic I write about")
- [ ] LinkedIn launch post (origin story: built this for myself, now opening it up)
- [ ] Product Hunt launch
- [ ] Offer free tier to first 100 newsletter subscribers (reward early audience)
- [ ] Case study: "How I built 10K subscribers in X months using this exact tool"

### Deliverable
Trendpilot.ai live as a paid SaaS. Nathan's distribution sells the product. The product builds more distribution. Full flywheel.

---

## Success Metrics

| Metric | 30 Days | 90 Days | 180 Days |
|--------|---------|---------|----------|
| LinkedIn followers | +500 | +2,000 | +5,000 |
| Newsletter subscribers | 250 | 2,000 | 10,000 |
| Weekly content pieces | 5 | 7 | 10 |
| Inbound leads/month | 3 | 10 | 25+ |
| Nathan's time/day on content | 30 min | 15 min | 15 min |
| Trendpilot MRR | — | — | $2K+ |

## Key Principle

**Distribution first. Product second. Ads last.**

Every dollar and every hour goes toward building the owned audience before anything else. The newsletter is the asset. LinkedIn is the acquisition channel. NarrativeReactor is the engine. Trendpilot is both the fuel AND the product.

Nathan's face, Nathan's voice, Nathan's opinions. The tools just make it sustainable at scale.

---

## Stack Overview

```
Trendpilot (trend discovery) → NarrativeReactor (content generation) → Postiz (scheduling & publishing)
     ↑                                                                        |
     └──────────── engagement analytics feedback loop ─────────────────────────┘
```

| Service | URL | Role |
|---------|-----|------|
| NarrativeReactor | TBD (Railway) | AI content engine, brand voice, multi-format generation |
| Trendpilot | TBD (Railway) | Trend discovery, newsletter platform, SaaS product |
| Postiz | https://postiz-production-6189.up.railway.app | Social scheduling, cross-platform publishing, analytics |
| Blotato | API fallback | Backup publishing if Postiz doesn't support a platform |
