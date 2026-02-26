-- Multi-table analytical schema for Invesco Signal Studio demo
-- Replaces the flat single-table schema

-- Drop existing tables if they exist (in dependency order)
DROP TABLE IF EXISTS signals CASCADE;
DROP TABLE IF EXISTS flows CASCADE;
DROP TABLE IF EXISTS holdings CASCADE;
DROP TABLE IF EXISTS advisors CASCADE;

-- advisors: 500 rows, AUM $50M-$2B
CREATE TABLE advisors (
  advisor_id TEXT PRIMARY KEY,
  full_name TEXT NOT NULL,
  firm_name TEXT NOT NULL,
  region TEXT NOT NULL,        -- NE, SE, MW, SW, W
  channel TEXT NOT NULL,       -- RIA, BD, Bank, Insurance
  aum_current BIGINT NOT NULL, -- current AUM in dollars
  aum_12m_ago BIGINT NOT NULL, -- AUM 12 months ago (for trend calc)
  client_count INTEGER NOT NULL,
  avg_account_size BIGINT GENERATED ALWAYS AS (aum_current / NULLIF(client_count, 0)) STORED,
  email TEXT,
  phone TEXT,
  city TEXT,
  state TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- holdings: advisor → ETF/fund positions
CREATE TABLE holdings (
  holding_id SERIAL PRIMARY KEY,
  advisor_id TEXT REFERENCES advisors(advisor_id),
  symbol TEXT NOT NULL,          -- e.g. VOO, IVV, SPY, IVVB, etc.
  fund_name TEXT NOT NULL,
  fund_type TEXT NOT NULL,       -- ETF, MF (mutual fund), ModelPortfolio
  fund_family TEXT NOT NULL,     -- Invesco, iShares, Vanguard, etc.
  aum_in_fund BIGINT NOT NULL,   -- dollars in this fund
  pct_of_aum DECIMAL(5,2),       -- % of advisor's total AUM
  as_of_date DATE NOT NULL,
  UNIQUE(advisor_id, symbol, as_of_date)
);

-- flows: monthly net flows per advisor per fund (12 months)
CREATE TABLE flows (
  flow_id SERIAL PRIMARY KEY,
  advisor_id TEXT REFERENCES advisors(advisor_id),
  symbol TEXT NOT NULL,
  flow_month DATE NOT NULL,      -- first day of month
  net_flow BIGINT NOT NULL,      -- positive = inflow, negative = outflow
  gross_inflow BIGINT NOT NULL,
  gross_outflow BIGINT NOT NULL
);

-- signals: pre-computed signals for interesting advisors
CREATE TABLE signals (
  signal_id SERIAL PRIMARY KEY,
  advisor_id TEXT REFERENCES advisors(advisor_id),
  signal_type TEXT NOT NULL,     -- AUM_DECLINE, CROSS_SELL_ETF, REVENUE_DEFENSE, RIA_CONVERSION, DORMANT
  signal_score DECIMAL(4,2),     -- 0.0-10.0 urgency
  signal_data JSONB,             -- details
  triggered_at TIMESTAMP DEFAULT NOW(),
  status TEXT DEFAULT 'active'   -- active, dismissed, actioned
);

-- Indexes for performance
CREATE INDEX idx_holdings_advisor ON holdings(advisor_id);
CREATE INDEX idx_holdings_symbol ON holdings(symbol);
CREATE INDEX idx_flows_advisor ON flows(advisor_id);
CREATE INDEX idx_flows_month ON flows(flow_month);
CREATE INDEX idx_signals_advisor ON signals(advisor_id);
CREATE INDEX idx_signals_status ON signals(status);
CREATE INDEX idx_signals_score ON signals(signal_score DESC);
CREATE INDEX idx_advisors_region ON advisors(region);
CREATE INDEX idx_advisors_channel ON advisors(channel);
CREATE INDEX idx_advisors_aum ON advisors(aum_current DESC);
