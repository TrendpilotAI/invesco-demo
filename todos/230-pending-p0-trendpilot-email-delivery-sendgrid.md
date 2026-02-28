# TODO: Trendpilot — Real Email Delivery via Resend/SendGrid

**Priority:** P0 — Product cannot function without this  
**Repo:** /data/workspace/projects/Trendpilot/  
**Effort:** 2-3 days  
**Dependencies:** 229-p0-supabase-migration (subscribers in DB), RESEND_API_KEY or SENDGRID_API_KEY

## Description
Email delivery is mocked. Trendpilot is a newsletter platform — it must actually send newsletters. Integrate Resend (recommended: simpler API, great developer UX) or SendGrid.

## Coding Prompt (Autonomous Execution)
```
In /data/workspace/projects/Trendpilot/:

1. Install: npm install resend
   (or @sendgrid/mail if preferred)

2. Create src/services/email/sender.ts:
   - Function: sendNewsletter(newsletter: NewsletterDraft, subscribers: Subscriber[]): Promise<SendResult>
   - Batch sends using Resend bulk API (max 100/batch)
   - Tracks sent/failed counts
   - Respects unsubscribe status

3. Create src/services/email/templates.ts:
   - HTML template for newsletter with: header, topic sections, footer with unsubscribe link
   - Text fallback version
   - Responsive CSS (mobile-first)
   - Support for custom branding (tenant theming)

4. Update src/services/scheduler/index.ts:
   - After AI writing pipeline: send generated newsletter to all active subscribers
   - Log send results to Supabase (newsletters table: sent_at, recipient_count, open_rate placeholder)

5. Add API routes:
   - POST /api/newsletters/:id/send — trigger manual send
   - POST /api/unsubscribe/:token — unsubscribe link handler
   - GET /api/newsletters/:id/stats — delivery stats

6. Add to .env.example: RESEND_API_KEY=

7. Tests in tests/email/:
   - sender.test.ts (mock Resend API)
   - templates.test.ts (snapshot HTML output)

Use Resend (resend.com) — free tier: 3000 emails/month.
```

## Acceptance Criteria
- [ ] Newsletter sends to real email addresses
- [ ] Unsubscribe link works end-to-end
- [ ] Batching handles 1000+ subscribers without timeout
- [ ] Send results logged to DB
- [ ] HTML template renders correctly on mobile
