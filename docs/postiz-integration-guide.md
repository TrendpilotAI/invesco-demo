# Postiz Integration Guide for NarrativeReactor

> **Last updated:** 2026-03-03
> **Instance:** https://postiz-production-6189.up.railway.app
> **Status:** ✅ Running (redirects to /auth — registration/login page active)

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL & Rate Limits](#base-url--rate-limits)
4. [API Endpoints](#api-endpoints)
5. [Webhook Support](#webhook-support)
6. [Node.js SDK](#nodejs-sdk)
7. [Code Examples](#code-examples)
8. [NarrativeReactor Integration Architecture](#narrativereactor-integration-architecture)
9. [Setup Checklist](#setup-checklist)

---

## Overview

Postiz is an open-source social media scheduling tool (alternative to Buffer/Hypefury). Our self-hosted instance on Railway provides the **publishing layer** for NarrativeReactor's content flywheel.

**Supported platforms:** X/Twitter, LinkedIn, LinkedIn Pages, Facebook, Instagram, YouTube, TikTok, Reddit, Discord, Slack, Pinterest, Dribbble, Medium, Dev.to, Hashnode, WordPress, Bluesky, Mastodon, Threads, Google My Business, and more (32 total).

**Integration methods:**
- **REST API** (`/public/v1/...`) — direct HTTP calls
- **Node.js SDK** (`@postiz/node`) — official SDK on npm
- **CLI** (`postiz` commands) — for scripting/automation
- **MCP Server** — for AI agent integration (Model Context Protocol)

---

## Authentication

### API Key (recommended for server-to-server)

1. Log into Postiz at `https://postiz-production-6189.up.railway.app`
2. Go to **Settings → Developers → Public API**
3. Generate an API key

```
Authorization: your-api-key
```

### OAuth2 (for multi-user apps)

OAuth2 tokens start with `pos_` and are used identically:

```
Authorization: pos_your-oauth-token
```

See [Postiz OAuth2 docs](https://docs.postiz.com/public-api/oauth) for the full OAuth flow.

---

## Base URL & Rate Limits

| Environment | Base URL |
|---|---|
| Our Railway instance | `https://postiz-production-6189.up.railway.app/public/v1` |
| Postiz Cloud | `https://api.postiz.com/public/v1` |

**Rate limit:** 30 requests per hour (schedule multiple posts per request to maximize throughput).

**Terminology:** The UI calls them "channels", the API calls them "integrations" — same thing.

---

## API Endpoints

### 1. List Connected Accounts (Integrations)

```
GET /public/v1/integrations
```

Returns array of connected social accounts with `id`, `name`, `picture`, `platform`.

### 2. Get Platform Schema / Settings

```
GET /public/v1/integrations/:integrationId/settings
```

Returns character limits, required fields, available options, and dynamic tools for a specific platform.

### 3. Create / Schedule a Post

```
POST /public/v1/posts
```

**Request body:**
```json
{
  "integrations": ["integration-id-1", "integration-id-2"],
  "type": "schedule",
  "date": "2026-03-15T14:00:00.000Z",
  "posts": [
    {
      "provider": "linkedin",
      "post": [
        {
          "content": "<p>Your post content here</p>",
          "image": []
        }
      ],
      "settings": {
        "__type": "linkedin"
      }
    }
  ]
}
```

**Post types:** `schedule`, `draft`, `now`

**Content format:** HTML with allowed tags: `<p>`, `<h1>`-`<h3>`, `<strong>`, `<u>`, `<ul>`, `<li>`

**Thread behavior:**
- Thread platforms (X, Threads, Bluesky): each item in `post[]` = thread post
- Comment platforms (LinkedIn, Facebook): first item = post, rest = comments

### 4. List Scheduled Posts

```
GET /public/v1/posts?startDate=2026-03-01T00:00:00Z&endDate=2026-03-31T23:59:59Z
```

Optional filters: `startDate`, `endDate`, `customer`

### 5. Delete a Post

```
DELETE /public/v1/posts/:postId
```

### 6. Platform Analytics

```
GET /public/v1/analytics/platform/:integrationId?days=30
```

Returns metrics like Followers, Impressions with daily data points and percentage change.

### 7. Post Analytics

```
GET /public/v1/analytics/post/:postId?days=30
```

Returns Likes, Comments, Shares, Impressions per post.

### 8. Upload Media

```
POST /public/v1/media/upload
```

Upload images/videos, returns a URL to reference in posts.

### 9. Trigger Platform Tools

```
POST /public/v1/integrations/:integrationId/trigger
```

Execute platform-specific helpers (e.g., get Reddit flairs, LinkedIn company pages, Discord channels).

---

## Webhook Support

**Postiz does NOT currently have native webhook support** for post-publish events.

### Workarounds for NarrativeReactor:

1. **Polling approach:** After scheduling a post, poll `GET /posts` periodically to check status changes (scheduled → published).

2. **Database-level triggers:** Since we self-host on Railway, we could add a PostgreSQL trigger or a lightweight worker that monitors the posts table for status changes and fires webhooks.

3. **Postiz Agent CLI:** The newer `postiz-agent` CLI (https://github.com/gitroomhq/postiz-agent) may provide event hooks — worth monitoring.

4. **MCP integration:** If NarrativeReactor uses an agent loop, the MCP server provides real-time tool access without webhooks.

---

## Node.js SDK

```bash
npm install @postiz/node
```

The SDK wraps the REST API. Import and configure:

```typescript
import { PostizClient } from '@postiz/node';

const postiz = new PostizClient({
  apiKey: process.env.POSTIZ_API_KEY,
  baseUrl: 'https://postiz-production-6189.up.railway.app/public/v1',
});
```

---

## Code Examples

### Schedule a LinkedIn Post

```typescript
import { PostizClient } from '@postiz/node';

const postiz = new PostizClient({
  apiKey: process.env.POSTIZ_API_KEY,
  baseUrl: process.env.POSTIZ_BASE_URL, // https://postiz-production-6189.up.railway.app/public/v1
});

async function scheduleLinkedInPost(content: string, scheduledDate: string) {
  // 1. Get integrations to find LinkedIn account
  const integrations = await postiz.integrations.list();
  const linkedin = integrations.find(
    (i) => i.platform === 'linkedin' || i.platform === 'linkedin-page'
  );

  if (!linkedin) throw new Error('No LinkedIn integration found');

  // 2. Schedule the post
  const result = await postiz.posts.create({
    integrations: [linkedin.id],
    type: 'schedule',
    date: scheduledDate,
    posts: [
      {
        provider: linkedin.platform,
        post: [{ content: `<p>${content}</p>`, image: [] }],
        settings: { __type: linkedin.platform },
      },
    ],
  });

  return result; // { postId, integration }
}

// Usage
await scheduleLinkedInPost(
  'Excited to share our latest insights on AI-driven content strategy. 🚀',
  '2026-03-15T14:00:00.000Z'
);
```

### Schedule a Twitter/X Post

```typescript
async function scheduleTwitterPost(content: string, scheduledDate: string) {
  const integrations = await postiz.integrations.list();
  const twitter = integrations.find((i) => i.platform === 'x');

  if (!twitter) throw new Error('No X/Twitter integration found');

  const result = await postiz.posts.create({
    integrations: [twitter.id],
    type: 'schedule',
    date: scheduledDate,
    posts: [
      {
        provider: 'x',
        post: [{ content: `<p>${content}</p>`, image: [] }],
        settings: { __type: 'x' },
      },
    ],
  });

  return result;
}

// Thread example
async function scheduleTwitterThread(tweets: string[], scheduledDate: string) {
  const integrations = await postiz.integrations.list();
  const twitter = integrations.find((i) => i.platform === 'x');

  if (!twitter) throw new Error('No X/Twitter integration found');

  const result = await postiz.posts.create({
    integrations: [twitter.id],
    type: 'schedule',
    date: scheduledDate,
    posts: [
      {
        provider: 'x',
        post: tweets.map((tweet) => ({ content: `<p>${tweet}</p>`, image: [] })),
        settings: { __type: 'x' },
      },
    ],
  });

  return result;
}
```

### Multi-Platform Post (LinkedIn + Twitter simultaneously)

```typescript
async function scheduleMultiPlatformPost(
  content: string,
  scheduledDate: string
) {
  const integrations = await postiz.integrations.list();
  const linkedin = integrations.find((i) => i.platform === 'linkedin');
  const twitter = integrations.find((i) => i.platform === 'x');

  const targets = [linkedin, twitter].filter(Boolean);
  if (targets.length === 0) throw new Error('No integrations found');

  const result = await postiz.posts.create({
    integrations: targets.map((t) => t!.id),
    type: 'schedule',
    date: scheduledDate,
    posts: targets.map((t) => ({
      provider: t!.platform,
      post: [{ content: `<p>${content}</p>`, image: [] }],
      settings: { __type: t!.platform },
    })),
  });

  return result;
}
```

### Fetch Engagement Metrics

```typescript
async function getPostEngagement(postId: string, days: number = 30) {
  const analytics = await postiz.analytics.post(postId, { days });

  // analytics is an array of metric objects:
  // [
  //   { label: "Likes", data: [{ total: "150", date: "2026-03-01" }, ...], percentageChange: 12.5 },
  //   { label: "Comments", data: [...], percentageChange: 8.0 },
  //   { label: "Shares", data: [...], percentageChange: -2.0 },
  // ]

  return analytics;
}

async function getPlatformAnalytics(integrationId: string, days: number = 30) {
  const analytics = await postiz.analytics.platform(integrationId, { days });

  // Returns: Followers, Impressions, etc. with daily data points
  return analytics;
}

// Aggregate engagement score for NarrativeReactor feedback loop
async function calculateEngagementScore(postId: string): Promise<number> {
  const metrics = await getPostEngagement(postId, 7);

  const weights: Record<string, number> = {
    Likes: 1,
    Comments: 3,
    Shares: 5,
    Impressions: 0.01,
  };

  let score = 0;
  for (const metric of metrics) {
    const weight = weights[metric.label] || 1;
    const latest = metric.data[metric.data.length - 1];
    score += parseInt(latest?.total || '0') * weight;
  }

  return score;
}
```

### Using Raw HTTP (without SDK)

```typescript
const POSTIZ_URL = 'https://postiz-production-6189.up.railway.app/public/v1';
const API_KEY = process.env.POSTIZ_API_KEY!;

async function postizFetch(path: string, options: RequestInit = {}) {
  const res = await fetch(`${POSTIZ_URL}${path}`, {
    ...options,
    headers: {
      Authorization: API_KEY,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!res.ok) throw new Error(`Postiz API error: ${res.status} ${await res.text()}`);
  return res.json();
}

// List integrations
const integrations = await postizFetch('/integrations');

// Schedule a post
const post = await postizFetch('/posts', {
  method: 'POST',
  body: JSON.stringify({
    integrations: ['integration-id'],
    type: 'schedule',
    date: '2026-03-15T14:00:00.000Z',
    posts: [{
      provider: 'linkedin',
      post: [{ content: '<p>Hello from NarrativeReactor!</p>', image: [] }],
      settings: { __type: 'linkedin' },
    }],
  }),
});

// Get post analytics
const analytics = await postizFetch(`/analytics/post/${post.postId}?days=30`);
```

---

## NarrativeReactor Integration Architecture

```
┌─────────────────────┐
│  NarrativeReactor    │
│  (Content Engine)    │
├─────────────────────┤
│ 1. Generate content  │
│ 2. Adapt per platform│
│ 3. Schedule via API  │──────► Postiz API ──► LinkedIn
│ 4. Track engagement  │                   ──► Twitter/X
│ 5. Feed back metrics │◄────────────────────► Facebook
│    for optimization  │                   ──► Medium, etc.
└─────────────────────┘
```

### Integration Flow

1. **Content Generation:** NarrativeReactor produces a content piece (article, insight, thread)
2. **Platform Adaptation:** Content is reformatted per platform (280 chars for X, long-form for LinkedIn, HTML for Medium)
3. **Scheduling:** `POST /public/v1/posts` with platform-specific payloads
4. **Status Monitoring:** Poll `GET /public/v1/posts` to confirm publication
5. **Engagement Tracking:** `GET /public/v1/analytics/post/:id` to measure performance
6. **Feedback Loop:** Engagement scores feed back to NarrativeReactor to optimize future content (topics, tone, timing)

### Environment Variables

```env
POSTIZ_BASE_URL=https://postiz-production-6189.up.railway.app/public/v1
POSTIZ_API_KEY=<your-api-key>
```

---

## Setup Checklist

- [ ] **Create account** on the Railway Postiz instance
- [ ] **Connect social accounts:** LinkedIn (personal + ForwardLane page), X/Twitter, others as needed
- [ ] **Generate API key:** Settings → Developers → Public API
- [ ] **Store API key** in Railway/environment secrets as `POSTIZ_API_KEY`
- [ ] **Install SDK:** `npm install @postiz/node`
- [ ] **Test connectivity:** Call `GET /public/v1/integrations` and verify accounts listed
- [ ] **Test scheduling:** Schedule a draft post, verify it appears in UI
- [ ] **Wire into NarrativeReactor:** Import the scheduling and analytics functions
- [ ] **Set up engagement polling:** Cron job to fetch analytics daily and feed into content optimization

---

## Additional Resources

- [Postiz Public API Docs](https://docs.postiz.com/public-api)
- [Postiz MCP Server](https://docs.postiz.com/mcp/introduction) — for AI agent integration
- [Postiz Agent CLI](https://github.com/gitroomhq/postiz-agent) — CLI tool designed for agents
- [Node.js SDK](https://www.npmjs.com/package/@postiz/node)
- [n8n Integration](https://www.npmjs.com/package/n8n-nodes-postiz)
- [Make.com Integration](https://apps.make.com/postiz)
