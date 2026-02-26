# 🏗️ ForwardLane Complete Platform Map
**Date:** Feb 22, 2026

## The Full System — Every Moving Piece

```
┌─────────────────── USER-FACING APPLICATIONS ────────────────────┐
│                                                                  │
│  SIGNAL STUDIO (NEW)          SIGNAL BUILDER (CURRENT)          │
│  Next.js 15 / App Router      React + Craco + Redux              │
│  React Flow visual builder     Pages: Builder, Catalog,          │
│  AI Chat (multi-model)         Collections, Creator, Preview,    │
│  Oracle Connect                Services, Settings               │
│  Conversation Memory           @tanstack/react-query             │
│  Victor's latest work          Last active: Apr 2024             │
│                                                                  │
│  FORWARDLANE ADVISOR (LEGACY)  WEALTH ADVISOR WEBAPP            │
│  Express.js + Node.js          Static HTML/jQuery/Bootstrap      │
│  4,752 files (!)               Dashboard with DataTables         │
│  35+ route modules:            Chat widget (Zeno)                │
│  - Admin, Signals, Clients     Demo/presentation view            │
│  - Portfolios, Alerts          Last active: legacy               │
│  - Products, Strategy                                            │
│  - NLC (NL Classification)     DEMO CLIENT VIEW                  │
│  - Compliance, Uploads         Static demo screens               │
│  - CRM, Relationships                                            │
│  MySQL + AMQP + DynamoDB       CB-FORWARDLANE-SITES             │
│  Last active: legacy           Static HTML/CSS marketing         │
│                                                                  │
├─────────────────── ADMIN / OPS LAYER ───────────────────────────┤
│                                                                  │
│  CORE ADMIN UI                 CORE ADMIN (BACKEND)             │
│  React + Antd + Redux-Saga     Flask + Python                    │
│  613 files                     Ansible deployment scripts        │
│  Pages:                        175 files                         │
│  - Clients Data & Prioritize                                     │
│  - Content Recommendations     FL WEB WIDGETS                    │
│  - Relationship Data Mgmt      Embeddable React widgets:         │
│  - System Admin                - Client Prioritization           │
│  - System Config               - Content Personalization         │
│  - System Status               - Content Insights                │
│  - Dashboards (Client/Doc      - Signals Insights                │
│    Ranking Signal Overview)    - Clients for Doc                  │
│  - Organization Settings       426 files, npm package            │
│  - API page                    Used by core-admin-ui +           │
│  - Test Data                   Salesforce embeds                 │
│                                                                  │
├─────────────────── BACKEND SERVICES ────────────────────────────┤
│                                                                  │
│  FORWARDLANE BACKEND (DJANGO 3.2)                                │
│  The Brain — 150 models, 2000+ PRs                               │
│  ┌─────────────────────────────────────────┐                     │
│  │ portfolio (38 models)  — Client, Holding,│                    │
│  │   Transaction, Campaign, Household,      │                    │
│  │   FinancialAccount, Flow, NBAction       │                    │
│  │ ranking (11) — BusinessRule, Signal      │                    │
│  │   Builder, Collections, Tags, Snooze     │                    │
│  │ customers/invesco (12) — MS Book Data,   │                    │
│  │   Rank Data, AUM, DS Recommendations,    │                    │
│  │   Trailing Sales                         │                    │
│  │ customers/lpl (8)                        │                    │
│  │ customers/pershing (1)                   │                    │
│  │ user (12) — Auth, SAML, Salesforce SSO   │                    │
│  │ ai (9) — Content/HCF/Similar Recommender │                    │
│  │ content_ingestion — Scraper, Docs        │                    │
│  │ pipeline_engine — Job management         │                    │
│  │ market_data (10) — Instruments           │                    │
│  │ document_ranking (3)                     │                    │
│  │ client_ranking (4)                       │                    │
│  │ access_guardian — Permissions/RBAC       │                    │
│  │ adapters — Bridge, Octane, Wealthbox     │                    │
│  │ entities — Entity extraction             │                    │
│  │ feedback                                 │                    │
│  └─────────────────────────────────────────┘                     │
│                                                                  │
│  SIGNAL BUILDER BACKEND        FRONT-END-AI                      │
│  Python / Clean Architecture   Minimal (196KB)                   │
│  Snowflake integration draft   AI frontend connector             │
│  SQL translators                                                 │
│  Alembic migrations           GENERATIVE AI                      │
│  Last active: Oct 2024        Minimal (192KB)                    │
│                                                                  │
├─────────────────── DATA LAYER ──────────────────────────────────┤
│                                                                  │
│  PostgreSQL "default"          PostgreSQL "analytical"            │
│  (forwardlane DB)              (ANALYTICAL DB)                    │
│  - All Django models           - Signal SQL execution target      │
│  - User/org/permissions        - Invesco materialized views       │
│  - Portfolio/holdings          - Trailing sales views             │
│  - Rankings/signals            - DataScienceRecommendation        │
│  - CRM notes/activities                                          │
│                                                                  │
│  Redis                         S3 (AWS)                          │
│  - Celery broker/results       - Document/file storage            │
│  - Caching                     - Data source imports              │
│                                                                  │
│  MySQL (legacy, via advisor)   DynamoDB (legacy, via advisor)     │
│                                                                  │
├─────────────────── BACKGROUND PROCESSING ───────────────────────┤
│                                                                  │
│  Celery Workers (7 queues)     Celery Beat Scheduler             │
│  - backend                     - Client ranking @6am,4pm         │
│  - content_ingestion           - Doc ranking @7am,5pm            │
│  - client_ranking              - Content ingestion every 15min   │
│  - document_ranking            - Invesco view refresh @5:10am    │
│  - user                        - Market data @5:30am             │
│  - ai                          - Pipeline every 2hrs             │
│  - pipeline                    - 20+ more scheduled tasks        │
│                                                                  │
├─────────────────── INTEGRATIONS ────────────────────────────────┤
│                                                                  │
│  Salesforce (OAuth2 + SAML)    Bridge (financial data)           │
│  Morningstar (fund data)       Wealthbox (CRM sync)             │
│  Octane (measurements)         IEX (market data)                │
│  Entity Extraction service     Sentry (error monitoring)         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Evolution Timeline

| Era | App | Tech | Status |
|-----|-----|------|--------|
| 2016-2019 | `forwardlane_advisor` | Express/Node/jQuery/MySQL | ⚰️ Legacy |
| 2017-2019 | `wealth-advisor-webapp` | Static HTML/jQuery | ⚰️ Legacy |
| 2018-2020 | `core-admin` + `core-admin-ui` | Flask + React/Antd | 🟡 Active for ops |
| 2019-2022 | `fl-web-widgets` | React embeddable widgets | 🟡 Used in Salesforce |
| 2023-2024 | `signal-builder-frontend` + `signal-builder-backend` | React/Craco + Python | 🟡 Current product |
| 2025-2026 | `signal-studio` | Next.js 15 / React Flow / AI | 🟢 Next gen |

## What Actually Matters for the NL Signal Feature

The **operating stack** that needs to work:

1. **Signal Studio** (frontend) — already has the UI, visual builder, AI chat
2. **ForwardLane Backend** (Django) — auth, signal CRUD, signal execution
3. **PostgreSQL "default"** — user/org/signal storage
4. **PostgreSQL "analytical"** — where signals RUN (SQL execution target)
5. **Redis** — Celery broker
6. **Celery Worker** — background signal execution, ranking jobs

**What we DON'T need for NL signals:**
- forwardlane_advisor (legacy Node.js app)
- wealth-advisor-webapp (static demo)
- core-admin / core-admin-ui (admin ops panel — nice to have, not blocking)
- fl-web-widgets (Salesforce embeds — needed later for Invesco, not now)
- signal-builder-frontend (predecessor to Signal Studio)
- Any of the 100+ infrastructure/ML repos
