# TODO-220: Demo Screen Recordings (Backup for Live Demo)
**Priority:** P0 — Essential failsafe
**Effort:** M (2-3 hours)
**Repo:** invesco-retention

## Description
Record polished screen recordings of all 4 demo views as backup for the live demo. If anything goes wrong during the live session (network, state corruption, mobile rendering), these recordings serve as seamless fallback.

## Views to Record
1. **/ (Home/Salesforce embed)** — `https://trendpilotai.github.io/invesco-demo/`
2. **Dashboard** — `https://trendpilotai.github.io/invesco-demo/dashboard.html`
3. **Signal Creation** — walk through NL query → push to Salesforce flow
4. **Mobile PWA** — `https://trendpilotai.github.io/invesco-demo/mobile.html` on iPhone

## Recording Spec
- Tool: Loom (preferred) or QuickTime + OBS
- Resolution: 1920x1080 (desktop), 390x844 (mobile simulation or real iPhone)
- Duration: Each view < 90 seconds
- Narration: Use the demo script from /data/workspace/projects/invesco-retention/materials/

## Storage
- Upload to Loom (share links with Megan + Craig)
- Save MP4s to /data/workspace/projects/invesco-retention/recordings/

## Acceptance Criteria
- [ ] All 4 views recorded
- [ ] Recordings accessible via shareable URL
- [ ] Recordings tested: play without account login required
- [ ] Backup URLs in demo day checklist
