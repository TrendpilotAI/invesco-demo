# 218 — Invesco Retention: Leave-Behind Package Assembly (P1)

**Priority:** 🟠 P1 — Professional close, Brian shares this internally  
**Project:** invesco-retention  
**Effort:** S (2 hrs)  
**Owner:** Honey + Nathan  
**Dependencies:** 211 (deploy URL), 212 (Loom recordings), 217 (support model)

---

## Task Description

After the Brian Kiley demo, everything the team shows him needs to arrive as a single, clean package — not 6 separate emails over 3 days. Brian will share this with Kelly, their legal team, and potentially Invesco's CTO.

The leave-behind should be a single Notion page or well-formatted email with everything linked/embedded. It must be sent the SAME DAY as the demo.

---

## Coding Prompt (Agent-Executable)

```
You are assembling the Invesco leave-behind package for the ForwardLane demo.

REPO: /data/workspace/projects/invesco-retention/

TASK:

1. Read all existing materials files:
   ls /data/workspace/projects/invesco-retention/materials/
   Read each .md file to understand what already exists.

2. Create a master leave-behind document at:
   /data/workspace/projects/invesco-retention/materials/LEAVE_BEHIND.md

   Structure:

   # ForwardLane × Invesco — Demo Follow-Up Package
   *Prepared for: Brian Kiley, [Kelly's name], Invesco Financial Services*
   *Date: [DATE]*

   ## 🔗 Live Demo
   > Try it yourself: [DEPLOYED_URL]
   > Username/Password: (none needed — open access)
   > Reset the demo: [DEPLOYED_URL]?reset=true

   ## 📹 Demo Recordings
   (These capture everything we showed you today)
   - [Salesforce Embed View — 2 min](LOOM_URL_1)
   - [Signal Creation + Push to Salesforce — 2 min](LOOM_URL_2)
   - [Territory Dashboard — 1 min](LOOM_URL_3)
   - [Mobile Experience — 1 min](LOOM_URL_4)
   - [Full Demo (8 min)](LOOM_URL_COMBINED)

   ## 📄 Documents
   - [Executive Brief](link) — 1-page summary of ForwardLane for Invesco
   - [Pilot Proposal](link) — 2-week pilot at zero cost
   - [ROI Analysis](link) — Revenue impact model for Invesco's distribution team
   - [Support Model](link) — Our SLA commitments and Ten Decoders program
   - [Technical Overview](link) — How the Salesforce integration works

   ## 🚀 Proposed Next Steps
   1. **This week:** Confirm pilot go-ahead (reply to this email)
   2. **Week 1:** ForwardLane engineer connects with your Salesforce admin (2-hr session)
   3. **Week 2:** 5 wholesalers get access, live signals from your data
   4. **Week 3:** First review — are the signals accurate? Are wholesalers using it?
   5. **Week 4:** Go/no-go decision on full rollout

   ## 📞 Your ForwardLane Team
   - Nathan Stevenson, CEO — nathan@forwardlane.com — +1 (912) 912-9545
   - [CSM Name], Customer Success — csm@forwardlane.com
   - [Support Engineer], Dedicated Support — support@forwardlane.com

   ---
   *All demo data is synthetic. No real Invesco advisor or client data was used.*

3. Read the DEPLOY_URL.md and RECORDING_URLS.md files (if they exist) and substitute
   real URLs into the template. If they don't exist yet, leave placeholders.

4. Create a PDF-ready version by also creating LEAVE_BEHIND_EMAIL.md with:
   - Subject line: "ForwardLane × Invesco — Everything from today's demo"
   - A shorter email body that links to the full package
   - Suitable for Nathan to send within 2 hours of the demo

5. List any materials that are MISSING and need to be created before this package is complete.

Report: What exists, what's missing, and the leave-behind package structure.
```

---

## Acceptance Criteria
- [ ] LEAVE_BEHIND.md created with all sections
- [ ] LEAVE_BEHIND_EMAIL.md created (subject + body)  
- [ ] All placeholder URLs clearly marked for substitution
- [ ] Missing materials listed with priority
- [ ] Package covers: demo URL, recordings, all 4 PDFs, next steps, contacts
- [ ] Synthetic data disclaimer included
- [ ] Nathan can send this within 2 hours of demo with minimal edits
