# TODO 359 — Signal Studio Frontend: Webhook Configuration UI

**Status:** pending  
**Priority:** medium  
**Project:** signal-studio-frontend  
**Estimated Effort:** 6–8 hours  

---

## Description

Users need to configure webhooks for signal outputs — specifying target URLs, secret keys, event types, and testing connectivity. This UI allows full CRUD on webhook configurations within a signal or from a global settings panel.

---

## Coding Prompt (Autonomous Agent)

```
Repo: /data/workspace/projects/signal-studio-frontend

Task: Build a Webhook Configuration UI component accessible from signal settings.

Step 1 — API Hooks
  Create `src/hooks/useWebhooks.ts`:
  - `useWebhooks(signalId: string)` — GET /api/signals/:signalId/webhooks
  - `useCreateWebhook()` — POST /api/signals/:signalId/webhooks
  - `useUpdateWebhook()` — PATCH /api/webhooks/:id
  - `useDeleteWebhook()` — DELETE /api/webhooks/:id
  - `useTestWebhook()` — POST /api/webhooks/:id/test

Step 2 — Webhook Form (Zod schema)
  Create `src/lib/validations/webhook.ts`:
  - `webhookSchema`: url (valid URL), secret (optional, min 8 chars if provided),
    events (array, min 1 item from enum: signal.run, signal.success, signal.failure)
  
  Create `src/components/webhooks/WebhookForm.tsx`:
  - React Hook Form + zod resolver
  - URL input, secret input (with show/hide toggle), events checkboxes
  - Submit calls create or update mutation depending on whether existing webhook passed as prop

Step 3 — Webhook List
  Create `src/components/webhooks/WebhookList.tsx`:
  - Table/list of configured webhooks: URL, events, status (active/inactive), last triggered
  - Actions: Edit (opens form), Delete (confirm dialog), Test (calls test endpoint, shows
    response status in a toast)

Step 4 — Integration
  Add a "Webhooks" tab or section to the signal detail/settings page.
  Mount <WebhookList signalId={signalId} /> there.

Step 5 — Verify
  `pnpm tsc --noEmit` + `pnpm build` pass.
```

---

## Dependencies

- TODO 355 (form validation) — establishes Zod + RHF pattern
- TODO 356 (toast system) — for test webhook feedback

---

## Acceptance Criteria

- [ ] Webhook list renders webhooks from API
- [ ] Create webhook form validates URL and events before submitting
- [ ] Edit existing webhook pre-fills form
- [ ] Delete shows confirmation before removing
- [ ] Test webhook button shows success/failure toast with HTTP status
- [ ] `pnpm tsc --noEmit` passes, `pnpm build` succeeds
