# 238 · P0 · Trendpilot — Implement Supabase Auth in Dashboard

## Status
pending

## Priority
P0 — dashboard is currently open to anyone

## Description
Add Supabase Auth to both the Express API (JWT middleware) and the React dashboard (login/logout UI). Use Supabase's built-in email magic link auth as the primary flow. Protect all API routes with JWT verification. The dashboard should redirect unauthenticated users to a login page.

## Dependencies
- TODO #236 (Supabase data store) must be complete
- `SUPABASE_URL` and `SUPABASE_ANON_KEY` env vars
- `SUPABASE_SERVICE_ROLE_KEY` for server-side verification

## Estimated Effort
1–2 days

## Coding Prompt

```
You are working on the Trendpilot project at /data/workspace/projects/Trendpilot/.

TASK: Add Supabase Auth — JWT middleware on Express API + login UI in React dashboard.

PART A — Express API Auth Middleware

1. Create `src/middleware/auth.ts`:
```ts
import { supabaseAdmin } from '@/lib/supabase.js';
import type { Request, Response, NextFunction } from 'express';

export async function requireAuth(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  
  const { data: { user }, error } = await supabaseAdmin.auth.getUser(token);
  if (error || !user) return res.status(401).json({ error: 'Invalid token' });
  
  (req as any).user = user;
  next();
}

export async function optionalAuth(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (token) {
    const { data: { user } } = await supabaseAdmin.auth.getUser(token);
    (req as any).user = user ?? null;
  }
  next();
}
```

2. Apply `requireAuth` to protected routes in `src/api/index.ts`:
```ts
import { requireAuth } from '@/middleware/auth.js';

// Protect dashboard-only routes
app.get('/api/newsletters', requireAuth, async (req, res) => { ... });
app.post('/api/newsletters', requireAuth, async (req, res) => { ... });
app.get('/api/subscribers', requireAuth, async (req, res) => { ... });
app.get('/api/topics', requireAuth, async (req, res) => { ... });
// Keep public: /health, /api/subscribe (newsletter signup form)
```

3. Keep existing API key auth for machine-to-machine routes (check `X-API-Key` header OR Bearer JWT).

PART B — React Dashboard Auth UI

4. In `dashboard/`, install Supabase client if not present:
```bash
npm install @supabase/supabase-js @supabase/auth-helpers-react
```

5. Create `dashboard/src/lib/supabase.ts`:
```ts
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);
```

6. Create `dashboard/src/contexts/AuthContext.tsx`:
```tsx
import { createContext, useContext, useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';
import type { User, Session } from '@supabase/supabase-js';

interface AuthCtx {
  user: User | null;
  session: Session | null;
  signIn: (email: string) => Promise<void>;
  signOut: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthCtx>(null!);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signIn = async (email: string) => {
    await supabase.auth.signInWithOtp({ email, options: { emailRedirectTo: window.location.origin } });
  };

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  return (
    <AuthContext.Provider value={{ user, session, signIn, signOut, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

7. Create `dashboard/src/pages/Login.tsx` — magic link form:
```tsx
import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

export function Login() {
  const { signIn } = useAuth();
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await signIn(email);
    setSent(true);
  };

  if (sent) return <div>Check your email for a magic link!</div>;

  return (
    <form onSubmit={handleSubmit}>
      <h1>Sign in to Trendpilot</h1>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" required />
      <button type="submit">Send Magic Link</button>
    </form>
  );
}
```

8. Wrap `dashboard/src/App.tsx` with `AuthProvider`. Add route guard:
```tsx
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  if (!user) return <Login />;
  return <>{children}</>;
}
```

9. Update `dashboard/src/api.ts` to attach Bearer token to all requests:
```ts
import { supabase } from './lib/supabase';

async function getAuthHeaders() {
  const { data: { session } } = await supabase.auth.getSession();
  return session ? { Authorization: `Bearer ${session.access_token}` } : {};
}

export async function fetchTopics() {
  const headers = await getAuthHeaders();
  const res = await fetch('/api/topics', { headers });
  return res.json();
}
```

10. Add `dashboard/.env`:
```
VITE_SUPABASE_URL=https://ycisqlzzsimtlqfabmns.supabase.co
VITE_SUPABASE_ANON_KEY=<anon key from Supabase dashboard>
```

PART C — Supabase Auth Config
11. In Supabase dashboard → Authentication → Settings:
    - Enable Email magic links
    - Set Site URL: https://trendpilot.ai (or localhost:5173 for dev)
    - Add redirect URL: http://localhost:5173/**
```

## Acceptance Criteria
- [ ] Unauthenticated requests to `/api/newsletters` return 401
- [ ] Dashboard redirects to login page when not authenticated
- [ ] Magic link email is received and clicking it logs user in
- [ ] After login, dashboard loads normally and API calls succeed
- [ ] User email visible in dashboard header/nav
- [ ] Sign out button clears session and redirects to login
- [ ] API key auth still works for machine-to-machine routes (backward compat)
