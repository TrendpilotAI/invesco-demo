# ForwardLane Full Stack Analysis: Can We Ship on Supabase or Snowflake?

**Date**: February 18, 2026  
**Analyst**: Honey  
**Repos Reviewed**: forwardlane-backend, signal-builder-backend, signal-builder-frontend, signal-studio (BB), front-end-ai, wealth-advisor-webapp, fl_web

---

## The Full Stack Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                                │
│                                                                  │
│  signal-builder-frontend    signal-studio        wealth-advisor  │
│  (React/Redux/ReactFlow)    (Next.js 16)         (legacy)       │
│  269 TS files               149 components        dead?         │
│  Auth: FL cookie/JWT        Auth: BFF proxy       Auth: FL JWT  │
└──────────┬──────────────────────┬────────────────────┬──────────┘
           │                      │                    │
           ▼                      ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                                 │
│                                                                  │
│  forwardlane-backend          signal-builder-backend             │
│  Django 3.2 + DRF             FastAPI + SQLAlchemy               │
│  2,485 Python files           527 Python files                   │
│  PostgreSQL (psycopg2)        PostgreSQL (asyncpg + psycopg2)    │
│  Celery 5.2 + Redis           Celery + Redis                     │
│  uWSGI                        uvicorn/gunicorn                   │
│                                                                  │
│  22 Celery beat tasks          Signal SQL translator             │
│  Custom JWT (prefix "JWT")     Signal node construction          │
│  SAML + Salesforce SSO         Analytical DB connector           │
│  Multi-org tenant isolation    Schema builder                    │
│  5 customer modules            NL→SQL translation                │
│  (LPL, Pershing, SEI,                                           │
│   Invesco, AdvisorTarget)                                        │
└──────────┬──────────────────────┬────────────────────────────────┘
           │                      │
           ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                    │
│                                                                  │
│  PostgreSQL (primary)          PostgreSQL (analytical)            │
│  - Users, orgs, permissions    - signal_builder_db               │
│  - Business rules, rankings    - Client signal results           │
│  - Content, documents          - Analytical schemas              │
│  - Portfolio, holdings         - Per-customer schemas             │
│  - CRM notes, campaigns         (Invesco, Pershing, etc.)       │
│  - tsvector search                                               │
│                                                                  │
│  Redis                         Oracle 23ai (Signal Studio only)  │
│  - Celery broker               - Vector search                   │
│  - Session cache               - Conversation memory             │
│  - Task results                - AI embeddings                   │
│                                                                  │
│  S3 (boto3)                                                      │
│  - Document storage                                              │
│  - Data source files                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## What Each Service Actually Does

### forwardlane-backend (Django 3.2) — The Brain

**2,485 Python files. This is the real product.**

| Module | What It Does | DB Tables | Celery Tasks |
|--------|-------------|-----------|-------------|
| **user** | Auth (JWT+SAML+Salesforce), orgs, permissions, 2FA | users, organizations, tokens, permissions | clean_autotest, health_check |
| **core** | Clients, documents, CRM notes, data sources, jobs, transactions, holdings, financial accounts | clients, documents, crm_notes, data_sources, jobs, holdings, transactions, financial_accounts | — |
| **ranking** | Business rules, signal builder rules, weighted scoring, collections | business_rules, business_rule_org_bindings, signal_builder_rules, collections | delete_old_snoozes |
| **client_ranking** | Per-client signal scoring + priority ranking | client_ranking_results (with tsvector) | run_ranking_for_all_orgs |
| **document_ranking** | Document relevance scoring | document_ranking_results | run_ranking, archive_results |
| **pipeline_engine** | ETL pipeline orchestration, goal miner | pipeline_services, pipeline_jobs | run_pipeline (public + private) |
| **content_ingestion** | RSS/web scraping, PDF parsing, content processing | content_ingestion_jobs, documents | run_content_ingestion |
| **ai** | Document recommender (content-based + HCF), keyword extraction, weight recommender | recommendations, keywords | run_cb_recommendation, aggregate_keywords, generate_weights |
| **portfolio** | Client data import, account management, campaigns | portfolio_imports, campaigns, accounts | client_data_import, campaign_status |
| **product_update** | Product/fund updates | product_updates | run_product_ingestion |
| **customers** | Per-customer modules: LPL, Pershing, SEI, Invesco, AdvisorTarget | customer-specific tables | Invesco: refresh_views |
| **adapters** | Wealthbox CRM, Bridge, Octane integrations | adapter-specific tables | wealthbox_file_creation, bridge_etl |
| **access_guardian** | Role-based permissions (RBAC) | permissions, groups | — |
| **market_data** | IEX market data integration | market_data | iex_daily |
| **feedback** | User feedback collection | feedback | — |

**Key dependencies that are HARD to replace:**
- Django ORM across all 2,485 files
- 22+ Celery beat scheduled tasks (the automation engine)
- Custom JWT with `JWT` prefix (not `Bearer`)
- SAML + Salesforce SSO
- Multi-org tenant isolation baked into every query
- Customer-specific business logic (Invesco materialized views, LPL/Pershing/SEI data schemas)

### signal-builder-backend (FastAPI) — The SQL Engine

**527 Python files. A separate service.**

This is NOT part of the Django monolith. It's a standalone **FastAPI** app with its own:
- PostgreSQL database (`signal_builder_db`)
- Celery workers
- Redis
- SQLAlchemy ORM (not Django ORM)
- Its own auth (talks to forwardlane-backend for JWT validation)

**What it does:**
1. **Signal CRUD** — Create, validate, publish signals (node-based visual graph)
2. **NL→SQL Translation** — Converts visual signal graphs into SQL queries
3. **Analytical DB** — Executes generated SQL against a separate analytical PostgreSQL
4. **Schema Builder** — Manages data schemas per customer (clients, holdings, transactions, CRM notes)
5. **Signal Results** — Stores and exports signal execution results

**Key insight:** The signal-builder-backend already has a `DataProvider` pattern — `apps/analytical_db/` abstracts the analytical database connection. It currently targets PostgreSQL but the abstraction exists.

### signal-builder-frontend (React/Redux) — The Visual Builder

**269 TypeScript files. The original Signal Builder UI.**

- React + Redux + ReactFlow
- Talks to signal-builder-backend (NOT the Django monolith directly)
- Auth: reads JWT from `forwardlane_auth_token` cookie OR calls `POST /users/login/` on the FL backend
- Has onboarding, catalog, collections, builder pages

---

## Can You Ship the Whole Product on Supabase?

### What maps cleanly to Supabase:

| ForwardLane Component | Supabase Equivalent | Effort |
|----------------------|---------------------|--------|
| **PostgreSQL (all tables)** | Supabase Postgres | Direct migration (same DB engine!) |
| **Auth (JWT, email/password)** | Supabase Auth | 2-3 days |
| **RBAC / permissions** | Supabase RLS policies | 3-5 days |
| **Multi-org tenant isolation** | RLS with `organization_id` | 2-3 days |
| **tsvector search** | Supabase supports tsvector natively | Free |
| **Vector search (Oracle)** | Supabase pgvector | 1-2 days |
| **S3 file storage** | Supabase Storage | 1 day |
| **Redis (session cache)** | Supabase Realtime + Edge Functions | 1-2 days |
| **API layer (Django REST)** | Supabase auto-generated REST (PostgREST) + Edge Functions | 2-4 weeks |
| **Conversation memory (Oracle)** | Supabase pgvector + tables | 2-3 days |

### What DOESN'T map to Supabase:

| ForwardLane Component | Why It's Hard | Alternative |
|----------------------|---------------|-------------|
| **22 Celery beat tasks** | Supabase has no job scheduler | Supabase pg_cron + Edge Functions, or keep a small worker service |
| **SAML / Salesforce SSO** | Supabase supports SAML on Pro plan ($25/mo) | ✅ Actually works |
| **Customer-specific modules** (LPL, Pershing, SEI, Invesco) | Hardcoded Python business logic, not just data | Must be reimplemented or kept as microservice |
| **Pipeline engine** (ETL orchestration) | Complex multi-step data pipelines with error handling | Need a separate pipeline service (Inngest, Trigger.dev, or keep Celery) |
| **Content ingestion** (RSS scraping, PDF parsing) | Server-side processing, not DB queries | Edge Functions or separate worker |
| **Signal NL→SQL translator** | Complex AST manipulation in Python | Keep as microservice or rewrite in TypeScript |
| **Wealthbox/Bridge/Octane adapters** | CRM-specific integration logic | Keep as microservices |
| **Django Admin** | Internal admin UI for managing orgs, users, rules | Build admin in Next.js or use Supabase Dashboard |

### The Honest Answer: **~60% yes, with caveats**

You can ship **Signal Studio** (the AI-powered front-end) entirely on Supabase. The data layer, auth, vector search, realtime — all native.

You CANNOT ship the **entire ForwardLane backend** on Supabase alone. The 22 Celery tasks, ETL pipelines, content ingestion, and customer-specific business logic need compute — not just a database.

**The architecture would be:**
```
Signal Studio (Next.js) → Supabase (Auth + DB + Storage + Realtime + pgvector)
                        → Worker Service (Celery tasks, ETL, content ingestion)
                        → OR: Inngest/Trigger.dev for serverless job scheduling
```

---

## Can You Ship on Snowflake?

Snowflake replaces the **analytical database** layer, not the application database.

### What maps to Snowflake:

| Component | Snowflake Fit | Notes |
|-----------|--------------|-------|
| **Analytical DB** (signal-builder-backend's `analytical_db/`) | ✅ Perfect | This is exactly what Snowflake is for |
| **Signal execution** (SQL queries against client data) | ✅ Perfect | Snowflake SQL is ANSI-compatible |
| **Client ranking** (batch processing) | ✅ Good | Snowflake Tasks replace Celery for batch SQL |
| **Document ranking** | ⚠️ Partial | Needs text processing, Snowpark can handle |
| **Vector search** | ✅ Cortex AI | `EMBED_TEXT()`, `VECTOR_COSINE_SIMILARITY()` |
| **Content ingestion** | ❌ No | Snowflake doesn't scrape websites or parse PDFs |
| **Auth/users** | ❌ No | Snowflake is a data warehouse, not an app DB |
| **CRUD operations** | ❌ No | Snowflake isn't designed for high-frequency row-level ops |

### The Honest Answer: **Snowflake replaces Oracle + analytical PostgreSQL, not the whole stack**

```
Signal Studio (Next.js) → Supabase (Auth + App DB + Storage)
                        → Snowflake (Analytical queries + Vector search + ML)
                        → Worker Service (ETL, content ingestion, adapters)
```

---

## The Recommended Architecture: Supabase + Snowflake + Workers

```
┌─────────────────────────────────────────────────────────┐
│  Signal Studio (Next.js on Vercel/Railway)              │
│  - UI, API routes, BFF                                   │
│  - Supabase Auth (email, Google, SAML)                  │
│  - Supabase Realtime (live signal updates)              │
└────────────┬────────────────────┬───────────────────────┘
             │                    │
    ┌────────▼────────┐  ┌───────▼──────────┐
    │   Supabase      │  │   Snowflake      │
    │   (App Layer)   │  │   (Data Layer)   │
    │                 │  │                   │
    │ - Users/Orgs    │  │ - Client data     │
    │ - Signals CRUD  │  │ - Holdings        │
    │ - Conversations │  │ - Transactions    │
    │ - Permissions   │  │ - Signal results  │
    │ - pgvector      │  │ - Cortex AI       │
    │ - File storage  │  │ - Vector search   │
    │ - Edge Functions│  │ - Snowpark ML     │
    └────────┬────────┘  └───────┬──────────┘
             │                    │
    ┌────────▼────────────────────▼──────────┐
    │   Worker Service (Railway/Render)       │
    │   Python/Node.js                        │
    │                                          │
    │ - Celery tasks → pg_cron + Inngest      │
    │ - Content ingestion (RSS, PDF)          │
    │ - CRM adapters (Wealthbox, Bridge)      │
    │ - NL→SQL translator                     │
    │ - Customer-specific ETL                 │
    └─────────────────────────────────────────┘
```

### What you can cut entirely:
- **Django 3.2 monolith** — replaced by Supabase + Edge Functions + Worker Service
- **uWSGI** — Vercel/Railway handles serving
- **Oracle 23ai** — replaced by Supabase pgvector + Snowflake Cortex
- **Custom JWT implementation** — replaced by Supabase Auth
- **Django Admin** — build admin pages in Next.js (or use Supabase Dashboard)

### What you must keep (in the Worker Service):
- **Signal NL→SQL translator** (apps/translators/) — 30+ Python files of AST manipulation. Not trivially rewritable.
- **Content ingestion** — PDF parsing, RSS scraping, web crawling
- **CRM adapters** — Wealthbox, Bridge file creation
- **Customer-specific ETL** — Invesco materialized views, LPL/Pershing data schemas

### Migration Effort Estimate:

| Phase | Work | Time |
|-------|------|------|
| **Phase 1: Signal Studio on Supabase** | Auth, app DB, pgvector, conversations | 1-2 weeks |
| **Phase 2: DataProvider abstraction** | Snowflake + Supabase + Oracle providers | 1-2 weeks |
| **Phase 3: Worker Service** | Extract Celery tasks, NL→SQL, content ingestion into standalone service | 2-3 weeks |
| **Phase 4: Customer migration** | Move customer data from PostgreSQL → Snowflake, validate | 2-4 weeks |
| **Phase 5: Decommission Django** | Verify all functionality works, sunset monolith | 1-2 weeks |
| **Total** | | **7-13 weeks** |

---

## Bottom Line

**Can you ship on Supabase?** Yes, for the application layer (auth, CRUD, storage, realtime, vector search). You still need a compute layer for background jobs and complex Python logic.

**Can you ship on Snowflake?** Yes, for the analytical/data layer (signal execution, client ranking, vector search, ML). Not for the application layer.

**The winning combo is both:** Supabase for the app, Snowflake for the data, a lightweight worker service for the Python business logic that can't be rewritten overnight.

**The Django monolith can be fully replaced.** It's not a question of if, it's a question of sequencing. Start with Signal Studio (already 70% decoupled), prove the Supabase + Snowflake stack works, then migrate the legacy ForwardLane features over time.
