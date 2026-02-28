# 227 · NarrativeReactor · Publisher Service Consolidation

**Status:** pending  
**Priority:** medium  
**Project:** NarrativeReactor  
**Created:** 2026-02-27

---

## Task Description

NarrativeReactor has two publisher services: `blotatoPublisher.ts` (Blotato API) and `publisher.ts` (generic). These overlap in responsibility and have similar interfaces. Consolidate into a single `PublisherService` with a unified adapter pattern, supporting Blotato + future platforms (Buffer, Later, etc).

---

## Coding Prompt (agent-executable)

```
Working in /data/workspace/projects/NarrativeReactor/src/services/:

1. Audit both publisher files:
   - Read blotatoPublisher.ts and publisher.ts fully
   - Document overlapping functions and unique capabilities

2. Create src/services/publishers/types.ts:
   interface PublishTarget { platform: string; accountId: string; credentials?: Record<string, string> }
   interface PublishPayload { content: string; mediaUrls?: string[]; scheduledAt?: Date; metadata?: Record<string, unknown> }
   interface PublishResult { success: boolean; postId?: string; url?: string; error?: string }
   interface PublisherAdapter { name: string; publish(target: PublishTarget, payload: PublishPayload): Promise<PublishResult>; getStatus(postId: string): Promise<PublishResult> }

3. Create src/services/publishers/BlotatoAdapter.ts:
   - Implement PublisherAdapter
   - Move all Blotato-specific logic from blotatoPublisher.ts here
   - Use BLOTATO_API_KEY env var

4. Create src/services/publishers/PublisherService.ts:
   - Registry pattern: Map<string, PublisherAdapter>
   - registerAdapter(adapter: PublisherAdapter)
   - publish(platform: string, target: PublishTarget, payload: PublishPayload): Promise<PublishResult>
   - publishMulti(targets: Array<{platform: string} & PublishTarget>, payload: PublishPayload): Promise<PublishResult[]>
   - Integrates with caching layer from TODO-225 for rate limiting

5. Re-export from src/services/publishers/index.ts
   Mark blotatoPublisher.ts and publisher.ts as @deprecated with JSDoc

6. Update flows/integrations.ts to use new PublisherService

7. Create src/__tests__/services/publishers/PublisherService.test.ts with mocked BlotatoAdapter
```

---

## Dependencies

- 225 (Redis caching — for rate limit cache)

## Effort Estimate

6–8 hours

## Acceptance Criteria

- [ ] Single import path: `import { PublisherService } from './publishers'`
- [ ] BlotatoAdapter passes all existing blotatoPublisher tests
- [ ] Multi-platform publish works in parallel via Promise.allSettled
- [ ] Old files deprecated but not deleted (backward compat for 1 sprint)
- [ ] Test coverage > 80% on new publisher module
