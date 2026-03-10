# 865 — Add HTTP Security Headers to next.config.mjs

**Repo:** signal-studio  
**Priority:** P0 — Critical Security  
**Effort:** 1 day  
**Status:** pending

## Problem
`next.config.mjs` has no `headers()` configuration. Missing all standard HTTP security headers:
- No Content-Security-Policy → XSS vulnerability
- No X-Frame-Options → clickjacking vulnerability
- No X-Content-Type-Options → MIME sniffing vulnerability
- No Strict-Transport-Security → downgrade attack vulnerability
- No Referrer-Policy → information leakage

## Exceptions
- `/easy-button/embed` already sets `X-Frame-Options: ALLOWALL` per-route (must remain as-is)

## Coding Prompt (for autonomous agent)
```typescript
// Edit /data/workspace/projects/signal-studio/next.config.mjs
// Add a headers() async function to nextConfig:

const nextConfig = {
  output: 'standalone',
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  serverExternalPackages: ['@xenova/transformers', 'onnxruntime-node', 'oracledb'],
  turbopack: {},
  experimental: {
    serverComponentsExternalPackages: ['oracledb'],
  },
  async headers() {
    return [
      {
        // Apply security headers to all routes
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
        ],
      },
      {
        // Apply stricter headers to non-embed routes
        source: '/((?!easy-button/embed).*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains',
          },
        ],
      },
      {
        // API routes get strict CSP
        source: '/api/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: "default-src 'none'; frame-ancestors 'none'",
          },
        ],
      },
    ]
  },
}
```

Note: Full CSP for pages requires careful audit of all script/style/image sources.
Start with headers that don't break functionality, then add CSP incrementally.

## Acceptance Criteria
- [ ] `curl -I https://[prod-url]/api/health` shows X-Content-Type-Options: nosniff
- [ ] `curl -I https://[prod-url]/` shows X-Frame-Options: SAMEORIGIN
- [ ] `curl -I https://[prod-url]/easy-button/embed` does NOT have X-Frame-Options: SAMEORIGIN (already has ALLOWALL)
- [ ] Lighthouse security audit shows improved score
- [ ] No visual regressions in UI

## Dependencies
- None (independent change)
