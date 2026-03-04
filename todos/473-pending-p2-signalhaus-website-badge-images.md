# TODO-473: Replace Placeholder Badge Divs with Real Logo Images

**Priority:** P2 (Medium)
**Effort:** S (1 hour)
**Repo:** signalhaus-website
**Status:** pending

## Problem

`src/app/page.tsx` renders social proof badges (Harvard Alumni, WEF, AWS Partner, AI Hot 100, AudienceLab) as styled `<div>` text elements. These look unpolished and reduce credibility vs real logo images.

## Agent Prompt

```
1. Download or source SVG/PNG logos for the 5 badges and place in /data/workspace/projects/signalhaus-website/public/badges/:
   - harvard-alumni.svg (or .png)
   - wef-technology-pioneer.svg
   - aws-partner.svg
   - ai-hot-100.svg
   - audiencelab.svg

   For logos that can't be found, create clean text-based SVG placeholders with the org's colors.

2. Update src/app/page.tsx badges section to use next/image:
```tsx
import Image from "next/image"

const badges = [
  { name: "Harvard Alumni", src: "/badges/harvard-alumni.svg", alt: "Harvard Alumni badge" },
  { name: "World Economic Forum", src: "/badges/wef-technology-pioneer.svg", alt: "WEF Technology Pioneer badge" },
  { name: "AWS Partner", src: "/badges/aws-partner.svg", alt: "AWS Partner badge" },
  { name: "AI Hot 100", src: "/badges/ai-hot-100.svg", alt: "AI Hot 100 award badge" },
  { name: "AudienceLab", src: "/badges/audiencelab.svg", alt: "AudienceLab partner badge" },
]

// In JSX:
{badges.map((badge) => (
  <div key={badge.name} className="flex items-center justify-center p-4 rounded-xl bg-white/5 border border-white/10">
    <Image src={badge.src} alt={badge.alt} width={120} height={40} className="opacity-80 hover:opacity-100 transition-opacity" />
  </div>
))}
```

3. Run: cd /data/workspace/projects/signalhaus-website && npx tsc --noEmit && npm run build
```

## Acceptance Criteria
- [ ] All 5 badges render as images (not text divs)
- [ ] Images use `next/image` for optimization
- [ ] Badge images are in `/public/badges/`
- [ ] Build succeeds
