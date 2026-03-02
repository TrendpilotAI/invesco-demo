# TODO-326: Welcome Email Sequence via Resend

**Priority:** P1  
**Effort:** 2 hours  
**Repo:** signalhaus-website  
**Status:** pending  

## Description
After a contact form submission, trigger a 3-email nurture sequence using Resend's `scheduledAt` feature. Keeps SignalHaus top-of-mind while Nathan follows up. No new tools needed — uses the existing Resend integration.

## Email Sequence
1. **Immediate** — "Thanks + what happens next" + Calendly link
2. **Day 2** — Relevant case study or ROI calculator link
3. **Day 5** — "Quick question" follow-up with value prop recap

## Coding Prompt (Agent-Executable)

```
In /data/workspace/projects/signalhaus-website/src/app/api/contact/route.ts:

After the successful Resend email send (after `if (!resp.ok)`), add a function
`scheduleWelcomeSequence(email, name)` that fires 3 Resend emails using scheduledAt:

1. Immediate confirmation to the LEAD (reply to their submission):
   - from: SignalHaus <hello@signalhaus.ai>
   - to: [email]
   - subject: "You're on Nathan's radar — here's what's next"
   - HTML: warm thank-you, Calendly link (https://calendly.com/signalhaus), 
           link to /roi-calculator, expected response time

2. Day 2 (scheduledAt: new Date(Date.now() + 2*24*60*60*1000).toISOString()):
   - subject: "A quick case study you might relate to"
   - HTML: link to /case-studies, highlight the most relevant metric ($50M+ value delivered)

3. Day 5 (scheduledAt: new Date(Date.now() + 5*24*60*60*1000).toISOString()):
   - subject: "Quick question, {{name}}"
   - HTML: one-line value prop + CTA to book a call

Add this as a non-blocking fire-and-forget (like Slack webhook).
Wrap in try/catch, log errors to console only.
Add CALENDLY_URL to env.ts and .env.example.

HTML templates should be clean, minimal, plain-text-friendly.
```

## Acceptance Criteria
- [ ] 3 emails scheduled on successful form submission
- [ ] Does not block main response
- [ ] From address is `hello@signalhaus.ai` (not no-reply)
- [ ] Calendly URL comes from env var
- [ ] Console error logged on failure (never surface to user)

## Dependencies
- Resend API key (already configured)
- TODO-329 (env.ts helper, recommended but not required)
