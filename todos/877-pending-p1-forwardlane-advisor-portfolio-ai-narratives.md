# TODO-877: AI Portfolio Narrative Generation

**Repo:** forwardlane_advisor  
**Priority:** P1  
**Effort:** 3-5 days  
**Status:** pending  
**Created:** 2026-03-10

## Problem

The recommendation engine generates portfolio scoring and positions but outputs raw data. Advisors must manually write client-facing summaries explaining portfolio performance, risk, and rebalancing suggestions. This is time-consuming and inconsistent.

## Solution

Build `app/llm/portfolio_narrator.js` — a service that takes recommendation engine output and generates:
1. **Portfolio Summary** — plain-English overview of current holdings and performance
2. **Risk Assessment** — narrative risk analysis (concentration, volatility, sector exposure)
3. **Rebalancing Rationale** — explains why specific changes are recommended
4. **Client Alert Digest** — AI-generated summary of triggered alerts

## Coding Prompt

```
Create /data/workspace/projects/forwardlane_advisor/app/llm/portfolio_narrator.js:

'use strict';

const gateway = require('./gateway');

/**
 * Generates AI narratives for portfolio data.
 * Uses LLM gateway (Claude primary, GPT-4o-mini fallback).
 */

/**
 * Generate a client-facing portfolio summary.
 * @param {Object} portfolioData - { portfolio, positions, performance, client }
 * @param {Function} callback - (err, narrative) => void
 */
function generatePortfolioSummary(portfolioData, callback) {
  const prompt = buildPortfolioPrompt(portfolioData);
  gateway.generateNarrative(prompt, callback);
}

/**
 * Generate rebalancing rationale.
 * @param {Object} recommendation - { before, after, rationale, scores }
 * @param {Function} callback - (err, narrative) => void
 */
function generateRebalancingNarrative(recommendation, callback) { ... }

/**
 * Generate alert digest summary.
 * @param {Array} alerts - Array of triggered AlertRule objects
 * @param {Function} callback - (err, digestText) => void
 */
function generateAlertDigest(alerts, callback) { ... }

module.exports = { generatePortfolioSummary, generateRebalancingNarrative, generateAlertDigest };

Also:
1. Add `generateNarrative(prompt, callback)` method to gateway.js — uses same primary/fallback pattern but for free-form generation (not classification)
2. Wire up in app/portfolios/ route — after recommendation job completes, call narrator and store result in `recommendation_portfolio.narrative` column
3. Add `narrative TEXT` column via new Sequelize migration
4. Display narrative in portfolio view Jade template
5. Add unit tests in test/unit/ using mocked gateway
```

## Acceptance Criteria

- [ ] Portfolio summary generated after each recommendation job
- [ ] Narrative stored in DB and displayed in portfolio view
- [ ] Rebalancing rationale explains specific changes in plain English
- [ ] Alert digest emails include AI-generated summary paragraph
- [ ] Tests pass with mocked LLM gateway

## Dependencies

- TODO-836 (Sequelize v6) — for clean migration support
- TODO-839 (test coverage) — narrative tests included in coverage target
- TODO-876 (streaming) — narratives can optionally stream for long-form output

## Business Impact

This is a **key differentiator** — competitors show raw numbers; ForwardLane shows AI-generated insights. Direct sales tool for enterprise demos.
