# TODO-898: Add Branded 404 Page
**Repo:** signalhaus-website  
**Priority:** P0 (Quick Win)  
**Status:** pending  
**Effort:** 30 minutes

## Problem
The signalhaus-website has no `src/app/not-found.tsx`. Accessing any invalid URL returns Next.js's default unstyled 404 page, which:
- Has no SignalHaus branding
- Has no navigation to help users find what they want
- Looks unprofessional to prospects who find dead links
- Misses an opportunity to route lost visitors to contact/ROI calculator

## Task
Create a branded 404 page matching the site's dark theme.

## Coding Prompt
```tsx
// Create: /data/workspace/projects/signalhaus-website/src/app/not-found.tsx

import Link from 'next/link'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: '404 — Page Not Found | SignalHaus',
}

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="max-w-lg mx-auto text-center">
        {/* Large 404 */}
        <div className="text-8xl font-bold text-indigo-400 mb-4">404</div>
        <h1 className="text-3xl font-bold mb-4">Page Not Found</h1>
        <p className="text-gray-400 mb-8">
          Looks like this page took an unexpected detour. Let&apos;s get you back on track.
        </p>
        
        {/* Helpful links */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <Link
            href="/"
            className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold transition"
          >
            ← Back to Home
          </Link>
          <Link
            href="/contact"
            className="px-6 py-3 border border-gray-700 hover:border-indigo-500 rounded-xl font-semibold transition"
          >
            Book a Consultation
          </Link>
        </div>

        {/* Quick nav */}
        <div className="text-sm text-gray-500">
          <p className="mb-2">Or explore:</p>
          <div className="flex flex-wrap gap-3 justify-center">
            {[
              { label: 'Services', href: '/services' },
              { label: 'Case Studies', href: '/case-studies' },
              { label: 'Pricing', href: '/pricing' },
              { label: 'ROI Calculator', href: '/roi-calculator' },
              { label: 'Blog', href: '/blog' },
            ].map(link => (
              <Link key={link.href} href={link.href} className="text-indigo-400 hover:text-indigo-300 transition">
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
```

## Dependencies
- None — standalone page

## Acceptance Criteria
- Accessing `/this-page-does-not-exist` renders branded 404
- Page matches SignalHaus dark theme
- Links to homepage, contact, and key pages
- `npm run build` passes
