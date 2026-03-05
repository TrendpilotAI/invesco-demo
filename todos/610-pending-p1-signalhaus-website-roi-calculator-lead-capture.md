# TODO-610: ROI Calculator Email Lead Capture

**Repo:** signalhaus-website  
**Priority:** P1  
**Effort:** S (2-3 hours)  
**Status:** pending

## Description
The ROI Calculator at `/roi-calculator` computes value but doesn't capture leads. After showing results, prompt the user to "Email me this ROI report" — high-intent lead capture moment.

## Tasks
1. After calculation results display, show an email capture form
2. On submit: send personalized Resend email with their ROI numbers
3. Also add contact to Resend Audience (newsletter) with opt-in checkbox
4. Track "roi_lead_captured" event in GA4

## Coding Prompt
In `src/components/ROICalculator.tsx`, after the results section:
```tsx
{results && (
  <div className="mt-8 p-6 border border-indigo-500/30 rounded-xl bg-indigo-950/20">
    <h3 className="text-lg font-semibold mb-2">📩 Email me this ROI report</h3>
    <p className="text-gray-400 text-sm mb-4">Get a personalized PDF with your numbers and implementation guide.</p>
    <form onSubmit={handleEmailCapture} className="flex gap-3">
      <input type="email" placeholder="your@email.com" className="flex-1 px-4 py-2 rounded-lg bg-gray-800 border border-gray-700" />
      <button type="submit" className="px-6 py-2 bg-indigo-600 rounded-lg font-semibold">Send Report</button>
    </form>
  </div>
)}
```

## Acceptance Criteria
- [ ] Email capture appears after ROI calculation
- [ ] Personalized email sent via Resend with their numbers
- [ ] Lead tracked in Resend Audience
- [ ] GA4 event fired on capture

## Dependencies
- TODO-609 (Resend Audiences setup)
