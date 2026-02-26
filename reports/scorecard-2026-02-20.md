# 🍯 Project Scorecard — 2026-02-20

## Overall Scores

| Project | UX | Caps | Code | Perf | Ease | Prod | X | **Total** |
|---------|:--:|:----:|:----:|:----:|:----:|:----:|:-:|:---------:|
| FlipMyEra | 7 | 7 | 7 | 6 | 6 | 7 | 6 | **6.8** |
| Second-Opinion | 6 | 7 | 6 | 5 | 7 | 5 | 7 | **6.5** |
| NarrativeReactor | 4 | 6 | 6 | 4 | 4 | 4 | 7 | **5.4** |
| Trendpilot | 4 | 6 | 7 | 5 | 5 | 5 | 6 | **5.8** |
| Railway SaaS Template | 4 | 4 | 5 | 5 | 4 | 4 | 4 | **4.6** |

---

## FlipMyEra

**Overall: 6.8/10**

> Most mature project in the portfolio. Strong modular architecture, real monitoring (Sentry + OTel), CI pipeline, 42 tests, Stripe payments, and Supabase backend. Good error boundaries and loading states. Missing dark mode, heavy dependency footprint, and some features feel half-baked (gallery, sharing). Genuinely shippable but needs polish pass.

### UX/Design: 7/10
Clean component library via Radix/shadcn. ErrorBoundary, skeleton loaders, lazy routes all present. Responsive via Tailwind. But 40+ Radix packages is overkill, no dark mode, and the gallery/sharing UX is unclear.
- ✅ Comprehensive shadcn/Radix component library
- ✅ Skeleton loading states and lazy routes
- ✅ ErrorBoundary with fallback UI
- ✅ Responsive Tailwind design
- ❌ No dark mode or theme customization
- ❌ Bloated dependency tree (40+ Radix packages)
- ❌ Gallery and sharing flows need work

### Capabilities: 7/10
Core story generation with streaming, ebook creation, Stripe billing, credit system, admin dashboard, referral system, A/B testing, and image review. Feature-rich for a solo project. Some features (quiz, era selection) feel bolted on.
- ✅ Full ebook generation pipeline with streaming
- ✅ Stripe billing + credit system
- ✅ Admin dashboard with analytics
- ✅ A/B testing and feature flags
- ❌ SwiftieQuiz feels gimmicky
- ❌ Image generation via proxy is fragile
- ❌ No offline/PWA support

### Code Quality: 7/10
Clean modular architecture (core/modules/integrations). TypeScript throughout. 42 test files covering hooks, components, and edge cases. CI runs lint + typecheck + test + build. Logger, rate limiter, validation utils all well-structured.
- ✅ Clear module boundaries (ebook, story, user, subscriptions)
- ✅ 42 test files with good coverage of critical paths
- ✅ Centralized config, logger, and API client
- ✅ CI pipeline: lint → typecheck → test → build
- ❌ Some modules lack tests (admin, gallery)
- ❌ No E2E tests running in CI (Playwright config exists but dormant)
- ❌ 377 source files is getting unwieldy for a single-dev project

### Performance: 6/10
Code splitting via lazy routes is good. OpenTelemetry instrumentation for web vitals. But 40+ Radix packages and heavy deps will hurt bundle size. No evidence of image optimization or CDN strategy.
- ✅ Lazy-loaded routes
- ✅ OpenTelemetry web instrumentation
- ✅ Performance utility module
- ❌ Heavy dependency count inflates bundle
- ❌ No image optimization pipeline
- ❌ No CDN or edge caching strategy

### Ease of Use: 6/10
Onboarding is story-first which is good. Credit wall modal guides monetization. But the TS/Taylor Swift niche is very narrow. FAQ page exists. No in-app help or tooltips.
- ✅ Story-first onboarding flow
- ✅ Credit system is clear
- ✅ FAQ page and legal pages present
- ❌ Very narrow niche limits audience
- ❌ No in-app help or guided tour
- ❌ Accessibility unclear — no WCAG audit evidence

### Prod Ready: 7/10
Sentry error tracking, OpenTelemetry traces, environment configs, CI/CD via GitHub Actions, .env.example with clear documentation. Supabase migrations managed. Production verification script exists. Missing: staging environment, rate limiting on frontend.
- ✅ Sentry + OpenTelemetry monitoring
- ✅ GitHub Actions CI pipeline
- ✅ Environment config management
- ✅ Production verification script
- ❌ No staging environment evident
- ❌ API keys in VITE_ prefix expose to client
- ❌ No rate limiting on API calls from frontend

### X-Factor: 6/10
AI story generation into ebooks is genuinely creative. The Taylor Swift angle gives personality. Streaming chapter generation is a nice touch. But the market is tiny and competitive in AI writing tools. Would need significant marketing to find its audience.
- ✅ Creative concept — AI era-based story transformation
- ✅ Streaming generation creates engaging UX
- ✅ Clear monetization model
- ❌ Very niche market (Swifties who want AI ebooks)
- ❌ AI writing space is crowded
- ❌ Differentiation beyond the TS theme is thin

### Top Recommendations
1. Add E2E tests to CI — Playwright config exists, wire it up
2. Implement dark mode — it's expected in 2026
3. Audit and trim Radix dependencies — many may be unused
4. Add staging environment for pre-production testing
5. Consider broadening beyond Taylor Swift to expand TAM

### Feature Inventory
| Feature | Status | Tests |
|---------|--------|-------|
| AI Story Generation (streaming) | ✅ complete | ✅ |
| Ebook Creation & Reader | ✅ complete | ✅ |
| Stripe Payments & Credits | ✅ complete | ✅ |
| User Authentication (Supabase) | ✅ complete | ❌ |
| Admin Dashboard | ✅ complete | ❌ |
| Gallery | 🔶 partial | ❌ |
| Referral System | ✅ complete | ✅ |
| Image Generation | ✅ complete | ✅ |
| A/B Testing | ✅ complete | ❌ |
| Swiftie Quiz | ✅ complete | ❌ |
| Sharing/Social | 🔶 partial | ❌ |

---

## Second-Opinion

**Overall: 6.5/10**

> Impressive medical AI app with multi-model consensus, Firebase backend, i18n, and a live demo. 23 test files, 5 CI workflows, FHIR R4 compliance. Strong README with badges. Missing: HIPAA compliance evidence, accessibility audit, and the component structure is flat (no modules). The concept is powerful but regulatory concerns are unaddressed.

### UX/Design: 6/10
Clean landing page with guided demo mode. Medical disclaimer present. Processing log window gives transparency. But flat component structure (all in /components/), no design system beyond basic UI folder. Confidence indicators and reasoning chains are nice touches.
- ✅ Guided demo mode for onboarding
- ✅ Processing log window for transparency
- ✅ Medical disclaimer front and center
- ✅ Confidence indicators on results
- ❌ Flat component structure — 20+ components in one directory
- ❌ No design system or component library
- ❌ Limited responsive design evidence
- ❌ No dark mode

### Capabilities: 7/10
Multi-model medical AI consensus (4 models), patient chat, consultation booking, insurance pre-auth, specialist directory, family sharing, research panel, and doctor questions. FHIR R4 compliant. Impressive feature breadth for a competition entry. Some features feel like stubs (insurance, booking).
- ✅ Multi-model AI consensus architecture
- ✅ FHIR R4 compliance
- ✅ i18n (English + Spanish)
- ✅ Research panel with evidence chains
- ❌ Insurance pre-auth likely a stub
- ❌ Consultation booking needs real backend
- ❌ No offline capability for medical records

### Code Quality: 6/10
TypeScript throughout. Custom hooks are well-abstracted (useAnalysisPipeline, useStepNavigation). 23 test files covering hooks, components, and services. 5 CI workflows (ci, deploy, staging, modal-deploy, hosting). But no module boundaries — everything is flat. Firebase functions well-organized though.
- ✅ Well-designed custom hooks
- ✅ 23 test files with good coverage
- ✅ 5 CI/CD workflows
- ✅ Firebase functions properly structured
- ❌ Flat project structure — no module boundaries
- ❌ 171 source files without clear organization
- ❌ No shared types directory
- ❌ Some components are very large

### Performance: 5/10
No evidence of code splitting or lazy loading. Firebase hosting provides CDN. Recharts for visualization adds bundle weight. No image optimization. Pipeline streaming is good for perceived perf on AI calls.
- ✅ Firebase CDN for hosting
- ✅ Streaming AI pipeline for perceived performance
- ❌ No lazy loading or code splitting
- ❌ Recharts adds significant bundle weight
- ❌ No performance monitoring
- ❌ No lighthouse or web vitals tracking

### Ease of Use: 7/10
Guided demo mode is excellent for first-time users. Step navigation makes the flow clear. Language switcher for i18n. Medical jargon highlighter helps accessibility. File uploader for medical docs.
- ✅ Guided demo mode
- ✅ Step-by-step navigation
- ✅ Medical jargon highlighter
- ✅ i18n support
- ❌ No WCAG accessibility audit
- ❌ Complex medical flows may confuse non-technical users
- ❌ No help documentation beyond demo

### Prod Ready: 5/10
Firebase hosting + functions deployed. Multiple CI workflows. But: no HIPAA compliance (critical for medical), no error monitoring (Sentry etc), no rate limiting on AI endpoints, no audit logging for medical data access.
- ✅ Firebase hosting with CDN
- ✅ Multiple deployment workflows
- ✅ Staging environment pipeline
- ❌ No HIPAA compliance — dealbreaker for real medical use
- ❌ No error monitoring
- ❌ No audit logging for sensitive data
- ❌ No rate limiting on AI endpoints

### X-Factor: 7/10
Multi-model medical consensus is a genuinely novel concept. The '4 models, 60 seconds, $0.02' pitch is compelling. FHIR compliance shows seriousness. Built for Kaggle MedGemma competition which adds credibility. Would I pay? Yes, if it had proper medical compliance.
- ✅ Novel multi-model consensus approach
- ✅ Compelling value prop ($0.02 per consultation)
- ✅ FHIR R4 compliance
- ✅ Competition-grade quality
- ❌ Regulatory barriers are massive
- ❌ Medical AI liability is unresolved
- ❌ Needs real clinical validation

### Top Recommendations
1. Add HIPAA compliance layer — required for any real medical use
2. Implement error monitoring (Sentry or similar)
3. Restructure into modules (analysis, auth, medical-records, etc.)
4. Add lazy loading and code splitting
5. Conduct WCAG accessibility audit for medical accessibility requirements

### Feature Inventory
| Feature | Status | Tests |
|---------|--------|-------|
| Multi-model AI Analysis | ✅ complete | ✅ |
| Patient Chat | ✅ complete | ✅ |
| File Upload (Medical Docs) | ✅ complete | ✅ |
| Auth (Firebase) | ✅ complete | ✅ |
| Guided Demo Mode | ✅ complete | ❌ |
| Research Panel | ✅ complete | ❌ |
| i18n (EN/ES) | ✅ complete | ❌ |
| Consultation Booking | 🔶 partial | ❌ |
| Insurance Pre-Auth | 🔶 partial | ❌ |
| Family Sharing | 🔶 partial | ❌ |
| Specialist Directory | 🔶 partial | ❌ |

---

## NarrativeReactor

**Overall: 5.4/10**

> Ambitious AI content engine with 30+ services covering everything from video stitching to podcast generation to social posting. Genkit-based with Claude integration. Dashboard exists. 33 test files. But: most services are likely stubs or early-stage, no README, massive scope creep risk. High strategic value if focused, currently spread too thin.

### UX/Design: 4/10
Dashboard exists with basic React/Vite setup but minimal UI. This is primarily a backend service — the 'UX' is really the API and dashboard. Dashboard has App.tsx, api.ts, and basic styling but no component library or design system.
- ✅ Dashboard exists as a management interface
- ✅ API-first design is appropriate for the use case
- ❌ Minimal dashboard UI — likely just scaffolding
- ❌ No design system or component library
- ❌ No loading states or error handling in dashboard
- ❌ No responsive design

### Capabilities: 6/10
Staggering service breadth: campaigns, video stitching, podcast generation, brand voice, social publishing (Blotato), content pipeline, trend tracking, audience personas, caption generation, approval workflows, team collab, and more. But breadth vs depth is the concern — 30+ services can't all be complete.
- ✅ 30+ specialized services
- ✅ Blotato social publishing integration
- ✅ TrendpilotBridge for ecosystem connectivity
- ✅ Content pipeline with multi-stage processing
- ❌ Many services are likely stubs
- ❌ Scope creep — too many features for one project
- ❌ No clear priority or MVP definition
- ❌ Video stitching and podcast gen require heavy infra

### Code Quality: 6/10
Clean service architecture in src/services/. TypeScript with Genkit + Claude. 33 test files covering services, flows, and e2e. CI pipeline exists. Well-organized test structure (__tests__/services, flows, lib, e2e). Agent communication service shows thoughtful design. But no README is a red flag.
- ✅ Clean service-oriented architecture
- ✅ 33 test files with good structure
- ✅ CI pipeline
- ✅ Agent communication framework
- ❌ No README — huge documentation gap
- ❌ Genkit wildcard deps ('*') are dangerous
- ❌ No API documentation
- ❌ StoryBible directory purpose unclear

### Performance: 4/10
Backend Node.js service — performance is about API throughput and job processing. No evidence of queue management, caching, or rate limiting. Video/audio processing services will be resource-intensive. No performance monitoring.
- ✅ Service isolation allows independent scaling
- ❌ No caching strategy
- ❌ No queue management for heavy jobs
- ❌ No performance monitoring
- ❌ Video/audio processing needs dedicated infra

### Ease of Use: 4/10
No README, no API docs, no onboarding guide. Dashboard is minimal. A developer would need to read source code to understand the system. The approval workflow and team collab features suggest multi-user intent but no user docs exist.
- ✅ Genkit dev server for local development
- ✅ Service names are descriptive
- ❌ No README or documentation
- ❌ No API documentation
- ❌ No onboarding flow
- ❌ Dashboard is bare-minimum

### Prod Ready: 4/10
CI exists. MkDocs setup for documentation (but likely empty). No error monitoring, no environment management evident, wildcard Genkit dependencies are a deployment risk. Agent logs/metrics directories exist which is promising.
- ✅ CI pipeline
- ✅ MkDocs documentation setup
- ✅ Agent logs and metrics directories
- ❌ Wildcard dependencies break reproducible builds
- ❌ No error monitoring
- ❌ No environment configuration
- ❌ No deployment documentation

### X-Factor: 7/10
The vision is compelling — an AI content engine that handles everything from ideation to publishing. TrendpilotBridge for ecosystem integration shows strategic thinking. Agent communication framework is forward-looking. If focused and completed, this could be the centerpiece of Nathan's AI network. But it needs ruthless prioritization.
- ✅ Compelling vision — full content lifecycle automation
- ✅ Ecosystem bridge design
- ✅ Agent-to-agent communication
- ✅ Highest strategic value in the portfolio
- ❌ Vision exceeds execution by a wide margin
- ❌ Needs ruthless feature prioritization
- ❌ Risk of becoming vaporware without focus

### Top Recommendations
1. Write a README — this is table stakes
2. Define MVP: pick 5 core services, complete them fully, shelve the rest
3. Replace wildcard Genkit dependencies with pinned versions
4. Add API documentation (OpenAPI/Swagger)
5. Implement job queue for video/audio processing (Bull/BullMQ)

### Feature Inventory
| Feature | Status | Tests |
|---------|--------|-------|
| Content Pipeline | 🔶 partial | ✅ |
| Campaign Management | 🔶 partial | ✅ |
| Social Publishing (Blotato) | 🔶 partial | ✅ |
| Brand Voice Engine | 🔶 partial | ❌ |
| Video Stitching | 🔶 partial | ❌ |
| Podcast Generator | 🔶 partial | ✅ |
| Trendpilot Bridge | 🔶 partial | ❌ |
| Agent Communication | 🔶 partial | ✅ |
| Dashboard | 🔶 partial | ❌ |
| Approval Workflow | 🔶 partial | ❌ |
| Caption Generator | 🔶 partial | ❌ |
| Performance Tracker | 🔶 partial | ❌ |

---

## Trendpilot

**Overall: 5.8/10**

> AI newsletter platform with solid backend architecture — Prisma, Supabase, multi-tenant support, white-labeling, team management. Impressive 86 test files (highest test coverage in portfolio). Dashboard exists. But: small source footprint (103 files) vs heavy test count suggests test-driven development or AI-generated tests. Backend-only, no user-facing frontend beyond dashboard.

### UX/Design: 4/10
Primarily a backend API service. Dashboard exists but unclear how complete it is. No landing page, no public-facing UI. The 'UX' is the API design and dashboard — both appear functional but minimal.
- ✅ Dashboard exists for management
- ✅ API-first design
- ❌ No public-facing frontend
- ❌ Dashboard likely minimal
- ❌ No design system
- ❌ No responsive design evidence

### Capabilities: 6/10
Newsletter generation, trend discovery, subscriber management, analytics, team management, multi-tenant support, white-labeling, feed builder, export service, and real-time features. Good enterprise features (multi-tenant, white-label) but core newsletter generation flow is unclear.
- ✅ Multi-tenant architecture
- ✅ White-labeling support
- ✅ Team management
- ✅ Feed builder for content curation
- ❌ Core newsletter generation unclear
- ❌ No AI integration visible in src (expected for 'AI-powered')
- ❌ Export service needs more formats
- ❌ Real-time features unclear

### Code Quality: 7/10
Clean architecture with models, services, API, middleware, and lib directories. Prisma for DB with migrations. Auth guard and API key middleware. 86 test files is outstanding — phased test structure (phase1-11) suggests systematic development. CI pipeline exists.
- ✅ 86 test files — highest in portfolio
- ✅ Prisma with managed migrations
- ✅ Clean separation: models/services/api/middleware
- ✅ Phased test organization
- ❌ Test-to-source ratio (86:103) may indicate over-testing or stub code
- ❌ No TypeScript strict mode evidence
- ❌ Middleware could use more error handling

### Performance: 5/10
Supabase + Prisma provide reasonable DB performance. Real-time lib suggests WebSocket support. But no caching, no CDN for newsletter delivery, no queue for batch newsletter sends.
- ✅ Supabase for managed infrastructure
- ✅ Real-time capability
- ❌ No caching layer
- ❌ No queue for batch operations
- ❌ No CDN for newsletter delivery
- ❌ No performance monitoring

### Ease of Use: 5/10
Basic README with setup instructions. API key auth for programmatic access. But no API documentation, no user guide, no onboarding flow for the dashboard.
- ✅ README with setup instructions
- ✅ API key authentication
- ✅ Multi-tenant isolates users cleanly
- ❌ No API documentation
- ❌ No user onboarding
- ❌ No help or documentation in dashboard

### Prod Ready: 5/10
CI pipeline, Prisma migrations, Supabase backend. Auth middleware present. But: no error monitoring, no logging framework, no deployment docs, no environment management beyond .env.
- ✅ CI pipeline
- ✅ Prisma migrations for DB versioning
- ✅ Auth middleware
- ❌ No error monitoring
- ❌ No structured logging
- ❌ No deployment documentation
- ❌ No staging environment

### X-Factor: 6/10
AI-powered newsletters is a hot market (Beehiiv, Substack). Multi-tenant + white-label makes this a potential SaaS play. The Trendpilot→NarrativeReactor bridge gives it ecosystem value. But needs the actual AI part to be visible and compelling.
- ✅ Hot market (AI newsletters)
- ✅ SaaS-ready architecture (multi-tenant, white-label)
- ✅ Ecosystem connectivity via NarrativeReactor bridge
- ❌ AI capabilities not evident in source code
- ❌ Crowded market needs clear differentiation
- ❌ No user-facing demo or landing page

### Top Recommendations
1. Make the AI capabilities visible — trend discovery and content generation should be front and center
2. Build a landing page / public-facing frontend
3. Add API documentation (OpenAPI spec)
4. Implement error monitoring and structured logging
5. Wire the NarrativeReactor bridge for real content generation

### Feature Inventory
| Feature | Status | Tests |
|---------|--------|-------|
| Subscriber Management | ✅ complete | ✅ |
| Newsletter Generation | 🔶 partial | ✅ |
| Trend Discovery | 🔶 partial | ✅ |
| Analytics | 🔶 partial | ✅ |
| Multi-tenant Support | ✅ complete | ✅ |
| White-labeling | 🔶 partial | ✅ |
| Team Management | ✅ complete | ✅ |
| Feed Builder | 🔶 partial | ✅ |
| API Key Auth | ✅ complete | ✅ |
| Dashboard | 🔶 partial | ❌ |
| Real-time Updates | 🔶 partial | ❌ |

---

## Railway SaaS Template

**Overall: 4.6/10**

> Lightweight SaaS starter template on Next.js 15 with Stripe, NextAuth, Prisma, Redis, and Resend. Only 31 source files and 3 tests — this is a template, not a product. Clean for what it is but very early-stage. Good bones, needs flesh.

### UX/Design: 4/10
Next.js app with dashboard and admin pages. Custom fonts (Geist). Error and 404 pages present. Chat widget included. But extremely minimal — 3 pages total (home, dashboard, admin). No component library beyond basic Providers.
- ✅ Custom Geist fonts
- ✅ Error and 404 pages
- ✅ Chat widget for support
- ❌ Only 3 pages
- ❌ No design system
- ❌ Minimal UI components
- ❌ No responsive design evidence

### Capabilities: 4/10
Stripe billing, NextAuth authentication, Redis caching, email via Resend, analytics module, admin page, dashboard. These are the right building blocks for SaaS but each is minimal. Chat widget is a nice touch.
- ✅ Stripe integration
- ✅ NextAuth with Prisma adapter
- ✅ Redis caching
- ✅ Email templates via Resend
- ❌ Each integration is minimal/starter-level
- ❌ No real features beyond auth + billing
- ❌ Admin page likely bare
- ❌ No user settings or profile

### Code Quality: 5/10
Clean lib/ directory with well-separated concerns (auth, prisma, redis, stripe, email, analytics). Middleware for route protection. Only 3 test files — barely any coverage. TypeScript throughout. Prisma for DB.
- ✅ Clean separation of concerns in lib/
- ✅ Middleware for route protection
- ✅ TypeScript throughout
- ✅ Prisma schema management
- ❌ Only 3 test files
- ❌ No component tests
- ❌ 31 source files — very thin
- ❌ No shared types

### Performance: 5/10
Next.js 15 provides good defaults (SSR, code splitting). Redis for caching. Geist fonts are small. But so little code that performance isn't really testable. No monitoring.
- ✅ Next.js 15 built-in optimizations
- ✅ Redis caching layer
- ✅ Minimal bundle (few dependencies)
- ❌ Too thin to meaningfully evaluate
- ❌ No performance monitoring
- ❌ No CDN configuration

### Ease of Use: 4/10
As a template, ease of use means: how easy is it to fork and build on? Clean structure helps. But no documentation, no setup guide, no .env.example visible. A developer would need to reverse-engineer the required env vars.
- ✅ Clean project structure
- ✅ Standard Next.js patterns
- ❌ No setup documentation
- ❌ No .env.example
- ❌ No contribution guide
- ❌ No architecture overview

### Prod Ready: 4/10
CI pipeline exists. Prisma migrations. NextAuth + middleware for auth. But: no error monitoring, no logging, no health check endpoint (ironic — there's a health test but unclear if endpoint exists), minimal test coverage.
- ✅ CI pipeline
- ✅ Auth middleware
- ✅ Prisma migrations
- ❌ No error monitoring
- ❌ No logging framework
- ❌ 3 tests is insufficient
- ❌ No deployment documentation

### X-Factor: 4/10
SaaS templates are a dime a dozen. This one has Railway-specific value (optimized for Railway deployment) but doesn't stand out otherwise. Needs a unique hook — maybe Railway-specific features like service management, usage monitoring, or one-click deploys.
- ✅ Railway-optimized deployment
- ✅ Solid tech stack choices
- ❌ Undifferentiated from hundreds of SaaS templates
- ❌ No Railway-specific features beyond hosting
- ❌ Too thin to be useful without significant work

### Top Recommendations
1. Add comprehensive README with setup instructions
2. Create .env.example with all required variables
3. Add Railway-specific features (service dashboard, usage monitoring) to differentiate
4. Increase test coverage — at least cover auth and billing flows
5. Add API routes for common SaaS patterns (webhooks, API keys, team management)

### Feature Inventory
| Feature | Status | Tests |
|---------|--------|-------|
| Stripe Billing | 🔶 partial | ✅ |
| NextAuth Authentication | ✅ complete | ❌ |
| Redis Caching | 🔶 partial | ✅ |
| Email (Resend) | 🔶 partial | ❌ |
| Admin Dashboard | 🔶 partial | ❌ |
| User Dashboard | 🔶 partial | ❌ |
| Chat Widget | 🔶 partial | ❌ |
| Analytics | 🔶 partial | ❌ |

---

## Historical Trend

*Daily scores will accumulate here over time.*

| Date | FlipMyEra | Second-Opinion | NarrativeReactor | Trendpilot | Railway SaaS |
|------|:---------:|:--------------:|:----------------:|:----------:|:------------:|
| 2026-02-20 | 6.8 | 6.5 | 5.4 | 5.8 | 4.6 |
