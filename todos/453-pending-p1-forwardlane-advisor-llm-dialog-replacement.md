# TODO 453 — forwardlane_advisor: Replace Watson NLC with Modern LLM

**Priority:** P1 | **Effort:** L | **Repo:** forwardlane_advisor

## Description
The hdialog module uses IBM Watson NLC (Natural Language Classifier) which is deprecated. Replace with Anthropic Claude or OpenAI GPT for vastly improved financial conversation capabilities.

## Full Coding Prompt
```
Replace IBM Watson NLC with a modern LLM in forwardlane_advisor's dialog engine.

Current Watson integration points:
- config/watson_services.js (connection config)
- app/nlc/ (NLC client)
- app/hdialog/ (dialog engine using Watson)
- watson-developer-cloud npm package

Migration steps:
1. Install Anthropic SDK: npm install @anthropic-ai/sdk
2. Create app/llm/llm_client.js:
   - Wrap Anthropic Claude API with same interface as Watson NLC
   - Support classify(text) -> {top_class, classes[]} response format
   - Support conversation(messages) -> response for dialog flows

3. Update app/hdialog/dialog.js:
   - Replace Watson classify calls with LLM-based intent detection
   - Map existing dialog intents to LLM prompts
   - Add system prompt with financial advisor context

4. Update app/hdialog/conversation_scenario_parser.js:
   - Ensure XML scenario parsing still works for dialog flows
   - Add LLM fallback for unrecognized intents

5. Add ANTHROPIC_API_KEY to environment config
6. Add streaming response support via SSE endpoint

7. Test with existing dialog scenarios in conversation_scenario.xml

Keep backward compatibility with existing dialog history records.
```

## Acceptance Criteria
- [ ] Watson NLC removed from dependencies
- [ ] Dialog conversations work with LLM backend
- [ ] Response quality meets or exceeds Watson NLC
- [ ] Streaming responses supported
- [ ] API key managed via environment variable

## Dependencies
- TODO 451, 452

## Estimated Effort
5-7 days
