# TODO-002: CRITICAL — Execute HIPAA BAA Before Production PHI

**Priority:** CRITICAL
**Status:** pending
**Category:** security, compliance

## Problem
The app processes medical images and health information. HIPAA requires a Business Associate Agreement (BAA) with Google Cloud (Firebase) and any AI model providers before handling real Protected Health Information (PHI).

Currently documented in `HIPAA_COMPLIANCE.md` as a TODO item.

## Required Actions
1. Execute BAA with Google Cloud (Firebase) — requires upgrading to a supported GCP plan
2. Execute BAA with any third-party model providers (if applicable)
3. Document all subprocessors
4. Conduct formal security risk assessment
5. Establish breach notification procedure

## Impact
Without a BAA, handling real patient data is a HIPAA violation with significant legal/financial exposure.

## Files
- `HIPAA_COMPLIANCE.md`
