# 🏗️ Signal Studio Architecture Deep Dive
**Date:** Feb 22, 2026 | **Analyst:** Honey 🍯

---

## System Architecture — As It Exists

```
┌─────────────────────────────────────────────────┐
│                 SIGNAL STUDIO                    │
│            (Next.js 15 / App Router)             │
│                                                  │
│  Pages: Signal Library, Signal Builder,          │
│         AI Chat, Oracle Connect, Data Mapper,    │
│         Login, Dashboard                         │
│                                                  │
│  Visual: React Flow editor, shadcn/ui,           │
│          Framer Motion, AI Elements suite         │
│                                                  │
│  Auth: JWT stored in localStorage,               │
│        proxied via BFF to backend                 │
├──────────────┬───────────────┬───────────────────┤
│   BFF API    │  Oracle API   │    AI Chat API    │
│ /api/signals │ /api/oracle/* │ /api/chat/*       │
│ /api/auth    │               │ /api/ai/completion│
│              │               │ /api/semantic/*   │
│ Proxies to   │ Direct Oracle │ OpenAI/Anthropic  │
│ CORE_API     │ 23ai via      │ /OpenRouter       │
│              │ oracledb      │                   │
└──────┬───────┴───────┬───────┴───────────────────┘
       │               │
       ▼               ▼
┌──────────────┐  ┌──────────────────────────────┐
│  FORWARDLANE │  │       ORACLE 23ai            │
│   BACKEND    │  │                              │
│  (Django 3.2)│  │  - Vector search (1536-dim)  │
│              │  │  - Oracle ML                 │
│  PostgreSQL  │  │  - Conversation memory       │
│  Celery+Redis│  │  - Semantic embeddings       │
│  S3 storage  │  │                              │
│  SAML SSO    │  └──────────────────────────────┘
│              │
│  KEY APPS:   │
│  - portfolio (38 models - Client, Holding, etc.)│
│  - ranking (11 models - BusinessRule, Signal)   │
│  - customers/invesco (12 models - MS book data) │
│  - customers/lpl (8 models)                     │
│  - ai (9 models - recommenders)                 │
│  - pipeline_engine (3 models)                   │
│  - content_ingestion (scraper, docs)            │
│  - access_guardian (permissions)                │
│  - user (12 models - auth, SAML, Salesforce)    │
│  - market_data (10 models - instruments)        │
│  - document_ranking (3 models)                  │
│  - client_ranking (4 models)                    │
│  TOTAL: ~150 Django models                      │
│                                                 │
│  API: /api/v1/                                  │
│  - users/ (login, SAML, Salesforce OAuth)       │
│  - signals/ (ranking/business rules)            │
│  - clients/ (portfolio management)              │
│  - ranking/ (business rules, collections, tags) │
│  - ai/ (content recommender, HCF, keywords)     │
│  - content-ingestion/ (scraper)                 │
│  - pipeline_engine/ (job management)            │
│  - portfolio/ (financial data)                  │
│  - document-ranking/                            │
│  - client-ranking/                              │
│  - access_guardian/ (permissions)               │
│                                                 │
│  Auth: JWT prefix "JWT" (not Bearer)            │
│  Celery queues: backend, content_ingestion,     │
│    client_ranking, document_ranking, user, ai,  │
│    pipeline                                     │
└─────────────────────────────────────────────────┘
```

---

## PR #17 Review — Victor's Auth Implementation

### What He Did (Clean, Professional)
- **18 files changed, +782 lines**
- Created centralized `lib/constants.ts` (`CORE_API` + `API_BASE`)
- Built `lib/api-client.ts` with `authFetch()` that adds `Authorization: JWT <token>` (not Bearer — matches Django backend's `JWT_AUTH_HEADER_PREFIX`)
- Login page (`/login`) → BFF proxy → `POST {CORE_API}/api/v1/users/login/`
- Auth context with localStorage persistence
- Route protection via `AuthLayout` (redirects to /login if unauthenticated)
- Dashboard shows user email + logout button
- Refactored all signal API routes to use centralized `API_BASE` constant
- Added `NEXT_PUBLIC_SKIP_AUTH` flag for dev mode

### Quality Assessment
- **Architecture:** ✅ Clean BFF pattern, no credentials on client
- **Security:** ⚠️ JWT in localStorage (XSS risk — industry standard but not ideal)
- **Code Quality:** ✅ Well-documented, centralized constants, no hardcoded URLs
- **Missing:** No token refresh mechanism, no token expiration handling
- **Reviewed by:** Qodo (automated), ForwardLane participant (not formally approved)

---

## The Core Data Model — What ForwardLane Actually Does

### portfolio.Client (the center of everything)
Every signal, ranking, recommendation, and data point orbits around `Client`. A client = a financial advisor/firm that Invesco wholesalers sell to.

### ranking.BusinessRule = "Signal"
What Signal Studio calls "signals" are `BusinessRule` objects in the backend. They have:
- Categories, tags, collections for organization
- Organization bindings (multi-tenant)
- Signal Builder Rules (visual builder output)
- Snooze functionality (dismiss temporarily)

### customers.invesco (12 models)
Deep Invesco-specific data:
- **MS Mutual Funds Book Data** — Morgan Stanley mutual fund positions by advisor
- **MS ETF Book Data** — Same for ETFs
- **MS SMA Book Data** — Separately managed accounts
- **MS UIT Book Data** — Unit investment trusts
- **Rank Data** — Invesco's book rank, gross/net sales rank
- **Assets Under Management** — Per-instrument AUM
- **DataScienceRecommendation** — ML-generated scores: opportunity, risk, upsell, cross-sell, defend revenue, distressed AUM, buying pattern changes, RIA opportunity
- **Trailing Sales** — Annual and monthly sales by asset type

### Key Insight: The `DataScienceRecommendation` model
This is the **brain** — ML-generated scores including:
- `opportunity_score`, `risk_score`
- `upsell_opportunity_score` + recommendation JSON
- `cross_sell_opportunity_score` + recommendation
- `defend_revenue_opportunity_score` + recommendation
- `distressed_aum_score` + peak/current/eroded values
- `ria_opportunity_score` + greenspace analysis

**This is exactly what Craig asked for in the Invesco retention meeting.** The data science is already there.

---

## Can We Build a Standalone SaaS? — Feasibility Analysis

### What Would a Standalone Version Need?

| Component | Current Dependency | Standalone Replacement | Effort |
|-----------|-------------------|----------------------|--------|
| **Auth** | ForwardLane Django backend | NextAuth.js or Clerk | 2-3 days |
| **User Management** | Django admin + user app | Supabase Auth + admin panel | 3-5 days |
| **Signal/Rule Engine** | Django ranking app (PostgreSQL) | Supabase/Railway Postgres + Prisma | 5-7 days |
| **Client Data Model** | 38 portfolio models + 12 Invesco models | Simplified Prisma schema | 3-5 days |
| **ML Recommendations** | Python (scikit-learn, pandas, numpy) | Keep Python service OR rebuild in Node | 5-10 days |
| **Content Ingestion** | Celery workers + scrapers | BullMQ + Node workers on Railway | 3-5 days |
| **Data Pipeline** | Celery beat + Django management commands | Railway cron + serverless functions | 2-3 days |
| **Oracle 23ai** | Direct oracledb connection | Keep as optional, add PostgreSQL + pgvector | 3-5 days |
| **AI Chat** | Already in Signal Studio (multi-model) | Already standalone ✅ | 0 days |
| **Visual Builder** | Already in Signal Studio (React Flow) | Already standalone ✅ | 0 days |
| **Salesforce Integration** | Django SAML + OAuth2 | Salesforce Connected App + JWT | 3-5 days |

### Total Estimated Effort: 30-50 days of focused development

### The Key Question: What's the minimum viable standalone?

**Option A: Fork Signal Studio + Replace Backend (Recommended)**
- Keep the entire Next.js frontend
- Replace Django BFF calls with direct Supabase/Postgres calls
- Deploy on Railway (Next.js + PostgreSQL + Redis)
- Add Clerk/NextAuth for auth
- Port the DataScienceRecommendation logic to a Python microservice
- **Timeline: 3-4 weeks for MVP**

**Option B: Keep Django Backend, Modernize Deploy**
- Dockerize forwardlane-backend for Railway
- Deploy Signal Studio frontend + Django backend + PostgreSQL + Redis + Celery
- More services to manage but preserves all existing logic
- **Timeline: 1-2 weeks to deploy, ongoing maintenance burden**

**Option C: Full Rewrite (Not Recommended)**
- Too much domain logic in 150 Django models
- Would take 3-6 months to replicate properly
- Not worth it unless you're building a completely different product

---

## My Recommendation

**Go with Option A** — Fork Signal Studio, replace the backend dependency.

### Why:
1. Signal Studio's frontend is **already 80% standalone** — AI chat, visual builder, signal library all work
2. The Django backend is **8 years of accumulated complexity** — 150 models, customer-specific code for Invesco/LPL/Pershing, legacy patterns (Django 3.2, Python 3.9)
3. The valuable IP is in the **signal logic and ML models**, not the CRUD — port just those
4. Railway deployment gives you **a modern SaaS stack** (auto-scaling, PR deploys, private networking)
5. You can **sell to any financial firm**, not just existing ForwardLane customers

### Phase 1 (Week 1-2): Standalone MVP
1. Fork Signal Studio
2. Add NextAuth + Supabase for auth and data
3. Create simplified signal/client Prisma schema
4. Seed with synthetic data for demos
5. Deploy on Railway

### Phase 2 (Week 3-4): Intelligence Layer
6. Port DataScienceRecommendation scoring to a Python service
7. Add pgvector for semantic search (replace Oracle 23ai)
8. Wire up AI chat to query real data

### Phase 3 (Month 2): SaaS Features
9. Multi-tenant organization support
10. Stripe billing
11. API keys for integrations
12. Salesforce sidebar app (Invesco demo)

---

## Repos Cloned Summary

| Repo | Size | Purpose | Status |
|------|------|---------|--------|
| `signal-studio` | 111MB | Next.js frontend | ✅ Cloned & analyzed |
| `forwardlane-backend` | 58MB | Django API backend | ✅ Cloned & analyzed |
| `signal-builder-backend` | 4.9MB | Older signal builder (Python) | ✅ Cloned |
| `front-end-ai` | 196KB | AI frontend (minimal) | ✅ Cloned |
| `generative-ai` | 192KB | Gen AI module (minimal) | ✅ Cloned |

The backend is 137 repos but most are infrastructure (Terraform, Ansible, K8s), legacy services, or data pipelines. The core product lives in `forwardlane-backend` + `signal-studio`.
