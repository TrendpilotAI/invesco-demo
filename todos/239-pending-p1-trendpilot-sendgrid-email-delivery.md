# 239 · P1 · Trendpilot — Integrate SendGrid Email Delivery

## Status
pending

## Priority
P1 — core product value (newsletter delivery)

## Description
Replace the mock `SubscriberStore.sendDigest()` with real transactional email delivery via SendGrid. Implement: subscriber confirmation emails (double opt-in), newsletter digest delivery to all active subscribers, and unsubscribe handling via SendGrid webhook or one-click link.

## Dependencies
- TODO #236 (Supabase data store) — subscribers must be in Supabase
- TODO #238 (Auth) — delivery must be triggered by authenticated users
- `SENDGRID_API_KEY` env var
- `FROM_EMAIL` env var (must be a verified SendGrid sender)

## Estimated Effort
1 day

## Coding Prompt

```
You are working on the Trendpilot project at /data/workspace/projects/Trendpilot/.

TASK: Wire real SendGrid email delivery for newsletter digests and subscriber confirmation.

STEP 1 — Install SendGrid:
```bash
npm install @sendgrid/mail
npm install --save-dev @types/sendgrid__mail
```

STEP 2 — Create `src/services/email/sendgrid.ts`:
```ts
import sgMail from '@sendgrid/mail';
import * as db from '@/services/db.js';

sgMail.setApiKey(process.env.SENDGRID_API_KEY!);

const FROM = { email: process.env.FROM_EMAIL ?? 'hello@trendpilot.ai', name: 'Trendpilot' };

export async function sendConfirmation(email: string, confirmUrl: string): Promise<void> {
  await sgMail.send({
    to: email,
    from: FROM,
    subject: 'Confirm your Trendpilot subscription',
    html: `
      <h2>Almost there!</h2>
      <p>Click the link below to confirm your subscription to Trendpilot.</p>
      <a href="${confirmUrl}" style="background:#6366f1;color:white;padding:12px 24px;border-radius:6px;text-decoration:none">
        Confirm Subscription
      </a>
      <p style="color:#666;font-size:12px;margin-top:24px">
        If you didn't request this, you can safely ignore this email.
      </p>
    `,
  });
}

export async function sendNewsletter(
  subject: string,
  htmlContent: string,
  recipientEmails: string[]
): Promise<{ sent: number; failed: number }> {
  if (recipientEmails.length === 0) return { sent: 0, failed: 0 };
  
  // SendGrid batch — max 1000 per call
  const batches = chunkArray(recipientEmails, 1000);
  let sent = 0;
  let failed = 0;

  for (const batch of batches) {
    try {
      await sgMail.sendMultiple({
        to: batch,
        from: FROM,
        subject,
        html: htmlContent,
        trackingSettings: {
          clickTracking: { enable: true },
          openTracking: { enable: true },
        },
      });
      sent += batch.length;
    } catch (err) {
      console.error('[sendgrid] Batch send error:', err);
      failed += batch.length;
    }
  }

  return { sent, failed };
}

export async function sendUnsubscribeConfirmation(email: string): Promise<void> {
  await sgMail.send({
    to: email,
    from: FROM,
    subject: "You've been unsubscribed from Trendpilot",
    html: `<p>You've been successfully unsubscribed. We're sad to see you go!</p>
           <p>If this was a mistake, you can <a href="${process.env.NEXT_PUBLIC_APP_URL}/subscribe">resubscribe here</a>.</p>`,
  });
}

function chunkArray<T>(arr: T[], size: number): T[][] {
  const chunks: T[][] = [];
  for (let i = 0; i < arr.length; i += size) chunks.push(arr.slice(i, i + size));
  return chunks;
}
```

STEP 3 — Update newsletter delivery route in `src/api/index.ts`:
```ts
import { sendNewsletter } from '@/services/email/sendgrid.js';

// POST /api/newsletters/:id/send
app.post('/api/newsletters/:id/send', requireAuth, async (req, res) => {
  const newsletter = await db.newsletters.findById(param(req, 'id'));
  if (!newsletter) return res.status(404).json({ error: 'Newsletter not found' });
  
  const activeSubscribers = await db.subscribers.list({ status: 'active' });
  const emails = activeSubscribers.map(s => s.email);
  
  const result = await sendNewsletter(newsletter.subject, newsletter.html_content, emails);
  
  // Update newsletter status
  await db.newsletters.update(newsletter.id, {
    status: 'sent',
    sent_at: new Date().toISOString(),
    recipient_count: result.sent,
  });
  
  res.json({ success: true, ...result });
});
```

STEP 4 — Subscriber confirmation flow:
```ts
// POST /api/subscribe — public endpoint
app.post('/api/subscribe', async (req, res) => {
  const { email } = req.body;
  
  // Create pending subscriber
  const sub = await db.subscribers.create({
    email,
    status: 'pending',
    subscribed_at: new Date().toISOString(),
  });
  
  // Generate confirmation token (use Supabase auth or a signed JWT)
  const token = Buffer.from(JSON.stringify({ id: sub.id, email })).toString('base64url');
  const confirmUrl = `${process.env.NEXT_PUBLIC_APP_URL}/api/confirm?token=${token}`;
  
  await sendConfirmation(email, confirmUrl);
  res.json({ success: true, message: 'Check your email to confirm your subscription' });
});

// GET /api/confirm?token=...
app.get('/api/confirm', async (req, res) => {
  try {
    const { id } = JSON.parse(Buffer.from(req.query.token as string, 'base64url').toString());
    await db.subscribers.update(id, { status: 'active' });
    res.redirect(`${process.env.NEXT_PUBLIC_APP_URL}?confirmed=true`);
  } catch {
    res.status(400).json({ error: 'Invalid or expired token' });
  }
});
```

STEP 5 — Unsubscribe route:
```ts
// GET /api/unsubscribe?email=...
app.get('/api/unsubscribe', async (req, res) => {
  const email = req.query.email as string;
  const sub = await db.subscribers.findByEmail(email);
  if (sub) {
    await db.subscribers.update(sub.id, { status: 'unsubscribed' });
    await sendUnsubscribeConfirmation(email);
  }
  res.redirect(`${process.env.NEXT_PUBLIC_APP_URL}?unsubscribed=true`);
});
```

STEP 6 — Add unsubscribe link to all newsletter HTML templates:
In the email HTML footer, add:
`<a href="${APP_URL}/api/unsubscribe?email={{email}}">Unsubscribe</a>`
```

## Acceptance Criteria
- [ ] `POST /api/subscribe` with a real email triggers a confirmation email via SendGrid
- [ ] Clicking confirmation link sets subscriber status to 'active' in Supabase
- [ ] `POST /api/newsletters/:id/send` delivers HTML email to all active subscribers
- [ ] SendGrid dashboard shows emails sent
- [ ] `GET /api/unsubscribe?email=X` sets status to 'unsubscribed' and sends confirmation
- [ ] No crashes when `SENDGRID_API_KEY` is missing (graceful degradation with log warning)
- [ ] Newsletters table updated with `sent_at` and `recipient_count` after send
