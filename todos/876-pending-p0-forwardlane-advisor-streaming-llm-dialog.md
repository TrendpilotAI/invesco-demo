# TODO-876: Add Streaming SSE LLM Dialog Responses

**Repo:** forwardlane_advisor  
**Priority:** P0  
**Effort:** 3-4 days  
**Status:** pending  
**Created:** 2026-03-10

## Problem

The LLM gateway (`app/llm/gateway.js`) currently uses a request/response model — the full AI response is generated before sending anything to the client. For a financial advisor chatbot, this means users stare at a blank screen for 2-5 seconds before seeing any text. This is a critical UX deficiency compared to modern AI products.

## Solution

Implement Server-Sent Events (SSE) streaming for the dialog endpoint using the Anthropic streaming SDK and Express SSE:

1. **Modify `app/llm/gateway.js`** — add `classifyIntentStream(text, callback)` that uses Anthropic's `stream()` API
2. **Add SSE endpoint** in `app/hdialog/routes_hdialog.js` — `POST /api/dialog/stream` that streams tokens to client
3. **Update frontend** in `views/` — replace XHR with `EventSource` for dialog responses
4. **Add streaming tests** in `test/llm-gateway.test.js` — mock stream events

## Coding Prompt

```
In /data/workspace/projects/forwardlane_advisor/app/llm/gateway.js:

1. Add a new export `classifyIntentStream(text, onToken, onComplete, onError)` that:
   - Uses `anthropic.messages.stream()` from @anthropic-ai/sdk
   - Calls `onToken(chunk)` for each text delta
   - Calls `onComplete(finalIntent)` when done (parses final accumulated text for intent)
   - Falls back to OpenAI streaming via `openai.chat.completions.stream()` if Anthropic fails

2. In app/hdialog/routes_hdialog.js (or equivalent dialog router):
   - Add route: `router.post('/dialog/stream', requireAuth, (req, res) => {...})`
   - Set headers: `Content-Type: text/event-stream`, `Cache-Control: no-cache`, `Connection: keep-alive`
   - Use gateway.classifyIntentStream() to pipe tokens as `data: {token}\n\n`
   - Send `data: [DONE]\n\n` when complete

3. In views/hdialog/ (relevant Jade template):
   - Add JavaScript to connect via EventSource on dialog form submit
   - Append each token to the response container in real-time
   - Show typing indicator while streaming

4. Tests in test/llm-gateway.test.js:
   - Mock Anthropic stream: emit multiple text_delta events, then message_stop
   - Assert onToken called for each chunk
   - Assert onComplete called with final parsed intent
   - Test fallback to OpenAI stream when Anthropic throws
```

## Acceptance Criteria

- [ ] Dialog responses stream token-by-token in the browser
- [ ] Fallback to OpenAI streaming works if Anthropic fails
- [ ] Stream is aborted cleanly if client disconnects
- [ ] Rate limiting still applies per-user on the streaming endpoint
- [ ] Streaming tests pass with mocked Anthropic SDK

## Dependencies

- TODO-838 (Watson dead code removal) — clean up hdialog routes first
- TODO-875 (rate limiting) — apply rate limits before streaming

## Notes

Use Anthropic SDK `stream()` not `create()`. See:
```js
const stream = await anthropic.messages.stream({
  model: 'claude-3-haiku-20240307',
  max_tokens: 1024,
  messages: [{ role: 'user', content: text }]
});
for await (const chunk of stream) {
  if (chunk.type === 'content_block_delta') onToken(chunk.delta.text);
}
```
