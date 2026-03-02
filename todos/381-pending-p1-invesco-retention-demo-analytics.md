# TODO-381: Demo Analytics — Track When Invesco Accesses Demo

**Repo:** invesco-retention
**Priority:** P1
**Effort:** S (1-2 hours)
**Status:** pending

## Description
Add lightweight analytics to the demo app to track which routes Brian Kiley's team visits, how long they spend, and get notified when Invesco accesses the demo.

## Acceptance Criteria
- [ ] PostHog or Plausible added to demo-app
- [ ] Page views tracked for all 4 demo routes
- [ ] Telegram notification when demo is accessed (via webhook or PostHog alert)
- [ ] No PII collected

## Coding Prompt
```
Add PostHog analytics to /data/workspace/projects/invesco-retention/demo-app/

1. npm install posthog-js
2. Add PostHog initialization in src/app/layout.tsx
3. Track pageview on each route with route name as property
4. Set up PostHog alert: when /salesforce is visited → send webhook to Telegram
5. Use environment variable NEXT_PUBLIC_POSTHOG_KEY (add to .env.example)
6. Wrap in try/catch so analytics failure never breaks the demo
```

## Dependencies
- Requires PostHog account (free tier sufficient)

## Notes
Sales intelligence: knowing when Invesco accesses the demo link gives Nathan advance notice before follow-up calls.
