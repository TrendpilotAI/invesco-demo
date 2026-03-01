# TODO-335: IT Security One-Pager — Remove the "IT Won't Approve" Blocker

**Repo:** invesco-retention  
**Priority:** P1 — Deal-unblocking  
**Effort:** 1 hour  
**Status:** Pending

## Description
A one-page document that Nathan can hand to Invesco's IT/security team. This removes the "our IT won't approve this" objection before it becomes a blocker. Must show data never leaves their perimeter.

## Action Prompt
Create /data/workspace/projects/invesco-retention/materials/it-security-overview.md:

**Include:**
1. Data Flow Diagram (ASCII/Mermaid):
   - Invesco Salesforce → Signal Studio LWC (client-side only)
   - Signal Studio API → ForwardLane AI Engine → Returns signals
   - ForwardLane API → Reads from Invesco Snowflake (read-only, scoped)
   - Nothing persisted outside Invesco perimeter except anonymized signal metadata

2. Security Posture:
   - ForwardLane API: TLS 1.3, OAuth 2.0, no data stored
   - Salesforce LWC: Deployed via standard package, CSP compliant
   - Snowflake: Read-only service account, row-level security preserved
   - SOC 2 Type II in progress (or available on request)

3. Compliance Notes:
   - FINRA/SEC: No client PII transmitted outside Invesco systems
   - Data residency: All computation on Invesco's cloud infrastructure

4. Contact for technical review: nathan@forwardlane.com

## Acceptance Criteria
- 1 page max
- Data flow diagram present
- Addresses FINRA/SEC compliance angle
- Reviewable by non-technical IT manager
