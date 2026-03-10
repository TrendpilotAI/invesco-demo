# Bolt.new — Pricing Deep Dive

## Pricing Evolution

### Phase 1: Unlimited Subscription (Oct 2024)
- **$9/month unlimited** — launched with this
- Users blew through limits in 48 hours
- Unsustainable: AI inference costs exceeded revenue
- Lesson: Unlimited AI is economically impossible at scale

### Phase 2: Token-Based Tiers (Late Oct/Nov 2024)
- Rapid pivot to usage-based pricing
- Introduced tiered token system
- ~50% of paying users upgraded to higher tiers immediately
- Revenue exploded from $60K to millions/month

### Phase 3: Current Pricing (as of March 2026)

#### Free — $0/month
- Public and private projects
- 300K tokens daily limit
- 1M tokens per month
- Bolt branding on websites
- 10MB file upload limit
- Website hosting
- Up to 333K web requests
- Unlimited databases

#### Pro — $25/month (billed monthly)
- No daily token limit
- Start at 10M tokens per month
- No Bolt branding
- Share sites privately
- 100MB file upload limit
- Website hosting
- Up to 1M web requests
- **Unused tokens roll over to next month** (added July 2025)
- Custom domain support
- SEO boosting
- Unlimited databases
- Expanded database capacity
- Choice of database provider
- Image editing with AI

#### Pro Tiers (Higher Token Volumes)
| Plan | Price/month | Tokens/month |
|------|-------------|-------------|
| Pro 25 | $25 | 10M |
| Pro 50 | $50 | 26M |
| Pro 100 | $100 | 55M |
| Pro 200 | $200 | 120M |
| Higher tiers | Up to $2,000 | Up to 1.2B |

#### Teams — $30/member/month (Popular, launched 2026)
Everything in Pro, plus:
- Centralized billing
- Team-level access management
- Granular admin controls & user provisioning
- Share with organization
- Private NPM registries support
- Design System knowledge with per-package prompts
- Token rollover

#### Enterprise — Custom
Everything in Pro, plus:
- SSO, audit logs, compliance
- Granular admin controls
- Dedicated account manager & 24/7 priority support
- Custom workflows, integrations & SLAs
- Scalable for large teams
- Flexible billing & procurement
- Data governance & retention
- Hands-on onboarding & enterprise training

## Key Pricing Mechanics

### Token System
- All AI interactions consume tokens
- Token consumption driven by:
  - Project file syncing to AI (larger projects = more tokens/message)
  - Code generation and iteration
  - Error detection and fixing
  - Every conversation turn
- ~97% of tokens consumed processing context, not generating code
- Long chat histories = progressively more expensive

### Token Rollover (July 2025)
- Paid subscription tokens roll over for **one additional month** (valid 2 months total)
- Active paid subscription required to access rolled-over tokens
- Significant retention feature — reduces "use it or lose it" anxiety

### Token Reloads
- Additional tokens purchasable separately
- Reload tokens generally don't expire while subscription active
- Safety net for power users who exceed monthly allocation

### Free Tier Strategy
- 1M tokens/month is genuinely useful — can build small projects
- 300K daily limit prevents abuse/bots
- Low cost to StackBlitz because WebContainers run on user's browser
- Engineering efficiency subsidizes free tier growth
- Drives activation → upgrade path based on genuine value

## Pricing Analysis

### Strengths
1. **Usage-aligned pricing** — pay more when you get more value
2. **Generous free tier** — drives massive top-of-funnel
3. **Wide tier range** — $0 to $2,000/month covers hobbyist to enterprise
4. **Token rollover** — reduces churn from "wasted month" perception
5. **Low marginal cost** — browser-side compute keeps free tier viable

### Weaknesses
1. **Token opacity** — users don't know how many tokens a task will consume before starting
2. **Error tax** — users pay tokens when AI makes mistakes, burns through debugging loops
3. **Project size penalty** — larger (more valuable) projects consume tokens faster per interaction
4. **Comparison shopping** — harder to compare value vs competitors without token-to-output clarity
5. **40% gross margins** — AI inference costs eat into revenue (vs SaaS typical 70-80%)

### Competitive Pricing Comparison
| Platform | Entry Paid | Top Tier | Model |
|----------|-----------|----------|-------|
| Bolt.new | $25/mo | $2,000/mo | Token-based |
| Lovable | $20/mo | $100/mo | Message-based |
| Replit | $25/mo | $220/mo | Usage-based |
| Cursor | $20/mo | $40/mo | Request-based |
| v0 (Vercel) | $20/mo | $50/mo | Message-based |

### Revenue Concentration
- Power users on $100-200/month plans drive disproportionate revenue
- ~50% of paid users on higher tiers
- Long tail of free/low-tier users = acquisition engine + potential upgrades
