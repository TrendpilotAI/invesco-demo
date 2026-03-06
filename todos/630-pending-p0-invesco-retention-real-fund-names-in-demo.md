# TODO #630 — Use Real Invesco Fund Names in Demo Data

**Priority:** P0 (Demo Quality)
**Effort:** XS (30 min)
**Repo:** invesco-retention
**Status:** pending

## Description
The synthetic demo data uses generic fund names. Switching to real Invesco fund tickers/names (QQQ, RSP, BLDG, IVW, CQQQ, etc.) would significantly increase demo authenticity and signal to Brian Kiley that we understand their product line. These are all public fund names — zero IP risk.

## Coding Prompt
```
In /data/workspace/projects/invesco-retention/synthetic-data/invesco_fund_catalog.json,
replace any generic fund names with real Invesco ETF names:
- QQQ (Invesco QQQ Trust — NASDAQ 100)
- RSP (Invesco S&P 500 Equal Weight ETF)
- BLDG (Invesco Real Estate ETF)
- IVW (iShares S&P 500 Growth ETF — note: this is iShares, pick Invesco equivalent)
- CQQQ (Invesco China Technology ETF)
- QQQM (Invesco NASDAQ 100 ETF — smaller shares version)
- BUL (Invesco BulletShares)
- KBWB (Invesco KBW Bank ETF)

Update the demo-app mock data references if they reference fund names directly.
Run: grep -r "fund_name\|fundName\|ticker" src/ to find all references.
```

## Acceptance Criteria
- [ ] Fund names in synthetic data match real Invesco products
- [ ] Demo app displays real fund names
- [ ] No generic "Fund A / Fund B" placeholders visible in demo
