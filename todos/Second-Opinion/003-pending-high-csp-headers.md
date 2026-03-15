# TODO-003: HIGH — Add Content Security Policy Headers

**Priority:** HIGH
**Status:** pending
**Category:** security

## Problem
No CSP headers configured. For a medical app handling sensitive data, CSP is essential to prevent XSS and data exfiltration.

## Fix
Add CSP headers in `firebase.json` hosting config:
```json
{
  "hosting": {
    "headers": [{
      "source": "**",
      "headers": [{
        "key": "Content-Security-Policy",
        "value": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://*.googleapis.com https://*.firebaseio.com"
      }]
    }]
  }
}
```

## Files
- `firebase.json`
