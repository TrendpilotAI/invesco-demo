# TODO #426: Print-to-PDF Leave-Behind Button
**Priority:** P0 | **Effort:** S (2-3h) | **Status:** Pending
**Repo:** invesco-retention | **Date:** 2026-03-04

## Description
Add a "Save as PDF / Print Brief" button to the /salesforce meeting brief view.
After seeing the AI-generated brief for Sarah Chen, Brian Kiley should be able to click one button and get a clean, Invesco-branded PDF he can forward to his team. This is a physical leave-behind generated from the demo itself — extremely high-value for deal closure.

## Coding Prompt (Agent-Executable)
```
In /data/workspace/projects/invesco-retention/demo-app/src/app/salesforce/page.tsx:

1. Add a "Print Brief" or "Save as PDF" button to the top-right of the meeting brief section.
   Style it as a secondary button with a printer/download icon.

2. Implement using window.print() with @media print CSS:
   - Add @media print styles to hide: nav, sidebar, demo banner, "Reset Demo" button, tab switcher
   - Show: advisor name, signal summary, recommended actions, Invesco logo
   - Use clean black-on-white styling for print
   - Add page title: "Signal Studio — Meeting Brief: {Advisor Name}"

3. Alternatively, use html2pdf.js (npm install html2pdf.js) for direct PDF download:
   - Button click → captures the meeting brief div → downloads as PDF
   - Filename: "signal-brief-{advisor-slug}-{date}.pdf"

4. The printed/downloaded PDF should include:
   - ForwardLane Signal Studio header with Invesco logo
   - Advisor name, AUM, last contact date
   - Top 3 signals with severity indicators
   - Recommended actions list
   - "Confidential — Demo purposes only" footer

5. Test in Chrome print preview. Confirm it looks clean.
6. Rebuild static export: cd demo-app && npm run build && npm run export
7. Deploy: git add -A && git commit -m "feat: print-to-pdf leave-behind button" && git push
```

## Acceptance Criteria
- [ ] "Print Brief" button visible in salesforce view
- [ ] window.print() or html2pdf.js produces clean branded PDF
- [ ] Nav/demo elements hidden in print view
- [ ] PDF includes advisor name, signals, and recommended actions
- [ ] Deployed to GitHub Pages

## Dependencies
None

## Impact
High — Physical leave-behind from the demo. Brian can forward to Vanessa, EA team.
