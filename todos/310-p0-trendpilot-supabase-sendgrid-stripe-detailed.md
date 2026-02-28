Title: 310 — Trendpilot: Wire Supabase persistence + SendGrid + Stripe (P0)
Repo: Trendpilot
Priority: P0
Owner: Trendpilot product engineer
Estimated effort: 2–4 days

Description:
Replace file-based persistence with Supabase tables, implement SendGrid for email delivery, and add Stripe checkout + webhooks for paid tiers.

Acceptance criteria:
- Supabase tables seeded and application reads/writes to Supabase
- Emails sent via SendGrid in staging and logged
- Stripe checkout in test mode works and webhooks handled securely

Execution steps / Agent-executable prompt:
1. Create Supabase schema and migration scripts; update app config
2. Implement data migration from file JSON to Supabase (script)
3. Integrate SendGrid for transactional emails; test in staging
4. Integrate Stripe Checkout + webhook handler; test in sandbox
5. Add CI checks for migrations

Verification tests:
- Data persists across app restarts
- SendGrid sends test email and logs response
- Stripe checkout flow completes in test mode

Notes:
- Do not use live API keys in staging; use test keys and env vars
- Coordinate with Nathan before switching production keys
