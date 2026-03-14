# TODO: Add Content Security Policy Headers

- **Project:** Second-Opinion
- **Priority:** HIGH
- **Status:** pending
- **Category:** Security
- **Effort:** S (1-2 hours)
- **Created:** 2026-03-14

## Description
No CSP headers configured in `firebase.json`. Missing X-Frame-Options, X-Content-Type-Options.

## Action Items
Add to `firebase.json` hosting config:
```json
{
  "headers": [{
    "source": "**",
    "headers": [
      { "key": "Content-Security-Policy", "value": "default-src 'self' *.googleapis.com *.firebase.com *.firebaseapp.com; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'" },
      { "key": "X-Frame-Options", "value": "DENY" },
      { "key": "X-Content-Type-Options", "value": "nosniff" },
      { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
    ]
  }]
}
```
Then deploy: `firebase deploy --only hosting`
