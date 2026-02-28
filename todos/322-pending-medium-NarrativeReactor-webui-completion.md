# 322 · NarrativeReactor — Web UI Next.js Completion

**Status:** pending  
**Priority:** medium  
**Project:** NarrativeReactor  
**Effort:** ~10h  

---

## Task Description

The `web-ui/` directory is a Next.js app with incomplete pages. This task audits which pages exist vs. which are needed, completes stub pages, adds API integration hooks, and ensures auth-protected routes redirect to login.

## Full Coding Prompt

```
You are working in /data/workspace/projects/NarrativeReactor/web-ui/.

## Step 0 — Audit
Read the web-ui/ directory structure. List all page files and categorize:
- Complete (has real UI)
- Stub (exists but is a placeholder)
- Missing (referenced in nav but no file)

## Step 1 — Auth layer
Create web-ui/lib/auth.ts:
```typescript
import { cookies } from 'next/headers';

export function getApiKey(): string {
  const cookieStore = cookies();
  return cookieStore.get('api_key')?.value ?? process.env.NEXT_PUBLIC_API_KEY ?? '';
}

export function requireAuth() {
  const apiKey = getApiKey();
  if (!apiKey) {
    // Return null — pages handle redirect
    return null;
  }
  return apiKey;
}
```

Create web-ui/middleware.ts:
```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const apiKey = request.cookies.get('api_key')?.value;
  const isLoginPage = request.nextUrl.pathname === '/login';

  if (!apiKey && !isLoginPage) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|login).*)'],
};
```

## Step 2 — Login page (web-ui/app/login/page.tsx)
Simple login form that POSTs API key to the Express backend to validate:
- Input for API key
- On success: set cookie and redirect to /
- On failure: show error message
- Use shadcn/ui Card + Input + Button if available

## Step 3 — Dashboard home (web-ui/app/page.tsx)
Cards showing:
- Total content generated (GET /api/cost-summary)
- Active campaigns count (GET /api/campaigns)
- Brand voices configured (GET /api/brands)
- Recent activity feed (last 10 operations from GET /api/activity or cost log)

Use React Server Components with fetch() to API.
Show loading skeletons while fetching.

## Step 4 — Campaign manager (web-ui/app/campaigns/page.tsx)
Table of campaigns with columns: Name, Status, Brand, Created, Actions
- Create campaign button → modal form
- Pause/Resume/Delete actions
- Pagination if > 20 campaigns
- Filter by status dropdown

## Step 5 — Content generator (web-ui/app/generate/page.tsx)
Form-based UI:
- Select brand voice (dropdown from GET /api/brands)
- Content type selector: blog, social, video-script, podcast
- Prompt textarea
- Generate button → calls POST /api/content/generate
- Result display with copy button
- Cost display: "This generation cost $X.XX"

## Step 6 — Brand voice manager (web-ui/app/brands/page.tsx)
- List of brands with their voice profiles
- Create/Edit brand form: name, tone (formal/casual/playful), keywords, sample text
- Analyze brand voice button → calls brandVoice service
- Preview how content will sound

## Step 7 — API client (web-ui/lib/api.ts)
Centralized fetch wrapper:
```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:3000';

export async function apiRequest<T>(
  path: string,
  options?: RequestInit & { apiKey?: string }
): Promise<T> {
  const { apiKey, ...fetchOptions } = options ?? {};
  const res = await fetch(`${API_BASE}${path}`, {
    ...fetchOptions,
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey ?? '',
      ...fetchOptions.headers,
    },
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${await res.text()}`);
  return res.json();
}
```

## Step 8 — Error boundary
Create web-ui/app/error.tsx global error boundary that shows friendly error + retry.
```

## Dependencies
- 317 (Docker/deployment — web-ui needs API_URL env var)
- 318 (OpenAPI docs — frontend team uses spec to build API calls)
- 319 (Dashboard auth — web-ui auth should align with dashboard auth model)

## Acceptance Criteria
- [ ] `pnpm dev` in web-ui/ starts without errors
- [ ] `pnpm build` in web-ui/ produces working Next.js build
- [ ] Unauthenticated navigation to any page → redirect to /login
- [ ] Login page accepts API key, sets cookie, redirects to /
- [ ] Dashboard home fetches and displays 4 metric cards
- [ ] Campaign manager renders table with mock or real data
- [ ] Content generator form submits and displays result
- [ ] API client handles errors gracefully (no uncaught promise rejections)
- [ ] TypeScript compiles with 0 errors
