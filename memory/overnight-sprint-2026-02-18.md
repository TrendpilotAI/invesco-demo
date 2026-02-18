# Overnight Sprint Plan — 2026-02-18
# 6 Batches, ~30 agents, High-Value Long-Running Tasks

## BATCH 1 — Second-Opinion Competition (RUNNING NOW)
> Priority: CRITICAL — Kaggle deadline Feb 24

1. [x] `so-demo-script` — Demo video script & storyboard ✅
2. [ ] `so-agentic-wire` — Wire AgenticPipeline into AnalysisDashboard (RUNNING)
3. [ ] `so-submission-prep` — Full submission polish + checklist (RUNNING)

## BATCH 2 — Second-Opinion: Competition-Winning Polish
> Make this the most impressive entry in the competition

4. [ ] **SO: Full E2E Test Suite** — Playwright tests covering every user journey: symptom input → model selection → analysis → results → FHIR export → PDF report. Cover demo mode + auth mode. 20+ test scenarios.
5. [ ] **SO: Mobile + Accessibility Overhaul** — Full responsive audit, WCAG 2.1 AA compliance, screen reader support, keyboard navigation, touch targets, reduced motion. This is a medical app — accessibility is critical for judges.
6. [ ] **SO: Production Performance** — Lighthouse 90+ on all metrics. Code split every route, lazy load heavy components, optimize images, add service worker with offline support, preload critical assets.
7. [ ] **SO: Interactive Demo Mode** — Build a guided walkthrough mode that auto-plays through 3 compelling medical cases with narration overlays. Judges should be able to click "Watch Demo" and see the app shine without configuring anything.
8. [ ] **SO: Architecture Documentation** — Full technical architecture doc with diagrams (Mermaid), data flow, model pipeline explanation, security model, HIPAA considerations. Judges love depth.

## BATCH 3 — FlipMyEra: Launch-Ready Revenue Machine
> Goal: This should be ready for real paying customers by morning

9. [ ] `fme-payment-audit` — Stripe flow hardening (RUNNING)
10. [ ] `fme-deploy-checklist` — Production hardening (RUNNING)
11. [ ] `fme-landing-conversion` — Conversion optimization (RUNNING)
12. [ ] **FME: Complete Onboarding Flow** — First-time user experience: welcome modal → template picker → sample ebook preview → "Create Your First Ebook" CTA → payment gate. Reduce time-to-value to under 60 seconds.
13. [ ] **FME: Content Marketing Engine** — Create 10 SEO-optimized blog post pages targeting Taylor Swift fan keywords. Long-tail: "taylor swift eras tour ebook", "custom taylor swift gifts", "swiftie birthday present ideas". Full Next.js/React pages with proper meta tags.
14. [ ] **FME: Admin Dashboard** — Revenue metrics, user signups, ebook generation stats, Stripe webhook logs, error tracking. Real-time charts. This is Nathan's command center for the business.

## BATCH 4 — NarrativeReactor: Content Ops Platform
> Goal: Working content automation pipeline

15. [ ] **NR: Full API + Auth Integration** — Wire all 8 routes with real JWT auth, rate limiting, input validation, error handling. Integration tests for every endpoint. This should be deployable.
16. [ ] **NR: Content Generation Pipeline** — End-to-end: topic input → AI research → draft generation → editing UI → multi-platform formatting (X thread, LinkedIn post, blog). Use OpenAI/DeepSeek APIs.
17. [ ] **NR: Publishing Connectors** — Build Blotato integration for cross-platform posting. X, LinkedIn, Instagram connectors. Schedule queue with calendar view. Analytics tracking per post.
18. [ ] **NR: Campaign Management UI** — React dashboard: create campaigns, set goals, track performance, A/B test content variations, manage content calendar. Dark theme matching existing design.

## BATCH 5 — Trendpilot: SaaS Product Build
> Goal: Functional trend monitoring SaaS

19. [ ] **TP: Full Stack Integration** — Merge all 5 phases into a working app: data ingestion → trend detection → alerting → API → dashboard. End-to-end smoke tests.
20. [ ] **TP: React Dashboard** — Real-time trend dashboard with charts (Recharts), filters, search, alert management, API key settings. Responsive, clean UI.
21. [ ] **TP: Deploy Pipeline** — Railway deployment config, health checks, Postgres migrations, Redis caching, environment management. One-click deploy docs.
22. [ ] **TP: Landing Page + Docs** — Marketing site with pricing page (4 tiers), feature comparison, API docs (Swagger UI), getting started guide. Conversion-optimized.

## BATCH 6 — Websites + Infrastructure
> Goal: Professional web presence + healthy infra

23. [ ] **ForwardLane.com Deploy** — GitHub repo, Vercel deploy, custom domain setup docs, OG images, sitemap, robots.txt, Google Analytics, structured data.
24. [ ] **SignalHaus.ai Deploy** — Same as above for SignalHaus.
25. [ ] **n8n Recovery** — Redeploy n8n on Railway, import viral video workflow, verify webhook endpoints, document setup.
26. [ ] **CI/CD Hardening** — GitHub Actions for all repos: lint, test, build, deploy preview. Branch protection rules. Dependabot. Security scanning.
27. [ ] **Infrastructure Status Dashboard** — Update /dashboard/ with real health checks for all services, deploy status, test counts, uptime metrics.
28. [ ] **Cross-Project Auth** — Shared auth library (JWT + Clerk) that all projects can use. Consistent user model across FlipMyEra, NarrativeReactor, Trendpilot.
