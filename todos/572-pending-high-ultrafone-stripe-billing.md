# TODO 572 — Stripe Billing Layer (SaaS)

**Priority:** HIGH  
**Repo:** Ultrafone  
**Effort:** 3-4 days  
**Status:** pending

## Description
Path from personal tool to product. Implement Stripe subscription billing with tiered plans.

## Plans
- **Personal** ($9/mo): 1 Twilio number, 500 calls/mo, basic screening
- **Pro** ($29/mo): 3 numbers, 2000 calls/mo, voice cloning, call recording
- **Business** ($99/mo): 10 numbers, unlimited calls, multi-user (5 seats), Slack/CRM integration

## Coding Prompt
```python
# 1. Install: pip install stripe
# 2. Create billing service: backend/services/billing_service.py
#    - create_checkout_session(user_id, plan)
#    - handle_webhook(event) — update user plan on payment
#    - get_subscription(user_id)
#    - cancel_subscription(user_id)

# 3. Create products in Stripe dashboard, store price IDs in settings.py

# 4. Add billing API routes: backend/api/billing.py
#    POST /api/billing/checkout → Stripe checkout session
#    POST /api/billing/webhook → Stripe webhook handler
#    GET /api/billing/subscription → current plan
#    POST /api/billing/cancel

# 5. Add plan enforcement in middleware:
#    - Check call count against plan limits
#    - Block >1 Twilio number on Personal plan

# 6. Frontend: Settings → Billing tab with plan upgrade UI
```

## Acceptance Criteria
- [ ] Stripe checkout flow working
- [ ] Webhook updates user plan in DB
- [ ] Plan limits enforced
- [ ] Upgrade/downgrade UI in settings
- [ ] Billing tab shows current plan + invoices

## Dependencies
- TODO 568 (keys managed via Railway)
