# TODO #842 — Second-Opinion: HIPAA PHI Encryption at Rest

**Priority:** P0  
**Effort:** M (3 days)  
**Repo:** /data/workspace/projects/Second-Opinion/  
**Created:** 2026-03-08 by Judge Agent v2

## Task Description

Implement proper HIPAA-compliant encryption at rest for all PHI stored in Firestore. Current implementation stores medical data in Firestore without field-level encryption, which is a compliance risk at scale.

## Implementation

### Audit PHI Fields
PHI in Firestore likely includes:
- Patient name, DOB, contact info
- Diagnosis text, symptoms
- Uploaded file references
- Analysis results and recommendations
- Chat messages with medical content

### Encryption Approach
Use Google Cloud KMS (already in Firebase project):

```typescript
// services/encryption.ts — already exists! Verify it's actually used
import { KeyManagementServiceClient } from '@google-cloud/kms';

const kmsClient = new KeyManagementServiceClient();

export async function encryptPHI(plaintext: string): Promise<string> {
  const keyName = kmsClient.cryptoKeyPath(
    process.env.GCP_PROJECT!,
    'global',
    'phi-keyring',
    'phi-key'
  );
  const [result] = await kmsClient.encrypt({ name: keyName, plaintext: Buffer.from(plaintext) });
  return Buffer.from(result.ciphertext as Uint8Array).toString('base64');
}
```

### Verify encryption.ts is Integrated
- Check if `encryption.ts` in services/ is actually called anywhere
- If not, wire it into all Firestore write operations for PHI fields
- Test round-trip: encrypt → store → retrieve → decrypt

### Acceptance Criteria
- [ ] All PHI fields encrypted before Firestore write
- [ ] Decryption happens server-side only (Cloud Functions)
- [ ] KMS key rotation policy set (90 days)
- [ ] console.log() audit in functions/src — no PHI logged in plaintext
- [ ] Legal: confirm encryption approach satisfies HIPAA Security Rule §164.312(a)(2)(iv)

## Dependencies
- #841 (Stripe) can proceed in parallel

## Risk
- High priority legal/compliance risk — blocking for any production PHI processing at scale
