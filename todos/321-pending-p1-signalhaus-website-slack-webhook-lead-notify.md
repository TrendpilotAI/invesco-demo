# TODO 321 — Slack Webhook Notification on Contact Form Submit

**Priority:** P1 — High  
**Repo:** signalhaus-website  
**Effort:** S (1-2 hours)  
**Dependencies:** TODO 315 (contact API hardened — done ✅)

---

## Description

When someone submits the contact form on signalhaus.ai, Nathan should get an instant Slack notification with the lead details. Currently all notifications go to email only. A Slack ping provides immediate visibility without checking inbox.

---

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/src/app/api/contact/route.ts:

1. Add env var: SLACK_WEBHOOK_URL (Slack incoming webhook URL)

2. After successful Resend email send, fire a Slack notification:
   - If SLACK_WEBHOOK_URL is set, POST to it with a formatted message
   - Fire-and-forget (don't await or fail the request if Slack fails)
   - Message format:
     ```
     🔔 *New SignalHaus Lead*
     *Name:* {name}
     *Email:* {email}
     *Company:* {company || 'N/A'}
     *Budget:* {budget || 'Not specified'}
     *Message:* {first 200 chars of message}
     ```

3. Add SLACK_WEBHOOK_URL to .env.example and .env.local.example

4. The Slack call should be wrapped in try/catch and logged but never block the response.

Sample implementation:
```ts
// Fire-and-forget Slack notification
if (process.env.SLACK_WEBHOOK_URL) {
  fetch(process.env.SLACK_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `🔔 *New SignalHaus Lead*\n*Name:* ${name}\n*Email:* ${email}\n*Company:* ${company || 'N/A'}\n*Budget:* ${budget || 'Not specified'}\n*Message:* ${message.slice(0, 200)}${message.length > 200 ? '...' : ''}`
    })
  }).catch(e => console.error('Slack notify failed:', e))
}
```
```

---

## Acceptance Criteria
- [ ] SLACK_WEBHOOK_URL added to .env.example
- [ ] Slack notification fires after successful email send
- [ ] Slack failure does NOT fail the contact form request
- [ ] Message includes name, email, company, budget, and truncated message
- [ ] `yarn build` passes
