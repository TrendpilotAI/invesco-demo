# TODO-350: Bundle Size Optimization

**Repo:** signal-studio-frontend  
**Priority:** P2  
**Effort:** S (2-3 hours)  
**Dependencies:** none

## Description
Next.js 15 with React 19 and lucide-react can have large bundles if not optimized. Audit and improve.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Install: npm install --save-dev @next/bundle-analyzer
2. Add to next.config.ts:
   const withBundleAnalyzer = require('@next/bundle-analyzer')({ enabled: process.env.ANALYZE === 'true' })
   module.exports = withBundleAnalyzer(nextConfig)

3. Run: ANALYZE=true npm run build — review output

4. Lucide React optimization:
   - Check if current imports use: import { Icon } from 'lucide-react' (fine for tree-shaking)
   - Ensure NOT using: import * as Icons from 'lucide-react'

5. Dynamic imports for heavy pages:
   - Signal builder (React Flow) → dynamic(() => import('@/components/signal-builder/SignalCanvas'), { ssr: false })
   - Admin page → dynamic import

6. Check for any large dependencies imported in layout (affects all pages)

7. Enable Next.js experimental features if helpful:
   - optimizePackageImports: ['lucide-react', '@radix-ui/react-icons']
   (Add to next.config.ts experimental block)

8. Image optimization: grep for raw <img> tags and replace with next/image
```

## Acceptance Criteria
- [ ] Bundle analyzer integrated
- [ ] No route > 200KB first load JS
- [ ] Dynamic imports for signal builder
- [ ] No raw <img> tags
