# TODO #425: Schedule Pilot CTA Webhook Integration

**Priority:** P1 (post-demo)
**Effort:** S (1-2 hours)
**Repo:** invesco-retention
**Source:** BRAINSTORM.md v3, Category 4.3

## Description

Wire the "Schedule Pilot" CTA button in the demo app to POST to a webhook (Zapier/Make.com)
that sends Nathan a Telegram notification when clicked.

If Brian demos the app solo between meetings, Nathan gets a real-time signal.

## Acceptance Criteria
- [ ] "Schedule Pilot" button in demo app sends a webhook POST on click
- [ ] Payload includes: timestamp, referrer URL, advisor context (which advisor was being viewed)
- [ ] Nathan receives a Telegram notification: "🎯 Schedule Pilot clicked — /salesforce?advisor=sarah-chen at 2:34 PM"
- [ ] Button click still opens the pilot proposal PDF/link as before (webhook is fire-and-forget)
- [ ] No backend required — use Make.com or Zapier webhook URL stored in environment variable

## Implementation Prompt

```
1. Create a Zapier/Make.com webhook that sends a Telegram message to Nathan (id: 8003607839)
2. In /data/workspace/projects/invesco-retention/demo-app/src/app/salesforce/page.tsx:
   - Find the "Schedule Pilot" / "Start Pilot" CTA button
   - Add onClick handler that calls: fetch(process.env.NEXT_PUBLIC_PILOT_WEBHOOK_URL, { method: 'POST', body: JSON.stringify({ event: 'pilot_cta_clicked', advisor: currentAdvisor?.name, timestamp: new Date().toISOString(), url: window.location.href }) })
   - Use fire-and-forget (no await, wrapped in try/catch)
3. Add NEXT_PUBLIC_PILOT_WEBHOOK_URL to .env.local and GitHub Pages deploy config
4. Test by clicking the button and confirming Telegram notification arrives
```

## Dependencies
- None

## Demo Impact
MEDIUM — Closes the loop if Brian explores solo.
