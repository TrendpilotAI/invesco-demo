# TODO — ForwardLane Repo Intelligence Sprint
**Generated:** 2026-03-08 | **Source:** Dependency Graph, Dead Code Radar, Tech Debt Heatmap, Vector Pipeline Review

## Priority Legend
- **P0** — Critical / blocking production
- **P1** — High impact, do this week
- **P2** — Medium, improves quality significantly
- **P3** — Nice to have, incremental improvement

---

## 🔴 Circular Dependencies (10 tasks)

- [ ] **RI-001** `[P1/L]` Break `core` ↔ `feedback` circular dep — move shared interfaces to `core.interfaces`
- [ ] **RI-002** `[P1/L]` Break `core` ↔ `forwardlane` circular dep — extract settings access pattern
- [ ] **RI-003** `[P1/M]` Break `ai` ↔ `document_ranking` circular dep — introduce service layer
- [ ] **RI-004** `[P1/M]` Break `portfolio` ↔ `customers.advisor_target` circular dep — use signals/events
- [ ] **RI-005** `[P1/M]` Break `portfolio` ↔ `customers.pershing` circular dep — customer adapter pattern
- [ ] **RI-006** `[P1/M]` Break `client_ranking` ↔ `customers.invesco` circular dep — critical for Invesco demo isolation
- [ ] **RI-007** `[P1/M]` Break `core.importer` ↔ `portfolio` circular dep — importer should not know portfolio internals
- [ ] **RI-008** `[P1/M]` Break `core.importer` ↔ `market_data` circular dep — same pattern
- [ ] **RI-009** `[P1/M]` Break `pipeline_engine` ↔ `user` circular dep — pipeline should be user-agnostic
- [ ] **RI-010** `[P1/M]` Break `product_update` ↔ `ranking` circular dep — content vs scoring separation

## 💀 Dead Code Removal (10 tasks)

- [ ] **RI-011** `[P2/S]` Remove orphaned `analytical` app — no imports in or out
- [ ] **RI-012** `[P2/S]` Audit `api` app — orphaned in dep graph, may be URL-routed only
- [ ] **RI-013** `[P2/S]` Remove orphaned `entities` app — confirmed dead code
- [ ] **RI-014** `[P2/S]` Audit `adapters.wealthbox` — leaf node, check if actively used
- [ ] **RI-015** `[P2/S]` Audit `customers.lpl` — leaf node, check if client is active
- [ ] **RI-016** `[P2/S]` Audit `customers.sei` — leaf node, check if client is active
- [ ] **RI-017** `[P2/M]` Remove `recommendation_top` if unused — leaf node in dep graph
- [ ] **RI-018** `[P2/S]` Remove auto-generated `versioneer.py` files — migrate to `setuptools-scm`
- [ ] **RI-019** `[P2/M]` Scan all Celery tasks for unused/unregistered tasks and remove
- [ ] **RI-020** `[P2/M]` Scan all management commands — remove any not called in 12+ months

## 🔥 Tech Debt Hotspots (10 tasks)

- [ ] **RI-021** `[P1/XL]` Split `easy_button/views.py` (1,813 LOC, 120 branches) into domain-specific view modules
- [ ] **RI-022** `[P1/L]` Split `portfolio/models.py` (933 LOC) — extract business logic to services
- [ ] **RI-023** `[P1/M]` Refactor `market_data/iex/iex_cloud_loader.py` (79 branches) — break into smaller functions
- [ ] **RI-024** `[P2/L]` Add tests for `easy_button/views.py` — highest-complexity file with zero coverage
- [ ] **RI-025** `[P2/L]` Add tests for `portfolio/models.py` — core domain model with zero coverage
- [ ] **RI-026** `[P2/M]` Add tests for `iex_cloud_loader.py` — market data integrity critical
- [ ] **RI-027** `[P2/M]` Resolve 160 TODO/FIXME/HACK markers across codebase — triage and close
- [ ] **RI-028** `[P2/S]` Replace `versioneer` with `setuptools-scm` in `libs/sentiment_analyze` and `libs/recommended_weights`
- [ ] **RI-029** `[P2/L]` Extract `core` god module — split into `core.models`, `core.services`, `core.utils`, `core.interfaces`
- [ ] **RI-030** `[P3/M]` Add type hints to top 20 hotspot files — improve IDE support and catch bugs

## 🏗️ Infrastructure & Upgrades (10 tasks)

- [ ] **RI-031** `[P0/M]` Push Python 3.11 upgrade branch and deploy to staging — already on `upgrade/python311-django42`
- [ ] **RI-032** `[P0/M]` Deploy new Entity Extraction FastAPI service to Railway — Dockerfile ready
- [ ] **RI-033** `[P0/S]` Set `DJANGO_ENV=production` in Railway to enable HTTPS redirect + HSTS
- [ ] **RI-034** `[P0/S]` Set `REDIS_URL` in Railway production to activate Redis caching
- [ ] **RI-035** `[P1/M]` Consolidate forwardlane-backend and signal-studio-backend into monorepo — confirmed near-identical (160K LOC each)
- [ ] **RI-036** `[P1/S]` Restrict `ALLOWED_HOSTS` in Railway production — verify tight whitelist
- [ ] **RI-037** `[P1/M]` Wire Entity Extraction service URL into Django backend settings — update `ENTITY_EXTRACTION_SERVICE_URL`
- [ ] **RI-038** `[P1/L]` Add CI pipeline for entity-extraction-service (pytest + Docker build + deploy)
- [ ] **RI-039** `[P2/M]` Add `select_related`/`prefetch_related` to all serializers with nested relations (N+1 query prevention)
- [ ] **RI-040** `[P2/M]` Audit all Django settings across repos — find contradictions and unused env vars

## 🔒 Security & Compliance (5 tasks)

- [ ] **RI-041** `[P0/M]` Rotate Ultrafone API keys — GROQ, Deepgram, Twilio, Fish Audio committed in `.env.development`
- [ ] **RI-042** `[P1/L]` Run secret scanner across all 137 repos full git history — find and rotate all committed credentials
- [ ] **RI-043** `[P1/M]` License audit — map all pip/npm deps to licenses, flag GPL contamination
- [ ] **RI-044** `[P1/L]` PII data flow map — trace personal data from ingestion → storage → API exposure
- [ ] **RI-045** `[P2/M]` Confirm `CORS_ALLOW_ALL` is NOT set in Railway production

## 📊 Oracle Vector Pipeline (5 tasks)

- [ ] **RI-046** `[P1/S]` Fix JSON vs CLOB type inconsistency in `insights_vectorized.metadata` column
- [ ] **RI-047** `[P1/M]` Add parallel embedding generation — currently sequential, bottleneck at scale
- [ ] **RI-048** `[P2/S]` Tighten vector search similarity threshold (currently 0 = matches everything)
- [ ] **RI-049** `[P2/M]` Add monitoring/alerting for vectorization pipeline failures
- [ ] **RI-050** `[P2/S]` Document Oracle connection setup in README for dev onboarding
