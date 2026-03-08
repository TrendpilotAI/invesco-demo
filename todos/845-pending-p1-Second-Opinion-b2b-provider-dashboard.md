# TODO #845 — Second-Opinion: B2B Provider/Doctor Dashboard

**Priority:** P1  
**Effort:** XL (3 weeks)  
**Repo:** /data/workspace/projects/Second-Opinion/  
**Created:** 2026-03-08 by Judge Agent v2

## Task Description

Build a B2B provider dashboard enabling clinics and doctors to white-label Second Opinion. This is the highest-revenue potential feature — targeting $199-2000/month per clinic.

## Implementation

### New Routes
```
/provider — Provider landing/signup
/provider/dashboard — Clinic admin view
/provider/patients — Patient list with analysis status
/provider/settings — White-label config, branding, pricing
/provider/billing — Usage stats, Stripe billing
```

### New Components
- `ProviderSignup.tsx` — Clinic registration flow (NPI number validation)
- `ProviderDashboard.tsx` — Overview: patient count, analyses this month, avg confidence
- `PatientList.tsx` — Table of referred patients + their analysis status
- `ClinicSettings.tsx` — Logo upload, custom colors, domain config
- `UsageBilling.tsx` — Monthly usage graph + current plan

### Firestore Schema
```
/clinics/{clinicId}
  name, npiNumber, logo, primaryColor, planTier, ownerId
  createdAt, trialEndsAt

/clinics/{clinicId}/staff/{userId}
  role: "admin" | "provider"
  
/users/{userId}
  clinicId? — links patient to clinic if referred
```

### Auth Changes
- Add `clinicId` claim to Firebase Auth token via Cloud Function
- Firestore rules: clinic staff can read patients with matching clinicId

### Key Features for MVP
1. Clinic signup with NPI verification (NPI Registry API — free)
2. Patient referral link generation (unique URL per clinic)
3. Clinic admin sees all referred patient analyses
4. White-label header with clinic logo
5. Monthly usage report email

### Acceptance Criteria
- [ ] Clinic can sign up, invite staff
- [ ] Unique referral link generates, patients linked to clinic
- [ ] Provider sees patient analysis list with status indicators
- [ ] White-label: clinic logo + colors applied throughout app
- [ ] Stripe billing at $199/month with 14-day trial
- [ ] NPI number validated against public NPI Registry API

## Dependencies
- #841 (Stripe) — needed for clinic billing
- #842 (HIPAA) — needed before PHI visible to clinic staff

## Revenue Impact
10 clinics × $199/month = $1,990 MRR baseline  
50 clinics × avg $500/month = $25,000 MRR at scale
