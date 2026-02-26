# 🌙 Overnight Task Ideas — Feb 20, 2026

## Ranked by Impact × Feasibility

### 1. 🏥 Kaggle Final Push (CRITICAL — deadline Feb 24)
- Add GOOGLE_API_KEY to Kaggle secrets and verify full 3-agent pipeline runs
- Create consumer-facing notebook (Main Track) with Tracey's story narrative
- Record/generate demo video showing the app in action
- **Impact: 10/10** — $100K prize, 4 days left

### 2. 🎵 FlipMyEra Payment E2E Hardening
- Full Stripe checkout → webhook → credit delivery flow testing
- Test edge cases: failed payments, duplicate webhooks, refunds, subscription upgrades
- Add Playwright E2E tests for the entire purchase flow
- Lighthouse audit and fix to get all scores 90+
- **Impact: 9/10** — this is the revenue blocker

### 3. 📈 Trendpilot Real Data Integration
- Wire up actual data sources (News API, Reddit API, RSS feeds)
- Run the full pipeline: ingest → deduplicate → rank → alert
- Generate first real trend report to prove the concept works end-to-end
- Build 3 sample dashboards with live data
- **Impact: 8/10** — transforms demo into product

### 4. 📝 NarrativeReactor README + Deploy
- Write comprehensive README (the only major project without one)
- Deploy to Railway with proper env config
- Wire the Trendpilot→NarrativeReactor bridge so trends auto-generate content
- First real content generation run through the full pipeline
- **Impact: 8/10** — strategic backbone needs to actually run

### 5. 💼 Invesco Demo Prototype
- Build the Salesforce-embedded meeting prep brief generator
- Synthetic data for 10 Invesco sales scenarios
- Mobile-responsive dashboard showing actionable insights (not reports)
- Record a 3-min demo video targeting Brian Kiley's requirements
- **Impact: 9/10** — $300K/year retention, but 2-3 week window

### 6. 🌐 ForwardLane + SignalHaus Website Deploy
- Import to Vercel, configure custom domains
- Add Google Analytics, structured data, OG images
- Set up forwardlane.com DNS → Vercel (if Nathan has domain access)
- signalhaus.ai is parked — need to activate it
- **Impact: 6/10** — professional web presence, low effort

### 7. 🔧 Fix All CI Pipelines
- FlipMyEra, Second-Opinion, NarrativeReactor, Trendpilot all have CI issues
- Fix every red pipeline to green
- Add Dependabot security fixes across all repos
- Ensure `npm test` passes in every project
- **Impact: 7/10** — foundation for everything else

### 8. 🤖 n8n Viral Video Workflow
- Redeploy n8n (DB should be healthy now after Temporal deletion)
- Import the 47-node viral video workflow
- Configure Blotato API for cross-platform posting
- Test with one sample video generation
- **Impact: 6/10** — content automation, but dependent on n8n health

### 9. 📊 Cross-Project Shared Auth Library
- Extract JWT + Clerk auth into a shared package
- Consistent user model across FlipMyEra, NarrativeReactor, Trendpilot
- SSO between projects (one login, all apps)
- Publish as internal npm package
- **Impact: 7/10** — reduces duplication, enables ecosystem

### 10. 🧪 Second-Opinion Test Coverage Sprint
- Medical app with only 23 tests is risky
- Target: 100+ tests covering all critical paths
- Focus: model inference, FHIR export, PDF generation, demo mode, auth flows
- Add Playwright E2E for the guided demo walkthrough
- **Impact: 8/10** — competition credibility + safety for a medical app

---

## Recommended Overnight Batch Order
1. **Kaggle Final Push** (#1) — highest urgency
2. **FlipMyEra Payment Hardening** (#2) — revenue blocker
3. **Fix All CI** (#7) — unlocks everything
4. **Second-Opinion Tests** (#10) — competition credibility
5. **Trendpilot Real Data** (#3) — product validation
6. **NarrativeReactor Deploy** (#4) — strategic backbone
7-10: Remaining tasks as time allows
