# INV-005 + INV-006 — Done ✅

**Completed:** 2026-03-08  
**Commit:** `23e8bff` → `main` on `TrendpilotAI/invesco-demo`

---

## INV-005: PostHog Analytics ✅

**Files changed:**
- `src/analytics.ts` — New PostHog analytics module
- `src/Root.tsx` — Calls `initPostHog()` + `trackPageView()` on load
- `src/InvescoDemoVideo.tsx` — Adds `SceneTracker` component (fires `scene_view` on frame 0 per scene)
- `.env.example` — Documents `NEXT_PUBLIC_POSTHOG_KEY` env var

**Events tracked:**
| Event | Function | Trigger |
|---|---|---|
| `demo_loaded` | auto on init | PostHog loads |
| `$pageview` | `trackPageView()` | Root loads |
| `scene_view` | `trackSceneView()` | Each scene renders |
| `view_meeting_brief` | `trackViewMeetingBrief()` | Call from scene component |
| `run_signal` | `trackRunSignal()` | Call from scene component |
| `push_to_salesforce` | `trackPushToSalesforce()` | Call from scene component |
| `ask_the_data` | `trackAskTheData()` | Call from scene component |

**PostHog Key:** `NEXT_PUBLIC_POSTHOG_KEY` env var (fallback: `phc_demo_invesco`)  
**Note:** Scene components can import tracking helpers from `./InvescoDemoVideo` to fire events at specific interaction points.

---

## INV-006: CVE Fix ✅

**Result:** `pnpm audit` → **No known vulnerabilities found**

**Note:** The repo is a Remotion video rendering project (not a Next.js app). `express-rate-limit` is not a dependency. All current dependencies are clean.

---

## Notes for Next Sprint
- Wire `trackViewMeetingBrief()`, `trackRunSignal()`, `trackPushToSalesforce()`, `trackAskTheData()` into specific ScreenScene interaction points once UI interactions are added
- Replace `phc_demo_invesco` placeholder key with real PostHog project API key in production env
