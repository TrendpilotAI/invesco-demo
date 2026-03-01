# TODO-343: AI Chat Streaming Implementation

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** M (4-8 hours)  
**Dependencies:** TODO-337, TODO-338

## Description
Chat page exists but likely shows no real streaming. Implement proper SSE/streaming for AI responses with typing indicators.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/src/app/(app)/chat/:

1. Read and understand current chat/page.tsx implementation

2. Create src/lib/api/chat-stream.ts:
   - streamChatMessage(message, conversationId?) → AsyncGenerator<string>
   - Uses fetch with ReadableStream reader
   - Parses SSE data: lines starting with "data: "

3. Update chat/page.tsx:
   - Message input at bottom with send button + Enter key submit
   - Messages list above (scroll to bottom on new message)
   - User messages on right, assistant on left with avatar
   - Typing indicator (animated dots) while streaming
   - Stream tokens into the assistant message as they arrive
   - Conversation selector on left sidebar (useChatConversations)
   - Context: show which signal the chat is about (if any)

4. Add markdown rendering for assistant messages:
   - npm install react-markdown
   - Code blocks with syntax highlighting

5. Add "New Conversation" button
```

## Acceptance Criteria
- [ ] Messages stream token-by-token
- [ ] Typing indicator while waiting for first token
- [ ] Conversations persist and are selectable
- [ ] Markdown rendered in responses
- [ ] Enter submits, Shift+Enter newline
