# TODO-569: Replace Watson NLC with Modern LLM Dialog Engine — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P0  
**Status:** pending

## Description
IBM Watson NLC is discontinued. Replace the entire hdialog conversation engine with a modern LLM (Claude 3.5 Sonnet or GPT-4o).

## Steps
1. Remove `watson-developer-cloud` from package.json
2. Install `@anthropic-ai/sdk` (or `openai`)
3. Refactor `app/hdialog/` to:
   - Route dialog queries through LLM API
   - Implement conversation history in MySQL (`dialog_history` table exists)
   - Add system prompt for financial advisory context
4. Implement SSE streaming for real-time response feel
5. Add `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` to env config
6. Update `app/hdialog/dialog_metrics_emmiter.js` and listener

## Coding Prompt for Agent
```
Refactor /data/workspace/projects/forwardlane_advisor/app/hdialog/ to replace Watson NLC with Anthropic Claude API.
Install @anthropic-ai/sdk. Create app/hdialog/llm_client.js that:
1. Takes user message + conversation history array
2. Calls Claude API with financial advisor system prompt
3. Returns streaming response via SSE
Preserve the dialog_history MySQL persistence (models/dialog_history.js).
Replace watson calls in app/hdialog/index.js with llm_client calls.
```

## Acceptance Criteria
- Dialog endpoints return LLM-generated responses
- Conversation history is persisted
- Streaming responses work in browser
- Watson SDK completely removed

## Dependencies
TODO-568 (Sequelize v6) — dialog_history model must work
