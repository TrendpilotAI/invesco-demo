# GTM Infrastructure Plan — Video Demos, Landing Pages, Payment Rails, Lead Gen

## Executive Summary

Build a repeatable GTM stack that can be spun up for any new project in hours, not weeks. Includes: video demo production, landing pages, payment rails, ad funnels, lead gen, and social media presence — all automated and A2UI-approved.

## 1. Video Demo Production Pipeline

### Style Guide: Anthropic Release Style
- **Dara Khosrowshahi / Amanda Askell / Daniela Amodei style**: Clean, confident, technically precise but accessible
- **Visual**: Clean UI recordings with subtle motion, no flashy transitions, product speaks for itself
- **Voice**: Nathan's voice via TTS — naturalistic, conversational, technical when needed, jargon-light
- **Format**: 30-60 second shorts (social), 2-5 minute overviews (YouTube/landing pages)
- **Cards**: Professional overview cards with key stats, gradients, clean typography

### Tools
- **Remotion** (already installed) — Programmatic video composition in React
- **OpenAI TTS** — Nathan's voice clone or high-quality voices (alloy, echo, onyx, shimmer)
- **BrowserUse** — Automated UI walkthroughs for screen captures
- **FFmpeg** — Video encoding (needs install)
- **Playwright** — Screenshot/screencast capture

### Video Types
| Type | Length | Platform | Purpose |
|------|--------|----------|---------|
| Feature Short | 30-60s | Twitter, TikTok, Threads | Quick feature highlight |
| Product Overview | 2-5min | YouTube, LinkedIn, Landing page | Full product walkthrough |
| Demo Walkthrough | 3-8min | Sales, Confluence | Internal/client demos |
| Release Card | 15-30s | All social | Animated feature card with stats |

## 2. Project Inventory — What Needs GTM

| Project | Stage | Needs Landing | Needs Payment | Needs Video | Priority |
|---------|-------|---------------|---------------|-------------|----------|
| **FlipMyEra** | 90% complete | ✅ Has (Netlify) | Stripe (configured) | ✅ Yes | P0 |
| **Ultrafone** | 75% complete | ❌ Need | Stripe | ✅ Yes | P1 |
| **Second-Opinion** | 50% complete | ✅ Has | Stripe | ✅ Yes | P1 |
| **Signal Studio** | Deployed | ForwardLane.com | Enterprise (contract) | ✅ Yes | P0 |
| **Invesco EasyButton** | Demo ready | N/A (enterprise) | N/A (enterprise) | ✅ Yes | P0 |
| **NarrativeReactor** | Early | ❌ Need | Stripe | ✅ Yes | P2 |
| **fast-browser-search** | Early | ❌ Need (OSS) | N/A (OSS) | ✅ Yes | P2 |

## 3. Repeatable Platform Stack (Cookie Cutter)

### For Each New Project:
```
1. Landing Page    → Next.js 15 template (Tailwind, dark mode, hero, features, pricing, CTA)
2. Auth            → Better Auth (open source, self-hosted, $0/mo at any scale)
3. Payment         → Stripe Checkout + Stripe Billing (subscriptions)
4. Database        → Supabase (or Railway Postgres)
5. Analytics       → PostHog (already configured)
6. Email/CRM       → Instantly (cold outreach) + Loops (transactional)
7. Social          → Blotato (automated posting)
8. Ads             → Meta Ads API + Google Ads API (generate + push)
9. Video           → Remotion (programmatic) + OpenAI TTS (voice)
10. Deploy         → Railway (backend) + Vercel/Netlify (frontend)
```

### Template Repo Structure:
```
project-template/
├── landing/           # Next.js 15 landing page
│   ├── src/app/
│   ├── components/    # Hero, Features, Pricing, CTA, Footer
│   └── stripe/        # Checkout integration
├── app/               # Main application
├── scripts/
│   ├── setup-stripe.sh
│   ├── setup-better-auth.sh
│   ├── setup-posthog.sh
│   └── generate-video.py
├── marketing/
│   ├── video-template/ # Remotion composition
│   ├── ad-copy/        # Generated ad variants
│   └── landing-copy/   # Generated landing copy
└── deploy/
    ├── railway.toml
    └── vercel.json
```

## 4. Lead Gen & Retargeting Pipeline

```
Content (Bragi social posts)
    ↓
Landing Page (optimized, A/B tested)
    ↓
Signup / Free Trial (Better Auth)
    ↓
Onboarding Email Sequence (Loops/Instantly)
    ↓
Retargeting Pixel (Meta + Google)
    ↓
Retargeting Ads (generated, pushed via API)
    ↓
Conversion → Stripe Payment
    ↓
Post-Purchase Nurture
```

### Tools for Lead Gen:
- **Instantly** — Cold email outreach, domain warming
- **Blotato** — Social posting (already configured)
- **Meta Ads API** — Generate and push Facebook/Instagram ads
- **Google Ads API** — Search and display ads
- **PostHog** — Conversion funnels, feature flags, A/B tests
- **Loops** — Transactional email, drip campaigns

## 5. Ad Generation Pipeline

For each project, Bragi generates:
- 5 ad copy variants (different hooks, CTAs)
- 3 audience segments
- Image assets (via OpenAI image gen or screenshots)
- A/B test plan
- Budget recommendation

## 6. Social Media Account Creation

### Needed New Accounts:
| Project | Twitter | Threads | TikTok | Instagram | YouTube |
|---------|---------|---------|--------|-----------|---------|
| Ultrafone | @ultrafone_ai | ❓ | @ultrafone_ai | @ultrafone_ai | Ultrafone |
| Second-Opinion | @secondopinion_ai | ❓ | ❓ | ❓ | ❓ |
| FlipMyEra | @flipmyera | ❓ | @flipmyera | @flipmyera | ❓ |
| fast-browser-search | @fastbrowsersrch | ❓ | ❓ | ❓ | ❓ |

## 7. Implementation Phases

### Phase A: Video Pipeline (Days 1-3)
- Install FFmpeg
- Build Remotion video templates (release card, feature short, product overview)
- Set up OpenAI TTS for voiceover generation
- Create first video: Invesco EasyButton demo
- Create first short: Security agent swarm in action

### Phase B: Template Stack (Days 3-5)
- Build reusable Next.js landing page template
- Integrate Stripe Checkout boilerplate
- Integrate Better Auth boilerplate
- Integrate PostHog boilerplate
- Test: spin up FlipMyEra landing in <2 hours

### Phase C: Lead Gen (Days 5-7)
- Set up Instantly for cold outreach
- Set up retargeting pixels (Meta + Google)
- Build ad copy generator (Bragi extension)
- Create first ad campaign for FlipMyEra

### Phase D: Scale (Days 7-10)
- Create social accounts for each product
- Set up Blotato for each new account
- Build project-launch automation script
- Test: launch new project from zero to live in <4 hours
