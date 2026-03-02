# TODO 388: Signal Studio Templates — Webhook Trigger Integration

**Priority:** P2  
**Repo:** signal-studio-templates  
**Effort:** M (2-3 days)  
**Status:** pending

---

## Description

Allow templates to execute automatically on webhook events (CRM updates, portfolio rebalances, market triggers). Results pushed to Slack/email. This transforms templates from on-demand queries into proactive signal delivery — a key differentiator for Invesco.

## Use Cases
- CRM creates new advisor → auto-run `meeting-brief` and email to wholesaler
- Portfolio rebalance event → auto-run `risk-drift-alert` and Slack alert if threshold breached
- Market volatility spike → auto-run `concentration-risk` for high-AUM advisors

## Coding Prompt

```
Add webhook trigger support to signal-studio-templates:

1. New file: engine/webhook-handler.ts
   - Interface WebhookConfig { templateId: string; params: Record<string, any>; notifyChannels: NotifyChannel[] }
   - Interface NotifyChannel { type: 'slack' | 'email'; endpoint: string; minRows?: number }
   - Class WebhookHandler { constructor(engine: TemplateEngine); register(event: string, config: WebhookConfig): void; handleEvent(event: string, payload: unknown): Promise<void> }
   - handleEvent: resolve params (merge webhook payload fields + static config), execute template, notify channels if minRows met

2. New file: api/webhooks.ts
   - POST /webhooks/:event — accepts JSON payload, calls WebhookHandler.handleEvent()
   - GET /webhooks — list registered webhook configs
   - POST /webhooks/register — register a new webhook config
   - Validate webhook signature (HMAC-SHA256 with shared secret)

3. Slack notifier: POST to Slack webhook URL with result summary
   - Format: template name, row count, top 3 rows as bullet list, link to full results

4. Add __tests__/webhook-handler.test.ts:
   - Test event routing to correct template
   - Test param merging from webhook payload
   - Test notification threshold (minRows) filtering

5. Add to README: Webhook Triggers section with example CRM integration
```

## Dependencies
- TODO 101 (API layer) must be completed first
- Requires Slack webhook URL in environment config

## Acceptance Criteria
- [ ] WebhookHandler class registers and handles events
- [ ] HMAC signature validation on incoming webhooks
- [ ] Slack notification sends formatted result summary
- [ ] API endpoints for webhook registration
- [ ] Tests covering event routing and param merging
