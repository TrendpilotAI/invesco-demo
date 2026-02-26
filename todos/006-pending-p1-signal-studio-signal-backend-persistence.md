---
status: pending
priority: p1
issue_id: "006"
tags: [signal-studio, persistence, backend, api, signals]
dependencies: ["005"]
---

# 006 — Signal Studio: Implement Signal Persistence to Backend (Replace localStorage)

## Problem Statement

`lib/signal-storage.ts` stores all signal data in `localStorage`. This means:
- Signals are lost when the user clears browser data
- Signals don't sync across devices or users
- No server-side backup, audit trail, or sharing
- The Django backend already has a `/api/v1/signals` CRUD API (confirmed active in production)

The `app/api/signals/route.ts` proxy to Django exists but isn't connected to signal creation flows.
Visual Builder, Signal Library, and Easy Button all use localStorage instead of the backend.

## Findings

- `lib/signal-storage.ts` — pure `localStorage` CRUD (getAllSignals, saveSignal, deleteSignal)
- `app/api/signals/route.ts` — GET + POST proxy to Django `${API_BASE}/signals`
- `app/api/signals/[id]/route.ts` — needs verification for GET/PUT/DELETE
- `app/visual-builder/builder/page.tsx` — likely calls `saveSignal()` from signal-storage
- `app/signal-library/page.tsx` — calls `getAllSignals()` from signal-storage
- Django backend has signals model with id, name, description, query_text, created_at, updated_at
- Auth token available via `useAuth()` hook and `lib/api-client.ts`

## Proposed Solutions

### Option A: Replace localStorage with API calls + optimistic UI (Recommended)
- New `lib/services/signal-service-api.ts` wraps the Next.js API proxy
- Keeps same interface as `signal-storage.ts` but calls API
- Add SWR/React Query for caching + revalidation
- Fallback to localStorage if API unavailable (offline mode)
- **Effort:** 6h | **Risk:** Medium

### Option B: Zustand store + API sync
- Zustand store as in-memory layer, syncs to API on mutations
- More complex state management

## Recommended Action

Option A: Create `lib/services/signal-service-api.ts` as drop-in replacement for `signal-storage.ts`.
Update all call sites. Add loading states.

## Acceptance Criteria

- [ ] `lib/services/signal-service-api.ts` created with `getAllSignals()`, `getSignalById()`, `saveSignal()`, `deleteSignal()` calling `/api/signals`
- [ ] `app/signal-library/page.tsx` uses `signal-service-api` instead of `signal-storage`
- [ ] `app/visual-builder/builder/page.tsx` saves to API on flow save
- [ ] `app/easy-button/page.tsx` loads signals from API
- [ ] `app/api/signals/[id]/route.ts` handles GET, PUT, DELETE and proxies to Django
- [ ] Created signals visible in Django admin after creation
- [ ] Optimistic UI: save shows immediately, rolls back on API error
- [ ] Error toast shown when API save fails
- [ ] `localStorage` still used as offline fallback
- [ ] `__tests__/lib/signal-service-api.test.ts` with mocked fetch assertions

## Files to Create/Modify

- `lib/services/signal-service-api.ts` — NEW: API-backed signal CRUD
- `lib/signal-storage.ts` — add deprecation comment, keep as offline fallback
- `app/api/signals/[id]/route.ts` — add GET, PUT, DELETE handlers
- `app/signal-library/page.tsx` — migrate to API service
- `app/visual-builder/builder/page.tsx` — migrate to API service
- `app/easy-button/page.tsx` — migrate to API service
- `__tests__/lib/signal-service-api.test.ts` — NEW: unit tests

## Technical Details

```typescript
// lib/services/signal-service-api.ts
import { Signal } from '@/lib/signal-storage'

const BASE = '/api/signals'

export async function getAllSignals(): Promise<Signal[]> {
  const res = await fetch(BASE, { cache: 'no-store' })
  if (!res.ok) throw new Error('Failed to load signals')
  const data = await res.json()
  return Array.isArray(data) ? data : data.results ?? []
}

export async function saveSignal(signal: Omit<Signal, 'updatedAt'>): Promise<Signal> {
  const method = signal.id ? 'PUT' : 'POST'
  const url = signal.id ? `${BASE}/${signal.id}` : BASE
  const res = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(signal),
  })
  if (!res.ok) throw new Error('Failed to save signal')
  return res.json()
}

export async function deleteSignal(id: string): Promise<boolean> {
  const res = await fetch(`${BASE}/${id}`, { method: 'DELETE' })
  return res.ok
}
```

## Estimated Effort

6 hours

## Work Log

### 2026-02-26 — Initial Planning

**By:** Honey Planning Agent

**Actions:**
- Traced localStorage usage across all call sites
- Confirmed Django signals API is live at /api/v1/signals
- Designed drop-in replacement service
