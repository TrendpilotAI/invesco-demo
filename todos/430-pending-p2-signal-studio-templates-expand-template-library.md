# TODO 430: Expand Template Library to 40+ Templates

**Repo:** signal-studio-templates  
**Priority:** P2 (High value, not blocking)  
**Effort:** M (1 week)  
**Status:** pending

## Description

Currently 20 templates across 5 categories. Doubling to 40 dramatically increases the "wow factor" in Invesco demos and broadens the use cases that justify the platform. Each new template follows the existing pattern exactly.

## Target Templates (20 new)

### Meeting Prep (4 new)
- `conference-attendee-intel` — Upcoming conferences + which advisors are attending
- `advisor-anniversary-alert` — Relationship milestones (1yr, 5yr, 10yr client)
- `pre-call-research-brief` — Auto-aggregate news/events for advisor's firm before a call
- `last-interaction-summary` — Most recent touchpoint details + outcome + next steps

### Sales Intelligence (4 new)  
- `whitespace-opportunity` — Advisors with gaps in their product mix vs their model
- `inbound-inquiry-triage` — Recent inquiries ranked by AUM + urgency
- `share-of-wallet-estimate` — Estimated total AUM vs what's allocated to your products
- `competitor-product-mention` — Advisors who mentioned competitor products in notes

### Risk & Compliance (4 new)
- `aum-decline-watchlist` — Accounts losing AUM above threshold
- `regulatory-change-impact` — Advisors affected by recent reg changes
- `overconcentration-alert` — Single-security concentration above compliance threshold
- `expiring-licenses-alert` — Advisor licenses expiring in next 90 days

### Product Marketing (4 new)
- `share-of-wallet-by-product` — Product-level penetration across territory
- `launch-readiness-score` — Which advisors are most likely to adopt new product
- `redemption-risk-indicators` — Leading indicators that a client may redeem
- `model-portfolio-alignment` — Advisors whose models align with your products

### Management (4 new)
- `advisor-tier-migration` — Advisors moving up/down tiers (growth/decline signals)
- `coverage-roi-analysis` — Revenue generated per wholesaler per region
- `team-activity-summary` — Weekly team call volume + meetings + outcomes
- `territory-carveout-candidate` — Advisors ready for dedicated coverage

## Acceptance Criteria

- [ ] 20 new template files created following existing pattern
- [ ] Each has: `id`, `name`, `description`, `category`, `sqlTemplate`, `parameters`, `outputSchema`, `exampleOutput`, `talkingPointsPrompt`, `visualBuilderNodes`
- [ ] All templates registered in `templates/index.ts`
- [ ] `templates.test.ts` updated: `expect(ALL_TEMPLATES.length).toBe(40)`
- [ ] README table updated

## Coding Prompt

```
For each new template, follow the exact pattern of an existing template in the same category.
Example reference: /data/workspace/projects/signal-studio-templates/templates/sales-intelligence/dormant-relationships.ts

Steps:
1. Create the template file in the correct category subdirectory
2. Export the template object matching the SignalTemplate interface exactly
3. Add the export to the category's index.ts
4. Add the template to templates/index.ts ALL_TEMPLATES array
5. Update the count test in __tests__/templates.test.ts

Start with the 5 highest-value templates:
1. whitespace-opportunity (sales-intelligence)
2. aum-decline-watchlist (risk-compliance) 
3. share-of-wallet-estimate (sales-intelligence)
4. conference-attendee-intel (meeting-prep)
5. launch-readiness-score (product-marketing)
```

## Dependencies

- None (independent work)

## Notes

Craig Lieb specifically asked for "easy buttons" — more templates = more easy buttons. Priority should be templates that map to common Invesco wholesaler workflows.
