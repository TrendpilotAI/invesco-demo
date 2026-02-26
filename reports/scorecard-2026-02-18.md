# 🍯 Project Scorecard — 2026-02-18

## Overall Scores

| Project | UX | Caps | Code | Perf | Ease | Prod | X | **Total** |
|---------|:--:|:----:|:----:|:----:|:----:|:----:|:-:|:---------:|
| FlipMyEra | - | - | - | - | - | - | - | **6.7** |
| Second-Opinion | - | - | - | - | - | - | - | **7.1** |
| NarrativeReactor | - | - | - | - | - | - | - | **5.3** |
| Trendpilot | - | - | - | - | - | - | - | **5.0** |
| Railway SaaS | - | - | - | - | - | - | - | **6.8** |

---

## FlipMyEra

**Overall: 6.7/10**

> FlipMyEra is a feature-rich Taylor Swift Eras Tour ebook/story creation platform built with React, Vite, Supabase, and Stripe. It has an impressive breadth of features (AI story generation, image generation, ebook reader, marketplace, gifting, affiliates, admin dashboards, SEO pages) but suffers from a bloated main bundle (1.1MB chunk), and some features feel like scaffolding rather than polished experiences. Architecture is solid with modular structure, lazy loading, error boundaries, and proper observability (Sentry, PostHog, OpenTelemetry). 324 source files across 19 modules with 36 tests — decent but test coverage is thin for the codebase size. Build succeeds cleanly. CI/CD exists via GitHub Actions with Dependabot. The niche targeting (Swifties) gives it strong X-factor but the sheer feature sprawl suggests many features are partially implemented.

### UX/Design: undefined/10
undefined

### Capabilities: undefined/10
undefined

### Code Quality: undefined/10
undefined

### Performance: undefined/10
undefined

### Ease of Use: undefined/10
undefined

### Prod Ready: undefined/10
undefined

### X-Factor: undefined/10
undefined

### Top Recommendations
1. Implement manualChunks in vite config to split the 1.1MB main bundle — target <300KB per chunk
2. Remove VITE_SUPABASE_SERVICE_ROLE_KEY from client-side — service role keys must never be in browser code
3. Move groq-sdk and stripe server-side calls to Supabase Edge Functions
4. Add integration tests for payment flow, auth flow, and ebook generation — these are revenue-critical
5. Audit feature completeness: cut or finish half-implemented modules (marketplace, affiliates) before launch
6. Add Lighthouse CI to the GitHub Actions pipeline for performance regression tracking
7. Consider moving to Next.js or Remix for SSR/SEO benefits on the 10 SEO landing pages

---

## Second-Opinion

**Overall: 7.1/10**

> Second-Opinion is an impressively ambitious medical AI consultation app built with React 19, Firebase, and Gemini. It features a robust multi-step workflow (landing → auth → intake → upload → analysis → results), 43 components, 30 services, Firebase Cloud Functions backend, i18n (en/es), FHIR R4 export, AES-GCM encryption, PWA support, and a comprehensive test suite (23 test files). The architecture is clean with custom hooks, lazy-loaded routes, and proper separation of concerns. However, it's a Kaggle competition/prototype — not yet battle-tested in production with real patients. The sheer breadth of features (telemedicine, insurance pre-auth, clinical trials, research mode, provider dashboard) suggests many are thin implementations rather than production-grade. Coverage thresholds are set low (20% lines) which is honest but concerning for medical software.

### UX/Design: undefined/10
undefined

### Capabilities: undefined/10
undefined

### Code Quality: undefined/10
undefined

### Performance: undefined/10
undefined

### Ease of Use: undefined/10
undefined

### Prod Ready: undefined/10
undefined

### X-Factor: undefined/10
undefined

### Top Recommendations
1. Add a proper routing solution (react-router or TanStack Router) instead of step-based state machine in App.tsx
2. Implement CI/CD with GitHub Actions: lint, type-check, test, build, deploy
3. Raise test coverage thresholds significantly — target 60%+ for medical software
4. Add HIPAA compliance documentation and audit trail for data access
5. Trim aspirational features and deepen the core flow (intake → upload → analysis → results)
6. Add proper accessibility testing (axe-core, keyboard nav testing)
7. Remove functions/node_modules from version control
8. Add rate limiting and input sanitization on Cloud Functions
9. Consider adding Sentry or similar error monitoring for production
10. Add E2E tests with Playwright for the critical happy path

---

## NarrativeReactor

**Overall: 5.3/10**

> NarrativeReactor is an ambitious AI content generation backend built on Genkit + Express with an impressive breadth of services (34+ service files covering video gen, TTS, podcasts, brand voice, campaigns, social publishing, etc.). However, it's fundamentally a backend API with a minimal static HTML dashboard — not a polished product. Many services use in-memory storage (Maps), auth is basic API key comparison (not timing-safe), CORS is wide open, and there's no Docker/deployment config. The feature surface is wide but shallow — lots of scaffolding, some real integrations (Fal.ai, Claude, Blotato), but unclear how much actually works end-to-end. Test coverage exists (15 test files) but is modest relative to the 66 source files. The static dashboard is functional but basic. This is a solid prototype/proof-of-concept, not production-ready software.

### UX/Design: undefined/10
undefined

### Capabilities: undefined/10
undefined

### Code Quality: undefined/10
undefined

### Performance: undefined/10
undefined

### Ease of Use: undefined/10
undefined

### Prod Ready: undefined/10
undefined

### X-Factor: undefined/10
undefined

### Top Recommendations
1. Add persistent storage (Postgres/Redis) — replace all in-memory Maps immediately
2. Split the 877-line routes file into domain-specific route modules
3. Add a real logging framework (pino/winston) with structured logging
4. Implement timing-safe auth comparison and restrict CORS origins
5. Add Dockerfile and docker-compose for reproducible deployment
6. Build a proper frontend (React/Next.js) or at minimum enhance the dashboard significantly
7. Add SSE/WebSocket support for streaming AI generation progress
8. Increase test coverage to at least 70%, especially for services
9. Add health check that verifies downstream dependencies (AI providers, etc.)
10. Add OpenAPI/Swagger documentation for the 69 API endpoints

---

## Trendpilot

**Overall: 5.0/10**

> Trendpilot is an ambitious trend aggregation and newsletter platform with a wide feature surface (25+ services covering aggregation, alerts, sentiment, SSO, compliance, white-labeling, etc.) but most services are thin in-memory implementations rather than production-grade integrations. The React dashboard is functional but uses inline styles exclusively with no responsive design, no routing library, and no accessibility considerations. The backend is a monolithic Express app with all routes in a single 400+ line file. Sentiment analysis uses naive word-list matching. Tests exist across 11 phases but can't run (deps not installed). Supabase schema with RLS is solid. Overall: a well-scaffolded MVP skeleton that looks impressive on paper but lacks depth in execution.

### UX/Design: undefined/10
undefined

### Capabilities: undefined/10
undefined

### Code Quality: undefined/10
undefined

### Performance: undefined/10
undefined

### Ease of Use: undefined/10
undefined

### Prod Ready: undefined/10
undefined

### X-Factor: undefined/10
undefined

### Top Recommendations
1. Replace inline styles with Tailwind CSS or CSS modules; add responsive breakpoints
2. Add react-router for proper URL-based navigation and deep linking
3. Move route definitions out of monolithic index.ts into route modules
4. Replace in-memory stores with actual Supabase queries — the schema is already there
5. Integrate a real NLP API (or at minimum a better lexicon like AFINN-165) for sentiment
6. Add error boundaries, loading skeletons, and empty states to dashboard
7. Wire up Supabase Auth in the dashboard — AuthContext exists but isn't connected
8. Install deps and verify tests actually pass before claiming test coverage
9. Add rate limiting, CORS configuration, and helmet middleware for security
10. Consider splitting into microservices or at least Express Router modules as the service count grows

---

## Railway SaaS

**Overall: 6.8/10**

> A solid SaaS starter template that covers the essential bases — auth, payments, API keys, admin panel, and Railway deployment. The architecture is clean and idiomatic Next.js App Router with proper separation of concerns. However, it's a template, not a product: no tests, limited UI polish, no loading states or optimistic updates, and the frontend is functional rather than beautiful. It would save a developer 2-3 days of boilerplate setup, which is genuinely valuable, but it's not something you'd ship as-is to paying customers.

### UX/Design: undefined/10
undefined

### Capabilities: undefined/10
undefined

### Code Quality: undefined/10
undefined

### Performance: undefined/10
undefined

### Ease of Use: undefined/10
undefined

### Prod Ready: undefined/10
undefined

### X-Factor: undefined/10
undefined

### Top Recommendations
1. Add at least integration tests for Stripe webhook handler and auth flows — these are the riskiest paths
2. Extract reusable UI components (Card, Button, Badge, Nav) instead of repeating Tailwind classes
3. Add GitHub Actions workflow for lint + type-check + test on PR
4. Add .next to .gitignore and remove the committed build artifacts
5. Add loading.tsx files for dashboard routes to show skeletons during server rendering
6. Add a simple chart library (recharts or similar) for the usage dashboard
7. Make admin panel actionable — role changes, plan overrides, user suspension
8. Add CSRF protection and security headers (Content-Security-Policy, etc.)
9. Add keyboard accessibility and aria labels to interactive elements
10. Consider adding a /docs or /api-docs page since this is an API-key-based product

---

## Historical Trend

*Daily scores will accumulate here over time.*

| Date | FlipMyEra | Second-Opinion | NarrativeReactor | Trendpilot | Railway SaaS |
|------|:---------:|:--------------:|:----------------:|:----------:|:------------:|
| 2026-02-18 | 6.7 | 7.1 | 5.3 | 5.0 | 6.8 |
