# 607 Done — Signal Studio Frontend BFF Proxy

**Status:** ✅ Complete  
**Commit:** `99d0886cb36d76b7da62df2e28fe2c3264c9aab2`  
**Branch:** main  
**Repo:** signal-studio (Bitbucket: forwardlane/signal-studio)

## What was done

Created Next.js BFF proxy routes at `/api/bff/easy-button/[...path]/route.ts` that:

1. **Forward auth headers** — passes `Authorization` (JWT) and `Cookie` headers from the client request to Django
2. **Proxy to Django easy_button endpoints** — maps `/api/bff/easy-button/*` → `CORE_API/api/v1/easy-button/*`
3. **Handle all HTTP methods** — GET, POST, PUT, PATCH, DELETE, OPTIONS
4. **Graceful error handling** — 504 on timeout (30s), 502 on network errors, with upstream URL in error body
5. **Updated `.env.example`** — documents BFF proxy routes and adds `NEXT_PUBLIC_CORE_API` hint

## Files changed

- `app/api/bff/easy-button/[...path]/route.ts` — new catch-all proxy handler
- `.env.example` — added BFF proxy documentation
