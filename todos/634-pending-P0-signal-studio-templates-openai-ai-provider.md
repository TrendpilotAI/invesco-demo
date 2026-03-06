---
id: 634
status: pending
priority: P0
repo: signal-studio-templates
title: Implement OpenAI AIProvider
effort: S (1 day)
dependencies: []
---

# Implement Concrete OpenAI AIProvider

## Problem
`AIProvider` is defined as an interface in `engine/template-engine.ts` but there is ZERO concrete implementation anywhere in the codebase. Calling `execute()` with `includeTalkingPoints: true` silently produces no talking points. This is demo-blocking for Invesco.

## Task
Create `src/providers/openai-ai-provider.ts` implementing the `AIProvider` interface using the OpenAI SDK.

## Coding Prompt
```
Create /data/workspace/projects/signal-studio-templates/src/providers/openai-ai-provider.ts

Implement the AIProvider interface from engine/template-engine.ts:
  interface AIProvider {
    generateTalkingPoints(prompt: string, data: Record<string, any>[]): Promise<string>;
  }

Requirements:
1. Use the `openai` npm package (add to dependencies)
2. Constructor takes apiKey and optional model (default: "gpt-4o")
3. generateTalkingPoints() should:
   - Format data rows as a compact JSON summary (top 5 rows max)
   - Call OpenAI chat completions with the template's talkingPointsPrompt
   - Return 3-5 bullet points of talking points for financial advisors
   - Handle errors gracefully (return empty string on failure, log error)
4. Export as named export: OpenAIAIProvider
5. Add to index.ts exports

Also create src/providers/mock-ai-provider.ts with pre-canned responses for testing.

Add types: @types/openai (if needed)
Run: pnpm add openai
```

## Acceptance Criteria
- [ ] `src/providers/openai-ai-provider.ts` exists and implements AIProvider
- [ ] Unit test in `__tests__/ai-provider.test.ts` with mocked OpenAI client
- [ ] Exported from `index.ts`
- [ ] `pnpm build` passes
- [ ] `pnpm test` passes
