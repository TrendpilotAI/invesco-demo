# 🔬 ForwardLane Repo Consolidation Analysis
**Date:** Feb 22, 2026 | **Analyst:** Honey 🍯

## What We Have Running (Railway)
- **Signal Studio** (Next.js 15) — visual builder, AI chat, NL→SQL ✅
- **Django Backend** — 150 models, auth, signal CRUD, API ✅
- **Dual Postgres + Redis + Celery** ✅

## The 13 Other Repos — Verdict

---

### 🟢 ABSORB: signal-builder-backend (Python/FastAPI)
**What it has that we DON'T:**
- **Schema Manager** — SQLAlchemy models for the analytical DB with FULL Invesco schema (60+ columns per table vs my 15-column simplified version). This is the source of truth.
- **Signal Construction Engine** — Visual node/edge graph → SQL compiler with 20+ validators for datasets, filters, group functions, ordering, objectives. This is Gap 5 solved.
- **Schema Builder** — Data node/data point abstraction that lets you browse available tables + columns. This is Gap 2 solved.
- **Signal UI storage** — Persists visual builder state server-side. This is Gap 3 partially solved.
- **Analytical DB Sync** — Keeps analytical DB in sync with Django default DB.

**Recommendation:** Don't deploy separately. **Extract the 3 key modules into Signal Studio's API routes:**
1. Schema manager schemas → replace my hardcoded schema context in NL→SQL prompt
2. Signal construction validators → add to /api/signals/validate endpoint
3. Signal node/edge models → wire to React Flow visual builder persistence

**Effort:** 3-4 days to extract and integrate
**Why not deploy as-is:** It's a FastAPI app with its own DB models (SQLAlchemy, Alembic). Running it separately means 2 Python backends + schema synchronization hell. Better to absorb the logic into Django or Signal Studio.

---

### 🟡 DEPLOY LATER: core-admin-ui (React/Antd)
**What it has that we DON'T:**
- **Signal Settings** — CRUD for signal collections, tags, weights, notifications. Full signal management UI.
- **System Admin** — Pipeline manager, job logs, ranking results, row rejects, NBActions.
- **System Status** — Dashboard showing system health.
- **Test Data** — CRUD pages for clients, contacts, CRM notes, documents, holdings, transactions, feedback, financial accounts.
- **Relationship Data Management** — Financial account ↔ client mapping.
- **Dashboards** — Client ranking signals overview, user feedback overview.
- **Org Settings** — Multi-tenant configuration.

**Recommendation:** Deploy as a separate Railway service later. It's an admin panel — Nathan and ops need it, but not for the Invesco demo. It talks to the Django API directly.

**Effort:** 1 day to Dockerize + deploy (Create React App, straightforward)
**When:** After Django backend is stable and seeded with real data.

---

### 🟡 DEPLOY LATER: core-admin (Flask)
**What it is:** The backend for core-admin-ui. Flask app with 20+ controllers for test data management, pipeline control, jobs, rankings, reprocessing.

**Recommendation:** Deploy alongside core-admin-ui as a pair. Both talk to the Django DB.

**Effort:** 1 day (Flask, simple Docker)
**When:** Same time as core-admin-ui.

---

### 🟡 EXTRACT WIDGETS: fl-web-widgets (React, npm package)
**What it has that we DON'T:**
- **Client Prioritization Widget** — Sortable client table with priority ranking, signal filters, collection filters. This is what Craig saw in Salesforce.
- **Signals Insights Widget** — Most-triggered signals by day/week/month with rule cards.
- **Content Personalization Widget** — Content recommendations per client.
- **Content Insights Widget** — Document cards with engagement metrics.
- **Clients for Document Widget** — Which clients should see a specific document.

**Recommendation:** Don't deploy as standalone. **Embed the Client Prioritization and Signals Insights widgets into Signal Studio as new pages/components.** They're React components that call the Django API — they'll work directly in our Next.js app with minimal adaptation.

**Effort:** 2-3 days to port the 2 key widgets into Signal Studio
**Why this matters:** These widgets ARE the Invesco demo. Craig asked for "easy buttons in Salesforce" — these are literally those buttons.

---

### 🔴 DON'T DEPLOY: signal-builder-frontend (React/Craco)
**Why:** Signal Studio IS the replacement. The old signal builder has: catalog, builder, creator, preview, collections, onboarding modules. All of these exist (better) in Signal Studio's React Flow builder.

**What to extract:** The onboarding flow is nice — multi-step wizard with data source selection. Could inspire Signal Studio's onboarding.

**Effort to extract onboarding:** 1 day
**Deploy:** Never. It's superseded.

---

### 🔴 DON'T DEPLOY: forwardlane_advisor (Express/Node)
**Why:** 4,752 files. Legacy Express app with MySQL, AMQP, DynamoDB. 35+ route modules covering everything from 2016-2019 era. This is the app Signal Studio replaces.

**What to extract:** Nothing. All functionality lives in Django backend + Signal Studio now.

---

### 🔴 DON'T DEPLOY: wealth-advisor-webapp
**Why:** Static HTML/jQuery demo dashboard. No dynamic functionality. Useful only as a design reference.

---

### 🔴 DON'T DEPLOY: demo-client-view
**Why:** Static demo screenshots. No code.

---

### 🔴 DON'T DEPLOY: front-end-ai
**Why:** 2 files, 12KB. Basically empty placeholder repo.

---

### 🔴 DON'T DEPLOY: generative-ai
**Why:** 2 files, 12KB. Empty placeholder.

---

### 🔴 DON'T DEPLOY: fl_web
**Why:** 218 files, appears to be an older marketing/web property. Not related to Signal Studio.

---

### 🔴 DON'T DEPLOY: cb-forwardlane-sites
**Why:** Static marketing site assets (26MB of images/CSS). Use forwardlane.com (Webflow) instead.

---

### 🔴 DON'T DEPLOY: web-site
**Why:** 1 file. Likely a redirect or placeholder.

---

## The Consolidation Plan

### Phase 1: Absorb Signal Builder Backend (This Week)
Extract 3 modules from `signal-builder-backend` into Signal Studio:

```
signal-builder-backend/          →  Signal Studio
├── apps/analytical_db/
│   └── schema_manager/          →  /api/schema/ endpoint (auto-detect tables)
│       └── schemas/invesco/     →  Replace hardcoded NL→SQL schema context
├── apps/signals/
│   └── features/
│       └── signal_construction/ →  /api/signals/validate endpoint
│           ├── signal_node.py   →  React Flow node persistence
│           └── signal_edge.py   →  React Flow edge persistence
└── apps/schema_builder/
    └── operations/              →  /api/signals/compile (visual → SQL)
        ├── basic_operators.py
        ├── group_functions.py
        ├── operators.py
        └── ordering.py
```

### Phase 2: Port Key Widgets (Next Week)
Port from `fl-web-widgets` into Signal Studio:

```
fl-web-widgets/                  →  Signal Studio
├── client-prioritization-widget →  /clients page (prioritized client table)
└── signals-insights-widget      →  /dashboard page (most-triggered signals)
```

### Phase 3: Deploy Admin Panel (Week After)
Deploy `core-admin` + `core-admin-ui` as Railway services:

```
Railway Project
├── Signal Studio (Next.js)      ← exists ✅
├── Django Backend               ← exists ✅
├── Core Admin UI (React/Antd)   ← NEW service
├── Core Admin API (Flask)       ← NEW service
├── Postgres x2 + Redis          ← exists ✅
└── Celery Worker + Beat         ← exists ✅
```

### What We're NOT Doing
- ❌ Not deploying 7 legacy repos
- ❌ Not running signal-builder-backend as a separate service
- ❌ Not running signal-builder-frontend (superseded)
- ❌ Not duplicating DB adapters or schema sync

## Summary Scorecard

| Repo | Files | Verdict | Value | Action |
|------|-------|---------|-------|--------|
| signal-builder-backend | 527 | 🟢 ABSORB | Schema manager + signal compiler | Extract into Signal Studio |
| core-admin-ui | 613 | 🟡 LATER | Admin/ops panel | Deploy as Railway service |
| core-admin | 175 | 🟡 LATER | Admin API | Deploy with core-admin-ui |
| fl-web-widgets | 430 | 🟡 EXTRACT | Salesforce widgets | Port 2 key widgets to SS |
| signal-builder-frontend | 368 | 🔴 SKIP | Superseded by SS | Extract onboarding only |
| forwardlane_advisor | 4773 | 🔴 SKIP | Legacy | Nothing to extract |
| wealth-advisor-webapp | 125 | 🔴 SKIP | Static demo | Design reference only |
| demo-client-view | 101 | 🔴 SKIP | Screenshots | Nothing |
| front-end-ai | 2 | 🔴 SKIP | Empty | Nothing |
| generative-ai | 2 | 🔴 SKIP | Empty | Nothing |
| fl_web | 218 | 🔴 SKIP | Old marketing | Nothing |
| cb-forwardlane-sites | 397 | 🔴 SKIP | Static assets | Nothing |
| web-site | 1 | 🔴 SKIP | Placeholder | Nothing |
