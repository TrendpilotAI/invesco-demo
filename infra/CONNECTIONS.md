# OpenClaw Infra Connections – Railway Project

Last updated: 2026-03-13

**Railway Project ID:** 90f53968-9390-4200-8c85-e1a49d65e196

---

## Core Connected Services

| Service        | Internal Host/Port          | Depends On           | Key Env Vars           | Description                         |
|----------------|----------------------------|----------------------|------------------------|-------------------------------------|
| OpenClaw Core  | openclaw.internal:5000     | Redis, Postgres, LanceDB, Convex, n8n, Temporal | REDIS_URL, PG_URL, CONVEX_URL, LANCEDB_PATH, N8N_URL, TEMPORAL_URL | Main agent orchestrator & API      |
| Convex         | convex.internal:443        | Postgres (backup)    | CONVEX_DEPLOY_KEY      | Realtime operational DB/dashboard    |
| Postgres       | postgres.internal:5432     | -                    | DATABASE_URL           | Main relational DB (long-term state) |
| LanceDB        | lancedb.internal:/mnt/data | S3/Filesystem backed | LANCEDB_PATH           | Vector AI-memory/search DB           |
| Redis          | redis.internal:6379        | -                    | REDIS_URL              | Cache, pub/sub, live state           |
| n8n            | n8n.internal:5678          | All above            | N8N_URL, API KEYS      | Automation & workflow engine         |
| Temporal.io    | temporal.internal:7233     | OpenClaw, n8n        | TEMPORAL_URL           | Durable background workflow engine   |

---

## Universal Rules
- All services run inside Railway's private network: communicate via hostnames above.
- Each service gets its connection/env vars via Railway console or secrets manager, *never* hard-coded or exposed externally.
- Sensitive data (API keys, secrets) are service-scoped and per-tenant isolated where applicable.
---

## Key Integration Flows
- **OpenClaw Core** can call, orchestrate, and pull/push to all services above for agents, memory, dashboards, and automation.
- **n8n** orchestrates multi-step flows, triggers Temporal workflows, syncs with external APIs.
- **Temporal.io** is used for long-running jobs, agent task orchestration (durable retries, timeouts, saga/cancellation workflows).
- **Convex** is the live source of ops state and triggers updates or webhooks to other services.
- **Postgres** stores main records for compliance, analytics, and backup/restore.
- **LanceDB** is the memory/search vector DB for all agent/workflow automation.
- **Redis** caches, queues, and supports real-time agent or dashboard features.

---

## Testing the Mesh
- Health checks, connect scripts, and agent startup tests verify all above services are live, reachable, and properly authorized at container/service start.
- Agents periodically refresh their knowledge of available internal services for routing/scheduling.

---

For onboarding, update this file and also edit MANIFEST.md to add/change protocols, workflow routes, or access boundaries as your infra grows.
