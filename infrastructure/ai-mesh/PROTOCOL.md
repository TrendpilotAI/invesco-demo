# AI Mesh — Agent Communication Protocol v1.0

## Overview

AI Mesh is an agent-to-agent communication protocol enabling autonomous agents to discover each other, exchange messages, share context, and delegate tasks.

## Architecture

```
┌─────────┐     ┌──────────────┐     ┌─────────┐
│ Agent A  │────▶│ Message Queue │◀────│ Agent B  │
└─────────┘     └──────────────┘     └─────────┘
      │                                     │
      ▼                                     ▼
┌──────────┐    ┌───────────────┐    ┌──────────┐
│ Registry │◀──▶│ Context Store  │◀──▶│ Registry │
└──────────┘    └───────────────┘    └──────────┘
                       │
                ┌──────────────┐
                │ Orchestrator  │
                └──────────────┘
```

## Message Types

| Type | Purpose |
|------|---------|
| `task_request` | Request an agent to perform work |
| `task_response` | Return results of completed work |
| `status_update` | Broadcast state changes |
| `capability_query` | Discover what agents can do |

## Message Schema

```typescript
interface Message {
  id: string;              // Unique message identifier
  type: MessageType;       // One of the four types above
  sender: string;          // Sender agent ID
  receiver: string;        // Receiver agent ID
  timestamp: number;       // Unix epoch ms
  payload: unknown;        // Arbitrary JSON payload
  correlationId: string;   // Links request/response pairs
  acknowledged: boolean;   // Delivery confirmation
}
```

## Agent Registry

Agents register with:
- **name** — unique identifier
- **capabilities** — list of skills (e.g., `["summarize", "translate"]`)
- **endpoint** — how to reach the agent
- **status** — `online | offline | busy`

Agents must send periodic heartbeats. After the configured timeout, agents are marked `offline` and excluded from capability queries.

## Context Store

A shared key-value store with:
- **Namespaces** — each agent gets a private namespace; `__global__` is shared
- **TTL** — optional time-to-live per entry
- **Last-write-wins** — no conflict resolution; latest write takes precedence

## Task Orchestration

1. **Submit** — a task with a required capability and priority
2. **Match** — orchestrator finds the best available agent
3. **Assign** — sends a `task_request` message
4. **Track** — task moves through states: `pending → assigned → in_progress → completed/failed`
5. **Retry** — failed tasks retry with exponential backoff up to `maxRetries`

### Priority Queue

Tasks are processed highest-priority-first. Equal priority tasks are FIFO.

### Retry & Backoff

Delay = `min(1000 * 2^(attempt-1), 30000)` ms

## Design Principles

1. **Simple** — in-memory, no external dependencies
2. **Extensible** — add new message types and capabilities freely
3. **Observable** — all state is inspectable via public APIs
4. **Decoupled** — agents communicate only through the protocol, never directly
