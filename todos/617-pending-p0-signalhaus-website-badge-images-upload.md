# TODO 617 — Upload Badge/Award Images to public/

**Repo:** signalhaus-website
**Priority:** P0
**Effort:** XS (30 minutes)
**Status:** pending

## Problem
`src/app/page.tsx` references 5 credential badge images in the `badges` array (Harvard Alumni, World Economic Forum Technology Pioneer, AWS Partner, AI Hot 100, AudienceLab) but NONE of these images exist in `public/`. This results in broken trust signals on the homepage.

## Task
1. Obtain or create badge images for:
   - Harvard Alumni (Nathan's credential)
   - World Economic Forum Technology Pioneer badge
   - AWS Partner logo
   - AI Hot 100 award badge
   - AudienceLab partner logo
2. Upload to `/public/badges/` directory
3. Update `src/app/page.tsx` badges array to use `next/image` with proper `src`, `width`, `height`, `alt` props
4. Test that all badges render correctly on homepage

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website/src/app/page.tsx:

1. Update the badges array to include src paths:
   const badges = [
     { name: "Harvard Alumni", src: "/badges/harvard-alumni.png", alt: "Harvard Alumni" },
     { name: "World Economic Forum", src: "/badges/wef-technology-pioneer.png", alt: "WEF Technology Pioneer" },
     { name: "AWS Partner", src: "/badges/aws-partner.png", alt: "AWS Partner" },
     { name: "AI Hot 100", src: "/badges/ai-hot-100.png", alt: "AI Hot 100" },
     { name: "AudienceLab", src: "/badges/audiencelab-partner.png", alt: "AudienceLab Partner" },
   ]

2. Update the badges rendering section to use next/image:
   import Image from "next/image"
   
   {badges.map((b) => (
     <div key={b.name} className="flex items-center justify-center">
       <Image src={b.src} alt={b.alt} width={120} height={60} className="opacity-70 hover:opacity-100 transition" />
     </div>
   ))}

3. Create /public/badges/ directory placeholder or ask Nathan to provide actual badge files
```

## Acceptance Criteria
- [ ] All 5 badge images display on homepage without 404 errors
- [ ] Images are using `next/image` for optimization
- [ ] Badges have proper alt text for accessibility
- [ ] Mobile: badges display in a 3-column grid or similar
