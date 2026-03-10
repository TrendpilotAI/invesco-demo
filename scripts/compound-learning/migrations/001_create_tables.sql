-- Compound Learning Pipeline — PostgreSQL Schema
-- Migration 001: Create all tables
-- Run: psql $DATABASE_URL -f 001_create_tables.sql

BEGIN;

-- ============================================================
-- compound_learnings — core knowledge store
-- ============================================================
CREATE TABLE IF NOT EXISTS compound_learnings (
    id              BIGSERIAL PRIMARY KEY,
    category        TEXT NOT NULL,          -- model_selection, architecture, client_insight, security, process, engineering, business
    subcategory     TEXT,
    title           TEXT NOT NULL,
    content         TEXT NOT NULL,
    project         TEXT,
    task            TEXT,
    session_key     TEXT,
    agent           TEXT NOT NULL DEFAULT 'honey',
    model           TEXT NOT NULL DEFAULT 'unknown',
    trigger         TEXT NOT NULL DEFAULT 'manual',   -- manual, auto, cron, feedback
    confidence      REAL NOT NULL DEFAULT 0.8,
    impact          TEXT NOT NULL DEFAULT 'medium',    -- low, medium, high, critical
    tags            TEXT[] DEFAULT '{}',
    applied_count   INT NOT NULL DEFAULT 0,
    last_applied_at TIMESTAMPTZ,
    search_vector   TSVECTOR,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_learnings_category    ON compound_learnings (category);
CREATE INDEX idx_learnings_project     ON compound_learnings (project);
CREATE INDEX idx_learnings_impact      ON compound_learnings (impact);
CREATE INDEX idx_learnings_agent       ON compound_learnings (agent);
CREATE INDEX idx_learnings_tags        ON compound_learnings USING GIN (tags);
CREATE INDEX idx_learnings_search      ON compound_learnings USING GIN (search_vector);
CREATE INDEX idx_learnings_created     ON compound_learnings (created_at DESC);

-- Auto-update search vector
CREATE OR REPLACE FUNCTION compound_learnings_search_trigger() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.content, '') || ' ' || COALESCE(NEW.category, '') || ' ' || COALESCE(NEW.project, ''));
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_learnings_search
    BEFORE INSERT OR UPDATE ON compound_learnings
    FOR EACH ROW EXECUTE FUNCTION compound_learnings_search_trigger();

-- ============================================================
-- compound_decisions — significant decision log
-- ============================================================
CREATE TABLE IF NOT EXISTS compound_decisions (
    id              BIGSERIAL PRIMARY KEY,
    title           TEXT NOT NULL,
    description     TEXT NOT NULL,
    reasoning       TEXT NOT NULL,
    alternatives    JSONB DEFAULT '[]',
    project         TEXT,
    stakeholder     TEXT,
    decided_by      TEXT NOT NULL DEFAULT 'honey',
    reversible      BOOLEAN NOT NULL DEFAULT TRUE,
    outcome         TEXT,                   -- filled later
    tags            TEXT[] DEFAULT '{}',
    search_vector   TSVECTOR,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_decisions_project    ON compound_decisions (project);
CREATE INDEX idx_decisions_decided_by ON compound_decisions (decided_by);
CREATE INDEX idx_decisions_search     ON compound_decisions USING GIN (search_vector);
CREATE INDEX idx_decisions_created    ON compound_decisions (created_at DESC);

CREATE OR REPLACE FUNCTION compound_decisions_search_trigger() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, '') || ' ' || COALESCE(NEW.reasoning, ''));
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_decisions_search
    BEFORE INSERT OR UPDATE ON compound_decisions
    FOR EACH ROW EXECUTE FUNCTION compound_decisions_search_trigger();

-- ============================================================
-- compound_model_performance — per-task model metrics
-- ============================================================
CREATE TABLE IF NOT EXISTS compound_model_performance (
    id                  BIGSERIAL PRIMARY KEY,
    model               TEXT NOT NULL,
    task_type           TEXT NOT NULL,       -- coding, analysis, writing, research, chat, routing
    completion_time_ms  INT NOT NULL DEFAULT 0,
    tokens_in           INT NOT NULL DEFAULT 0,
    tokens_out          INT NOT NULL DEFAULT 0,
    cost_usd            NUMERIC(10,6) NOT NULL DEFAULT 0,
    quality_score       REAL,               -- 0.0-1.0
    success             BOOLEAN NOT NULL DEFAULT TRUE,
    project             TEXT,
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_model_perf_model     ON compound_model_performance (model);
CREATE INDEX idx_model_perf_task      ON compound_model_performance (task_type);
CREATE INDEX idx_model_perf_success   ON compound_model_performance (success);
CREATE INDEX idx_model_perf_created   ON compound_model_performance (created_at DESC);
CREATE INDEX idx_model_perf_model_task ON compound_model_performance (model, task_type);

-- ============================================================
-- compound_patterns — detected recurring patterns
-- ============================================================
CREATE TABLE IF NOT EXISTS compound_patterns (
    id              BIGSERIAL PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    description     TEXT NOT NULL,
    recommendation  TEXT NOT NULL,
    category        TEXT NOT NULL DEFAULT 'general',
    occurrences     INT NOT NULL DEFAULT 1,
    auto_apply      BOOLEAN NOT NULL DEFAULT FALSE,
    learning_ids    BIGINT[] DEFAULT '{}',
    search_vector   TSVECTOR,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_patterns_category   ON compound_patterns (category);
CREATE INDEX idx_patterns_auto_apply ON compound_patterns (auto_apply);
CREATE INDEX idx_patterns_search     ON compound_patterns USING GIN (search_vector);

CREATE OR REPLACE FUNCTION compound_patterns_search_trigger() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', COALESCE(NEW.name, '') || ' ' || COALESCE(NEW.description, '') || ' ' || COALESCE(NEW.recommendation, ''));
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_patterns_search
    BEFORE INSERT OR UPDATE ON compound_patterns
    FOR EACH ROW EXECUTE FUNCTION compound_patterns_search_trigger();

-- ============================================================
-- compound_feedback_loop — human corrections
-- ============================================================
CREATE TABLE IF NOT EXISTS compound_feedback_loop (
    id                BIGSERIAL PRIMARY KEY,
    session_key       TEXT NOT NULL,
    agent_action      TEXT NOT NULL,
    human_correction  TEXT NOT NULL,
    category          TEXT NOT NULL DEFAULT 'general',
    severity          TEXT NOT NULL DEFAULT 'important',  -- minor, important, critical
    resolved          BOOLEAN NOT NULL DEFAULT FALSE,
    learning_id       BIGINT REFERENCES compound_learnings(id),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_feedback_session  ON compound_feedback_loop (session_key);
CREATE INDEX idx_feedback_severity ON compound_feedback_loop (severity);
CREATE INDEX idx_feedback_resolved ON compound_feedback_loop (resolved);
CREATE INDEX idx_feedback_created  ON compound_feedback_loop (created_at DESC);

-- ============================================================
-- compound_daily_metrics — aggregated daily stats
-- ============================================================
CREATE TABLE IF NOT EXISTS compound_daily_metrics (
    id                  BIGSERIAL PRIMARY KEY,
    date                DATE NOT NULL UNIQUE,
    total_learnings     INT NOT NULL DEFAULT 0,
    total_decisions     INT NOT NULL DEFAULT 0,
    total_tasks         INT NOT NULL DEFAULT 0,
    total_feedback      INT NOT NULL DEFAULT 0,
    patterns_detected   INT NOT NULL DEFAULT 0,
    avg_quality_score   REAL,
    total_cost_usd      NUMERIC(10,4) NOT NULL DEFAULT 0,
    total_tokens        BIGINT NOT NULL DEFAULT 0,
    top_model           TEXT,
    top_task_type       TEXT,
    learnings_by_category JSONB DEFAULT '{}',
    models_used         JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_daily_metrics_date ON compound_daily_metrics (date DESC);

COMMIT;
