# 217 — Invesco Retention: Support Model Polish (P1)

**Priority:** 🟠 P1 — Addresses Kelly's objection directly  
**Project:** invesco-retention  
**Effort:** XS-S (1 hr)  
**Owner:** Nathan + Honey  
**Dependencies:** None

---

## Task Description

Kelly (Invesco's internal champion) raised concerns about the support burden of adopting ForwardLane. The `support-model.md` doc needs to directly answer: "What happens when something breaks? Who do we call? How fast do you respond?"

The "Ten Decoders" framing needs to be sharpened into a concrete SLA tier with named contacts and response times. This doc goes in the leave-behind package and may be reviewed by Kelly's legal/ops team.

---

## Coding Prompt (Agent-Executable)

```
You are polishing the Invesco support model document for the retention pitch.

FILE: /data/workspace/projects/invesco-retention/materials/support-model.md
(If this file doesn't exist, create it from scratch.)

TASK: Rewrite/enhance the support-model.md to be a professional, confidence-inspiring document.

STRUCTURE THE DOC AS:

# ForwardLane Support Model — Invesco Financial Services
*Your dedicated partnership tier*

## Your Support Team

| Role | Name | Contact | Response Time |
|------|------|---------|---------------|
| Dedicated Support Engineer | [Name TBD] | direct@forwardlane.com | 2 hours |
| Customer Success Manager | [Name TBD] | csm@forwardlane.com | 4 hours |
| Engineering Escalation | Nathan Stevenson | nathan@forwardlane.com | Same day |

## SLA Commitments

| Issue Type | Response SLA | Resolution SLA |
|-----------|-------------|----------------|
| P0 — System down | 30 minutes | 4 hours |
| P1 — Feature broken | 2 hours | Next business day |
| P2 — Minor bug | 24 hours | 1 week |
| P3 — Enhancement | 1 week | Roadmap scheduled |

## The Ten Decoders Program

Invesco is enrolled in ForwardLane's Ten Decoders program — our highest-touch support tier, reserved for 10 strategic enterprise accounts. This includes:

- **Dedicated Slack channel** (#forwardlane-invesco) with direct access to our engineering team
- **Weekly sync** (30 min) with your Customer Success Manager
- **Monthly product roadmap briefing** — you influence our roadmap
- **On-site visits** (2x/year) for training and relationship building
- **Priority feature requests** — your asks go to the top of our backlog

## Onboarding & Training

- Week 1: Technical onboarding (Salesforce integration setup)
- Week 2: Wholesaler training (2-hour virtual session, recorded)
- Week 3: First data review with your CS team
- Ongoing: Monthly check-ins, quarterly business reviews

## Security & Compliance

- All data processing within your existing Salesforce infrastructure
- No client data leaves your environment
- SOC 2 Type II in progress (expected Q2 2026)
- FINRA-reviewed data handling procedures

## What "Zero Incremental IT Burden" Means

ForwardLane deploys as a Salesforce-native Lightning Web Component. Your IT team's involvement:
- Day 1: Add the ForwardLane package from Salesforce AppExchange (~30 min)
- Day 7: Data mapping session with our engineer (~1 hr)
- Ongoing: Zero — we maintain the integration, you just use it

---

Ensure the tone is confident and specific (no vague promises). 
Add a final section: "Kelly, [Name of Kelly's manager], and the Invesco legal team are welcome to review our full MSA. We're happy to sign your standard vendor agreement."

After writing: Run `wc -l` on the file and confirm it's >60 lines.
Report: The key changes made and whether the doc addresses support burden directly.
```

---

## Acceptance Criteria
- [ ] SLA table with specific response times (not vague)
- [ ] Ten Decoders program clearly explained with concrete benefits
- [ ] Named roles (even if "TBD") with contact emails
- [ ] Zero-IT-burden section directly answers Kelly's concern
- [ ] Document is professional enough to share with Kelly's ops team
- [ ] Length: 60+ lines, formatted cleanly in Markdown
