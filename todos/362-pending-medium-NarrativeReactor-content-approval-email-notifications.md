# 362 · NarrativeReactor — Content Approval Email Notifications

**Priority:** medium  
**Effort:** M (1–3 days)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

The `contentPipeline` tracks `status: draft | approved | rejected` but there's no notification system. When a new draft is ready for review, send an email to the configured reviewer with a preview and direct approve/reject links. Also notify on publish success/failure.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/:

## Email Service

1. Create src/lib/emailService.ts using Resend (preferred) or Nodemailer as fallback:

Add to .env.example:
  RESEND_API_KEY=re_...
  NOTIFICATION_EMAIL=reviewer@example.com

npm install resend

import { Resend } from 'resend';
const resend = new Resend(process.env.RESEND_API_KEY);

export const emailService = {
  async sendDraftReady(opts: {
    contentId: string;
    title: string;
    preview: string;      // first 500 chars of content
    platform: string;
    cost: number;
    toEmail: string;
  }): Promise<void> {
    const baseUrl = process.env.DASHBOARD_URL || 'http://localhost:3000';
    await resend.emails.send({
      from: 'NarrativeReactor <noreply@narrativereactor.ai>',
      to: opts.toEmail,
      subject: `📝 Draft Ready for Review: ${opts.title}`,
      html: `
        <h2>New Content Draft Ready</h2>
        <p><strong>Platform:</strong> ${opts.platform}</p>
        <p><strong>AI Cost:</strong> $${opts.cost.toFixed(4)}</p>
        <blockquote>${opts.preview}...</blockquote>
        <p>
          <a href="${baseUrl}/api/content/${opts.contentId}/approve?token=TOKEN" style="background:#22c55e;color:#fff;padding:8px 16px;border-radius:4px;text-decoration:none">✅ Approve</a>
          &nbsp;
          <a href="${baseUrl}/api/content/${opts.contentId}/reject?token=TOKEN" style="background:#ef4444;color:#fff;padding:8px 16px;border-radius:4px;text-decoration:none">❌ Reject</a>
        </p>
      `
    });
  },

  async sendPublishResult(opts: {
    contentId: string;
    title: string;
    success: boolean;
    platform: string;
    error?: string;
    toEmail: string;
  }): Promise<void> { /* similar HTML email */ }
};

2. Add one-click approve/reject token system:
   - Generate a short-lived signed token (JWT, 24h expiry) for approve/reject links
   - POST /api/content/:id/approve?token=TOKEN — validates token, updates status
   - POST /api/content/:id/reject?token=TOKEN — validates token, updates status
   - No login required for token-based actions (reviewer may not have dashboard access)

3. Wire notifications into contentPipeline:
   - After status changes to 'draft' → emailService.sendDraftReady()
   - After publish attempt → emailService.sendPublishResult()

4. Add env guard: only send if RESEND_API_KEY and NOTIFICATION_EMAIL are set.
   Log a warning if not configured; don't throw.

5. Add to .env.example:
   RESEND_API_KEY=
   NOTIFICATION_EMAIL=
   DASHBOARD_URL=https://your-domain.com

## Tests

6. tests/unit/emailService.test.ts:
   - Mock Resend client
   - sendDraftReady() calls resend.emails.send with correct subject/to
   - No-op when RESEND_API_KEY not set (no throw)
   - Approve token validates and updates content status
   - Expired token returns 401
```

---

## Dependencies

- `contentPipeline` must persist status to SQLite (completed per TODO.md)
- Resend account or SMTP credentials needed (env-gated)
- #360 multi-tenant: notification email should be per-tenant config

## Acceptance Criteria

- [ ] `emailService.sendDraftReady()` sends correctly formatted email
- [ ] One-click approve/reject links work without dashboard login
- [ ] Tokens expire after 24 hours
- [ ] Notifications only fire if `RESEND_API_KEY` is set (safe no-op otherwise)
- [ ] Unit tests mock Resend and verify call shape
- [ ] `.env.example` documents all new variables
