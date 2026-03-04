# TODO-472: Welcome Email Sequence via Resend (3-step nurture)

**Priority:** P1 (High)
**Effort:** M (2 hours)
**Repo:** signalhaus-website
**Status:** pending
**Depends on:** TODO-469

## Problem

After contact form submit, leads receive one email confirmation but no follow-up nurture. A 3-step sequence would increase conversion from inquiry → booked call.

## Solution

Use Resend's `scheduledAt` field to queue 3 emails:
1. **Immediate**: Thank you + Calendly link + what to expect
2. **Day 2**: Relevant case study
3. **Day 5**: ROI calculator link with context

## Agent Prompt

```
Add welcome email sequence to /data/workspace/projects/signalhaus-website/src/app/api/contact/route.ts

1. Create /data/workspace/projects/signalhaus-website/src/lib/email-sequences.ts:

```typescript
const RESEND_API = "https://api.resend.com/emails"

interface SequenceRecipient {
  name: string
  email: string
  company?: string
  budget?: string
}

async function scheduleEmail(
  apiKey: string,
  to: string,
  subject: string,
  html: string,
  scheduledAt?: string
): Promise<void> {
  try {
    await fetch(RESEND_API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        from: "Nathan at SignalHaus <nathan@signalhaus.ai>",
        to: [to],
        subject,
        html,
        ...(scheduledAt ? { scheduled_at: scheduledAt } : {}),
      }),
    })
  } catch {
    // fire-and-forget
  }
}

export async function sendWelcomeSequence(
  apiKey: string,
  recipient: SequenceRecipient
): Promise<void> {
  const { name, email, company } = recipient
  const firstName = name.split(" ")[0]
  const companyNote = company ? ` at ${company}` : ""
  
  // Email 1: Immediate
  await scheduleEmail(
    apiKey,
    email,
    `Thanks for reaching out, ${firstName} — here's what happens next`,
    `<p>Hi ${firstName},</p>
    <p>Thanks for getting in touch about AI automation${companyNote}. I've received your message and will follow up within 24 hours.</p>
    <p>In the meantime, you can <a href="https://calendly.com/signalhaus/consultation">book a free 30-min consultation directly here</a>.</p>
    <p>Looking forward to learning about your workflow challenges.</p>
    <p>— Nathan<br/>SignalHaus AI</p>`
  )
  
  // Email 2: Day 2 — Case study
  const day2 = new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString()
  await scheduleEmail(
    apiKey,
    email,
    `How we cut compliance review time by 40% — a real example`,
    `<p>Hi ${firstName},</p>
    <p>While you're evaluating whether SignalHaus is the right fit, here's a quick case study:</p>
    <p><strong>Client:</strong> Enterprise wealth management firm<br/>
    <strong>Challenge:</strong> Manual compliance review across 10,000+ client communications<br/>
    <strong>Solution:</strong> AI agent that classifies, flags, and routes compliance items<br/>
    <strong>Result:</strong> 40% reduction in review time, 0 compliance misses in 6 months</p>
    <p><a href="https://signalhaus.ai/case-studies">Read more case studies →</a></p>
    <p>— Nathan</p>`,
    day2
  )
  
  // Email 3: Day 5 — ROI calculator
  const day5 = new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString()
  await scheduleEmail(
    apiKey,
    email,
    `${firstName}, what's your automation ROI potential?`,
    `<p>Hi ${firstName},</p>
    <p>Before our call, it's worth quantifying what AI automation could be worth for your team.</p>
    <p>I built a quick ROI calculator — takes 2 minutes:</p>
    <p><a href="https://signalhaus.ai/roi-calculator" style="background:#6366f1;color:white;padding:12px 24px;border-radius:6px;text-decoration:none;display:inline-block;">Calculate Your ROI →</a></p>
    <p>Most clients find $200K–$2M in annual workflow savings. Curious what your number is?</p>
    <p>— Nathan</p>`,
    day5
  )
}
```

2. In route.ts, after Resend email success, call the sequence:
```typescript
const { sendWelcomeSequence } = await import("@/lib/email-sequences")
sendWelcomeSequence(RESEND_API_KEY!, { name, email, company, budget }).catch(() => {})
```

3. Run: cd /data/workspace/projects/signalhaus-website && npx tsc --noEmit
```

## Acceptance Criteria
- [ ] 3 emails scheduled: immediate, day 2, day 5
- [ ] Sequence failure does NOT block contact form success response
- [ ] Uses Resend `scheduled_at` for delays
- [ ] TypeScript compiles clean
