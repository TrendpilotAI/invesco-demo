# Fix SignalHaus Contact Form Backend

**Priority:** CRITICAL  
**Effort:** 2 hours  
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Problem
The contact form at `/contact` has `onSubmit` that only calls `setSubmitted(true)` — no data is ever sent anywhere. Every lead is silently dropped.

## Task
Create a Next.js API route that sends contact form submissions to Nathan via email (Resend API) and optionally posts to Slack/n8n webhook.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/:

1. Create src/app/api/contact/route.ts:
   - POST handler accepting { name, email, company, budget, message }
   - Use Resend API (npm install resend) to send email to nathan@signalhaus.ai
   - Email subject: "New Lead: {name} from {company}"
   - Return { success: true } or { error: message }

2. Update src/app/contact/page.tsx form onSubmit to:
   - Call fetch('/api/contact', { method: 'POST', body: JSON.stringify(formData) })
   - Show loading state during submission
   - Handle errors (show error message if API fails)
   - Keep success state on 200 response

3. Add RESEND_API_KEY to .env.example
4. Add basic rate limiting: check X-Forwarded-For, reject if >3 requests/hour from same IP

Environment variable needed: RESEND_API_KEY
Resend docs: https://resend.com/docs/send-with-nextjs
```

## Acceptance Criteria
- [ ] Form submission sends email to Nathan
- [ ] Success state shown after real API call
- [ ] Error state shown if API fails
- [ ] `.env.example` documents RESEND_API_KEY
- [ ] Rate limiting prevents spam
