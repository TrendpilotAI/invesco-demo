---
status: ready
priority: p2
issue_id: "003"
tags: [ai-agent, vercel-ai-sdk, tools, chat]
dependencies: ["001", "002"]
---

# Signal Agent Framework

## Problem Statement

Build an AI agent specialized for ForwardLane wholesalers that can analyze book of business, research clients, draft communications, and send via email/SMS.

## Findings

- Built system prompt with ForwardLane domain knowledge
- Created tool definitions: analyze_book, get_client_summary, draft_email, send_email, send_sms, get_morning_brief
- Designed chat UI component with quick actions
- Configured Twilio/Resend env vars in Railway

## Proposed Solutions

- **Chosen:** Use Vercel AI SDK for agent + chat UI
- Alternative: Mastra — deferred (too new, wait for 1.0)
- Alternative: LangChain — rejected (overkill for Node.js project)

## Recommended Action

Continue with Vercel AI SDK, wire Django auth, add Twilio/Resend keys.

## Acceptance Criteria

- [x] Create agent system prompt
- [x] Define agent tools
- [x] Build /api/agent endpoint
- [x] Create chat UI component
- [x] Add to Signal Studio
- [ ] Wire Django auth for user context
- [ ] Add Twilio credentials
- [ ] Add Resend API key
- [ ] Test full agent flow

## Work Log

### 2026-02-22 - Signal Agent Build

**By:** Honey AI

**Actions:**
- Created lib/agent/prompt.ts with system prompt
- Created lib/agent/tools.ts with tool definitions
- Built /api/agent/route.ts endpoint
- Created /api/agent/research for client data aggregation
- Created /api/agent/morning-brief for daily summaries
- Built components/agent/signal-agent-chat.tsx UI
- Added /agent page to Signal Studio
- Added Twilio/Resend env vars to Railway

**Results:** Agent framework deployed, needs credentials and auth wiring
