# TODO #423: Add Seismic Content Recommendations to Meeting Brief

**Priority:** P0 (pre-demo)
**Effort:** S (2-3 hours)
**Repo:** invesco-retention
**Source:** BRAINSTORM.md v3, Category 1.9

## Description

Add a "Recommended Content" section to the Salesforce meeting brief page. Show 2-3 Seismic documents relevant to this advisor's current allocation/signals.

Invesco already uses Seismic as their content distribution platform. Seeing Signal Studio surface Seismic content recommendations creates an "aha moment" — it fits directly into their existing workflow.

## Acceptance Criteria
- [ ] Meeting brief page (`/salesforce`) has a "Content to Share" section
- [ ] Shows 2-3 Seismic document cards (title, type, relevance reason)
- [ ] Documents are tied to advisor's allocation signals (e.g., if over-weight International Equity, show international equity thought leadership)
- [ ] Looks native to the Salesforce SLDS design system
- [ ] Works in static export (no backend required — synthetic data only)

## Implementation Prompt

```
In /data/workspace/projects/invesco-retention/demo-app/src/app/salesforce/page.tsx:

1. Add a "Recommended Seismic Content" section to the meeting brief accordion
2. Create a synthetic content recommendation array in mock-data.ts:
   type SeismicContent = {
     title: string;
     type: 'Article' | 'Deck' | 'Video' | 'One-Pager';
     relevanceReason: string;
     datePublished: string;
     thumbnail?: string;
   }
3. Map each advisor to 3 relevant documents based on their signal data
4. For Dr. Sarah Chen (advisor sarah-chen): show International Equity Q4 Outlook, ESG Integration Guide, Alternative Investments Overview
5. Style with SLDS card component pattern, file icon, and "Share" button (no-op click)
6. Add to the salesforce page accordion as a collapsible section defaultOpen=false
```

## Dependencies
- None (standalone feature)

## Demo Impact
HIGH — Invesco uses Seismic. This directly answers "how does it integrate with our stack?"
