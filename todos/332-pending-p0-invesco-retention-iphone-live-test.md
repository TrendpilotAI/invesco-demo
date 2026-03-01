# TODO-332: iPhone Live Test — Full Demo Flow on Physical Device

**Repo:** invesco-retention  
**Priority:** P0 — Demo-blocking  
**Effort:** 30 minutes  
**Status:** Pending

## Description
The demo must work flawlessly on a physical iPhone (Safari). Decision-makers may pull out their phone during the meeting. A single broken layout or unresponsive tap destroys credibility.

## Action Prompt
Run the full demo flow at https://trendpilotai.github.io/invesco-demo/ on a real iPhone:

1. Open each route: `/`, `/dashboard`, `/salesforce`, `/mobile`
2. Check for: layout breaks, text overflow, unresponsive touch targets, missing images, JS errors (Safari Web Inspector)
3. Test the "Push to Salesforce" toast interaction on mobile
4. Test the signal creation flow on `/create`
5. Verify the PWA install prompt appears on iOS Safari
6. Document any issues found with screenshot + fix

## Acceptance Criteria
- All 4 routes render correctly on iPhone 13/14/15 Safari
- No touch targets < 44px
- No horizontal scroll on any page
- "Push to Salesforce" toast visible and dismissible
- Zero JS console errors on Safari

## Dependencies
- Demo deployed at trendpilotai.github.io/invesco-demo/

## Notes
If issues found, fix in mobile-pwa/app.css and redeploy via GitHub Pages.
