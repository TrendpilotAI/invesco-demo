# Honey iOS — Design Brief
**Version:** 1.0  
**Date:** 2026-02-24  
**Status:** Draft  
**Author:** Honey 🍯 (design research subagent)

---

## Table of Contents
1. [Vision & North Star](#1-vision--north-star)
2. [Research Findings](#2-research-findings)
3. [Feature Specification](#3-feature-specification)
4. [UI/UX Principles](#4-uiux-principles)
5. [Visual Design System](#5-visual-design-system)
6. [Interaction Patterns](#6-interaction-patterns)
7. [Screen Inventory](#7-screen-inventory)
8. [Architecture Diagram](#8-architecture-diagram)
9. [Tech Stack Recommendation](#9-tech-stack-recommendation)
10. [Implementation Roadmap](#10-implementation-roadmap)

---

## 1. Vision & North Star

> **"Your AI command center, always in your pocket."**

Honey iOS is not another chat app. It is Nathan's mission control for a living, breathing AI infrastructure — 42+ projects, dozens of running agents, cron jobs, services, and deployments all visible and controllable from one beautifully designed, voice-first iOS app.

### What Makes It Different from ChatGPT/Claude Mobile

| Feature | ChatGPT | Claude | Honey iOS |
|---------|---------|--------|-----------|
| Single-thread chat | ✅ | ✅ | ✅ |
| Multi-agent visibility | ❌ | ❌ | ✅ |
| Cron job monitoring | ❌ | ❌ | ✅ |
| Service health dashboard | ❌ | ❌ | ✅ |
| Voice-first, hands-free | Partial | ❌ | ✅ |
| Push alerts for agent events | ❌ | ❌ | ✅ |
| Quick-fire task dispatch | ❌ | ❌ | ✅ |
| Project scorecard (42 projects) | ❌ | ❌ | ✅ |
| Real-time streaming agents | ❌ | ❌ | ✅ |

### Personas

**Primary: Nathan (Owner/Operator)**
- Moving fast between tasks all day
- Needs quick status checks while away from desk
- Voice commands while driving, walking, cooking
- Wants push alerts before they become fires
- Power user — comfortable with technical depth

**Secondary: Future Team Members**
- Delegated access to specific projects/agents
- Read-only dashboards

---

## 2. Research Findings

### Competitive Analysis

**ChatGPT iOS (★4.9 — 5.8M ratings)** — The gold standard for AI chat UX:
- **Advanced Voice Mode**: Real-time waveform orb, interruption handling, emotion detection
- Seamless text/voice mode switching in one tap
- Streaming text rendering with smooth token-by-token animation
- Clean empty state with task-type pickers (Write, Code, Analyze, etc.)
- History sidebar with search
- **Weakness**: No agent/infra visibility whatsoever; single-model-single-thread

**Perplexity (★4.8 — 421K ratings)** — Premium search-meets-AI feel:
- Source citations inline with answer streaming
- Focus modes (web, academic, social) visible in UI
- Slick input bar with microphone, image, and attachment buttons
- Discovery/trending section in home tab
- **Weakness**: Not agentic, no task dispatch

**Claude by Anthropic (★4.7 — 52K ratings)** — Most "thoughtful" feel:
- Code blocks with syntax highlighting, copy button
- Project/context sidebar
- Markdown rendering, tables, LaTeX
- **Weakness**: No voice, no agent monitoring

### Key Design Patterns from Top Apps

#### Streaming Text
- Token-by-token render with trailing cursor blink (3px wide, brand color)
- Bubble height auto-expands using spring animation (damping 0.8, response 0.4)
- No jank — use `LazyVStack` with pinned bottom anchoring, not `ScrollView` offset hacks
- Thinking/reasoning block collapsible (shows duration: "thought for 4s ▸")

#### Voice Input/Output
- ChatGPT's orb model: animated gradient sphere that morphs with audio amplitude
- Three states: idle (small orb), listening (expands + waveform rings), speaking (pulses outward)
- Haptic feedback: `.impactFeedback(.medium)` on voice start, `.notificationFeedback(.success)` on stop
- Wake word option ("Hey Honey") via `SFSpeechRecognizer`

#### Quick Actions
- Bottom input bar swipe-up expands slash command palette
- Recently used commands pinned at top
- `⌘K` keyboard shortcut pops command palette (iPadOS)

#### Session Management
- Left sidebar (iPad) or swipe-right from edge (iPhone)
- Sessions grouped: Today, Yesterday, Last 7 Days, Older
- Session preview: first 60 chars of first user message
- Swipe-left on session: Archive, Pin, Delete

---

## 3. Feature Specification

### 3.1 Core Chat

| Feature | Priority | Description |
|---------|----------|-------------|
| Streaming text chat | P0 | SSE/WebSocket streaming, token-by-token render |
| Voice input | P0 | Tap mic → `AVAudioSession` → Deepgram STT |
| Voice output | P0 | Fish Audio TTS with Nathan's preferred voice |
| Model switcher | P0 | Kimi K2 / Claude Sonnet / GPT-4o / Deepseek |
| Image attachment | P1 | Photo library + camera, passed as base64 |
| File attachment | P1 | iCloud Drive, Files app, PDF/code/text |
| Code blocks | P1 | Syntax highlighting (Highlight.js via WKWebView or native) |
| Markdown render | P1 | Tables, headers, bold, lists, LaTeX |
| Message reactions | P2 | Copy, regenerate, edit, thumb up/down |
| Multi-turn editing | P2 | Tap any message to edit + re-run from that point |

### 3.2 Agent Monitor (The Killer Feature)

> View all running sub-agents in real-time — like `htop` but for AI agents.

| Feature | Priority | Description |
|---------|----------|-------------|
| Live agent list | P0 | Active agents with elapsed time + status |
| Agent detail view | P0 | Full streaming output, tool calls, cost |
| Steer agent | P0 | Send mid-session steering message |
| Kill agent | P0 | Terminate with confirmation modal |
| Spawn agent | P0 | Quick-dispatch from mobile |
| Agent history | P1 | Past 7 days of completed/failed agents |
| Agent cost tracking | P1 | Per-agent token cost + cumulative daily |
| Drift score badge | P1 | 0-10 drift indicator from drift correction system |

### 3.3 Cron Job Monitor

| Feature | Priority | Description |
|---------|----------|-------------|
| Cron list | P0 | All scheduled jobs, next run time |
| Last run status | P0 | ✅/❌ with elapsed time + exit code |
| Run history | P1 | Last 20 runs per job, sparkline of success rate |
| Manual trigger | P1 | Run now button with confirmation |
| Mute alerts | P2 | Silence a flappy job for N hours |

### 3.4 Project Dashboard

> 42 projects at a glance with health scores.

| Feature | Priority | Description |
|---------|----------|-------------|
| Project grid | P0 | Card grid (2-col), color-coded health |
| Health score | P0 | 0-100 score per project (test pass rate, uptime, deploy age) |
| Quick actions | P0 | Tap project → recent agents, last deploy, chat about it |
| Score history | P1 | 7-day sparkline per project |
| Filter/sort | P1 | By status, language, last activity |
| Deploy status | P1 | Railway/Netlify/Firebase deploy badges |

### 3.5 Service Health

| Feature | Priority | Description |
|---------|----------|-------------|
| Service list | P0 | All services with up/down badge |
| Response time | P0 | Last ping latency |
| Uptime sparkline | P1 | 24h uptime bar chart |
| Push on down | P0 | Immediate push notification when service drops |
| Quick restart | P2 | Trigger Railway redeploy |

### 3.6 Push Notifications

| Category | Priority | Example |
|----------|----------|---------|
| Agent completed | P0 | "Research agent finished: 3 findings saved" |
| Agent failed | P0 | "⚠️ Build agent failed after 8 min" |
| Service down | P0 | "🔴 Postiz is down (502)" |
| Service restored | P1 | "✅ Postiz is back online" |
| Cron failure | P1 | "Cron 'daily-summary' failed" |
| Budget alert | P2 | "Daily API spend: $8.40 (80% of limit)" |

Notifications use APNs with rich payloads — include action buttons (View, Dismiss, Fix It).

### 3.7 Voice Commands ("Hey Honey")

Quick-fire commands Nathan needs most:
```
"What are my running agents?"
"Check services"
"Fix the build"  → spawns build-fixing agent
"Check services" → shows dashboard
"What happened overnight?" → queries agent history
"How much have I spent today?"
"Summarize the second-opinion project"
"Deploy FlipMyEra"
```

Hands-free flow: wake word → brief haptic → speak → Honey responds verbally + shows result card.

---

## 4. UI/UX Principles

### 4.1 Speed Is the Feature
Every interaction must feel instant:
- **Optimistic UI**: Message appears in bubble immediately; API call fires in background
- **Skeleton screens**: 200ms shimmer before any data loads (never blank screens)
- **Prefetch next token**: Begin TTS synthesis of first sentence while rest streams in
- **Background refresh**: `BGAppRefreshTask` to refresh agent/service status every 15 min
- **Haptic confirmation**: Every button tap that triggers work gets `.impactFeedback(.light)`

### 4.2 Information Without Overwhelm
Nathan is a power user, but mobile screen real estate is precious:
- **Progressive disclosure**: Show top 3 items → "See all 42" expansion
- **Status-first design**: Color + icon conveys status before reading text
- **Contextual depth**: Tap to go deeper; default view is scannable
- **Dismiss is always easy**: Swipe down on sheets, tap anywhere outside modals

### 4.3 Voice as First-Class
The app works equally well with eyes-off:
- All screens have audio summary available ("Read this screen")
- Navigation responds to voice via accessibility labels + custom voice actions
- CarPlay-optimized mode for driving scenarios

### 4.4 Reliability Aesthetics
The app should feel as dependable as the infrastructure it monitors:
- **Errors are explicit**: Never swallow errors silently; always show what failed and what to do
- **Stale data is labeled**: Show "Last updated 3 min ago" when live data fails
- **Offline mode**: Core content cached; badge shows "Offline" clearly

### 4.5 Delight Without Distraction
Micro-interactions that reward, not distract:
- Agent completion → satisfying check animation + haptic
- Service coming back online → green pulse animation
- Long-press actions with haptic preview (like 3D Touch feel)
- Success states use the bee/honey color palette

---

## 5. Visual Design System

### 5.1 Color Palette

```
┌─────────────────────────────────────────────────────────┐
│  HONEY DESIGN SYSTEM — COLOR TOKENS                      │
├──────────────────┬──────────────────┬───────────────────┤
│  Token           │  Light Mode      │  Dark Mode        │
├──────────────────┼──────────────────┼───────────────────┤
│  brand.primary   │  #F5A623 (honey) │  #F5A623          │
│  brand.secondary │  #FF8C00 (amber) │  #FFB347 (lighter)│
│  brand.accent    │  #FF6B35 (fire)  │  #FF8C61          │
├──────────────────┼──────────────────┼───────────────────┤
│  bg.primary      │  #FFFFFF         │  #0A0A0B          │
│  bg.secondary    │  #F5F5F7 (Apple) │  #1C1C1E          │
│  bg.tertiary     │  #EBEBEB         │  #2C2C2E          │
│  bg.elevated     │  #FFFFFF         │  #3A3A3C          │
├──────────────────┼──────────────────┼───────────────────┤
│  text.primary    │  #000000         │  #F2F2F7          │
│  text.secondary  │  #3C3C43 (60%)   │  #EBEBF5 (60%)    │
│  text.tertiary   │  #3C3C43 (30%)   │  #EBEBF5 (30%)    │
├──────────────────┼──────────────────┼───────────────────┤
│  status.healthy  │  #34C759         │  #30D158          │
│  status.warning  │  #FF9500         │  #FF9F0A          │
│  status.error    │  #FF3B30         │  #FF453A          │
│  status.neutral  │  #8E8E93         │  #636366          │
├──────────────────┼──────────────────┼───────────────────┤
│  agent.running   │  #5AC8FA (blue)  │  #64D2FF          │
│  agent.done      │  #34C759 (green) │  #30D158          │
│  agent.failed    │  #FF3B30 (red)   │  #FF453A          │
│  agent.idle      │  #8E8E93 (gray)  │  #636366          │
└──────────────────┴──────────────────┴───────────────────┘
```

**Dark Mode First**: The primary design target is dark mode. It's where power users live, it's premium, and it's aesthetically aligned with a monitoring/ops tool.

### 5.2 Typography

Using **SF Pro** (system font — zero bundle overhead, perfect Dynamic Type support):

```
Display:   SF Pro Display,  32pt, weight .bold,    tracking -0.5
Title1:    SF Pro Display,  28pt, weight .semibold, tracking -0.3
Title2:    SF Pro Text,     22pt, weight .semibold, tracking -0.2
Title3:    SF Pro Text,     20pt, weight .semibold
Headline:  SF Pro Text,     17pt, weight .semibold
Body:      SF Pro Text,     17pt, weight .regular
Callout:   SF Pro Text,     16pt, weight .regular
Subhead:   SF Pro Text,     15pt, weight .regular
Footnote:  SF Pro Text,     13pt, weight .regular
Caption1:  SF Pro Text,     12pt, weight .regular
Caption2:  SF Pro Text,     11pt, weight .regular
Code:      SF Mono,         14pt, weight .regular,  tracking 0
```

Always use `scaledFont()` / `@ScaledMetric` for Dynamic Type compliance.

### 5.3 Spacing System (4pt grid)

```
xxs:  4pt   — tight label gaps
xs:   8pt   — small padding
sm:   12pt  — compact section padding
md:   16pt  — standard content padding
lg:   24pt  — section separators
xl:   32pt  — major layout gaps
xxl:  48pt  — hero/splash spacing
```

### 5.4 Corner Radii

```
small:  8pt   — chips, badges, pills
medium: 12pt  — cards, cells
large:  16pt  — input fields, primary buttons
xl:     20pt  — full sheets, featured cards
pill:   999pt — action buttons, status badges
```

### 5.5 Shadow & Depth (Dark Mode)

Instead of drop shadows (which don't work well in dark mode), use:
- **Layered backgrounds**: `bg.primary` → `bg.secondary` → `bg.elevated`
- **Subtle border**: `Color.white.opacity(0.08)` 1pt border on elevated cards
- **Ambient glow for status**: Running agent cards get a subtle `brand.primary.opacity(0.15)` glow
- For agent orb: radial gradient glow using `brand.primary` color

### 5.6 Iconography

Use **SF Symbols 5** exclusively:
- Fill variants for status indicators (consistent visual weight)
- Multicolor where meaningful (green ✅, red ⚠️)
- Custom symbols for Honey branding (bee, hexagon)

Key icon mapping:
```
chat.message.fill     → conversation
waveform              → voice mode
timer.fill            → cron jobs
cpu.fill              → agents
network               → services
square.grid.2x2.fill  → projects
bell.fill             → notifications
play.fill             → run/start
stop.fill             → terminate
arrow.clockwise       → retry/refresh
```

### 5.7 Animation Principles

**Spring Physics (all animations)**:
```swift
// Standard interactive
.spring(response: 0.35, dampingFraction: 0.7, blendDuration: 0)

// Playful/celebratory
.spring(response: 0.5, dampingFraction: 0.6, blendDuration: 0)

// Snappy/UI feedback
.spring(response: 0.25, dampingFraction: 0.85, blendDuration: 0)
```

**Timing curves for non-spring**:
- Enter: `.easeOut(duration: 0.2)`
- Exit: `.easeIn(duration: 0.15)`
- Status change: `.easeInOut(duration: 0.3)`

**Streaming text**: Characters render with `opacity` 0→1, `offset` y: 4→0, staggered 20ms per word group. Don't animate individual characters (performance killer).

---

## 6. Interaction Patterns

### 6.1 Chat Input Bar

```
┌─────────────────────────────────────────────────┐
│  ┌──────────────────────────────┐  🎤  ↑        │
│  │  Message Honey…              │               │
│  └──────────────────────────────┘               │
└─────────────────────────────────────────────────┘
        ↑ tap mic           ↑ send (enabled when text)
```

**State machine**:
- **Empty**: mic icon visible (tappable), send hidden
- **Typing**: send icon appears with spring scale animation, mic hidden
- **Recording**: input bar morphs to voice mode (see below)
- **Sending**: send button spins, input disabled, optimistic bubble added
- **Streaming**: status text "Honey is thinking…" below input bar

**Swipe up on input bar** → slash command palette slides up:
```
/ run-agent   Run a new sub-agent
/ check       Check a service
/ status      Full system status
/ fix         Fix something (quick dispatch)
/ summarize   Summarize a project
/ deploy      Trigger deployment
[custom templates pinned at top]
```

### 6.2 Voice Mode

**Entry**: Tap microphone → input bar morphs (200ms spring) into full-width voice bar:

```
┌─────────────────────────────────────────────────┐
│          🎤  LISTENING…                          │
│     ▁▃▅▇▅▃▁▃▅▃▁  (waveform visualization)       │
│     [tap to stop]    [tap to cancel]             │
└─────────────────────────────────────────────────┘
```

Waveform: 20 bars, heights driven by `AVAudioRecorder.averagePower(forChannel:)`, updated at 30fps using `CADisplayLink`. Bars animate with `.spring(response: 0.15, dampingFraction: 0.5)`.

**Honey Speaking**: Animated orb (90pt diameter):
```
         ╭─────────╮
        /  (honey   \     ← radial gradient pulse
       |   orb 🍯)   |       synced to TTS amplitude
        \  animated /
         ╰─────────╯
```
- Idle: subtle breathing scale (0.95→1.05, 2s cycle)
- Speaking: amplitude-driven scale + glow radius
- Done: shrinks back with bounce

### 6.3 Agent Monitor Live Feed

```
┌─────────────────────────────────────────────────┐
│  🤖 RUNNING AGENTS (3)            [+ New Agent]  │
├─────────────────────────────────────────────────┤
│  ●  research-ios-design           12:34 elapsed  │
│     "Searching GitHub for SwiftUI patterns…"     │
│     Drift: ▓▓▓░░ 3/10   Cost: $0.12  [Steer][✕] │
├─────────────────────────────────────────────────┤
│  ●  fix-build-agent                0:47 elapsed  │
│     "Analyzing error in main.swift:47…"          │
│     Drift: ▓░░░░ 1/10   Cost: $0.03  [Steer][✕] │
├─────────────────────────────────────────────────┤
│  ●  daily-summary                  2:03 elapsed  │
│     "Reading memory files…"                      │
│     Drift: ▓▓░░░ 2/10   Cost: $0.08  [Steer][✕] │
└─────────────────────────────────────────────────┘
```

**Tap on agent** → full-screen agent detail:
- Full streaming log with auto-scroll (with "jump to bottom" FAB when scrolled up)
- Tool call accordion: expand to see each tool call + arguments + result
- Real-time token count + cost ticker
- Steer modal: text input with AI suggestions for common corrections

**WebSocket connection** to OpenClaw gateway for live streaming updates. Reconnect with exponential backoff on disconnect.

### 6.4 Project Dashboard

**Grid view** (2 columns, scrollable):
```
┌───────────────┐ ┌───────────────┐
│ FlipMyEra     │ │ Trendpilot    │
│  ████████░░   │ │  ██████████   │
│  Score: 84    │ │  Score: 96    │
│  ✅ Netlify   │ │  🔵 Local     │
│  2h ago       │ │  1d ago       │
└───────────────┘ └───────────────┘
┌───────────────┐ ┌───────────────┐
│ NarrativeRx   │ │ Second-Opin.  │
│  ████████████ │ │  ████░░░░░░   │
│  Score: 100   │ │  Score: 42    │
│  ✅ Modal     │ │  ⚠️ Building  │
│  5h ago       │ │  Active       │
└───────────────┘ └───────────────┘
```

Score color coding:
- 80-100: `status.healthy` (green)
- 60-79: `status.warning` (orange)
- 0-59: `status.error` (red)

**Score calculation** (server-side, surfaced in API):
```
score = (test_pass_rate × 40) + (uptime_7d × 30) + (deploy_age_score × 20) + (lint_score × 10)
```

### 6.5 Quick Actions (Home Screen Widget + Lock Screen)

**Widget sizes**:
- Small (2×2): Honey orb + "3 agents running" status
- Medium (4×2): Top 3 agents + quick action buttons
- Large (4×4): Full dashboard summary

**Lock Screen widget**: Service health summary (red/green dots for top 5 services)

**Dynamic Island** (iPhone 14+):
- Show active agent count in compact mode
- Expand to show current agent activity + elapsed time
- Tap to open Honey directly to agent monitor

---

## 7. Screen Inventory

### Tab Bar (5 tabs)

```
┌──────┬──────┬──────┬──────┬──────┐
│  💬   │  🤖   │  ⏰   │  📊   │  ⚙️  │
│ Chat  │Agents│ Cron │Dash  │ More │
└──────┴──────┴──────┴──────┴──────┘
```

### Screen List

| # | Screen | Tab | Priority |
|---|--------|-----|----------|
| 1 | Chat Home (conversation list) | Chat | P0 |
| 2 | Chat Thread | Chat | P0 |
| 3 | Voice Mode overlay | Chat | P0 |
| 4 | Model Picker sheet | Chat | P0 |
| 5 | Slash Command Palette | Chat | P1 |
| 6 | Agent Monitor (live list) | Agents | P0 |
| 7 | Agent Detail (streaming log) | Agents | P0 |
| 8 | Agent Steer Modal | Agents | P0 |
| 9 | Spawn Agent sheet | Agents | P1 |
| 10 | Agent History | Agents | P1 |
| 11 | Cron Job List | Cron | P0 |
| 12 | Cron Job Detail + History | Cron | P1 |
| 13 | Project Dashboard Grid | Dash | P0 |
| 14 | Project Detail | Dash | P0 |
| 15 | Service Health List | Dash | P0 |
| 16 | Service Detail | Dash | P1 |
| 17 | Push Notification Settings | More | P1 |
| 18 | API + Connection Settings | More | P0 |
| 19 | Budget / Cost Tracking | More | P2 |
| 20 | Onboarding flow (3 screens) | — | P0 |

### Key Empty States

| Screen | Empty State Message | Action |
|--------|--------------------|----|
| Chat Home | "Start talking to Honey" + large orb | Tap to begin |
| Agent Monitor | "No agents running" + idle orb | + New Agent |
| Cron Jobs | "No cron jobs configured" | Link to docs |
| Project Dashboard | "No projects tracked" | Link to TOOLS.md |

### Loading States
- All lists: 4-item skeleton with shimmer (200ms delay before showing)
- Agent log: pulsing "thinking…" indicator at bottom
- Service ping: spinner badge on service icon

---

## 8. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HONEY iOS APP                                │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  ┌──────────┐  │
│  │   ChatView  │  │ AgentMonitor│  │  CronMonitor  │  │Dashboard │  │
│  │             │  │             │  │              │  │          │  │
│  │ SwiftUI     │  │ SwiftUI     │  │  SwiftUI      │  │ SwiftUI  │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘  └────┬─────┘  │
│         │                │                │               │         │
│  ┌──────▼────────────────▼────────────────▼───────────────▼──────┐  │
│  │                    App Store Layer (ViewModels)                 │  │
│  │   ChatViewModel  AgentViewModel  CronViewModel  DashViewModel  │  │
│  │                  @MainActor, ObservableObject                   │  │
│  └──────────────────────────┬─────────────────────────────────────┘  │
│                             │                                        │
│  ┌──────────────────────────▼─────────────────────────────────────┐  │
│  │                      Service Layer                              │  │
│  │                                                                 │  │
│  │  ┌───────────────┐  ┌──────────────┐  ┌──────────────────────┐ │  │
│  │  │  HoneyAPI     │  │ WebSocket    │  │  LocalCache          │ │  │
│  │  │  (REST client)│  │ (live stream)│  │  (CoreData/SwiftData)│ │  │
│  │  │  URLSession   │  │ Starscream   │  │                      │ │  │
│  │  └───────┬───────┘  └──────┬───────┘  └────────────────────── ┘ │  │
│  └──────────┼─────────────────┼──────────────────────────────────┘  │
│             │                 │                                      │
│  ┌──────────▼─────────────────▼──────────────────────────────────┐  │
│  │              Platform Services Layer                            │  │
│  │  APNs     AVFoundation   SFSpeech   WidgetKit  Dynamic Island  │  │
│  │  (push)   (TTS/audio)    (STT)      (widgets)  (Live Activity) │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS / WSS
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                     OPENCLAW GATEWAY                                  │
│                                                                       │
│  ┌────────────┐  ┌───────────┐  ┌───────────────┐  ┌─────────────┐ │
│  │ Chat API   │  │ Agent API │  │  Cron API      │  │ Health API  │ │
│  │ /v1/chat   │  │ /v1/agents│  │  /v1/cron      │  │ /v1/health  │ │
│  │ (SSE)      │  │ (WS live) │  │               │  │            │ │
│  └────────────┘  └───────────┘  └───────────────┘  └─────────────┘ │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                  REDIS EVENT BUS                                 │  │
│  │   honey.agent.* | honey.cron.* | honey.service.* | honey.deploy│  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  OpenClaw Agent Runtime ←→ Subagents ←→ Temporal.io                  │
│  Railway Services ←→ Health Monitor ←→ Event Publisher               │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Flow: Chat Message

```
User types → [optimistic bubble added] → ViewModel.sendMessage()
    → HoneyAPI.streamChat(messages:)
    → URLSession SSE stream → AsyncStream<String>
    → @Published responseText accumulates tokens
    → View re-renders each token chunk (≤100ms batching)
    → Stream ends → mark complete → save to SwiftData
```

### Data Flow: Agent Status

```
App foreground → WebSocket.connect("/v1/agents/stream")
    → Server pushes: {type: "agent_update", agent_id: x, status: y, output: z}
    → AgentViewModel.handleUpdate() → @Published agents array mutated
    → AgentMonitorView re-renders diff
    → App background → WS disconnect, APNs takes over
    → APNs push → notification banner + badge update
    → App foreground → WS reconnect, catch up missed events
```

### Push Notification Flow

```
OpenClaw → Redis event → Notification Publisher
    → APNs endpoint → Apple servers
    → iPhone → HoneyApp receives push
    → UNUserNotificationCenter presents banner
    → User taps → deep link to relevant screen
       e.g., honey://agents/{id} → Agent Detail view
```

---

## 9. Tech Stack Recommendation

### Core Framework

**SwiftUI + Swift Concurrency (async/await + actors)**
- No UIKit unless absolutely necessary (AVFoundation overlays)
- `@Observable` macro (iOS 17+) for ViewModels
- `SwiftData` for local persistence (replaces CoreData verbosity)
- Structured concurrency: `TaskGroup` for parallel API calls

**Minimum iOS version**: iOS 17.0
- Rationale: `@Observable`, SwiftData, Liquid Glass-ready, Dynamic Island APIs
- Market coverage: ~85% of active iPhones as of 2026

### Networking

| Concern | Solution | Why |
|---------|----------|-----|
| REST API | `URLSession` (native) | No dependencies, async/await |
| Streaming (SSE) | `URLSession.bytes(for:)` | Native SSE via `AsyncBytes` |
| WebSocket | `URLSessionWebSocketTask` | Native, no Starscream needed |
| Auth | Bearer token + JWT refresh | Stored in Keychain |

### Voice / Audio

| Concern | Solution |
|---------|----------|
| Speech-to-Text | Deepgram SDK (existing key) or `SFSpeechRecognizer` (offline fallback) |
| Text-to-Speech | Fish Audio API (existing account, $0.015/min) |
| Wake word | `SFSpeechRecognizer` continuous mode with "Hey Honey" detection |
| Audio session | `AVAudioSession.sharedInstance()` with `.playAndRecord` category |
| Waveform | `AVAudioRecorder.averagePower()` → real-time bar chart |

### Local Storage

| Data | Storage | Reason |
|------|---------|--------|
| Chat messages | SwiftData | Persistent, queryable |
| Agent history | SwiftData | Persistent |
| Service status cache | SwiftData | Offline support |
| API key / credentials | Keychain | Security |
| User preferences | `@AppStorage` / UserDefaults | Lightweight |
| Unsent messages | SwiftData | Offline compose |

### Push Notifications

| Component | Solution |
|-----------|----------|
| APNs registration | `UIApplication.registerForRemoteNotifications()` |
| Token upload | POST to OpenClaw gateway |
| Rich notifications | `UNNotificationServiceExtension` (inline images, custom UI) |
| Live Activities | `ActivityKit` for long-running agent progress |

### UI Libraries

**Keep dependencies minimal** — the fewer, the better:

| Need | Solution |
|------|---------|
| Markdown rendering | `swift-markdown-ui` (GitHub: gonzalezreal/swift-markdown-ui, 2.4K⭐) |
| Code highlighting | `Splash` (JohnSundell/Splash, 1.7K⭐) or WKWebView with Prism.js |
| Charts/sparklines | `Swift Charts` (Apple, native iOS 16+) |
| Haptics | `UIFeedbackGenerator` (native) |
| Lottie animations | `lottie-ios` (airbnb, for onboarding only) |

**Avoid**: RxSwift, Alamofire, Kingfisher (overkill for this app)

### Architecture Pattern

**MVVM + Repository**

```
Views (SwiftUI)
  ↕ @Observable ViewModels
    ↕ Repository (protocol)
      ↕ Remote DataSource (URLSession)
      ↕ Local DataSource (SwiftData)
```

- ViewModels own business logic; Views own presentation
- Repository pattern for testability + offline support
- `@MainActor` on all ViewModels for safe UI updates
- Dependency injection via environment (`.environment(\.honeyClient, ...)`)

### Testing

| Layer | Tool |
|-------|------|
| Unit tests | XCTest + Swift Testing framework |
| UI tests | XCUITest (smoke tests for core flows) |
| Snapshot tests | `swift-snapshot-testing` (critical screens) |
| Mocks | Protocol-based (no magic mock libraries) |

### CI/CD

```
GitHub Actions:
  push → build + unit tests → TestFlight (via Fastlane)
  tag → App Store submission

Fastlane:
  lane :beta → increment_build, build, upload_to_testflight
  lane :release → build, upload_to_app_store
```

---

## 10. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2) — "It Works"

**Goal**: Working chat + OpenClaw connection

- [ ] Project setup: SwiftUI, Swift Package Manager, SwiftData
- [ ] Authentication: API key entry + Keychain storage
- [ ] HoneyAPI client: REST + SSE streaming
- [ ] Chat UI: bubble layout, streaming text, send/receive
- [ ] Basic voice input: `SFSpeechRecognizer` mic button
- [ ] Settings screen: endpoint URL, API key, model picker
- [ ] Test: end-to-end message with real OpenClaw

### Phase 2: Agent Monitor (Weeks 3-4) — "See What's Happening"

**Goal**: Real-time agent visibility

- [ ] WebSocket client for live agent stream
- [ ] Agent list view with live status, elapsed time
- [ ] Agent detail view with scrolling log
- [ ] Steer + Kill actions with confirmation
- [ ] Push notification registration + basic agent alerts
- [ ] Connection resilience: reconnect with backoff

### Phase 3: Dashboard (Weeks 5-6) — "Command Center"

**Goal**: Projects + cron + services in one view

- [ ] Project grid with health scores
- [ ] Service health list with ping status
- [ ] Cron job list with last run status
- [ ] Deep link routing: notification → specific screen
- [ ] WidgetKit: small + medium home screen widgets
- [ ] Live Activity: active agent in Dynamic Island

### Phase 4: Voice-First (Weeks 7-8) — "Hands-Free"

**Goal**: Full voice workflow, premium feel

- [ ] Fish Audio TTS integration (streaming playback)
- [ ] Deepgram STT integration (higher accuracy)
- [ ] Voice orb animation (amplitude-driven)
- [ ] Wake word detection ("Hey Honey")
- [ ] Voice command routing (query → agent dispatch → speak result)
- [ ] CarPlay consideration: simplified voice-only UI

### Phase 5: Polish (Weeks 9-10) — "Feels Premium"

**Goal**: App Store submission quality

- [ ] Onboarding flow (3 screens)
- [ ] Empty states for all screens
- [ ] Error states with recovery actions
- [ ] Skeleton loading screens
- [ ] Accessibility audit (VoiceOver, Dynamic Type, High Contrast)
- [ ] Performance profiling (Instruments: hangs, memory, battery)
- [ ] App Store screenshots + metadata
- [ ] TestFlight beta → feedback loop

---

## Appendix A: Design References

### Apps to Study Closely

1. **ChatGPT iOS** — Gold standard for AI chat UX, voice mode
2. **Perplexity** — Source citations, focus modes, premium feel
3. **Linear** (project management) — Speed, keyboard shortcuts, dark mode polish
4. **Things 3** — Information density done right, delightful micro-interactions
5. **Raycast** — Command palette pattern, quick actions
6. **Warp Terminal** — AI-integrated terminal, agent-like feel
7. **Superwall** (paywall tool) — Excellent SwiftUI animation patterns
8. **NetNewsWire** — Well-structured list + detail, open source SwiftUI reference

### Design Tools

- Figma (design + prototyping)
- SF Symbols app (icon reference)
- Simulator (layout verification)
- Instruments (performance)

### Resources

- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/) — Always the source of truth
- [WWDC 2024: SwiftUI Animations](https://developer.apple.com/videos/wwdc2024/) — Latest animation APIs
- [swift-markdown-ui](https://github.com/gonzalezreal/swift-markdown-ui) — Markdown component
- [Designing for the Dynamic Island](https://developer.apple.com/design/human-interface-guidelines/live-activities)

---

## Appendix B: API Contract (Sketch)

The OpenClaw gateway needs these endpoints for the iOS app:

```
# Chat
POST   /v1/chat                  → SSE stream of tokens
GET    /v1/conversations         → list conversations
GET    /v1/conversations/:id     → messages in conversation

# Agents
GET    /v1/agents                → list all agents (running + recent)
GET    /v1/agents/:id            → agent detail + log
WS     /v1/agents/stream         → live updates for all agents
POST   /v1/agents/:id/steer      → send steering message
DELETE /v1/agents/:id            → kill agent
POST   /v1/agents                → spawn new agent

# Cron
GET    /v1/cron                  → list all cron jobs
GET    /v1/cron/:id/history      → last N runs
POST   /v1/cron/:id/run          → manual trigger

# Projects
GET    /v1/projects              → list all projects with scores
GET    /v1/projects/:id          → project detail

# Services
GET    /v1/services              → list services with health
GET    /v1/services/:id/history  → uptime history

# Push
POST   /v1/push/register         → register APNs token
DELETE /v1/push/register         → deregister

# Budget
GET    /v1/budget/today          → today's API spend
GET    /v1/budget/history        → 30-day history
```

---

*This brief is a living document. Update it as design decisions solidify and user feedback arrives from TestFlight beta.*
