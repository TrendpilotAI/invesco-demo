# TODO 521: Provider/Doctor Dashboard
**Repo:** Second-Opinion  
**Priority:** P1 — B2B Revenue  
**Effort:** 3 days  
**Status:** pending

## Description
Create a separate `/doctor` interface for healthcare providers to review patient-submitted cases. This pivots Second-Opinion from B2C to B2B SaaS — clinics pay per provider seat (~$99/mo) vs consumers paying $9.99.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:

1. Add `role: "patient" | "provider"` to Firestore user documents
2. Create components/ProviderDashboard.tsx:
   - Case queue with patient name (anonymized), date, urgency score
   - Click → CaseReview.tsx (full AI analysis + ability to annotate/override)
   - Approve/Reject/Request-More-Info actions
   - Patient notification sent via Firebase when provider responds
3. Add /doctor route in App.tsx with role-guard (provider only)
4. Create services/providerService.ts:
   - getCaseQueue(providerId) → list of cases assigned to provider
   - annotateCase(caseId, annotation) → saves to Firestore
   - notifyPatient(caseId, message) → Firebase Cloud Message or email
5. Add provider onboarding flow (license verification field in Auth.tsx)
6. Wire FHIR export button: services/fhir.ts → "Export to EHR" CTA
```

## Acceptance Criteria
- [ ] Provider role separate from patient role in Firestore
- [ ] Provider sees case queue sorted by urgency
- [ ] Can annotate, approve, reject AI findings
- [ ] Patient receives notification when provider responds
- [ ] FHIR export available per case
- [ ] Mobile responsive

## Dependencies
- TODO 519 (Stripe) for provider subscription tier
