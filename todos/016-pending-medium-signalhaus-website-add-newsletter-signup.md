---
status: pending
priority: p2
issue_id: "016"
tags: [nextjs, newsletter, resend, email-marketing, signalhaus-website]
dependencies: ["010"]
---

# Add Newsletter Signup ("The Signal")

## Problem Statement

The site has no email capture mechanism for visitors who aren't ready to book a call or contact immediately. Without a newsletter, early-funnel prospects leave and are never heard from again. A bi-weekly AI insights newsletter ("The Signal") builds an owned audience, keeps leads warm, and establishes Nathan as a thought leader — all compounding assets for the business.

## Findings

- No email capture form or CTA anywhere on the site
- No newsletter-related code or dependencies
- Footer and homepage both have space for a newsletter CTA section
- BRAINSTORM.md Section 1.F: rates this P2/MED/S effort
- TODO 010 installs Resend — newsletter subscribers can be added to a Resend Audience
- Resend Audiences feature handles subscriber management (free tier: unlimited contacts)

## Proposed Solutions

### Option 1: Resend Audience + inline API route (Recommended)

**Approach:** Add a newsletter signup form (name + email) that POSTs to `/api/newsletter`. The API route adds the subscriber to a Resend Audience. Use the Resend SDK already installed in TODO 010.

**Pros:**
- Zero additional dependencies (Resend already installed)
- Resend Audiences handles unsubscribe, list management
- Consistent architecture with contact form

**Cons:**
- Requires creating a Resend Audience and storing its ID in env vars

**Effort:** 2-3 hours

**Risk:** Low

---

### Option 2: ConvertKit / Mailchimp

**Approach:** Use a third-party ESP's API to capture subscribers.

**Pros:**
- More powerful email marketing automation
- Better visual email builder

**Cons:**
- Additional service account + API key
- Adds complexity when Resend already provides this

**Effort:** 3-4 hours

**Risk:** Low

---

## Recommended Action

Implement Option 1 (Resend Audience). No new services needed. Place the newsletter signup in two locations:
1. **Footer** — always visible on every page
2. **Homepage** — dedicated section between Testimonials and final CTA

## Technical Details

**Files to create:**
- `src/app/api/newsletter/route.ts` — API route for subscriber capture
- `src/components/NewsletterSignup.tsx` — reusable signup component

**Files to modify:**
- `src/components/Footer.tsx` — add `<NewsletterSignup />` in footer
- `src/app/page.tsx` — add newsletter section on homepage
- `.env.example` — add `RESEND_AUDIENCE_ID`

**API route:**
```typescript
// src/app/api/newsletter/route.ts
import { Resend } from 'resend';
import { NextRequest, NextResponse } from 'next/server';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: NextRequest) {
  const { email, name, honeypot } = await request.json();

  if (honeypot) return NextResponse.json({ success: true });
  if (!email || !email.includes('@')) {
    return NextResponse.json({ error: 'Valid email required' }, { status: 400 });
  }

  try {
    await resend.contacts.create({
      email,
      firstName: name?.split(' ')[0] || '',
      lastName: name?.split(' ').slice(1).join(' ') || '',
      audienceId: process.env.RESEND_AUDIENCE_ID!,
      unsubscribed: false,
    });

    // Welcome email
    await resend.emails.send({
      from: 'Nathan at SignalHaus <nathan@signalhaus.ai>',
      to: [email],
      subject: 'Welcome to The Signal ⚡',
      html: `
        <p>Hi${name ? ` ${name.split(' ')[0]}` : ''},</p>
        <p>You're in. Welcome to <strong>The Signal</strong> — bi-weekly AI insights for enterprise leaders serious about automation.</p>
        <p>Expect: case studies, frameworks, and the occasional contrarian take on where AI is actually going.</p>
        <p>First issue coming soon.</p>
        <p>— Nathan</p>
        <p><a href="https://www.signalhaus.ai">signalhaus.ai</a></p>
      `,
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Newsletter signup error:', error);
    return NextResponse.json({ error: 'Failed to subscribe' }, { status: 500 });
  }
}
```

**Reusable component:**
```tsx
// src/components/NewsletterSignup.tsx
"use client";
import { useState } from 'react';

interface Props {
  variant?: 'inline' | 'section';
}

export default function NewsletterSignup({ variant = 'section' }: Props) {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');

    try {
      const res = await fetch('/api/newsletter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, name }),
      });

      if (!res.ok) throw new Error();
      setStatus('success');
    } catch {
      setStatus('error');
    }
  };

  if (variant === 'section') {
    return (
      <section className="py-24 px-6">
        <div className="max-w-2xl mx-auto text-center">
          <p className="text-indigo-400 font-semibold text-sm uppercase tracking-wider mb-3">The Signal</p>
          <h2 className="text-4xl font-bold mb-4">AI Insights for Enterprise Leaders</h2>
          <p className="text-gray-400 text-lg mb-10">
            Bi-weekly: case studies, automation frameworks, and what's actually working in enterprise AI. No fluff.
          </p>
          {status === 'success' ? (
            <div className="p-6 bg-gray-900 rounded-2xl border border-gray-800">
              <span className="text-3xl mb-2 block">⚡</span>
              <p className="font-semibold">You're in. Check your inbox for a welcome note.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="Your name"
                className="flex-1 px-4 py-3 bg-gray-900 border border-gray-800 rounded-xl focus:border-indigo-500 focus:outline-none transition"
              />
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="you@company.com"
                required
                className="flex-1 px-4 py-3 bg-gray-900 border border-gray-800 rounded-xl focus:border-indigo-500 focus:outline-none transition"
              />
              <button
                type="submit"
                disabled={status === 'loading'}
                className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold transition disabled:opacity-50 whitespace-nowrap"
              >
                {status === 'loading' ? 'Subscribing...' : 'Subscribe Free'}
              </button>
            </form>
          )}
          {status === 'error' && (
            <p className="text-red-400 text-sm mt-3">Something went wrong. Please try again.</p>
          )}
        </div>
      </section>
    );
  }

  // Inline/footer variant
  return (
    <div>
      <p className="font-semibold mb-1">The Signal Newsletter</p>
      <p className="text-gray-500 text-sm mb-3">Bi-weekly AI insights. No spam.</p>
      {status === 'success' ? (
        <p className="text-indigo-400 text-sm">✓ You're subscribed!</p>
      ) : (
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="your@email.com"
            required
            className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm focus:border-indigo-500 focus:outline-none transition"
          />
          <button
            type="submit"
            disabled={status === 'loading'}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-sm font-medium transition disabled:opacity-50"
          >
            {status === 'loading' ? '...' : 'Join'}
          </button>
        </form>
      )}
    </div>
  );
}
```

**Environment variables to add:**
```
RESEND_AUDIENCE_ID=aud_xxxxxxxxxxxx
```

**Setup steps for Nathan:**
1. Go to Resend Dashboard → Audiences → Create Audience "The Signal"
2. Copy the Audience ID → set as `RESEND_AUDIENCE_ID` in Vercel

## Acceptance Criteria

- [ ] `src/app/api/newsletter/route.ts` creates Resend Audience contacts
- [ ] Welcome email sent to new subscribers
- [ ] `src/components/NewsletterSignup.tsx` created with `section` and `inline` variants
- [ ] Newsletter section added to homepage (between Testimonials and CTA)
- [ ] Inline variant added to Footer
- [ ] `RESEND_AUDIENCE_ID` added to `.env.example`
- [ ] Form shows loading state during submission
- [ ] Form shows success state after subscription
- [ ] Form shows error message on failure
- [ ] Honeypot field present for spam protection
- [ ] No TypeScript errors

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Designed newsletter signup using Resend Audiences (same SDK as TODO 010)
- Created reusable component with section and inline variants
- Added welcome email flow
