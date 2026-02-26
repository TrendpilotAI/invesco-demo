---
status: pending
priority: p0
issue_id: "004"
tags: [signal-studio, oracle, railway, devops, credentials]
dependencies: []
---

# 004 — Signal Studio: Configure Oracle 23ai Production Credentials & Wallet for Railway

## Problem Statement

Signal Studio's Oracle 23ai connection is configured for local development using file-based wallet paths
(`/Users/nathanstevenson/...`) that don't exist in Railway containers. The production app currently
cannot establish a connection to Oracle Autonomous Database — all Oracle-backed routes return errors.
This blocks NL→SQL, vector search, data-pipeline, and OML features for Invesco.

## Findings

- `lib/oracle-service.ts` reads `ORACLE_WALLET_PATH` and `ORACLE_INSTANT_CLIENT_PATH` env vars
- `ORACLE-SETUP.md` shows wallet lives at `/Users/nathanstevenson/Development/Signal Studio/signal-library/wallet`
- `railway.json` uses Docker build — wallet files and Instant Client not present in container
- `Dockerfile` needs Oracle Instant Client installed + wallet files injected at build/deploy time
- Three environment variable sets needed: credentials, wallet base64, TNS config
- `lib/oracle-service.ts` `initializeInstantClient()` auto-detects `/usr/lib/oracle/23/client64/lib` — Railway needs this path

## Proposed Solutions

### Option A: Base64-encode wallet into Railway env vars (Recommended)
- Encode each wallet file as a base64 env var (`ORACLE_WALLET_CWALLET_SSO_B64`, etc.)
- At app startup, decode and write to `/tmp/oracle-wallet/`
- Install Oracle Instant Client in Dockerfile
- **Pros:** No secrets in repo, Railway-native, works in ephemeral containers
- **Effort:** Medium (4h) | **Risk:** Low

### Option B: Use Oracle ORDS REST endpoints only
- Remove `node-oracledb` dependency, use ORDS HTTP endpoints for all DB ops
- **Pros:** Simpler, no native libs
- **Cons:** ORDS has limited SQL execution surface, breaks existing code

### Option C: Commit wallet to private repo branch
- **Pros:** Simple
- **Cons:** Security nightmare — reject

## Recommended Action

Implement Option A. Encode wallet files as Railway environment variables. Add startup script that
decodes them before Next.js server initializes. Update Dockerfile to install Oracle Instant Client 23.

## Acceptance Criteria

- [ ] `Dockerfile` installs Oracle Instant Client (`libaio1`, `oracle-instantclient23.x-basiclite`)
- [ ] `lib/oracle-service.ts` decodes wallet from env vars at startup (writes to `/tmp/oracle-wallet/`)
- [ ] `scripts/encode-wallet.sh` script created to base64-encode wallet files into `.env.railway` format
- [ ] Railway service has env vars: `ORACLE_USER`, `ORACLE_PASSWORD`, `ORACLE_CONNECT_STRING`, `ORACLE_WALLET_B64_*` (one per wallet file)
- [ ] `GET /api/oracle/health` returns `{ ok: true }` in Railway production
- [ ] `GET /api/oracle/tables` returns table list in Railway production
- [ ] No wallet files committed to git (`.gitignore` updated)
- [ ] `ORACLE-RAILWAY-SETUP.md` doc created with step-by-step instructions

## Files to Create/Modify

- `Dockerfile` — add Oracle Instant Client apt/rpm install steps
- `lib/oracle-service.ts` — add `decodeWalletFromEnv()` call before `initializeInstantClient()`
- `lib/oracle/wallet-setup.ts` — NEW: decode base64 env vars → `/tmp/oracle-wallet/` at startup
- `scripts/encode-wallet.sh` — NEW: helper to base64-encode wallet files
- `.env.example` — add `ORACLE_WALLET_CWALLET_SSO_B64=` etc.
- `ORACLE-RAILWAY-SETUP.md` — NEW: Railway deployment guide for Oracle

## Technical Details

```typescript
// lib/oracle/wallet-setup.ts
export function decodeWalletFromEnv(): string | null {
  const walletDir = '/tmp/oracle-wallet'
  const files = {
    'cwallet.sso': process.env.ORACLE_WALLET_CWALLET_SSO_B64,
    'ewallet.p12': process.env.ORACLE_WALLET_EWALLET_P12_B64,
    'tnsnames.ora': process.env.ORACLE_WALLET_TNSNAMES_B64,
    'sqlnet.ora': process.env.ORACLE_WALLET_SQLNET_B64,
  }
  // mkdir -p, write each file from base64, return walletDir
}
```

Dockerfile addition:
```dockerfile
RUN apt-get update && apt-get install -y libaio1 wget && \
    wget -q https://download.oracle.com/otn_software/linux/instantclient/2380000/instantclient-basiclite-linux.x64-23.8.0.0.0dbru.zip && \
    unzip instantclient-basiclite-*.zip -d /opt/oracle && \
    rm instantclient-basiclite-*.zip && \
    echo /opt/oracle/instantclient_23_8 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig
ENV ORACLE_INSTANT_CLIENT_PATH=/opt/oracle/instantclient_23_8
```

## Estimated Effort

4 hours

## Work Log

### 2026-02-26 — Initial Planning

**By:** Honey Planning Agent

**Actions:**
- Identified wallet path mismatch between local dev and Railway container
- Documented wallet files needed for base64 encoding
- Designed `wallet-setup.ts` decode-on-startup approach
