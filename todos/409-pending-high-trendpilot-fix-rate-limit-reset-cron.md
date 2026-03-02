# 409 — Wire API Key Rate Limit Daily Reset Cron

**Priority:** HIGH (P1) — Revenue bug: paid users get permanently locked out  
**Repo:** Trendpilot  
**Effort:** XS (1 hour)  
**Dependencies:** None

## Problem
`ApiKeyStore.resetDailyCounts()` in `src/services/apiKeys/index.ts` exists but is never called. After an API key hits its daily request limit, it is permanently blocked — no reset occurs. This would lock out paying customers.

## Coding Prompt
```
In /data/workspace/projects/Trendpilot/src/services/scheduler/index.ts:

1. Import ApiKeyStore from '@/services/apiKeys'
2. Add a daily cron job that fires at midnight UTC (cron: '0 0 * * *'):
   - Call apiKeyStore.resetDailyCounts()
   - Log: "Daily API key rate limits reset"
3. Also add a daily cron for data retention policy enforcement:
   - Import RetentionPolicyManager from '@/services/compliance'
   - Call retentionManager.enforcePolicies() 

Write a test in tests/scheduler/rateLimitReset.test.ts verifying:
- resetDailyCounts is called at midnight
- counts are zeroed out correctly
```

## Acceptance Criteria
- [ ] `resetDailyCounts()` wired into midnight cron
- [ ] Test confirms daily reset behavior
- [ ] Verified via scheduler logs on startup
