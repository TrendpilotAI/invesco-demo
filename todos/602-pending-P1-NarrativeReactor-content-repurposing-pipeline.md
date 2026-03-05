# TODO-602: Content Repurposing Pipeline — NarrativeReactor

**Priority:** P1 (Revenue Feature)
**Repo:** NarrativeReactor
**Effort:** 1.5 days
**Dependencies:** None

## Problem
Users must manually reformulate content for different platforms. One blog post should instantly become a Twitter thread, LinkedIn post, and newsletter snippet.

## Task
Add `POST /api/content/repurpose` endpoint that takes existing content and generates platform-specific variants in one call.

## Acceptance Criteria
- [ ] `POST /api/content/repurpose` accepts `{ content_id, formats: ['twitter_thread', 'linkedin', 'newsletter'] }`
- [ ] Returns all variants in a single response
- [ ] Each variant respects platform character limits (Twitter: 280/tweet, LinkedIn: 3000, Newsletter: no limit)
- [ ] Variants maintain brand voice (pull brand from content_id)
- [ ] All variants saved to content_library with `repurposed_from` reference
- [ ] Unit tests for the new service
- [ ] OpenAPI spec updated

## Agent Prompt
```
In /data/workspace/projects/NarrativeReactor:
1. Create src/services/contentRepurposer.ts with function repurposeContent(contentId, formats)
2. Fetch original content from contentLibrary by contentId
3. For each format in formats, generate a Genkit flow call with format-specific instructions:
   - twitter_thread: break into numbered tweets, each ≤280 chars
   - linkedin: professional tone, 1500-3000 chars, add CTA
   - newsletter: email-friendly, personal tone, include subject line
4. Save each variant to contentLibrary with parent_id = contentId
5. Add route in src/routes/index.ts: POST /api/content/repurpose
6. Add to OpenAPI spec in src/openapi.ts
7. Write tests in src/__tests__/services/contentRepurposer.test.ts
8. Run: npm test
```
