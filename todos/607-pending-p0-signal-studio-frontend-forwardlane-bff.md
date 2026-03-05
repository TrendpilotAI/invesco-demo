# TODO-607: Wire ForwardLane BFF Proxy Routes

**Repo:** signal-studio-frontend  
**Priority:** P0 (Production Blocker)  
**Effort:** M (2-3 days)  
**Status:** pending

## Description

Signal Studio hits Oracle directly for everything. The real ForwardLane signal catalog, user management, client portfolios, and entitlements all live behind the ForwardLane Django backend (`CORE_API`). Need BFF proxy routes at `/api/bff/*` that authenticate and forward requests to the Django API.

## Acceptance Criteria
- [ ] `/api/bff/signals` → GET forwardlane signals list
- [ ] `/api/bff/signals/:id` → GET signal detail
- [ ] `/api/bff/clients` → GET client list
- [ ] `/api/bff/portfolios` → GET portfolio data
- [ ] JWT from frontend forwarded to Django in `Authorization` header
- [ ] Error responses from Django normalized to consistent format
- [ ] TanStack Query hooks updated to use BFF routes where applicable
- [ ] `CORE_API` env var documented in `.env.example`

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend:

1. Create app/api/bff/[...path]/route.ts - a catch-all proxy route
2. Extract JWT from request Authorization header
3. Forward request to process.env.CORE_API + path with same method/body
4. Normalize error responses
5. Update lib/api-client.ts to add bff() helper
6. Update relevant TanStack Query hooks (lib/services/) to use /api/bff/* endpoints
7. Add CORE_API to .env.example with documentation
8. Add __tests__/api/bff.test.ts with mocked fetch
```

## Dependencies
- ForwardLane Django backend must be running and accessible
