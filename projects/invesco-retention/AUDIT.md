# Invesco Signal Studio — Code Audit
**Date:** 2026-02-26  
**Auditor:** Honey (Code Optimization Agent)  
**Scope:** demo-app/src/ — pages, components/ui, lib, config files

---

## Summary

| Severity | Count | Status |
|---|---|---|
| 🔴 CRITICAL | 3 | ✅ Fixed |
| 🟠 HIGH | 3 | ✅ Fixed |
| 🟡 MEDIUM | 4 | Documented |
| 🟢 LOW | 5 | Documented |

---

## 🔴 CRITICAL

### C0 — JSX Fragment parse error crashes Vercel build in salesforce/page.tsx
**File:** `src/app/salesforce/page.tsx:113`  
**Issue:** `{!loading && (<>` — JSX fragment inside conditional causes Turbopack parse error: "Expected '</', got 'ident'" at line 401. The build **fails entirely** — this page does not exist in production. This is the hero demo page.  
**Fix:** Replace `<>...</>` with `<div className="contents">...</div>` (CSS `display: contents` is a transparent wrapper — no visual impact).  
**Status:** ✅ Fixed — build now passes

---

### C1 — Non-null assertion crash in mobile/page.tsx
**File:** `src/app/mobile/page.tsx:13`  
**Issue:** `const advisor = getAdvisor('sarah-chen')!;` — hardcoded ID with non-null assertion `!`. If the ID doesn't resolve (e.g., mock-data rebuild changes the `makeId()` output, or the data changes), this silently crashes at runtime as a TypeError when any advisor property is accessed.  
**Fix:** Add a null guard fallback.  
**Status:** ✅ Fixed

```ts
// Before
const advisor = getAdvisor('sarah-chen')!;

// After
const advisor = getAdvisor('sarah-chen') ?? advisors[0];
```

---

### C2 — Unused imports in mock-data.ts (dead code — affects bundle)
**File:** `src/lib/mock-data.ts:8`  
**Issue:** `getSignalOutput` and `getAdvisorPractice` are imported from `combined-data.ts` but never used anywhere in `mock-data.ts`. This is dead code that adds weight to the module graph unnecessarily.  
**Fix:** Remove unused named imports.  
**Status:** ✅ Fixed

---

## 🟠 HIGH

### H1 — `import-data.ts` is dead code — included in production bundle
**File:** `src/lib/data/import-data.ts`  
**Issue:** `import-data.ts` is a Node.js build script (reads from filesystem, uses `path`, `fs`) that should NEVER run in the browser or Next.js runtime. It is NOT imported anywhere in the app, so it won't be bundled — BUT it sits in `src/lib/data/` which is within the TypeScript compilation scope. The `tsconfig.json` `include` pattern `**/*.ts` will compile it. It has a `fs.readFileSync` at module level — this could cause a Vercel build failure if the TypeScript compiler tries to resolve `__dirname` in a bundler environment (Next.js uses bundler resolution mode).  
**Fix:** Move to a scripts folder outside `src/`, or add a note. Best practice: rename to `import-data.script.ts` and add to `.gitignore`/build ignore, or move to root `scripts/`. For safety, added `.ts` compile exclusion note in tsconfig comment.  
**Status:** ✅ Fixed — moved to `scripts/import-data.ts` outside src

---

### H2 — Missing security headers in next.config.ts
**File:** `next.config.ts`  
**Issue:** The config is completely empty `{}`. For a production Vercel deploy of a financial demo, missing CSP, X-Frame-Options, and HSTS headers is a risk if the demo is publicly accessible.  
**Fix:** Add standard security headers.  
**Status:** ✅ Fixed

---

### H3 — `eslint-disable-next-line @typescript-eslint/no-explicit-any` in combined-data.ts
**File:** `src/lib/data/combined-data.ts:3851`  
**Issue:** The `digitalEngagement` export is typed as `DigitalEngagement & Record<string, any>`. The `any` suppression is because the `email_engagement` array is not in the `DigitalEngagement` type, but IS accessed at runtime via array spread. The proper fix is to extend the type.  
**Fix:** Add `email_engagement` to `DigitalEngagement` type in `types.ts`.  
**Status:** ✅ Fixed

---

## 🟡 MEDIUM

### M1 — stagger-5 class defined but never used
**File:** `src/app/globals.css:133`  
**Issue:** `.stagger-5` is defined but page.tsx only uses `stagger-1` through `stagger-4` (4 cards, `i+1` from 0..3). Minor dead CSS.  
**Fix:** Remove or keep for future use (low priority). Not fixed to avoid touching CSS.

---

### M2 — `scroll-area.tsx` UI component is unused
**File:** `src/components/ui/scroll-area.tsx`  
**Issue:** The `ScrollArea` component exists in `/components/ui/` but is not imported by any page. Adds to bundle if imported elsewhere.  
**Fix:** Can be removed if no future use is planned. Kept for demo flexibility.

---

### M3 — `tabs.tsx` UI component is unused
**File:** `src/components/ui/tabs.tsx`  
**Issue:** The `Tabs` component is not imported anywhere in the app pages.  
**Fix:** Can be removed. Kept for demo flexibility.

---

### M4 — hardcoded `new Date('2026-02-18')` in mock-data.ts
**File:** `src/lib/mock-data.ts` — `daysSince()` function  
**Issue:** The "today" date is hardcoded. `lastContactDaysAgo` values will be increasingly wrong as time passes. For a live demo on March 2026, the Sarah Chen "21 days ago" counter will read as ~28 days.  
**Fix:** Change to `new Date()` for dynamic calculation.  
**Status:** ✅ Fixed (low risk, demo-safe)

---

## 🟢 LOW

### L1 — Variable `inter.variable` used as `font-sans` class alias but font is called `Geist`
**File:** `src/app/layout.tsx:5`  
**Issue:** The Inter font is loaded and assigned to `--font-geist-sans` CSS variable — likely a copy-paste from the Next.js template. The variable name is misleading but functionally harmless.  
**Fix:** Rename to `--font-inter` for clarity, or leave as-is (cosmetic only).

---

### L2 — Mobile page bottom nav uses `fixed` + `translate` for centering
**File:** `src/app/mobile/page.tsx`  
**Issue:** `fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[430px]` — this works for iOS but may clip on very narrow screens. Also no `padding-bottom: env(safe-area-inset-bottom)` for iPhone home indicator. Touch targets (bottom nav items) are `py-3` which is ~48px — acceptable but borderline.  
**Fix:** Add `pb-[env(safe-area-inset-bottom)]` and ensure `min-height: 44px` touch targets.

---

### L3 — `separator.tsx` re-exports Radix but is unused in mobile/create views
**File:** `src/components/ui/separator.tsx`  
**Issue:** Minor unused import in some pages. Not a real concern.

---

### L4 — Bundle size: combined-data.ts is ~3500 lines of inline JSON
**File:** `src/lib/data/combined-data.ts`  
**Issue:** The entire synthetic dataset (~200KB of data) is inlined in a TypeScript file. Next.js will bundle this into the JS chunk. For a demo this is acceptable, but in production this would be moved to a DB. Current size is acceptable for demo purposes.

---

### L5 — `stagger-${i+1}` in page.tsx uses dynamic class names
**File:** `src/app/page.tsx:53`  
**Issue:** Tailwind purges dynamic class names like `stagger-${i+1}` unless they're in the `safelist` config. However, since these are custom CSS classes (not Tailwind utilities), they live in `globals.css` and are always included — so this is safe. No action needed.

---

## Animation Classes Check ✅
- `animate-fade-in-up` — defined at `globals.css:121`
- `stagger-1` through `stagger-4` — defined at `globals.css:129-132`
- `stagger-5` — defined but unused (LOW)
- All animation classes used in page.tsx are defined ✅

## import-data.ts Usage Check ✅
- `import-data.ts` is **NOT** imported by any source file
- It is a generator script only (noted in file header)
- **Risk:** It resides in `src/lib/data/` within TypeScript's compile scope — moved to `scripts/` ✅

---

## Files Modified
1. `src/app/salesforce/page.tsx` — fixed JSX fragment parse error blocking build (C0)
2. `src/app/mobile/page.tsx` — null guard for advisor (C1)
3. `src/lib/mock-data.ts` — removed dead imports, fixed hardcoded date (C2, M4)
4. `src/lib/data/types.ts` — added `email_engagement` to DigitalEngagement (H3)
5. `next.config.ts` — added security headers (H2)
6. `scripts/import-data.ts` — moved out of src/ compile scope (H1)

---

## Round 2 Audit — 2026-02-27

### Summary
Demo is live. Core bugs fixed. Focusing on demo-day failure modes.

### 🟠 HIGH — Static Export Missing `/mobile` Route

**File:** `demo-app/out/`
**Issue:** The `out/` directory has `mobile/` folder and `mobile.html` — but the GitHub Pages deploy URL structure matters. If the PWA links to `/mobile` (no .html), GitHub Pages serves 404. Check all internal links use `.html` suffix for static export compatibility.
**Fix:** Verify all navigation links in index.html use `mobile.html` not `/mobile`
**Effort:** XS

### 🟠 HIGH — Service Worker Cache Version

**File:** `mobile-pwa/sw.js:1`
**Issue:** Cache is named `signal-studio-v1` (hardcoded). If any PWA assets change, the service worker won't invalidate the cache for returning users — they'll see stale content. Since the demo was recently deployed, returning visitors (Megan/Craig testing) may see old version.
**Fix:** Bump to `signal-studio-v2` or use a timestamp-based cache key. Or add a `?v=2` param to all asset URLs in ASSETS array.
**Effort:** XS

### 🟡 MEDIUM — PWA Not HTTPS on localhost

**File:** `mobile-pwa/`
**Issue:** Service workers require HTTPS (or localhost). If demoed from GitHub Pages (HTTPS), this is fine. If ever run locally for demo prep, SW registration will silently fail on iOS Safari.
**Mitigation:** Always demo from the GitHub Pages URL, never localhost.
**Effort:** N/A (documentation only)

### 🟡 MEDIUM — No Offline Fallback for Dashboard

**File:** `mobile-pwa/sw.js`
**Issue:** The PWA service worker caches the core app assets but dashboard data is in `data.js`. If `data.js` fails to cache (e.g., first visit with poor connection), the app shows a blank state.
**Fix:** Ensure `data.js` is in the ASSETS cache list — it already is, so this should be fine. Verify by testing on throttled connection.
**Effort:** XS (test only)

### 🟢 LOW — Demo App Bundle Size Unknown

**File:** `demo-app/out/`
**Issue:** No bundle analysis was run. Given it's a Next.js static export with Tailwind + Radix UI, bundle could be 200-500KB. On mobile (4G, not WiFi), initial load could be 2-4 seconds.
**Fix:** Add `ANALYZE=true` build for visibility. For the demo, ensure Megan/Craig + Brian are on WiFi.
**Effort:** XS (analysis) / M (if optimization needed)

### 🟢 LOW — Salesforce LWC Missing SFDX Auth

**File:** `salesforce-lwc/`
**Issue:** The LWC package is well-structured but deploying to a real Salesforce sandbox requires `sfdx auth:web:login` and a connected app setup. The `docs/connected-app-setup.md` exists but deployment hasn't been tested end-to-end in a live org.
**Risk:** Low for demo (using HTML mockup). Higher if Invesco asks for "deploy in our sandbox" during pilot.
**Fix:** Test deploy in ForwardLane's own Salesforce sandbox before demo.
**Effort:** M

### ✅ Confirmed Working
- All 4 routes present in `out/`: index, dashboard, salesforce, mobile, create
- Service worker structure correct for GitHub Pages HTTPS
- Push-to-Salesforce toast implemented (TODO-213 ✅)
- Invesco branding in SF chrome (TODO-214 ✅)
- Skeleton loaders (TODO-215 ✅)
- Demo reset via ?reset=true (TODO-216 ✅)
