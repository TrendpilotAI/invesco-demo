# TODO-446: Case Study PDF Downloads (Gated Lead Capture)

**Repo:** signalhaus-website  
**Priority:** P2 (Lead Gen)  
**Effort:** M (~3 hours)  
**Status:** pending

## Description
Case studies on the site are text-only. Converting 1-2 into downloadable PDFs behind an email gate creates high-intent lead capture. Enterprise buyers love case study PDFs for internal sharing. Use Resend to deliver the PDF link after email capture.

## Acceptance Criteria
- [ ] Case studies page has "Download Full Case Study (PDF)" CTA for 1-2 studies
- [ ] Clicking opens a modal with name + email form
- [ ] On submit: Resend sends email with PDF link or attachment
- [ ] Lead email captured and forwarded to Nathan via existing Slack webhook
- [ ] PDF hosted in /public/downloads/ or served from a CDN URL
- [ ] Form has same rate limiting as contact form

## Coding Prompt
```
1. Create /data/workspace/projects/signalhaus-website/src/components/PDFDownloadModal.tsx
   - Modal with name + email fields
   - Submit → POST /api/download-case-study
   - Shows success message after submit

2. Create /data/workspace/projects/signalhaus-website/src/app/api/download-case-study/route.ts
   - Validate name (required, max 100) + email (required, valid format)
   - Rate limit (3 downloads per IP per hour)
   - Send Resend email with PDF download link
   - Fire Slack webhook with lead details (name, email, which case study)
   - Return 200 on success

3. Add "Download PDF" button to case studies in src/app/case-studies/page.tsx
   - Opens PDFDownloadModal
   - Pass case study title as prop

4. Create placeholder PDF or link to Google Drive URL for now.
   Store PDF URL in NEXT_PUBLIC_CASE_STUDY_PDF_URL env var.
```
