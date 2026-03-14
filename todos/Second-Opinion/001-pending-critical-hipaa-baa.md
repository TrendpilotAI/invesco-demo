# TODO: Sign HIPAA BAA with Google Cloud / Firebase

- **Project:** Second-Opinion
- **Priority:** CRITICAL
- **Status:** pending
- **Category:** Security / Compliance
- **Effort:** S (administrative, not code)
- **Created:** 2026-03-14

## Description
No HIPAA Business Associate Agreement has been signed with Google Cloud / Firebase. **Storing any real patient data without a BAA is a HIPAA violation** that carries fines of $100-$50,000 per incident.

## Action Items
1. Go to https://console.cloud.google.com/support for project `gen-lang-client-0003791133`
2. Request and sign BAA with Google Cloud
3. Also execute BAAs with any AI model providers (Google AI for Gemini/MedGemma)
4. Document all subprocessors in HIPAA_COMPLIANCE.md
5. Block production access to real patient data until BAA is signed

## Risk
Without BAA: any real PHI stored = federal HIPAA violation. Competition demo data is fine, but the moment real patients use this, BAA is legally required.

## References
- `HIPAA_COMPLIANCE.md` — TODO section lists this
- `BRAINSTORM.md` — Top 5 Actions #1
- `PLAN.md` — Phase 1.1 item #1
