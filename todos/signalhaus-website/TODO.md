# SignalHaus Website — TODO
*Generated: 2026-03-15 | Source: BRAINSTORM.md, PLAN.md, AUDIT.md + repo inspection*

## Composite Score: 6.5/10

| Dimension | Score | Notes |
|-----------|-------|-------|
| Code Quality | 6/10 | Clean TS strict, good structure, but DRY violations, no linting config, CSP unsafe-inline |
| Test Coverage | 2/10 | Only 1 test file (roi.test.ts). 0 coverage on API routes, MDX, components |
| Security | 5/10 | Upstash configured but in-memory fallback still present. No CAPTCHA. CSP has unsafe-inline/eval |
| Documentation | 8/10 | Excellent — BRAINSTORM, PLAN, AUDIT, README, DEPLOY docs all present and thorough |
| Architecture | 7/10 | Solid Next.js 16 App Router, proper separation, MDX blog, sitemap, JSON-LD |
| Business Value | 8/10 | Core marketing site for SignalHaus AI consultancy. Direct revenue funnel |

---

## 🔴 CRITICAL Issues

- [ ] **[SECURITY] Rate limiter fallback to in-memory Map** — Upstash deps installed but `getRatelimit()` in `api/contact/route.ts` falls back to `new Map()` when env vars missing. Verify UPSTASH_REDIS_REST_URL + TOKEN are set in Vercel production. If not, rate limiting is broken on every cold start.
- [ ] **[SECURITY] No bot protection (CAPTCHA/Turnstile)** — Contact form has no challenge. Automated bots bypass string-based XSS checks trivially.
- [ ] **[TESTING] Near-zero test coverage** — Only `src/lib/__tests__/roi.test.ts` exists. No tests for contact API, validation, MDX parsing, or any components.

---

## P0 — Do Now (Quick Wins + Critical Fixes)

- [ ] Verify Upstash env vars are set in Vercel production (not just installed in package.json)
- [ ] Add Cloudflare Turnstile to contact form (`@marsidev/react-turnstile`) — 2h
- [ ] Link RSS feed in layout.tsx `<head>` — `<link rel="alternate" type="application/rss+xml">` — 15min
- [ ] Add `typecheck` step to CI: `npx tsc --noEmit` in `.github/workflows/ci.yml` — 15min
- [ ] Add `npm audit --audit-level=moderate` to CI pipeline — 5min

## P1 — This Sprint (High Impact)

- [ ] Write Vitest unit tests for `validateContact()` — all branches (missing fields, bad email, XSS patterns, budget whitelist) — 1h
- [ ] Write Vitest unit tests for `getAllPostsMeta()` and `getPostBySlug()` — 1h
- [ ] Write API integration tests for `/api/contact` with mocked Resend/Slack — 1.5h
- [ ] Add ESLint + Prettier config (eslint-config-next + @typescript-eslint) — 1h
- [ ] HubSpot CRM sync on contact form submission — 2h
- [ ] Calendly/cal.com booking embed on /contact page — 2h
- [ ] Newsletter signup route (`/api/subscribe`) + CTA component + Resend Audiences — 4h

## P2 — Next Sprint (Medium Impact)

- [ ] Dynamic OG images via `next/og` ImageResponse for blog posts — 3h
- [ ] `/services/[slug]` detail pages with Service JSON-LD — 4h
- [ ] `/case-studies/[slug]` detail pages with detailed MDX content — 3h
- [ ] Zod schema for contact form validation (replace hand-rolled) — 1h
- [ ] Extract shared SEO config to `src/lib/seo.ts` (DRY openGraph.images) — 1h
- [ ] Add author Person JSON-LD to blog Article schema — 30min
- [ ] Email ROI report after calculator lead capture — 3h
- [ ] Playwright E2E tests (contact form, ROI wizard, navigation) — 4h
- [ ] Add `React.cache()` to `getAllPostsMeta()` for perf — 15min

## P3 — Polish & Nice-to-Have

- [ ] Vercel Analytics + Speed Insights components — 30min
- [ ] Sentry error monitoring (`@sentry/nextjs`) — 1h
- [ ] Lazy-load TestimonialCarousel with `dynamic()` — 30min
- [ ] CSP nonce-based hardening (replace unsafe-inline for scripts) — 2h
- [ ] Bundle analysis with `@next/bundle-analyzer` — 30min
- [ ] Dependabot config (`.github/dependabot.yml`) — 15min
- [ ] About page Person JSON-LD for Nathan Stevenson — 30min

---

## ✅ Recently Completed (since AUDIT.md)

- [x] Fix missing `/logo.png` — now exists in `/public/logo.png`
- [x] Branded 404 page — `src/app/not-found.tsx` created with full SignalHaus branding
- [x] Extract ROI `calculate()` to `src/lib/roi.ts` — done with types
- [x] ROI unit tests — `src/lib/__tests__/roi.test.ts` exists
- [x] Upstash deps installed — `@upstash/ratelimit` + `@upstash/redis` in package.json
- [x] GitHub Actions CI pipeline — `.github/workflows/ci.yml` exists
- [x] Vitest configured — in package.json scripts + vitest.config.ts

---

## Env Vars Still Needed (verify in Vercel)

```
UPSTASH_REDIS_REST_URL      — Rate limiting (verify set in prod!)
UPSTASH_REDIS_REST_TOKEN     — Rate limiting (verify set in prod!)
NEXT_PUBLIC_TURNSTILE_SITE_KEY — Bot protection (not yet implemented)
TURNSTILE_SECRET_KEY          — Bot protection (not yet implemented)
HUBSPOT_ACCESS_TOKEN          — CRM sync (not yet implemented)
NEXT_PUBLIC_CALENDLY_URL      — Booking embed (not yet implemented)
RESEND_AUDIENCE_ID            — Newsletter (not yet implemented)
```
