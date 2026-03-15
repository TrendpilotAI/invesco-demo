# TODO-008: MEDIUM — Implement Data Retention Policies

**Priority:** MEDIUM
**Status:** pending
**Category:** security, compliance

## Problem
`services/dataRetention.ts` exists but HIPAA compliance doc lists data retention policy as a TODO. Need to:
- Define retention periods for medical queries and uploaded images
- Implement automated cleanup (Cloud Function cron)
- Honor user deletion requests (GDPR/CCPA right to erasure)

## Files
- `services/dataRetention.ts`
- `HIPAA_COMPLIANCE.md`
