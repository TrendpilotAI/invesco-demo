# INV-001 Done — Salesforce Chrome Wrapper around Meeting Brief

**Completed:** 2026-03-08  
**Branch:** main (source) + gh-pages (deployed)  
**File modified:** `projects/invesco-retention/demo-app/src/app/salesforce/page.tsx`

---

## What Was Done

Enhanced the existing `/salesforce` page in the `demo-app` Next.js project with a full **Salesforce Lightning record page chrome wrapper** around the Meeting Brief / Meeting Prep view.

### Components Added

#### 1. `SFGlobalNav` — SF Lightning Global Navigation Bar
- Waffle/app launcher icon (9-dot grid)
- Salesforce cloud logo + "ForwardLane / Sales Cloud" brand
- Hidden global search bar (desktop only)
- App nav tabs: Contacts (active), Accounts, Opportunities, Reports, Dashboards
- Utility icons: bell (notifications), help (?), user avatar (JM initials)
- Advisor selector dropdown for demo switching
- Agentforce badge

#### 2. `SFBreadcrumb` — Breadcrumb Trail
- Home (with home icon) › Contacts › [Advisor Name]
- Truncates long names (max-w-48)

#### 3. `SFRecordHeader` — Highlight Panel / Record Header
- SF Avatar + advisor name (h1) + title
- Firm pill, Channel pill, AUM badge (green), YoY growth badge (green/red)
- Quick stats grid (Phone, Region, Last Contact, Opp. Score)
- Action button row: **Meeting Brief** (primary), Email, Call, Log to SF / Logged ✓
- "More actions" kebab button
- Tab navigation: Details, Related, Activity, Signal Studio, News

#### 4. `SFSideRail` — SF Record Fields Panel (right column)
- 18 standard SF record fields:
  - Account Name, Channel, Region, Office Location, Certifications, Practice Focus, AUM, AUM Growth YoY, Net Flows, Client Count, Avg Client AUM, Revenue (Annual), Invesco Wallet %, Relationship Mgr, Last Contact, Phone, Email, Office Address
- Edit button header

### Layout Change
- **Before:** 2-column (Contact Record | Signal Studio Brief)
- **After:** 3-column (Contact Record | Signal Studio Meeting Brief | SF Side Rail)

### SF Color Scheme
- Primary blue: `#0176D3`
- Dark navy: `#032D60`
- Background gray: `#F3F3F3`
- Success green: `#2E844A`
- Error red: `#EA001E`
- Warning orange: `#FE9339`

---

## Deployment

1. Built with `NODE_ENV=production npm run build` → `out/` directory
2. `out/` contents copied to `TrendpilotAI/invesco-demo` gh-pages branch
3. Pushed to `gh-pages` branch → GitHub Pages auto-deploys
4. Source committed + force-pushed to `main` branch

**Live URL:** https://trendpilotai.github.io/invesco-demo/salesforce

---

## Files Changed
- `projects/invesco-retention/demo-app/src/app/salesforce/page.tsx` — complete rewrite with SF chrome
