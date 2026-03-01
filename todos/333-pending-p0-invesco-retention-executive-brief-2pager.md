# TODO-333: 2-Page Executive Brief — Leave-Behind Document

**Repo:** invesco-retention  
**Priority:** P0 — Deal-closing  
**Effort:** 2 hours  
**Status:** Pending

## Description
A polished 2-page leave-behind document that sells the deal without Nathan in the room. Brian Kiley will share this internally. It must be skimmable in 90 seconds and answer every CFO-level question.

## Action Prompt
Create /data/workspace/projects/invesco-retention/materials/invesco-executive-brief.md (and a PDF-ready HTML version):

**Page 1: Problem → Solution → Outcome**
- Problem: Wholesalers have data in 5 systems, zero synthesis, miss signals that predict churn
- Solution: Signal Studio — AI-powered meeting intelligence embedded in Salesforce
- Outcome: Wholesalers arrive to every meeting with a ranked action list. Retention improves. AUM stays.
- Include 2-3 specific metrics (e.g., "34% of advisors show pre-churn signals 90 days before redemption")

**Page 2: Architecture + Pilot Terms + Success Metrics**
- Architecture: Simple diagram showing Salesforce LWC ← ForwardLane AI ← Snowflake + Seismic + CRM data
- Pilot: 6-week pilot, fixed fee, specific success criteria
- Success Metrics: Wholesaler adoption rate, signals actioned, retention improvement (measurable)
- Contact: Nathan Stevenson, ForwardLane

## Acceptance Criteria
- Document is 2 pages max (letter size)
- Readable without Nathan present
- No jargon — CFO/CEO readable
- Invesco-specific language (reference their actual data stack)
- Includes architecture diagram (even ASCII/Mermaid is fine for now)

## Dependencies
- materials/ directory must exist
