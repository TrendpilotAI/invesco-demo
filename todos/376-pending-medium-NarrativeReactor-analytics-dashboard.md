# 376 — Add Analytics Dashboard with Cost/Performance Trends

## Task Description
`costTracker.ts` already accumulates per-call AI cost data. Extend it to expose structured analytics via API endpoints, then surface them in the React dashboard with charts showing cost trends, content generation counts, and publish success rates.

## Coding Prompt
You are working on the NarrativeReactor repo at `/data/workspace/projects/NarrativeReactor/`.

### Step 1: Analytics SQLite Table
If `costTracker.ts` uses a flat JSON file (`data/costs.json`), migrate it to SQLite first (see BRAINSTORM.md P0 item). Add to `src/lib/db.ts`:

```sql
CREATE TABLE IF NOT EXISTS analytics_events (
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,   -- 'generation', 'publish', 'campaign_complete', 'error'
  tenant_id TEXT,
  brand_id TEXT,
  model TEXT,
  tokens_used INTEGER,
  cost_usd REAL,
  duration_ms INTEGER,
  status TEXT,                -- 'success' | 'error'
  metadata TEXT,              -- JSON blob for extra fields
  created_at INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE INDEX IF NOT EXISTS idx_analytics_events_created_at ON analytics_events(created_at);
CREATE INDEX IF NOT EXISTS idx_analytics_events_event_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_events_tenant_id ON analytics_events(tenant_id);
```

### Step 2: Analytics Service
Create `src/services/analyticsService.ts` with methods:
- `recordEvent(event: AnalyticsEvent)` — insert event row
- `getCostSummary(from: Date, to: Date, tenantId?: string)` → `{ total_usd, by_model, by_day }`
- `getGenerationStats(from: Date, to: Date)` → `{ count, success_rate, avg_duration_ms, by_type }`
- `getPublishStats(from: Date, to: Date)` → `{ total, success, failed, by_platform }`
- `getDailyTrends(days: number)` → array of `{ date, cost, generations, publishes }`

### Step 3: Analytics API Routes
Add to `src/routes/` or `src/index.ts`:
- `GET /api/analytics/summary?from=&to=` → cost + generation summary
- `GET /api/analytics/trends?days=30` → daily trend data for charts
- `GET /api/analytics/costs?days=7` → cost breakdown by model

All endpoints require valid API key (standard auth middleware).

### Step 4: Instrument Existing Code
Update `contentPipeline.ts`, `schedulerWorker.ts`, and publisher code to call `analyticsService.recordEvent()` on:
- Each AI generation call (type: 'generation', include model + tokens + cost)
- Each publish attempt (type: 'publish', include platform + status)
- Each campaign completion (type: 'campaign_complete')

### Step 5: Dashboard Charts
In `dashboard/src/` (React app), add an Analytics page:
- Cost over time (line chart) — use Recharts or Chart.js (check what's already installed)
- Generation count by day (bar chart)
- Model cost breakdown (pie chart)
- Publish success rate (stat cards)

Fetch from `/api/analytics/trends?days=30` and `/api/analytics/summary`.

### Step 6: Tests
Add `src/__tests__/services/analyticsService.test.ts`:
- `recordEvent` inserts row
- `getCostSummary` aggregates correctly
- `getDailyTrends` returns correct day count

## Dependencies
370 (DB indexes), 375 (multi-tenant: tenant_id column in analytics table)

## Estimated Effort
L

## Acceptance Criteria
- [ ] `analytics_events` table in SQLite with proper indexes
- [ ] `analyticsService.ts` with all 5 query methods
- [ ] `/api/analytics/summary`, `/api/analytics/trends`, `/api/analytics/costs` endpoints work
- [ ] Content pipeline instruments at least generation + publish events
- [ ] Dashboard Analytics page renders cost trend chart
- [ ] Analytics service tests pass (no real AI calls)
- [ ] All existing tests pass
