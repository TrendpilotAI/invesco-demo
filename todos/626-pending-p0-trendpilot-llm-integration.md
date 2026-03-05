# TODO 626: Trendpilot — Implement Real LLM Integration (AI Newsletter Generation)

**Priority:** P0 — Critical (this IS the product)
**Effort:** XL (3-5 days)
**Repo:** /data/workspace/projects/Trendpilot/
**Created:** 2026-03-05

## Problem
Trendpilot is marketed as "AI-powered newsletter generation" but zero OpenAI/Anthropic API calls exist anywhere in the codebase. The aggregator fetches trends but no AI summarization, writing, or curation happens. The core value proposition is not implemented.

## Dependencies
- None (can start immediately with API keys)
- TODO 229/236 (Supabase migration) should follow to persist generated content

## Acceptance Criteria
- [ ] `src/services/ai/summarizer.ts` — summarizes an article into 2-3 sentences
- [ ] `src/services/ai/writer.ts` — generates newsletter section copy from trend data
- [ ] `src/services/ai/curator.ts` — selects and orders topics for a digest
- [ ] `src/services/feedBuilder.ts` updated to call AI writer before email assembly
- [ ] AI generation triggered by scheduler when digest time fires
- [ ] LLM provider configurable via env: `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- [ ] Unit tests mocking LLM calls

## Full Coding Prompt

```
Implement LLM integration for Trendpilot newsletter generation at /data/workspace/projects/Trendpilot/

1. Add OpenAI dependency:
   cd /data/workspace/projects/Trendpilot && npm install openai

2. Create src/services/ai/client.ts:
   - Singleton OpenAI client initialized from process.env.OPENAI_API_KEY
   - Fallback error if key not set
   - Export: getAIClient()

3. Create src/services/ai/summarizer.ts:
   - Function: summarizeArticle(title: string, url: string, content: string): Promise<string>
   - Uses GPT-4o-mini with system prompt: "You are a concise tech journalist. Summarize in 2 sentences."
   - Returns the summary string

4. Create src/services/ai/writer.ts:
   - Function: generateNewsletterSection(topics: TrendResult[], tone: string): Promise<string>
   - Takes top 3-5 trending topics
   - Uses GPT-4o with prompt: "Write a newsletter section about these trending topics in {tone} tone"
   - Returns HTML string suitable for email

5. Create src/services/ai/curator.ts:
   - Function: curateTopics(topics: TrendResult[], userPreferences: string[]): Promise<TrendResult[]>
   - Uses GPT-4o-mini to rank/filter topics by relevance to preferences
   - Returns sorted array

6. Update src/services/feedBuilder.ts:
   - Import writer from services/ai/writer.ts
   - In buildFeed(), after aggregating trends, call writer.generateNewsletterSection()
   - Include AI-generated copy in the feed output

7. Add env vars to .env.example:
   OPENAI_API_KEY=sk-...
   AI_MODEL=gpt-4o-mini
   AI_TEMPERATURE=0.7

8. Write tests in tests/phase1/ai/:
   - Mock openai module
   - Test summarizer returns string
   - Test writer returns HTML
   - Test curator returns sorted array
```

## Risk
- API costs: budget ~$0.01-0.05 per newsletter at GPT-4o-mini rates
- Rate limits: add retry logic with exponential backoff
