001-pending-high-signal-studio-securty-auth.md

TODO: Implement initial auth middleware scaffolding and protective measures for Signal Studio routes.

- Priority: critical (P0) / high impact
- Description: Add an authentication layer to protect all API routes. Start with a Next.js Edge middleware or equivalent, validate tokens from requests, and allow a subset of public routes (health, login, embed) without auth.
- Full coding prompt for autonomous agent:
  - Create middleware.ts in the Next.js app root implementing edge middleware.
  - Define PUBLIC_ROUTES list: ['/api/auth/login', '/api/control-plane/health', '/easy-button/embed']
  - Check for session token via cookies or Authorization header. If missing, redirect or error based on route type.
  - Validate JWT or session; if invalid, block protected routes with 401 or redirect to /login for browser requests.
  - Export config.matcher for ['/api/:path*', '/easy-button/:path*']
- Dependencies: SEC-002, SEC-003, TEST-001, TEST-002
- Estimated effort: 6h
- Acceptance criteria:
  - All protected API routes return 401 without a valid token.
  - Public routes continue to work without auth.
  - Middleware is invoked for API and browser requests on matched paths.
