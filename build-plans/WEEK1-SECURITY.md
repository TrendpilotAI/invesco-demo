# Build Plan: Security & Revenue Blockers (Week 1)

## Wave 1 — Quick Wins (Day 1)

### Task 431: ForwardLane conftest.py Fix
- **Project**: ForwardLane Backend
- **Effort**: 0.25 days
- **Priority**: MUST
- **Files**: `tests/conftest.py`
- **Change**: `is_wealthbox_adapter_enabled` → `is_wealthbox_adapter_enabled()`
- **Test**: Run pytest, verify Wealthbox tests are skipped when disabled

### Task 426: SignalHaus Budget Validation Fix
- **Project**: SignalHaus Website
- **Effort**: 0.5 days
- **Priority**: MUST
- **Files**: `src/app/api/contact/route.ts`, `src/components/ContactForm.tsx`
- **Change**: Align budget options between form and API validation
- **Test**: Submit form with each budget option, verify no validation errors

### Task 433: ForwardLane SECRET_KEY Fix
- **Project**: ForwardLane Backend
- **Effort**: 1 day
- **Priority**: MUST
- **Files**: `forwardlane/settings/base.py`
- **Change**: Move SECRET_KEY to env var, add startup check, DEBUG default False
- **Test**: Verify app fails fast in production with missing SECRET_KEY

---

## Wave 2 — Core Security (Days 2-5)

### Task 402: FlipMyEra API Keys → Edge Functions
- **Project**: FlipMyEra
- **Effort**: 5 days
- **Priority**: MUST
- **Approach**:
  1. Create Supabase Edge Functions for Groq and OpenAI
  2. Move secret keys to server-side env vars
  3. Add rate limiting in edge functions
  4. Remove VITE_ prefix keys from client
  5. Update ai.ts to call edge functions
- **Files**: `.env`, `src/modules/story/services/ai.ts`, Supabase functions
- **Test**: Verify API calls work through edge functions, keys not exposed in bundle

### Task 413: Signal Studio Auth Middleware
- **Project**: Signal Studio
- **Effort**: 5 days
- **Priority**: MUST
- **Approach**:
  1. Add Next.js middleware validating JWT tokens
  2. Implement server-side session verification
  3. Add CSRF protection
  4. Create withAuth() wrapper for API routes
- **Files**: `middleware.ts`, `lib/auth.ts`, API routes
- **Test**: Verify unauthenticated requests return 401

### Task 451: Ultrafone Real-Time Call Approval
- **Project**: Ultrafone
- **Effort**: 2 days
- **Priority**: MUST
- **Approach**:
  1. Implement Redis pub/sub for approval requests
  2. Add `/api/calls/{call_id}/approve` endpoint
  3. Wire WebSocket to close the loop
- **Files**: `receptionist.py`, `api/calls.py`
- **Test**: Trigger approval, verify real-time forwarding

---

## Wave 3 — Data & Functionality (Days 6-14)

### Task 403: FlipMyEra Credit System Fix
- **Project**: FlipMyEra
- **Effort**: 2 days
- **Priority**: MUST
- **Approach**:
  1. Move credit deduction to server-side edge function
  2. Add database transaction with SELECT FOR UPDATE
  3. Add idempotency keys to story generation
  4. Implement credit balance verification
- **Files**: Edge functions, Supabase database
- **Test**: Verify credit deduction is atomic, no double-charging

### Task 411: Signal Studio Server-Side Storage
- **Project**: Signal Studio
- **Effort**: 5 days
- **Priority**: MUST
- **Approach**:
  1. Create PostgreSQL-backed signal repository
  2. Replace localStorage with API calls
  3. Update AI chat to query real signal service
- **Files**: `lib/signal-storage.ts`, API routes, database
- **Test**: Verify signals persist across sessions and devices

### Task 461: NarrativeReactor Persistent Database
- **Project**: NarrativeReactor
- **Effort**: 5 days
- **Priority**: MUST
- **Approach**:
  1. Introduce SQLite or PostgreSQL
  2. Create data-access layer with repositories
  3. Migrate all Map-based stores
- **Files**: All in-memory stores, database schema
- **Test**: Verify state persists across restarts

---

## Dependencies

```
Wave 1 (Day 1)
├── 431 (conftest) ──────────┐
├── 426 (budget validation)  │
└── 433 (SECRET_KEY) ────────┘

Wave 2 (Days 2-5)
├── 402 (API keys edge) ──────┐
├── 413 (auth middleware)     │
└── 451 (call approval) ──────┘

Wave 3 (Days 6-14)
├── 403 (credit system)      ← depends on 402
├── 411 (server storage)     ← depends on 413
└── 461 (persistent DB)     ← depends on nothing
```

## Execution Strategy

- **Wave 1**: Can run in parallel (all independent)
- **Wave 2**: 402 and 413 can run in parallel, 451 can run immediately
- **Wave 3**: 403 depends on 402, 411 depends on 413, 461 is independent

## Success Criteria

1. All MUST items completed
2. All tests passing
3. No security vulnerabilities in production
4. Revenue-blocking bugs fixed
