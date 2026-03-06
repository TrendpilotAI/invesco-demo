# TODO-631: Content Performance Feedback Loop

**Repo:** NarrativeReactor  
**Priority:** P1  
**Effort:** 3 days  
**Status:** pending

## Description
Track published post engagement via Blotato webhooks and feed performance data back into AI generation prompts to continuously improve content quality.

## Acceptance Criteria
- [ ] Blotato webhook receiver for engagement events (likes, clicks, shares, impressions)
- [ ] Engagement data stored in SQLite performance_metrics table
- [ ] Performance score computed per content item (weighted engagement index)
- [ ] High-performing content surfaced in brand voice prompts as examples
- [ ] A/B variant tracking: create 2 variants per generation, track which performs better
- [ ] Performance dashboard route: GET /api/analytics/performance

## Coding Prompt
```
In /data/workspace/projects/NarrativeReactor:

1. Create src/services/engagementTracker.ts
   - Tables: engagement_events(id, content_id, platform, event_type, value, recorded_at)
   - Methods: recordEngagement, getTopPerformers(brandId, limit), getEngagementScore(contentId)

2. Add POST /webhooks/blotato in src/index.ts
   - Verify BLOTATO_WEBHOOK_SECRET signature
   - Parse event and call engagementTracker.recordEngagement

3. Modify src/flows/content-generation.ts
   - Before generating, fetch top 3 performers for the brand via engagementTracker.getTopPerformers
   - Inject examples into system prompt: "These posts performed well: ..."

4. Create A/B variant logic in contentPipeline.ts
   - generateVariants(prompt, n=2) — generate n content variants
   - Store all variants, track which gets published
   - Feed winner back as training example

5. Add GET /api/analytics/performance endpoint
```

## Dependencies
- TODO-599 (pino logging)
- Existing blotatoPublisher.ts service
