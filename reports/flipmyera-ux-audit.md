# FlipMyEra.com — UX Audit Report

**Date:** 2026-02-14 14:42 UTC
**Audited URL:** https://flipmyera.com

---

## 📊 Summary

### ⚡ Performance

| Page | Load Time (s) | Status |
|------|--------------|--------|
| homepage_desktop | 4.88 | 200 |
| auth_desktop | 2.68 | 200 |
| page_plans_desktop | 1.91 | 200 |
| page_faq_desktop | 1.98 | 200 |
| page_sign-up_desktop | ? | ? |

### 🔍 SEO

#### homepage

- **Title:** Flip My Era
- **Meta Description:** Lovable Generated Project
- **OG Image:** /og-image.png
- **OG Title:** ⚠️ MISSING
- **Canonical:** ⚠️ MISSING

#### auth

- **Title:** Flip My Era
- **Meta Description:** Lovable Generated Project
- **OG Image:** /og-image.png
- **OG Title:** ⚠️ MISSING
- **Canonical:** ⚠️ MISSING

#### page_plans

- **Title:** Flip My Era
- **Meta Description:** Lovable Generated Project
- **OG Image:** /og-image.png
- **OG Title:** ⚠️ MISSING
- **Canonical:** ⚠️ MISSING

#### page_faq

- **Title:** Flip My Era
- **Meta Description:** Lovable Generated Project
- **OG Image:** /og-image.png
- **OG Title:** ⚠️ MISSING
- **Canonical:** ⚠️ MISSING


### ♿ Accessibility

#### homepage

- ✅ All images have alt text
- ✅ No broken images detected
- ✅ Form inputs have labels/placeholders
- **Heading structure:**
      H3: Flip My  Era
  H1: Choose Your Era
      H3: 1989
      H3: The Life of a Showgirl
      H3: Folklore/Evermore
      H3: Red
      H3: Reputation
      H3: Lover
      H3: Midnights
      H3: Product
      H3: Support
      H3: Legal

#### auth

- ✅ All images have alt text
- ✅ No broken images detected
- ✅ Form inputs have labels/placeholders
- **Heading structure:**
  H1: FlipMyEra
      H3: Sign In to FlipMyEra
  H1: Sign in to FlipMyEra
      H3: Product
      H3: Support
      H3: Legal

#### page_plans

- ✅ All images have alt text
- ✅ No broken images detected
- ✅ Form inputs have labels/placeholders
- **Heading structure:**
  H1: FlipMyEra
      H3: Sign In to FlipMyEra
  H1: Sign in to FlipMyEra
      H3: Product
      H3: Support
      H3: Legal

#### page_faq

- ✅ All images have alt text
- ✅ No broken images detected
- ✅ Form inputs have labels/placeholders
- **Heading structure:**
  H1: 404
    H2: Page Not Found
      H3: Product
      H3: Support
      H3: Legal


### 🐛 Console Errors

#### page_faq

- [error] `404 Error: User attempted to access non-existent route: /faq`


### 🔗 Broken Links

- ❌ [403] `https://accounts.flipmyera.com/sign-up` (text: "Sign up")

### 🎴 Era Card Interactions



### 🔐 Auth Page Test

**URL:** https://flipmyera.com/auth

**Inputs found:** 2
- `<input type="text" name="identifier" placeholder="Enter your email address">`
- `<input type="password" name="password" placeholder="Enter your password">`

**Buttons found:** 7
- `<button>` "Sign In"
- `<button>` "Sign In"
- `<button>` "Register"
- `<button>` "Continue with Google"
- `<button>` ""
- `<button>` ""
- `<button>` "Continue"

**Form fill test:**
- ✅ email: filled successfully
- ✅ password: filled successfully


### 📸 Screenshots

All screenshots saved to `projects/flip-my-era/screenshots/audit/`

- `homepage_desktop.png` — homepage_desktop
- `auth_desktop.png` — auth_desktop
- `page_plans_desktop.png` — page_plans_desktop
- `page_faq_desktop.png` — page_faq_desktop
- `homepage_mobile.png` — homepage_mobile
- `auth_mobile.png` — auth_mobile
- `page_plans_mobile.png` — page_plans_mobile
- `page_faq_mobile.png` — page_faq_mobile


### 👁️ Visual/UX Observations (from screenshots)

#### Homepage — Desktop
- ✅ Hero section is visually striking — era card carousel with "Showgirl Era" centered looks great
- ✅ "Begin Your Story" CTA is prominent with good contrast (pink/purple gradient)
- ✅ Era selection grid is clean — 7 eras with beautiful imagery and short descriptions
- ⚠️ **Large empty white space** below the era cards section (bottom ~30% of page is blank)
- ⚠️ **No navigation bar** — only a "Sign In" button in top-right. No logo/nav links on homepage header
- ⚠️ **Footer says "© 2025"** — should be 2026 if launching now
- ⚠️ **Heading hierarchy issue**: "Flip My Era" in hero is H3, but "Choose Your Era" is H1. The main page title should be H1
- ℹ️ "Midnights" card sits alone on a 4th row — consider 4+3 grid or 2-column layout for better balance

#### Homepage — Mobile
- ✅ Cards stack nicely in single column
- ✅ Hero carousel adapts well
- ⚠️ Same large blank space issue at bottom
- ⚠️ Cards are quite tall on mobile — lots of scrolling needed (7 full-width cards)

#### Auth Page — Desktop
- ✅ Clean Clerk-powered sign-in form with Google OAuth
- ✅ Sign In / Register tab toggle works
- ✅ Form fields have proper labels ("Email address")
- ⚠️ **Page title is generic** "Flip My Era" — should be "Sign In — FlipMyEra"
- ⚠️ **Duplicate H1 tags**: "FlipMyEra" and "Sign in to FlipMyEra" are both H1

#### /plans Route
- ❌ **Redirects to auth/sign-in** instead of showing pricing — unauthenticated users can't see plans before signing up (bad for conversion)

#### /faq Route
- ❌ **404 page** — FAQ link in footer is broken. The 404 page itself looks nice though (good error UX)

#### /sign-up Route
- ❌ **Returns error** — links to `accounts.flipmyera.com/sign-up` which returns 403

#### General Issues
- ⚠️ **Meta description is "Lovable Generated Project"** on ALL pages — this is a placeholder and will look terrible in Google search results
- ⚠️ **OG image is a relative path** (`/og-image.png`) — should be absolute URL for social sharing
- ⚠️ **No favicon visible** in screenshots (hard to tell, but worth verifying)
- ⚠️ **No loading states visible** — when era cards are clicked, unclear what happens for unauthenticated users
- ⚠️ **Era cards don't appear to navigate anywhere** — the audit couldn't detect click handlers (likely requires auth)

---

## 🎯 Prioritized Recommendations

### 🔴 Critical (Fix Before Launch)
1. **Fix meta description** — "Lovable Generated Project" → real description on ALL pages
2. **Fix /faq route** — footer links to a 404
3. **Fix /sign-up link** — returns 403 from Clerk subdomain
4. **Fix OG image** — use absolute URL (`https://flipmyera.com/og-image.png`)
5. **Add og:title** to all pages

### 🟡 Important
6. **Fix heading hierarchy** — homepage hero should be H1, not H3
7. **Remove duplicate H1** on auth page
8. **Show /plans to unauthenticated users** — let people see pricing before signing up
9. **Optimize homepage load time** (4.88s → target <3s)
10. **Update copyright year** to 2026
11. **Add unique page titles** (e.g., "Sign In — FlipMyEra", "Choose Your Era — FlipMyEra")

### 🟢 Nice to Have
12. **Add canonical URLs** to all pages
13. **Remove blank space** at bottom of homepage
14. **Add navigation** to homepage header (logo, links)
15. **Balance era card grid** — 7 cards in 3-col leaves orphan; consider layout adjustment
16. **Add loading/redirect feedback** when clicking era cards while unauthenticated