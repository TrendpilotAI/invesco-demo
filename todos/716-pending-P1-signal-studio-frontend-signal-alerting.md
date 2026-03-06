# TODO-716: Signal Alerting & Scheduling System

**Repo**: signal-studio-frontend  
**Priority**: P1  
**Effort**: L (3-5 days)  
**Status**: pending

## Description
Enterprise clients need to schedule signals to run automatically and receive alerts when thresholds are crossed. This is a critical revenue feature.

## Coding Prompt
```
Implement signal alerting and scheduling for signal-studio-frontend:

1. Database schema (add to Oracle or Supabase based on current auth strategy):
   - SIGNAL_SCHEDULES table: id, signal_id, cron_expression, last_run, next_run, status
   - SIGNAL_ALERTS table: id, signal_id, condition (threshold config JSON), channel (email/slack), created_at
   - SIGNAL_ALERT_HISTORY table: id, alert_id, triggered_at, result_count, notification_sent

2. API Routes:
   - POST /api/signals/[id]/schedule — create/update schedule
   - DELETE /api/signals/[id]/schedule — remove schedule
   - POST /api/signals/[id]/alerts — create alert rule
   - GET /api/signals/[id]/alerts — list alert rules
   - POST /api/cron/run-scheduled — webhook endpoint for cron job runner

3. Alert UI:
   - Add "Schedule & Alerts" tab to signal detail page
   - Schedule picker: run every X hours/days, or cron expression
   - Alert conditions: "notify when result count > N" or "notify when column value changes"
   - Notification channels: email (via SendGrid), Slack webhook URL

4. Background execution:
   - /api/cron/run-scheduled: queries SIGNAL_SCHEDULES for due signals, runs them, checks alert conditions, sends notifications
   - Can be triggered by Vercel cron or external cron service

5. Email template: simple HTML email with signal name, run time, result count, link to view results.
```

## Acceptance Criteria
- [ ] User can schedule a signal to run hourly/daily
- [ ] User can configure email alert when signal results exceed threshold
- [ ] Alert fires and email is sent in test environment
- [ ] Schedule history visible in UI
