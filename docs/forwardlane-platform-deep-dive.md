# ForwardLane Platform — Complete Deep Dive
**Prepared by Honey 🍯 — March 7, 2026**

---

## Executive Summary

ForwardLane is a **multi-layered AI-powered wealth management intelligence platform** built over ~10 years across 137 Bitbucket repos and now consolidated into ~20 active repositories. The platform spans three major systems: the **Django monolith** (core backend), the **Signal Builder** (FastAPI graph→SQL compiler), and **Signal Studio** (Next.js 15 frontend). Everything runs on Railway with dual PostgreSQL, Redis, and Celery.

The platform's core innovation is turning **natural language into executable financial SQL** — a capability no competitor has at this price point ($0.01/query).

---

## Part 1: System Architecture

### The Three Pillars

```
┌──────────────────────────────────────────────────────────────────┐
│                     SIGNAL STUDIO (Next.js 15)                   │
│  signal-studio-production.up.railway.app                         │
│                                                                  │
│  25+ pages: Signal Builder │ Signal Library │ Easy Button        │
│  Agent Chat │ Analytics │ Visual Builder │ Canvas │ Templates    │
│  Oracle Connect │ Oracle ML │ Data Mapper │ Admin │ Demo         │
└──────────────────────┬───────────────────────────────────────────┘
                       │ API calls
┌──────────────────────▼───────────────────────────────────────────┐
│              SIGNAL BUILDER BACKEND (FastAPI + SQLAlchemy)        │
│  django-backend-production-3b94.up.railway.app                   │
│                                                                  │
│  12 App Modules:                                                 │
│  ├── signals/       → Core: signal CRUD, versions, runs          │
│  ├── translators/   → THE KEY IP: semantic→SQL translation       │
│  ├── analytical_db/ → External DB sync, schema management        │
│  ├── schema_builder/→ Org schema configuration                   │
│  ├── users/         → Auth, JWT, onboarding                      │
│  ├── webhooks/      → HMAC-signed webhook delivery               │
│  ├── audit/         → Audit log middleware                        │
│  ├── events/        → Event bus (EventManager)                   │
│  ├── admin/         → Admin panel                                │
│  ├── health/        → Health checks                              │
│  └── web_services/  → ForwardLane API integration                │
│                                                                  │
│  Patterns: DI containers │ Clean Architecture │ Async SQLAlchemy │
│  Celery + Redis for background signal execution                  │
└──────────────────────┬───────────────────────────────────────────┘
                       │ DB + data sync
┌──────────────────────▼───────────────────────────────────────────┐
│           FORWARDLANE BACKEND (Django 3.2 + DRF)                 │
│  The Original Monolith — 150+ Models, Python 3.9                 │
│                                                                  │
│  20 Django Apps:                                                 │
│  ├── core/              → Base models, DataSource, Job, Document │
│  ├── entities/          → NER extraction, CRM entities           │
│  ├── easy_button/       → Salesforce "Easy Button" actions       │
│  ├── portfolio/         → Holdings, accounts, transactions       │
│  ├── ranking/           → Client/document ranking engine         │
│  ├── client_ranking/    → Client priority scoring                │
│  ├── document_ranking/  → Document relevance scoring             │
│  ├── recommendation_top/→ Top recommendations engine             │
│  ├── ai/                → ML model serving                       │
│  ├── analytical/        → Raw SQL analytical queries             │
│  ├── content_ingestion/ → Document import pipeline               │
│  ├── pipeline_engine/   → ETL pipeline orchestration             │
│  ├── market_data/       → Market data feeds                      │
│  ├── product_update/    → Product/fund update tracking           │
│  ├── access_guardian/   → Permissions, groups, RBAC              │
│  ├── user/              → Organizations, teams, users            │
│  ├── user_behavior/     → Advisor activity tracking              │
│  ├── feedback/          → Client/advisor feedback loops          │
│  ├── customers/         → Multi-tenant customer installations    │
│  └── forwardlane/       → Django project settings/config         │
│                                                                  │
│  Supporting: adapters/ │ libs/ │ seeds/ │ scripts/               │
└──────────────────────────────────────────────────────────────────┘
```

### Infrastructure (Railway)

| Service | Tech | URL |
|---|---|---|
| **Signal Studio** | Next.js 15 | signal-studio-production.up.railway.app |
| **Django Backend** | Django 3.2 + Gunicorn | django-backend-production-3b94.up.railway.app |
| **PostgreSQL (Primary)** | Postgres 15 | railway.internal |
| **PostgreSQL (Analytical)** | Postgres 15 | railway.internal |
| **Redis** | Redis 7 | railway.internal |
| **Celery Worker** | Python 3.9 | internal |
| **Celery Beat** | Python 3.9 | internal |

---

## Part 2: The Data Model (150+ Models)

### Core Domain Models

**Clients & Households:**
- `Client` — Individual client records
- `Household` / `HouseholdClient` — Household groupings
- `ClientSegment` — Client segmentation
- `ClientAccountSummary` — Account-level summaries
- `ClientOrganization` — Client-org relationships
- `ClientEmployee`, `ClientJob`, `ClientSubsidiary` — Employment/business data
- `Churn` — Churn prediction data
- `UserClient` — Advisor-client relationships

**Advisors & Teams:**
- `Advisor` — Advisor profiles
- `AdvisorPortfolioSummary` — Per-advisor portfolio metrics
- `AdvisorTraining`, `AdvisorWebinar` — Training/education tracking
- `AdvisorWebpageVisit` — Digital behavior tracking
- `PMTeam`, `PMTeamMember`, `PMTeamProduct` — Portfolio management teams
- `OrganizationTeam`, `TeamRole`, `UserTeam` — Team structure

**Portfolio & Holdings:**
- `FinancialAccount`, `FinancialAccountClient`, `FinancialAccountInvestObj`
- `Holding`, `HoldingAccount`, `HoldingType`, `HoldingsAggregation`
- `MutualFundHolding`, `MutualFundsInstrumentData`
- `AssetsUnderManagement` — AUM tracking
- `Transaction`, `TransactionAccount`, `TransactionType`, `TransactionSubtype`
- `TransactionsAggregation`
- `Flow`, `FlowBinding` — Cash flow tracking

**Products & Instruments:**
- `Product`, `Fund`, `Instrument`, `InstrumentBridge`
- `ApprovedInstrument`, `OrgInstrumentIdentifier`
- `AssetType`, `AssetSubtype`
- `InvestmentObjective`
- `PricingData`

**Market Data:**
- `SectorPerformance`, `EquitiesAdditionalMktData`, `EquitiesCorpAction`
- `MSExchangeTradedFundsBookData/RankData` — Morningstar ETF data
- `MSMutualFundsBookData/RankData` — Morningstar mutual fund data
- `MSSeparatelyManagedAccountsBookData` — SMA data
- `MSUnitInvestmentTrustsBookData` — UIT data
- `InvescoTrailingAnnualSalesByAssetType` / `InvescoTrailingMonthlySalesByAssetType`

**Business Rules & Signals:**
- `BusinessRule`, `BusinessRuleCategory`, `BusinessRuleCollection`
- `BusinessRuleParameter`, `BusinessRuleTag`, `BusinessRuleSnooze`
- `Signal`, `SignalBuilderRule`
- `IntentSignals`, `TickerIntent`, `InterestTopic`
- `NBAction`, `NBActionBusinessRuleBinding` — Next Best Action

**Recommendations & Ranking:**
- `DataScienceRecommendation` — THE KEY ML MODEL (scores per advisor)
- `RecommendedBusinessRule`
- `RecommenderLog`, `DocumentRecommendationLog`
- `ClientRankingHistory`, `ClientRankingMetadata`
- `DocumentRankingResult`, `DocumentRankingMetadata`
- `LikedNBA` — Advisor preference tracking

**Content & Documents:**
- `Document`, `DocumentEntity`, `DocumentMeta`, `DocumentMetaSummarization`
- `DocumentTopic`, `DocumentTopicDescription`
- `DocumentRecommenderMatrixData`
- `ContentIngestionJob`, `ContentIngestionDocument`

**CRM & Activities:**
- `CrmActivity`, `CrmCallNote`, `CrmEmail`, `CrmNote`
- `CRMNoteEntity`, `CRMNoteMeta`
- `Campaign`, `ClientCampaign`
- `LoginHistory`, `UserAuditHistory`, `UserBehavior`
- `PracticeMetric`

**Infrastructure:**
- `Organization`, `OrganizationPreferences`, `OrganizationRegion`
- `DataSource`, `DataSourceLocation`, `DataSourceOrganizationBinding`
- `ImportJob`, `ImportJobInstance`, `Job`, `CoreJobLog`
- `PipelineService`, `PipelineServiceBinding`
- `SalesforceSecret`, `Wealthbox` — External service configs
- `AccessGuardianCustomGroup/Permission/PermissionsSet` — RBAC

---

## Part 3: The Key IP — NL→SQL Translation Engine

### How It Works

The `translators/` module in `signal-builder-backend` is the crown jewel:

```
User types: "Show me clients with >$500K in equities 
             who haven't been contacted in 90 days"
                              │
                              ▼
              ┌─ Semantic Layer Translators ─┐
              │  Parse natural language into  │
              │  signal node graph            │
              └──────────────┬───────────────┘
                             │
              ┌──────────────▼───────────────┐
              │  Signal Data Translators       │
              │  Graph nodes → SQLAlchemy      │
              │  expressions                   │
              └──────────────┬───────────────┘
                             │
              ┌──────────────▼───────────────┐
              │  SQL Compiler                  │
              │  Expressions → executable      │
              │  PostgreSQL query              │
              └──────────────┬───────────────┘
                             │
                             ▼
              Actionable client list + data
              Cost: ~$0.01 per generation
```

### Invesco Schema

- **22 tables**, **200+ columns**
- Covers: advisor profiles, client accounts, holdings, transactions, AUM, product data, Morningstar analytics
- Fully mapped and tested

### Signal Builder Frontend

Visual graph-based signal construction:
- Drag-and-drop nodes
- Filter conditions, aggregations, groupings
- Preview SQL output
- Save to Signal Library
- Schedule execution via Celery

---

## Part 4: The Five Frontend Generations

| Gen | Era | Tech | Status |
|---|---|---|---|
| **Gen 1** | 2016-2017 | Express.js server-rendered | Dead |
| **Gen 2** | 2017-2019 | jQuery + custom widgets | Dead |
| **Gen 3** | 2019-2021 | React + Ant Design (`fl_web`) | Legacy, some features still referenced |
| **Gen 4** | 2021-2023 | React + Craco (`signal-builder-frontend`) | Active for signal builder |
| **Gen 5** | 2023-2026 | Next.js 15 (`signal-studio`) | **Current primary** |

### Signal Studio (Gen 5) — 25+ Pages

| Page | Function |
|---|---|
| `/signal-builder` | Visual graph-based signal construction |
| `/signal-library` | Browse, search, manage saved signals |
| `/signal-studio` | NL→SQL natural language signal creation |
| `/easy-button` | Salesforce-embedded quick actions |
| `/easy-button/embed` | iFrame embed for Salesforce LWC |
| `/analytics` | Signal performance dashboards |
| `/agent` | AI agent chat interface |
| `/chat` | Conversational signal exploration |
| `/canvas` | Visual signal canvas |
| `/visual-builder/*` | Enhanced visual signal builder (3 variants) |
| `/templates` | Signal templates marketplace |
| `/oracle-connect` | Oracle DB connection manager |
| `/oracle-ml` | Oracle ML model integration |
| `/data-mapper` | Schema mapping tool |
| `/admin` | Admin dashboard |
| `/session-dashboard` | Active session management |
| `/demo/*` | Demo pages (AI prompt, animated input) |

---

## Part 5: The Satellite Repos

### Active & Critical

| Repo | Tech | Purpose | Status |
|---|---|---|---|
| **forwardlane-backend** | Django 3.2 | Core monolith, 150+ models | Production on Railway |
| **signal-builder-backend** | FastAPI + SQLAlchemy | NL→SQL engine, signal execution | Production on Railway |
| **signal-studio** | Next.js 15 | Primary frontend | Production on Railway |
| **signal-builder-frontend** | React + Craco | Legacy signal builder UI | Active, Gen 4 |
| **signal-studio-frontend** | Next.js | Signal Studio alternate frontend | Active |
| **signal-studio-auth** | Auth service | JWT/session management | Active |
| **signal-studio-data-provider** | Data service | External data connectors | Active |
| **signal-studio-templates** | Templates | Signal template marketplace | Active |
| **signal-studio-api-docs** | Docs | API documentation site | Active |
| **invesco-retention** | React + Salesforce LWC | Invesco demo & retention tools | **Live demo** |
| **forwardlane_advisor** | Node.js (Express) | Legacy advisor portal (Gen 1-2) | Legacy, being replaced |
| **core-entityextraction** | Python | NER extraction service | Needs rewrite as FastAPI |

### Supporting

| Repo | Purpose | Status |
|---|---|---|
| **core-admin / core-admin-ui** | Internal admin tools | Active |
| **fl-web-widgets** | Embeddable widgets | Legacy |
| **fl_web** | Gen 3 React frontend | Legacy |
| **forwardlane-website** | Marketing site | Active |
| **salesforce-lightning-nowbrief** | Salesforce LWC for NowBrief | Active |
| **wealth-advisor-webapp** | Advisor web application | Legacy |
| **cb-forwardlane-sites** | Cloudflare/Bitbucket sites | Infrastructure |

---

## Part 6: The ML & AI Layer

### DataScienceRecommendation Model
- Generates per-advisor ML scores
- Factors: client portfolio composition, activity history, market conditions, document relevance
- Powers the recommendation engine that tells advisors which clients to contact and why

### Document Ranking Engine
- Ingests market commentary, product updates, research notes
- Ranks relevance per advisor per client
- Matrix-based collaborative filtering (`DocumentRecommenderMatrixData`)
- Feeds into Next Best Action

### Client Ranking Engine
- Scores clients by priority for advisor attention
- Tracks ranking history over time (`ClientRankingHistory`)
- Uses: AUM, activity recency, churn risk, opportunity signals

### Next Best Action (NBA)
- Combines business rules + ML scores + market signals
- Outputs: "Call this client because [reason], suggest [product/action]"
- Advisors can like/dismiss (`LikedNBA`, `DismissedAbstract`)
- Feedback loop improves future recommendations

### Content Ingestion Pipeline
- Ingests PDFs, market commentary, product literature
- Entity extraction (NER) via `core-entityextraction`
- Topic modeling (`DocumentTopic`, `DocumentTopicDescription`)
- Auto-summarization (`DocumentMetaSummarization`)
- Feeds document ranking engine

---

## Part 7: Easy Button (Salesforce Integration)

The "Easy Button" is ForwardLane's **Salesforce-native interface** — purpose-built for the Invesco use case:

- **Salesforce Lightning Web Component** (`salesforce-lightning-nowbrief`)
- Embeds directly into advisor's Salesforce workflow
- One-click actions: meeting prep, client brief, signal check
- `easy-button/` module in Django: 6+ models for action definitions, bindings, business rules
- `/easy-button/embed` in Signal Studio for iframe embedding
- This is what Craig Lieb specifically asked for — "easy buttons" not complex dashboards

---

## Part 8: Data Sources & Integrations

### Current Data Connectors
- **Morningstar** — Fund data, ETF data, SMA data, UIT data (multiple book/rank datasets)
- **Oracle** — Client portfolio data (Oracle Connect + Oracle ML pages in Signal Studio)
- **Salesforce** — CRM sync, activity data, Easy Button integration
- **Wealthbox** — CRM integration (`Wealthbox` model)
- **Custom CSV/ETL** — Pipeline engine for bulk data import

### Data Enrichment (New — Code Complete)
- **Data Waterfall Pipeline** — 7 providers (Hunter → FindyMail → Icypeas → QuickEnrich → Forager → Wiza → LeadIQ)
- Two-tier caching (Redis + DB, 30-day TTL)
- Located at `signal-studio-backend/enrichment/`

---

## Part 9: What's Working vs. What's Not

### ✅ Working & Production

| Component | Status | Notes |
|---|---|---|
| Signal Studio (Next.js) | **Live** | 25+ pages, Railway |
| Signal Builder Backend (FastAPI) | **Live** | NL→SQL working |
| Django Backend | **Live** | API serving, models intact |
| Dual PostgreSQL | **Live** | Primary + analytical |
| Redis + Celery | **Live** | Background jobs running |
| Invesco Demo | **Live** | trendpilotai.github.io/invesco-demo |
| NL→SQL on Invesco schema | **Tested** | 22 tables, 200+ columns |

### ⚠️ Needs Attention

| Component | Issue | Priority |
|---|---|---|
| **core-entityextraction** | Expected 404, needs FastAPI rewrite | P1 |
| **signal-studio-frontend Oracle pipeline** | "Not Started" since Oct 2025 | P0 — architectural blocker |
| **forwardlane_advisor (Node.js)** | Legacy Gen 1-2, should be sunset | P2 |
| **fl_web (React/Antd)** | Gen 3, some features not yet ported to Gen 5 | P2 |
| **Django version** | 3.2 (LTS expired April 2024) | P1 — security risk |
| **Python version** | 3.9 (EOL October 2025) | P1 — security risk |
| **psycopg2 raw connections** | In analytical views, bypasses ORM | P1 — fragile |
| **jsonpickle** | ✅ Just removed (was RCE vector) | Done |
| **Celery idempotency** | ✅ Just added Redis locks | Done |

### 🔴 Known Risks

| Risk | Detail |
|---|---|
| **Django 3.2 EOL** | No security patches since April 2024. Upgrade to 4.2 LTS is non-trivial with 150+ models |
| **Python 3.9 EOL** | End of life October 2025. Need 3.11+ migration |
| **Single developer history** | Victor Presnyackiy was primary contributor across 2000+ PRs |
| **137 repos** | Only ~20 active, but dead repos create confusion. Need archival |
| **No CI/CD pipeline** | Bitbucket Pipelines configs exist but not all active |
| **Test coverage** | Uneven — signal-builder-backend has tests, Django backend spotty |

---

## Part 10: The Competitive Moat

### What ForwardLane Has That Others Don't

1. **NL→SQL Signal Engine** — No competitor generates financial signals from natural language at $0.01/query
2. **10 Years of Domain Models** — 150+ models encoding deep wealth management domain knowledge
3. **DataScienceRecommendation** — ML-powered per-advisor personalization
4. **Next Best Action Engine** — Rules + ML + signals → actionable advisor recommendations
5. **Salesforce-Native Easy Button** — Embedded where advisors already work
6. **Full-Stack AI** — From content ingestion → entity extraction → document ranking → client ranking → signal generation → advisor action
7. **Invesco Relationship** — $300K enterprise client proving the platform at scale
8. **Honey AI Network** — 48 models, 9 cron jobs, self-healing infrastructure running 24/7, automatically improving the codebase

### The Platform Play

ForwardLane isn't just an RIA tool — it's a **wealth management intelligence platform** that could be:
- Licensed as SaaS to other RIAs
- White-labeled for broker-dealers
- Embedded into custodian platforms (Schwab, Altruist)
- Sold as the AI layer that sits on top of Orion/Envestnet/Tamarac

---

*Saved to: `/data/workspace/docs/forwardlane-platform-deep-dive.md`*
