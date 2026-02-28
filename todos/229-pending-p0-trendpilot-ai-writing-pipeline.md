# TODO: Trendpilot — AI Writing Pipeline (Summarizer + Writer + Tone)

**Priority:** P0 — Core value proposition  
**Repo:** /data/workspace/projects/Trendpilot/  
**Effort:** 5-7 days  
**Dependencies:** None (requires OPENAI_API_KEY or ANTHROPIC_API_KEY env var)

## Description
The core Trendpilot value prop is "newsletters that write themselves." Currently, the platform aggregates and ranks trending topics but has ZERO LLM integration. The AI writing pipeline must be built:

1. **Summarizer service** — Given a topic + raw article snippets, produce a 2-3 sentence summary
2. **Writer service** — Given a list of summarized topics, produce a full newsletter section (intro, body, CTA)
3. **Tone system** — Apply tone presets (casual, professional, witty, analytical) to generated content
4. **Curator service** — Pick the top N topics for a given niche/audience profile

## Coding Prompt (Autonomous Execution)
```
In /data/workspace/projects/Trendpilot/src/services/, create:

1. src/services/ai/summarizer.ts
   - Function: summarizeTopic(topic: Topic, apiKey: string): Promise<string>
   - Uses OpenAI gpt-4o-mini with structured output
   - Returns 2-3 sentence summary optimized for newsletter readers
   - Handles rate limits with exponential backoff

2. src/services/ai/writer.ts
   - Function: writeNewsletter(topics: SummarizedTopic[], config: NewsletterConfig): Promise<NewsletterDraft>
   - NewsletterConfig: { tone: 'casual'|'professional'|'witty'|'analytical', niche: string, audienceSize: number }
   - Produces: { subject: string, previewText: string, sections: Section[], callToAction: string }
   - Uses streaming for large newsletters

3. src/services/ai/toneEngine.ts
   - Function: applyTone(content: string, tone: TonePreset): Promise<string>
   - Tone presets stored in src/config/tones.json

4. src/services/ai/curator.ts
   - Function: curateTopics(topics: Topic[], profile: UserProfile, limit: number): Topic[]
   - Scores topics by relevance to user niche using semantic similarity

5. Wire into scheduler (src/services/scheduler/index.ts):
   - After aggregation run: summarize → curate → write → store draft in Supabase

6. Add API routes in src/api/index.ts:
   - POST /api/newsletters/generate — trigger manual generation
   - GET /api/newsletters/:id/preview — preview draft HTML

7. Add tests in tests/phase-ai/:
   - summarizer.test.ts (mock OpenAI)
   - writer.test.ts
   - toneEngine.test.ts

Use OPENAI_API_KEY from env. Add to .env.example.
```

## Acceptance Criteria
- [ ] Can generate a newsletter from the latest aggregation run via API call
- [ ] Tone system produces noticeably different output for each preset
- [ ] Tests pass with mocked OpenAI responses
- [ ] Newsletter draft stored in Supabase (or JSON if Supabase migration pending)
- [ ] Subject line + preview text generated automatically
