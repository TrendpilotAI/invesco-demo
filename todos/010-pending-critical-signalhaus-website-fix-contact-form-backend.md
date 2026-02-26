---
status: pending
priority: p1
issue_id: "010"
tags: [nextjs, resend, api, contact-form, signalhaus-website]
dependencies: []
---

# Fix Contact Form Backend — Wire Resend API

## Problem Statement

The contact form at `src/app/contact/page.tsx` is completely broken as a lead-capture tool. When a user submits the form, `onSubmit` calls `setSubmitted(true)` and nothing else — no email is ever sent, no lead is ever captured. This is a **revenue-critical bug**: prospects who fill out the form believe they've made contact but Nathan receives nothing.

**Files affected:**
- `src/app/contact/page.tsx` — form component with broken submit handler
- `src/app/api/contact/route.ts` — **does not exist** (must be created)
- `package.json` — needs `resend` dependency added

## Findings

- `onSubmit` handler (line ~31): `e.preventDefault(); setSubmitted(true);` — no fetch, no API call
- No `src/app/api/` directory exists at all
- No environment variables for email delivery configured
- No `.env.example` file exists
- Form captures: name, email, company, budget, message — all valuable lead data
- `"use client"` directive is present (correctly needed for form state, but metadata is broken — see TODO 017)

## Proposed Solutions

### Option 1: Resend API Route Handler (Recommended)

**Approach:** Create `src/app/api/contact/route.ts` as a Next.js Route Handler that accepts POST requests, validates input, and sends email via Resend SDK.

**Pros:**
- Resend has excellent deliverability, generous free tier (3,000 emails/month)
- Full control over email template
- Can store leads in Resend Audience for newsletter later
- Native Next.js App Router pattern

**Cons:**
- Requires `RESEND_API_KEY` env var in Vercel dashboard

**Effort:** 2-3 hours

**Risk:** Low

---

### Option 2: Formspree (Zero-backend)

**Approach:** Replace form action with Formspree endpoint. No backend code needed.

**Pros:**
- No API route to write
- Works without any server code

**Cons:**
- Less control over email format
- Paid tier needed for custom `from` address
- Harder to extend (CRM integration, etc.)

**Effort:** 30 minutes

**Risk:** Very Low

---

## Recommended Action

Implement Option 1 (Resend API Route Handler). This is the foundation for all future email features (newsletter, auto-responder, CRM integration). Steps:

1. `npm install resend` in the project
2. Create `src/app/api/contact/route.ts`
3. Update `src/app/contact/page.tsx` form to POST to `/api/contact`
4. Create `.env.example` with required vars
5. Add spam protection (honeypot field)

## Technical Details

**Affected files:**
- `src/app/contact/page.tsx` — update `onSubmit` to fetch `/api/contact`
- `src/app/api/contact/route.ts` — **create new file**
- `package.json` — add `resend` dependency
- `.env.example` — **create new file**
- `.env.local` — add actual keys (not committed)

**New API route structure:**
```typescript
// src/app/api/contact/route.ts
import { Resend } from 'resend';
import { NextRequest, NextResponse } from 'next/server';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: NextRequest) {
  const body = await request.json();
  const { name, email, company, budget, message, honeypot } = body;

  // Spam check
  if (honeypot) {
    return NextResponse.json({ success: true }); // silent fail for bots
  }

  // Validation
  if (!name || !email || !message) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }

  try {
    // Notify Nathan
    await resend.emails.send({
      from: 'SignalHaus Contact <contact@signalhaus.ai>',
      to: [process.env.CONTACT_TO_EMAIL || 'nathan@signalhaus.ai'],
      subject: `New Lead: ${name} from ${company || 'Unknown'} — ${budget || 'Budget TBD'}`,
      html: `
        <h2>New Contact Form Submission</h2>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Company:</strong> ${company || 'Not provided'}</p>
        <p><strong>Budget:</strong> ${budget || 'Not provided'}</p>
        <hr/>
        <p><strong>Message:</strong></p>
        <p>${message}</p>
      `,
      replyTo: email,
    });

    // Auto-reply to prospect
    await resend.emails.send({
      from: 'Nathan at SignalHaus <nathan@signalhaus.ai>',
      to: [email],
      subject: "Got your message — talk soon",
      html: `
        <p>Hi ${name},</p>
        <p>Thanks for reaching out! I've received your message and will be in touch within 24 hours.</p>
        <p>In the meantime, feel free to book a time directly: <a href="https://calendly.com/signalhaus">calendly.com/signalhaus</a></p>
        <p>— Nathan</p>
      `,
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Email send error:', error);
    return NextResponse.json({ error: 'Failed to send message' }, { status: 500 });
  }
}
```

**Updated form onSubmit:**
```typescript
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);

const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  setIsLoading(true);
  setError(null);

  const formData = new FormData(e.currentTarget);
  const data = Object.fromEntries(formData.entries());

  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!res.ok) throw new Error('Failed to send');
    setSubmitted(true);
  } catch {
    setError('Something went wrong. Please try again or email us directly.');
  } finally {
    setIsLoading(false);
  }
};
```

**Add honeypot field to form (hidden, bots fill it, humans don't):**
```html
<input type="text" name="honeypot" style={{display:'none'}} tabIndex={-1} autoComplete="off" />
```

**Environment variables needed:**
```
RESEND_API_KEY=re_xxxxxxxxxxxx
CONTACT_TO_EMAIL=nathan@signalhaus.ai
```

## Resources

- Resend docs: https://resend.com/docs/send-with-nextjs
- Resend free tier: 3,000 emails/month, 100/day
- Next.js Route Handlers: https://nextjs.org/docs/app/building-your-application/routing/route-handlers

## Acceptance Criteria

- [ ] `npm install resend` added to package.json dependencies
- [ ] `src/app/api/contact/route.ts` exists and handles POST requests
- [ ] Form submits via `fetch('/api/contact', { method: 'POST', ... })`
- [ ] Nathan receives notification email on every submission with all lead fields
- [ ] Prospect receives auto-reply email confirming receipt
- [ ] Honeypot field added to form for basic spam protection
- [ ] `.env.example` created with `RESEND_API_KEY` and `CONTACT_TO_EMAIL`
- [ ] Form shows loading state during submission
- [ ] Form shows error message if submission fails (with fallback email link)
- [ ] `setSubmitted(true)` only called after confirmed API success
- [ ] No API keys committed to git

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Reviewed `src/app/contact/page.tsx` — confirmed broken submit handler
- Confirmed no `src/app/api/` directory exists
- Documented Resend integration pattern with full code examples
- Identified honeypot spam protection approach

**Learnings:**
- This is the single highest-ROI fix for the site — zero leads are being captured currently
- Resend is the right choice: free tier sufficient, excellent DX, enables future newsletter
