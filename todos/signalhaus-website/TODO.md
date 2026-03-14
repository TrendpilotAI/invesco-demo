# TODO — SignalHaus Website
*Last scored: 2026-03-14 | Composite: 6.8/10*

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 7/10 | TypeScript strict, clean architecture, extracted ROI lib. DRY violations in metadata. |
| Test Coverage | 3/10 | Only `roi.test.ts` (19 tests). No validation, API, or E2E tests. |
| Security | 5/10 | Upstash rate limiter ✅, CSP/HSTS ✅, but no CAPTCHA, CSP uses unsafe-inline/eval. |
| Documentation | 8/10 | Excellent BRAINSTORM/PLAN/AUDIT/DEPLOY/README docs. |
| Architecture | 7/10 | Clean App Router structure, proper separation. Missing detail pages for SEO depth. |
| Business Value | 8/10 | Core marketing site for SignalHaus AI consultancy. Direct lead generation. |

## ⚠️ HIGH PRIORITY Issues

### Security
- [ ] **Add Cloudflare Turnstile bot protection** on contact form — no CAPTCHA means bots can spam freely (BRAINSTORM §4.1)
- [ ] **Harden CSP** — `unsafe-inline` and `unsafe-eval` in script-src significantly weaken XSS protection (AUDIT §1)

### Testing
- [ ] **Add validateContact() unit tests** — all 6 fields, XSS patterns, budget whitelist (most critical untested logic)
- [ ] **Add /api/contact integration tests** — mock Resend+Slack, test happy path, 422, 429
- [ ] **Add Playwright E2E tests** — contact form flow, ROI calculator wizard, page navigation
- [ ] **Set up CI pipeline** — GitHub Actions: lint → typecheck → build → test → npm audit

### Lead Capture
- [ ] **HubSpot CRM integration** — leads currently go to email+Slack only; no pipeline tracking
- [ ] **Calendly/cal.com booking embed** — reduce friction from "email → reply → schedule" to instant booking
- [ ] **Newsletter signup + drip sequence** — capture non-ready leads via Resend Audiences

## 📋 MEDIUM PRIORITY

### SEO & Content
- [ ] **Dynamic OG images** via `next/og` — blog posts all share static `/og-image.png`
- [ ] **Service detail pages** `/services/[slug]` — SEO depth per service offering
- [ ] **Case study detail pages** `/case-studies/[slug]` — detailed social proof with schema markup
- [ ] **Add blog author to Article JSON-LD** — missing Person schema in blog posts

### Code Quality
- [ ] **Zod validation** — replace hand-rolled `validateContact()` with Zod schema
- [ ] **Extract seo.ts constants** — DRY up repeated `openGraph.images` and site URL across pages
- [ ] **ESLint + Prettier config** — no linting beyond Next.js defaults

## 🔽 LOW PRIORITY / NICE TO HAVE

- [ ] **Vercel Analytics + Speed Insights** — free, just add components
- [ ] **Sentry error monitoring** — capture API route exceptions
- [ ] **Lazy-load TestimonialCarousel** — `dynamic(() => import(...), { ssr: false })`
- [ ] **React.cache() on getAllPostsMeta** — FS reads on every request
- [ ] **Bundle analysis** — check ROI calculator bundle impact
- [ ] **Dependabot config** — `.github/dependabot.yml` for automated dep updates
- [ ] **Email ROI report** — send branded HTML report after ROI calculator lead capture

## ✅ COMPLETED (since last audit)

- [x] Replace in-memory rate limiter with Upstash Redis (commit ca5a07e)
- [x] Extract ROI calculate() to src/lib/roi.ts + 19 Vitest tests (commit 6b15b1d)
- [x] Fix missing logo.png (commit 068c124)
- [x] Branded 404 page (commit 068c124)
- [x] Link RSS feed in layout head (commit 068c124)
- [x] Vercel prod-ready config (commit 059442f)
