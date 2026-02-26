---
module: Signal Studio
date: 2026-02-22
problem_type: ai_agent_development
component: signal_agent
symptoms:
  - "Needed AI agent that understands ForwardLane data"
  - "Wholesalers need book analysis, client research, email drafting"
root_cause: no_specialized_agent
severity: medium
tags: [ai-agent, vercel-ai-sdk, tools, chat, automation]
---

# Signal Agent Framework

## Problem

Build an AI agent specialized for ForwardLane wholesalers that can:
- Analyze book of business
- Research clients before calls
- Draft personalized communications
- Send via email/SMS

## Investigation

1. Built system prompt with ForwardLane domain knowledge
2. Created tool definitions for agent actions
3. Designed chat UI for interaction

## Failed Attempts

- **Attempt 1:** Generic GPT-4 prompt → Didn't know ForwardLane data structure
- **Attempt 2:** No tools → Agent couldn't take actions
- **Attempt 3:** LangChain too heavy → Vercel AI SDK simpler

## Solution

### 1. System Prompt
```typescript
// lib/agent/prompt.ts
export const SIGNAL_AGENT_SYSTEM_PROMPT = `You are Signal Agent, the AI assistant 
inside ForwardLane's Signal Studio. You help financial wholesalers manage 
advisor relationships.

You have access to:
- Analytical database (holdings, transactions, Invesco data)
- ML recommendations (risk, opportunity, upsell scores)
- CRM notes (meeting history)
- Email/SMS sending (when configured)

Example:
User: "How's my book?"
You: "3 high-priority: (1) Smith - 26% AUM decline, (2) Chen - cross-sell opp..."
`
```

### 2. Tool Definitions
```typescript
const SIGNAL_AGENT_TOOLS = [
  { name: "analyze_book", description: "Generate SQL queries..." },
  { name: "get_client_summary", description: "Research specific client..." },
  { name: "draft_email", description: "Generate personalized email..." },
  { name: "send_email", description: "Send via Resend (when configured)" },
  { name: "send_sms", description: "Send via Twilio (when configured)" },
  { name: "get_morning_brief", description: "Daily priority summary" },
]
```

### 3. API Endpoints
```
POST /api/agent          - Main agent chat
GET  /api/agent         - Capabilities
POST /api/agent/research     - Client research
POST /api/agent/morning-brief - Daily brief
```

### 4. Chat UI
```typescript
// components/agent/signal-agent-chat.tsx
// Quick actions:
// - "How's my book doing?"
// - "Research client 1"
// - "Draft an email about AUM decline"
// - "What's my morning brief?"
```

## Tested Examples

**"Show me advisors with declining AUM"** → Returns signal with SQL
**"Research client 1"** → Aggregates: holdings + signals + CRM + ML scores
**"Morning brief"** → Risk accounts + opportunities summary

## Prevention

- Keep agent domain-specific (don't generalize)
- Test tools individually before agent integration
- Add observability for debugging

## Related Issues

- See also: railway-signal-studio-fullstack-deployment
- See also: nl-sql-signal-generation

## Future Enhancements

- Add Twilio SMS (credentials configured)
- Add Resend email (needs API key)
- Wire to Django auth for user context
- Morning brief automation via Celery Beat
