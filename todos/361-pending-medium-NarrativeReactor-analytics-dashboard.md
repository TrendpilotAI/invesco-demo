# 361 · NarrativeReactor — Analytics Dashboard (Content Performance & Cost Trends)

**Priority:** medium  
**Effort:** M (1–3 days)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

`performanceTracker` and `costTracker` services collect data but there's no visual dashboard. Build an analytics view in the React dashboard showing content performance (publish success rate, engagement), AI cost trends over time, and per-tenant usage breakdowns.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/:

## Backend: Analytics API

1. Create src/routes/analyticsRoutes.ts:

GET /api/analytics/overview
Response: {
  totalContent: number,
  publishedToday: number,
  totalCost: number,        // from costTracker
  costThisMonth: number,
  avgCostPerContent: number,
  successRate: number       // % published successfully
}

GET /api/analytics/cost-trend?days=30
Response: Array<{ date: string; cost: number; requests: number }>
-- Query SQLite: GROUP BY date(created_at)

GET /api/analytics/content-performance?limit=20
Response: Array<{ id: string; title: string; platform: string; status: string; publishedAt: string; cost: number }>

2. Implement by querying existing costTracker data + content table.
   Add created_at indexing if missing for efficient date queries.

## Frontend: Analytics View

3. In dashboard/src/, create components/Analytics.tsx:

Install: npm install recharts (if not present)

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar } from 'recharts';

Display:
a) Overview cards (4 KPI tiles): Total Content | Published Today | Total AI Cost | Success Rate
b) Cost Trend LineChart (30-day sparkline)  
c) Recent Content table with status badges and cost column

Use fetch('/api/analytics/overview', { credentials: 'include' }) for data.

4. Add Analytics tab to dashboard navigation:
   <nav>
     <a href="#dashboard">Dashboard</a>
     <a href="#analytics">Analytics</a>   {/* new */}
   </nav>

5. Add React state routing or use existing router to show Analytics component on tab click.

## Styling

6. Match existing dashboard styles. Use CSS variables or Tailwind (whichever the project uses).
   KPI tiles: white card, bold number, muted label.
   Chart: 400px height, responsive container.

## Tests

7. Add tests/unit/analyticsRoutes.test.ts:
   - GET /api/analytics/overview returns correct shape
   - GET /api/analytics/cost-trend returns array with date+cost fields
   - Scoped by tenant_id if multi-tenant is active
```

---

## Dependencies

- #360 multi-tenant (tenant scoping for analytics)
- `costTracker` and `contentPipeline` services must persist to SQLite

## Acceptance Criteria

- [ ] `/api/analytics/overview` returns all 6 KPI fields
- [ ] `/api/analytics/cost-trend` returns 30 days of data
- [ ] Analytics tab visible and functional in React dashboard
- [ ] Cost trend chart renders without errors
- [ ] Data is scoped to authenticated tenant
