# TODO 620 — Second-Opinion: CSP Headers + Cloud Function Rate Limiting
**Priority**: P2 | **Effort**: 4h | **Repo**: Second-Opinion

## Description
Security hardening: Add Content-Security-Policy headers to Firebase Hosting and implement per-user rate limiting on Cloud Functions to prevent API abuse.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:

1. **CSP Headers in firebase.json**:
   Add to the "hosting" section headers array:
   {
     "key": "Content-Security-Policy",
     "value": "default-src 'self'; script-src 'self' 'unsafe-inline' https://apis.google.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://*.googleapis.com https://*.firebaseio.com https://firestore.googleapis.com; frame-ancestors 'none'"
   }
   Also add: X-Frame-Options: DENY, X-Content-Type-Options: nosniff

2. **Rate limiting in Cloud Functions**:
   In functions/src/pipeline.ts (or a new functions/src/rateLimit.ts):
   - Use Firestore to track API calls per user per hour
   - Limit: 10 analysis calls/hour for free tier, 50/hour for paid
   - Return HTTP 429 with Retry-After header when limit hit
   - Use Firebase Admin Firestore for rate limit counters

3. **Input validation**:
   In functions/src/pipeline.ts:
   - Validate file MIME type server-side (not just client-side)
   - Max file size: 20MB
   - Allowed types: image/jpeg, image/png, image/heic, application/pdf

Deploy with: firebase deploy --only functions,hosting:rules
```

## Acceptance Criteria
- [ ] CSP headers present in production (verify with securityheaders.com)
- [ ] Rate limiting returns 429 when exceeded
- [ ] File type validation rejects invalid uploads server-side
- [ ] No regression in normal usage

## Dependencies
- Requires Firebase Functions to be deployed
