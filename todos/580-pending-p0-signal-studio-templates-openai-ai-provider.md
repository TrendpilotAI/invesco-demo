# TODO 580: Implement Concrete OpenAI AIProvider

**Repo:** signal-studio-templates  
**Priority:** P0 (Critical — talking points will NEVER work without this)  
**Effort:** S (2–4 hours)  
**Status:** pending

## Description

`AIProvider` is defined as an interface but has **zero concrete implementations** anywhere in the codebase. The `execute()` method silently skips talking points generation when `aiProvider` is undefined. This means the core differentiator (AI talking points for advisors) doesn't work at all without a consumer implementing this themselves.

This is a P0 blocker for the Invesco demo — Craig Lieb explicitly wants "easy buttons" and talking points are the AI magic.

## Coding Prompt

```typescript
// Create: src/providers/openai-ai-provider.ts
import OpenAI from "openai";
import { AIProvider } from "../../engine/template-engine";

export class OpenAIProvider implements AIProvider {
  private client: OpenAI;
  
  constructor(apiKey?: string, private model = "gpt-4o-mini") {
    this.client = new OpenAI({ apiKey: apiKey ?? process.env.OPENAI_API_KEY });
  }

  async generateTalkingPoints(prompt: string, data: Record<string, any>[]): Promise<string> {
    const response = await this.client.chat.completions.create({
      model: this.model,
      messages: [
        { role: "system", content: "You are a financial advisor assistant. Generate concise, actionable talking points based on data provided. Focus on insights that help advisors have better client conversations." },
        { role: "user", content: `${prompt}\n\nData:\n${JSON.stringify(data.slice(0, 20), null, 2)}` }
      ],
      max_tokens: 500,
      temperature: 0.7,
    });
    return response.choices[0].message.content ?? "";
  }
}

// Also create: src/providers/mock-ai-provider.ts for testing/demo
export class MockAIProvider implements AIProvider {
  async generateTalkingPoints(prompt: string, data: Record<string, any>[]): Promise<string> {
    return `• ${data.length} records identified for attention\n• Consider reaching out to top opportunities this week\n• Review risk factors before next advisor meetings`;
  }
}
```

## Acceptance Criteria

- [ ] `src/providers/openai-ai-provider.ts` implements `AIProvider` interface
- [ ] `src/providers/mock-ai-provider.ts` for testing and demos
- [ ] Both exported from `index.ts`
- [ ] `openai` added to dependencies (`pnpm add openai`)
- [ ] Unit tests for MockAIProvider
- [ ] README updated with OpenAI provider setup
- [ ] API factory `createTemplateRouter()` accepts optional AIProvider or creates default from env

## Dependencies
- TODO 429 (DataProvider implementations)
