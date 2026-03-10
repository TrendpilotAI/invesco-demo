#!/usr/bin/env python3
"""Push FlipMyEra tickets to GitHub Issues."""
import json
import requests
import time
import os

GH_TOKEN = os.environ.get("GH_TOKEN", "")
REPO = "TrendpilotAI/flip-my-era"
HEADERS = {"Authorization": f"token {GH_TOKEN}", "Content-Type": "application/json"}
MILESTONE = 1  # Production Launch

def create_issue(title, body, labels=None):
    resp = requests.post(
        f"https://api.github.com/repos/{REPO}/issues",
        headers=HEADERS,
        json={"title": title, "body": body, "labels": labels or [], "milestone": MILESTONE}
    )
    if resp.status_code in (200, 201):
        d = resp.json()
        print(f"  ✅ #{d['number']}: {title}")
        return d["number"]
    else:
        print(f"  ❌ FAILED: {title} ({resp.status_code}: {resp.text[:100]})")
        return None
    # Rate limit
    time.sleep(0.5)

print("🎯 FlipMyEra — GitHub Issues\n")

# Phase 1 (already done as PRs, create tracking issues)
print("Phase 1: Stop-Ship (PRs already merged/open)")
create_issue(
    "[Phase 1] create-checkout: Fix price mapping + CORS + API version",
    "**Status: PR merged to main**\n\n- Server-side price ID resolution\n- Wildcard CORS → origin allowlist\n- Stripe API version fixed\n- Supabase auth.getUser() verification added\n- Idempotency keys passed to Stripe",
    labels=["billing", "security"]
)

create_issue(
    "[Phase 1] groq-storyline: Add pre_authorized_transaction_id support",
    "**Status: PR merged to main**\n\n- Prevents potential double-charging when called after credits-validate\n- Direct calls still deduct credits normally",
    labels=["billing"]
)

create_issue(
    "[Phase 1] stripe-webhook: Remove CORS headers",
    "**Status: PR merged to main**\n\nServer-to-server endpoint doesn't need CORS.",
    labels=["security"]
)

# Phase 2
print("\nPhase 2: Revenue & Retention")
create_issue(
    "[Phase 2] Wire Gallery to real Supabase data",
    "**PR #78** `fix/gallery-and-dead-code`\n\n- Replace SAMPLE_EBOOKS mock with real Supabase query\n- Loading skeletons, empty state, pagination\n- Delete billing.ts (283 dead lines)\n\n**Tests:** 471 passing ✅",
    labels=["P1:high"]
)

create_issue(
    "[Phase 2] BetterAuth end-to-end migration",
    "**PR #83** `feat/better-auth-migration`\n\n- BetterAuth server config with Postgres\n- Netlify Function catch-all for /api/auth/*\n- Drop-in AuthProvider (same interface, zero consumer changes)\n- SQL migration for BetterAuth tables\n- Dual-verification in edge functions (BetterAuth + legacy Supabase JWT)\n\n**Tests:** 568 passing ✅\n\n**Deploy steps:**\n1. Set Netlify env vars: DATABASE_URL, BETTER_AUTH_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET\n2. Run SQL migration in Supabase\n3. Update Google OAuth redirect URLs",
    labels=["auth", "P1:high"]
)

# Phase 3
print("\nPhase 3: Bundle Optimization")
create_issue(
    "[Phase 3] Remove OpenTelemetry + unused Radix + dedup modules",
    "**PR #80** `fix/bundle-optimization`\n\n- 13 OTel packages removed (~200KB)\n- 5 Radix UI packages removed (~50KB)\n- creator/ merged into creators/\n- ErrorBoundary added to all routes\n- Total: -1,704 lines\n\n**Tests:** 471 passing ✅",
    labels=["bundle", "P2:medium"]
)

# Phase 4
print("\nPhase 4: Testing")
create_issue(
    "[Phase 4] Edge function tests for payment critical path",
    "**PR #81** `fix/edge-function-tests`\n\n- create-checkout.test.ts: 34 tests\n- credits-validate.test.ts: 30 tests\n- groq-storyline.test.ts: 33 tests\n- Total: 97 new tests, all passing ✅",
    labels=["testing", "P1:high"]
)

# Phase 5
print("\nPhase 5: SEO & Analytics")
create_issue(
    "[Phase 5] PostHog funnel events + SEO enhancements",
    "**PR #82** `fix/seo-analytics-polish`\n\n- 5 PostHog funnel events wired\n- SEO keywords + structured data dates on 10 pages\n- RSS feed link in index.html\n- logo.png placeholder\n\n**Tests:** 471 passing ✅",
    labels=["seo", "P2:medium"]
)

# Post-launch
print("\nPost-Launch: Growth")
create_issue(
    "[Growth] Referral credits — 'Give a story, get a story'",
    "Viral loop for teen audience. User shares invite link → friend signs up → both get credits.\n\nHighest ROI growth feature per brainstorm doc.",
    labels=["P2:medium"]
)

create_issue(
    "[Growth] Social sharing cards — TikTok/IG format",
    "Generate 1080x1920 sharing cards for ebook covers. Public story URLs with OG tags.\n\nThis is how organic growth happens — teen users share on TikTok/IG.",
    labels=["P2:medium"]
)

create_issue(
    "[Growth] A/B test pricing — $2.99 vs $4.99 per ebook",
    "Set up PostHog feature flags to A/B test credit pack pricing. Let data decide.",
    labels=["P2:medium"]
)

create_issue(
    "[Growth] Complete all 13 Taylor Swift era templates",
    "Content completeness for superfans. Each era needs a prompt template with era-specific theming.",
    labels=["P2:medium"]
)

create_issue(
    "[Growth] Public story pages with SEO",
    "flipmyera.com/story/{slug} — shareable public pages with proper OG tags and JSON-LD.\n\nDrives organic long-tail traffic from Google.",
    labels=["seo", "P2:medium"]
)

# Stripe setup
print("\nPre-Launch: Stripe")
create_issue(
    "[Pre-Launch] Create real Stripe products and configure price IDs",
    "**Must do before launch:**\n\n1. Create products in Stripe Dashboard:\n   - 3 credit packs: Single ($2.99/5cr), Album ($9.99/20cr), Tour ($19.99/50cr)\n   - 2 subscription tiers: Speak Now ($4.99/mo), Midnights ($9.99/mo)\n   - 2 annual tiers\n2. Set `credits` in price metadata\n3. Update edge function price ID maps\n4. Set Netlify env vars\n5. Configure webhook endpoint in Stripe Dashboard",
    labels=["billing", "P0:stop-ship"]
)

create_issue(
    "[Pre-Launch] Fix Dependabot vulnerabilities (1 high, 2 moderate)",
    "GitHub flagged 3 vulnerabilities on default branch. Review and fix before launch.\nhttps://github.com/TrendpilotAI/flip-my-era/security/dependabot",
    labels=["security", "P1:high"]
)

print(f"\n{'='*50}")
print("Done! All FlipMyEra issues pushed to GitHub")
