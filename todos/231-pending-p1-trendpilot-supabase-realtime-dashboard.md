# TODO: Trendpilot — Replace Dashboard Polling with Supabase Realtime

**Priority:** P1 — UX improvement + infrastructure efficiency  
**Repo:** /data/workspace/projects/Trendpilot/  
**Effort:** 1-2 days  
**Dependencies:** Supabase migration done

## Description
Dashboard currently polls every 30 seconds. Replace with Supabase Realtime subscriptions for instant updates when new trends are aggregated.

## Coding Prompt (Autonomous Execution)
```
In /data/workspace/projects/Trendpilot/dashboard/src/:

1. Update dashboard/src/hooks.ts:
   - Replace setInterval polling with supabase.channel() subscription
   - Subscribe to: INSERT on aggregations table
   - On new aggregation: fetch latest topics, update state

2. Wire src/lib/realtime.ts to the Express API:
   - Broadcast events when scheduler completes an aggregation run
   - Events: 'new-trends', 'alert-triggered', 'newsletter-sent'

3. Add Supabase client to dashboard:
   - dashboard/src/lib/supabase.ts (browser client with anon key)
   - Env vars: VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY

4. Update dashboard/src/App.tsx:
   - Show live "Last updated: X seconds ago" indicator
   - Flash animation when new data arrives
   - Connection status indicator (green/red dot)

5. Update dashboard/vite.config.ts to expose VITE_ env vars

6. Tests: update tests/phase4/dashboard.test.ts for realtime behavior
```

## Acceptance Criteria
- [ ] Dashboard updates within 2 seconds of new aggregation
- [ ] No polling requests visible in network tab
- [ ] Connection drops gracefully reconnect
- [ ] "Last updated" timestamp shown
