# Deploy SignalHaus Website to Vercel

**Priority:** CRITICAL  
**Effort:** 1 hour  
**Repo:** signalhaus-website at /data/workspace/projects/signalhaus-website/

## Problem
The website is complete but not deployed. Every day offline = missed leads.

## Task
Push to GitHub and deploy to Vercel with custom domain signalhaus.ai.

## Steps
1. Push repo to GitHub: `git push origin main` (TrendpilotAI/signalhaus-website)
2. Go to vercel.com/new, import TrendpilotAI/signalhaus-website
3. Framework: Next.js (auto-detected)
4. Add environment variables: RESEND_API_KEY
5. Deploy
6. In Vercel → Settings → Domains: add www.signalhaus.ai
7. Update DNS CNAME: www → cname.vercel-dns.com
8. Verify https://www.signalhaus.ai returns 200

## Dependencies
- 221 (contact form backend) should be done first

## Acceptance Criteria
- [ ] https://www.signalhaus.ai loads correctly
- [ ] Contact form submits successfully in production
- [ ] SSL certificate valid
- [ ] www redirects work
