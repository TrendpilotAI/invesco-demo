# 241 · P2 · Trendpilot — WebSocket Realtime Updates (Supabase Realtime)

## Status
pending

## Priority
P2 — UX improvement (replace polling)

## Description
Replace the React dashboard's 30-second polling (`setInterval`) with Supabase Realtime subscriptions. When new topics are inserted into the `topics` table, the dashboard updates instantly. Also push newsletter status changes (draft → sent) in real time.

## Dependencies
- TODO #236 (Supabase data store) — topics must be in Supabase for Realtime to work
- TODO #238 (Auth) — Realtime channels need authenticated Supabase client

## Estimated Effort
1 day

## Coding Prompt

```
You are working on the Trendpilot project at /data/workspace/projects/Trendpilot/.

TASK: Replace dashboard polling with Supabase Realtime subscriptions.

STEP 1 — Enable Realtime on Supabase tables:
In Supabase dashboard → Database → Replication, enable Realtime for:
- `topics` table (INSERT events)
- `newsletters` table (UPDATE events)
- `subscribers` table (INSERT events)

Or via SQL migration:
```sql
ALTER TABLE topics REPLICA IDENTITY FULL;
ALTER TABLE newsletters REPLICA IDENTITY FULL;
ALTER TABLE subscribers REPLICA IDENTITY FULL;
-- Add tables to supabase_realtime publication:
ALTER PUBLICATION supabase_realtime ADD TABLE topics, newsletters, subscribers;
```

STEP 2 — Create `dashboard/src/hooks/useRealtimeTopics.ts`:
```ts
import { useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';

export function useRealtimeTopics(initialTopics: Topic[] = []) {
  const [topics, setTopics] = useState<Topic[]>(initialTopics);

  useEffect(() => {
    const channel = supabase
      .channel('topics-changes')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'topics' },
        (payload) => {
          setTopics(prev => [payload.new as Topic, ...prev].slice(0, 100));
        }
      )
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, []);

  return topics;
}
```

STEP 3 — Create `dashboard/src/hooks/useRealtimeNewsletters.ts`:
```ts
import { useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';

export function useRealtimeNewsletters(initial: Newsletter[] = []) {
  const [newsletters, setNewsletters] = useState<Newsletter[]>(initial);

  useEffect(() => {
    const channel = supabase
      .channel('newsletters-changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'newsletters' },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setNewsletters(prev => [payload.new as Newsletter, ...prev]);
          } else if (payload.eventType === 'UPDATE') {
            setNewsletters(prev =>
              prev.map(n => n.id === payload.new.id ? { ...n, ...payload.new } as Newsletter : n)
            );
          } else if (payload.eventType === 'DELETE') {
            setNewsletters(prev => prev.filter(n => n.id !== payload.old.id));
          }
        }
      )
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, []);

  return newsletters;
}
```

STEP 4 — Update `dashboard/src/App.tsx` (or relevant page components):
Remove `setInterval` polling:
```tsx
// REMOVE THIS:
useEffect(() => {
  const interval = setInterval(fetchTopics, 30000);
  return () => clearInterval(interval);
}, []);

// REPLACE WITH:
const topics = useRealtimeTopics(initialTopics);
```

STEP 5 — Add a "Live" badge to the dashboard header:
```tsx
function LiveBadge() {
  const [connected, setConnected] = useState(false);
  
  useEffect(() => {
    const channel = supabase.channel('connection-test')
      .subscribe((status) => {
        setConnected(status === 'SUBSCRIBED');
      });
    return () => { supabase.removeChannel(channel); };
  }, []);
  
  return (
    <span className={`live-badge ${connected ? 'connected' : 'disconnected'}`}>
      {connected ? '● LIVE' : '○ Connecting...'}
    </span>
  );
}
```

STEP 6 — Add CSS for live badge:
```css
.live-badge.connected { color: #22c55e; font-size: 12px; font-weight: 600; }
.live-badge.disconnected { color: #94a3b8; font-size: 12px; }
```

STEP 7 — Presence for concurrent editors (optional enhancement):
```ts
// Show how many users are viewing the dashboard
const channel = supabase.channel('dashboard', {
  config: { presence: { key: user.id } }
});
channel.on('presence', { event: 'sync' }, () => {
  const state = channel.presenceState();
  setActiveUsers(Object.keys(state).length);
}).subscribe(async (status) => {
  if (status === 'SUBSCRIBED') {
    await channel.track({ user: user.email, online_at: new Date().toISOString() });
  }
});
```
```

## Acceptance Criteria
- [ ] No `setInterval` polling in dashboard components
- [ ] Adding a new topic via API appears in dashboard within 2 seconds (no refresh)
- [ ] Newsletter status change (draft → sent) updates in dashboard in real time
- [ ] "● LIVE" badge shows green when Realtime channel is connected
- [ ] Badge shows grey when connection drops
- [ ] No memory leaks — channel subscriptions cleaned up on component unmount
- [ ] Works with authenticated Supabase client (respects RLS policies)
