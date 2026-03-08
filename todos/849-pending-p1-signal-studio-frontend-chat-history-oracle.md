# TODO-849: Persist AI Chat History to Oracle

## Repo
signal-studio-frontend

## Priority
P1

## Description
AI chat sessions are currently ephemeral — all conversation history is lost on page reload. Users lose context between sessions, reducing the value of AI-powered signal analysis.

## Task
1. Create Oracle table `CHAT_SESSIONS` (session_id, user_id, created_at, updated_at)
2. Create Oracle table `CHAT_MESSAGES` (id, session_id, role, content, model, created_at)
3. Add DDL script to `scripts/sql/create-chat-tables.sql`
4. Implement `lib/oracle/chat-history.ts` with CRUD operations
5. Add API routes: `GET /api/chat/sessions`, `POST /api/chat/sessions`, `GET /api/chat/sessions/[id]/messages`
6. Wire chat UI to load/save session history
7. Add session list to chat sidebar

## Acceptance Criteria
- [ ] Chat history persists across page reloads
- [ ] Users can see their previous sessions in sidebar
- [ ] Old sessions load correctly with full message history
- [ ] Tests cover CRUD operations for chat history

## Effort
M (2-3 days)
