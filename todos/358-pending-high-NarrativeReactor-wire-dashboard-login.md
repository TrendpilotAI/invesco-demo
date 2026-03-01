# 358 · NarrativeReactor — Wire React Dashboard Login to /login Endpoint Fully

**Priority:** high  
**Effort:** M (1–3 days)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

The Express backend has JWT-cookie-based dashboard auth (`/login`, `/logout`). The React dashboard (`dashboard/`) needs to be fully wired: show login form when unauthenticated, submit to `/login`, store the JWT cookie, and redirect to the main dashboard view. Currently the wiring is incomplete.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/dashboard/:

1. Inspect the dashboard source:
   ls dashboard/src/
   cat dashboard/src/App.tsx (or App.jsx)

2. Create/update src/components/Login.tsx:

import { useState } from 'react';

export default function Login({ onSuccess }: { onSuccess: () => void }) {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',   // required for cookie
      body: JSON.stringify({ password }),
    });
    if (res.ok) {
      onSuccess();
    } else {
      setError('Invalid password');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Dashboard Login</h2>
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
      <button type="submit">Login</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  );
}

3. Update src/App.tsx to check auth state on load:

import { useState, useEffect } from 'react';
import Login from './components/Login';

function App() {
  const [authed, setAuthed] = useState<boolean | null>(null);

  useEffect(() => {
    fetch('/dashboard', { credentials: 'include' })
      .then(r => setAuthed(r.ok))
      .catch(() => setAuthed(false));
  }, []);

  if (authed === null) return <div>Loading...</div>;
  if (!authed) return <Login onSuccess={() => setAuthed(true)} />;
  return <MainDashboard />;
}

4. Add logout button in dashboard header:
   const logout = () => fetch('/logout', { method: 'POST', credentials: 'include' })
                         .then(() => setAuthed(false));

5. Ensure Vite proxy config (vite.config.ts) proxies /login, /logout, /dashboard to Express:
   server: { proxy: { '/login': 'http://localhost:3000', '/logout': 'http://localhost:3000', '/api': 'http://localhost:3000' } }

6. Test: npm run dev in dashboard/, visit localhost:5173, confirm login flow works end-to-end.
```

---

## Dependencies

- Backend `/login` endpoint with JWT cookie (already exists per TODO.md)
- Dashboard Vite dev server running

## Acceptance Criteria

- [ ] Unauthenticated visit shows login form
- [ ] Correct password logs in (cookie set, dashboard renders)
- [ ] Wrong password shows error message
- [ ] Logout clears cookie and returns to login form
- [ ] No hardcoded credentials in frontend code
- [ ] Vite proxy routes auth endpoints to Express
