# 319 · NarrativeReactor — Dashboard Authentication

**Status:** pending  
**Priority:** critical  
**Project:** NarrativeReactor  
**Effort:** ~4h  

---

## Task Description

The dashboard directory may expose admin UI without authentication. Any unauthenticated user with network access could view analytics, campaign data, brand configs, and cost summaries. This task audits the dashboard and adds session-based auth with a simple JWT/cookie flow.

## Full Coding Prompt

```
You are working in /data/workspace/projects/NarrativeReactor/.

## Step 0 — Audit
First, read dashboard/ to understand what it serves:
- Is it a static HTML file? Express-served? Next.js?
- Are any /dashboard/* routes currently protected?
- Check src/index.ts and src/routes/ for dashboard route mounts.

## Step 1 — Install dependencies (if dashboard is Express-served)
```bash
pnpm add jsonwebtoken cookie-parser
pnpm add -D @types/jsonwebtoken @types/cookie-parser
```

## Step 2 — Create src/middleware/dashboardAuth.ts
```typescript
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

const DASHBOARD_SECRET = process.env.DASHBOARD_SECRET!;
const DASHBOARD_PASSWORD = process.env.DASHBOARD_PASSWORD!;

export function dashboardAuth(req: Request, res: Response, next: NextFunction) {
  const token = req.cookies?.dashboard_token;
  if (!token) {
    return res.redirect('/dashboard/login');
  }
  try {
    jwt.verify(token, DASHBOARD_SECRET);
    next();
  } catch {
    res.clearCookie('dashboard_token');
    return res.redirect('/dashboard/login');
  }
}

export function dashboardLogin(req: Request, res: Response) {
  if (req.method === 'GET') {
    return res.send(`<!DOCTYPE html>
<html><head><title>Dashboard Login</title></head>
<body style="font-family:sans-serif;max-width:400px;margin:100px auto">
<h2>NarrativeReactor Dashboard</h2>
<form method="POST">
  <input type="password" name="password" placeholder="Password" required style="width:100%;padding:8px;margin:8px 0">
  <button type="submit" style="width:100%;padding:8px;background:#6366f1;color:white;border:none;cursor:pointer">Login</button>
</form>
</body></html>`);
  }
  
  const { password } = req.body;
  if (password !== DASHBOARD_PASSWORD) {
    return res.status(401).send('Invalid password');
  }
  
  const token = jwt.sign({ dashboard: true }, DASHBOARD_SECRET, { expiresIn: '8h' });
  res.cookie('dashboard_token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 8 * 60 * 60 * 1000,
  });
  res.redirect('/dashboard');
}

export function dashboardLogout(req: Request, res: Response) {
  res.clearCookie('dashboard_token');
  res.redirect('/dashboard/login');
}
```

## Step 3 — Mount in src/index.ts
```typescript
import cookieParser from 'cookie-parser';
import { dashboardAuth, dashboardLogin, dashboardLogout } from './middleware/dashboardAuth';

app.use(cookieParser());

// Dashboard auth routes (no auth required)
app.route('/dashboard/login').get(dashboardLogin).post(express.urlencoded({ extended: false }), dashboardLogin);
app.get('/dashboard/logout', dashboardLogout);

// All /dashboard routes require auth
app.use('/dashboard', dashboardAuth);
// ... existing dashboard route mount here
```

## Step 4 — Update src/lib/env.ts
Add required vars:
- `DASHBOARD_SECRET` — JWT signing secret (required, min 32 chars)
- `DASHBOARD_PASSWORD` — Dashboard login password (required)

## Step 5 — Update .env.example
```
DASHBOARD_SECRET=change-me-to-a-random-32-char-string
DASHBOARD_PASSWORD=change-me-to-a-secure-password
```

## Step 6 — Tests
Create tests/security/dashboard-auth.test.ts:
- GET /dashboard without cookie → 302 to /dashboard/login
- POST /dashboard/login with wrong password → 401
- POST /dashboard/login with correct password → sets cookie, redirects
- GET /dashboard with valid cookie → 200 (not redirect)
```

## Dependencies
- 316 (helmet/cookie security headers should be in place first)

## Acceptance Criteria
- [ ] `GET /dashboard` without auth → redirects to `/dashboard/login`
- [ ] Login with wrong password → 401
- [ ] Login with correct password → 8h JWT cookie set, redirected to dashboard
- [ ] `DASHBOARD_SECRET` and `DASHBOARD_PASSWORD` validated at startup
- [ ] Cookie is `httpOnly`, `secure` in production, `sameSite: lax`
- [ ] Logout clears cookie and redirects to login
- [ ] Tests pass
