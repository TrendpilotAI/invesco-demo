---
status: complete
priority: p1
issue_id: "002"
tags: [nl-to-sql, api, openai, signals]
dependencies: ["001"]
---

# NL→SQL Signal Generation Engine

## Problem Statement

Build an API endpoint that converts natural language descriptions into executable SQL queries for financial signal creation.

## Findings

- Extracted complete schema from signal-builder-backend: 22 tables, 200+ columns
- Created comprehensive ANALYTICAL_SCHEMA context for LLM
- Built /api/signals/generate endpoint using Vercel AI SDK

## Proposed Solutions

- **Chosen:** Hardcode full schema in prompt — fastest path to working

## Recommended Action

Build NL→SQL endpoint with full Invesco schema context.

## Acceptance Criteria

- [x] Extract full schema from signal-builder-backend
- [x] Create /api/signals/generate endpoint
- [x] Test with 3 real queries
- [x] Document solution

## Work Log

### 2026-02-22 - NL→SQL Engine Build

**By:** Honey AI

**Actions:**
- Extracted schema from apps/analytical_db/schema_manager/schemas/
- Created lib/schema-context.ts with 200+ columns
- Built /api/signals/generate using generateObject from ai-sdk
- Tested: "advisors declining AUM", "MF declining ETF growing", "high cross-sell zero SMA"

**Results:** All 3 test queries returned valid SQL with correct JOINs
