# TODO-727: Social Sharing — TikTok & Instagram Share Cards

**Repo:** flip-my-era  
**Priority:** P1  
**Effort:** Medium (3-5 hours)  
**Status:** pending

## Description
FlipMyEra's primary audience is teens/Swifties on TikTok and Instagram. No social sharing is implemented. Shareable story cards would be the #1 growth channel.

## Coding Prompt
```
In /data/workspace/projects/flip-my-era/:

1. Create StoryShareCard component (src/modules/story/components/StoryShareCard.tsx)
   - OG-image style card: era title, first paragraph excerpt, illustrated cover image
   - Dimensions: 1080x1920 (TikTok/Reels) and 1080x1080 (square for IG)
   - Use html-to-image or canvas API to render as PNG

2. Add "Share" button to story completion screen
   - "Share to TikTok" — uses TikTok Web Share API or native share
   - "Share to Instagram" — uses Web Share API (mobile) or copy link
   - "Copy Link" — generates /story/{id} shareable URL

3. Create public story route (src/app/pages/StoryPublicPage.tsx)
   - Route: /story/:id
   - Shows story title, excerpt, era theme, cover image
   - CTA: "Create your own story at FlipMyEra"
   - No auth required to view
   - Add to react-router routes

4. Update Supabase RLS on ebooks table
   - Add is_public boolean column (default false)
   - When user clicks "Share", prompt to make public
   - Public stories visible without auth at /story/:id

5. Update sitemap.xml generation to include public stories
```

## Acceptance Criteria
- [ ] Story completion screen has Share button
- [ ] Share generates a 1080x1920 image card downloadable
- [ ] Public story page accessible at /story/:id without login
- [ ] Web Share API used on mobile for native sharing
- [ ] OG tags on public story page for link previews
