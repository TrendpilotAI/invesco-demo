# Project Scorecard — Feb 20, 2026 (Evening Run)

## Scoring: 7 categories, weighted average (UX 20%, Capabilities 20%, Code Quality 15%, Performance 10%, Ease of Use 15%, Production Readiness 10%, X-Factor 10%)

---

### 🎵 FlipMyEra — 6.9/10 (+0.1)
| Category | Score | Notes |
|----------|-------|-------|
| UX/Design | 7 | Solid Tailwind UI, responsive, loading states. Onboarding wizard added. |
| Capabilities | 8 | Ebook gen, Stripe payments, templates (Beyoncé/BTS/etc), sharing, referrals, subscriptions, AI art, creator profiles. Feature-rich. |
| Code Quality | 7 | 377 src files, 42 tests, TypeScript, Vitest, good structure. Test ratio could be higher. |
| Performance | 6 | Code split from 1.1MB→652KB, but still chunky. Lazy loading in place. |
| Ease of Use | 7 | Onboarding flow, template picker, sample preview. SEO content pages. |
| Production Readiness | 7 | CI/CD, Netlify, Sentry, env.example, security headers. No Docker. |
| X-Factor | 7 | Unique niche (Swiftie ebooks). Multiple artist templates. Creator marketplace concept. |
| **Weighted** | **6.9** | Closest to revenue. Needs: payment flow E2E testing, Lighthouse optimization. |

---

### 🏥 Second-Opinion — 6.6/10 (stable)
| Category | Score | Notes |
|----------|-------|-------|
| UX/Design | 7 | Demo mode, mobile responsive, narrative media, knowledge graph UI. |
| Capabilities | 8 | Multi-model consensus, FHIR export, PDF reports, telemedicine, research mode, multi-language (6 langs). |
| Code Quality | 6 | 147 src, 23 tests. JS→TS migration done but test coverage low for a medical app. node_modules fragile. |
| Performance | 6 | Code split from 420KB→292KB. Service worker, preconnect. |
| Ease of Use | 7 | Guided demo with 3 medical cases. Good docs (256-line README, ARCHITECTURE.md). |
| Production Readiness | 6 | 5 CI workflows, Firebase hosting, HIPAA audit logging. No monitoring. Firebase SA key ephemeral. |
| X-Factor | 8 | Real origin story (Tracey's wrist). 35,035x cheaper than human second opinion. Kaggle competition entry. No real competitors (41 repos scanned). |
| **Weighted** | **6.6** | Kaggle deadline Feb 24. Needs: Gemini API key in Kaggle secrets, more test coverage. |

---

### 📈 Trendpilot — 5.9/10 (+0.1)
| Category | Score | Notes |
|----------|-------|-------|
| UX/Design | 5 | Dashboard exists but rough. Dark theme. Charts via Recharts. |
| Capabilities | 7 | Trend detection, alerting (spike/velocity/threshold), API with 4-tier pricing, white-label, enterprise SSO, GDPR. |
| Code Quality | 7 | 98 src, 86 tests (best test ratio!). Zod models, good TDD. OpenAPI spec. |
| Performance | 5 | No bundle optimization yet. |
| Ease of Use | 5 | API docs exist but onboarding rough. Landing page needs work. |
| Production Readiness | 6 | CI, Docker, Railway config, health checks. Postgres migrations. |
| X-Factor | 5 | Crowded trend space but enterprise features differentiate. |
| **Weighted** | **5.9** | Best test coverage. Needs: frontend polish, real data sources connected. |

---

### 📝 NarrativeReactor — 5.5/10 (+0.1)
| Category | Score | Notes |
|----------|-------|-------|
| UX/Design | 5 | Dark admin dashboard, campaign management. Functional not polished. |
| Capabilities | 7 | Content pipeline, Blotato publishing, campaigns, video tools, multi-brand, voice (Fish Audio). 220 tests in pipeline. |
| Code Quality | 6 | 105 src, 33 tests. Express routes with auth/rate limiting. No README. |
| Performance | 4 | No optimization work done. |
| Ease of Use | 4 | No README. No onboarding. Developer-facing only. |
| Production Readiness | 5 | CI exists. env.example. No deploy yet. No monitoring. |
| X-Factor | 6 | Trendpilot→NarrativeReactor data flywheel is strong concept. Multi-brand voice cloning. |
| **Weighted** | **5.5** | Strategic backbone but needs README, deploy, and frontend polish. |

---

### 🚀 Railway SaaS Template — 4.7/10 (+0.1)
| Category | Score | Notes |
|----------|-------|-------|
| UX/Design | 4 | Basic template UI. |
| Capabilities | 5 | Next.js/Stripe/Prisma/Redis starter. Auth, billing, API. |
| Code Quality | 4 | 81 src, 3 tests. Minimal coverage. |
| Performance | 5 | Next.js defaults. |
| Ease of Use | 5 | README (192 lines), env.example, deploy button. |
| Production Readiness | 5 | Docker, CI, Railway config. |
| X-Factor | 4 | Many SaaS templates exist. Needs differentiation. |
| **Weighted** | **4.7** | Template project — value is as a starting point, not a product. |

---

## Trend
| Project | Feb 19 | Feb 20 AM | Feb 20 PM | Delta |
|---------|--------|-----------|-----------|-------|
| FlipMyEra | 6.7 | 6.8 | 6.9 | +0.2 |
| Second-Opinion | 6.6 | 6.5 | 6.6 | ±0 |
| Trendpilot | 5.5 | 5.8 | 5.9 | +0.4 |
| NarrativeReactor | 4.6 | 5.4 | 5.5 | +0.9 |
| Railway SaaS | 4.5 | 4.6 | 4.7 | +0.2 |
