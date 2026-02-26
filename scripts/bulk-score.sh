#!/bin/bash
# Bulk score all projects based on analysis
PY="python3 /data/workspace/scripts/score-projects.py update"

# === CORE — ForwardLane/SignalHaus business ===
$PY "forwardlane-backend" '{"category":"CORE","revenue_potential":9,"strategic_value":10,"completeness":8,"urgency":9,"effort_remaining":6,"summary":"Django backend, 2059 files, 150 models. Heart of ForwardLane platform. Deployed on Railway."}'
$PY "signal-studio" '{"category":"CORE","revenue_potential":9,"strategic_value":10,"completeness":6,"urgency":9,"effort_remaining":5,"summary":"Next.js 15 Signal Studio frontend, 273 files. Deployed but not wired to backend yet."}'
$PY "signal-builder-backend" '{"category":"CORE","revenue_potential":8,"strategic_value":9,"completeness":7,"urgency":8,"effort_remaining":6,"summary":"FastAPI graph→SQL compiler, 304 files. NL→SQL engine works. Deployed on Railway."}'
$PY "signal-builder-frontend" '{"category":"CORE","revenue_potential":7,"strategic_value":7,"completeness":5,"urgency":5,"effort_remaining":4,"summary":"React signal builder UI, 68 files. Older frontend, may be superseded by signal-studio."}'
$PY "signal-studio-frontend" '{"category":"CORE","revenue_potential":6,"strategic_value":5,"completeness":4,"urgency":3,"effort_remaining":3,"summary":"Earlier Next.js frontend attempt, 28 files. Likely superseded by signal-studio."}'
$PY "core-entityextraction" '{"category":"CORE","revenue_potential":5,"strategic_value":7,"completeness":3,"urgency":6,"effort_remaining":3,"summary":"Flask NLP/NER service, 26 files. Ancient deps (Flask 1.0, spacy 3.4). Needs full rewrite as FastAPI."}'
$PY "core-admin" '{"category":"CORE","revenue_potential":3,"strategic_value":5,"completeness":6,"urgency":2,"effort_remaining":6,"summary":"Python admin tools, 98 files. Internal tooling for ForwardLane ops."}'
$PY "core-admin-ui" '{"category":"CORE","revenue_potential":3,"strategic_value":5,"completeness":6,"urgency":2,"effort_remaining":6,"summary":"React admin UI, 128 files. Internal dashboard for ForwardLane management."}'
$PY "signal-studio-auth" '{"category":"CORE","revenue_potential":4,"strategic_value":6,"completeness":4,"urgency":4,"effort_remaining":5,"summary":"Auth service for Signal Studio, 11 files. Small but critical for demo auth flow."}'
$PY "signal-studio-data-provider" '{"category":"CORE","revenue_potential":5,"strategic_value":6,"completeness":4,"urgency":4,"effort_remaining":5,"summary":"Data provider service, 18 files. Feeds data to Signal Studio frontend."}'
$PY "signal-studio-templates" '{"category":"CORE","revenue_potential":6,"strategic_value":7,"completeness":4,"urgency":6,"effort_remaining":5,"summary":"Signal templates, 30 files. Pre-built signal definitions — key for Easy Button demo."}'
$PY "signal-studio-api-docs" '{"category":"CORE","revenue_potential":2,"strategic_value":4,"completeness":3,"urgency":2,"effort_remaining":7,"summary":"API documentation. Sparse but useful for developer onboarding."}'
$PY "forwardlane_advisor" '{"category":"CORE","revenue_potential":6,"strategic_value":7,"completeness":7,"urgency":3,"effort_remaining":6,"summary":"Advisor-facing app, 458 files. Mature React app, may have reusable components."}'

# === PRODUCT — Revenue-generating standalone products ===
$PY "flip-my-era" '{"category":"PRODUCT","revenue_potential":7,"strategic_value":5,"completeness":8,"urgency":4,"effort_remaining":8,"summary":"Taylor Swift ebook creator, 222 files. Closest to ship. Netlify + Clerk + Stripe. Needs final QA."}'
$PY "Ultrafone" '{"category":"PRODUCT","revenue_potential":8,"strategic_value":6,"completeness":6,"urgency":3,"effort_remaining":5,"summary":"AI phone receptionist with social engineering detection. 77 files, 75% complete. Big consumer market."}'
$PY "Second-Opinion" '{"category":"PRODUCT","revenue_potential":6,"strategic_value":5,"completeness":5,"urgency":3,"effort_remaining":4,"summary":"Medical AI second opinion app, 208 files. Kaggle MedGemma competition entry."}'
$PY "CreatorConnect" '{"category":"PRODUCT","revenue_potential":5,"strategic_value":4,"completeness":3,"urgency":2,"effort_remaining":3,"summary":"Creator platform, 23 files. TDD plan with 26 tests. Early stage."}'
$PY "Trendpilot" '{"category":"PRODUCT","revenue_potential":6,"strategic_value":5,"completeness":5,"urgency":2,"effort_remaining":4,"summary":"Trend analysis platform, 136 files. Supabase backend. Mid-stage."}'

# === MARKETING — Websites, landing pages ===
$PY "signalhaus-website" '{"category":"MARKETING","revenue_potential":4,"strategic_value":6,"completeness":3,"urgency":3,"effort_remaining":6,"summary":"SignalHaus.ai website, 9 files. Needs content and polish."}'
$PY "forwardlane-website" '{"category":"MARKETING","revenue_potential":3,"strategic_value":5,"completeness":3,"urgency":2,"effort_remaining":6,"summary":"ForwardLane.com website, 8 files. Minimal."}'
$PY "haidef-landing" '{"category":"MARKETING","revenue_potential":2,"strategic_value":2,"completeness":1,"urgency":1,"effort_remaining":2,"summary":"Landing page, 0 files. Empty/placeholder."}'
$PY "second-opinion-landing" '{"category":"MARKETING","revenue_potential":3,"strategic_value":3,"completeness":2,"urgency":2,"effort_remaining":5,"summary":"Second Opinion landing page, 0 source files. Needs build."}'
$PY "invesco-retention" '{"category":"MARKETING","revenue_potential":9,"strategic_value":9,"completeness":5,"urgency":10,"effort_remaining":5,"summary":"Invesco retention strategy docs, 7 files. Critical context for $300K demo. High urgency."}'

# === INFRA — Internal tools, ops ===
$PY "agent-ops-center" '{"category":"INFRA","revenue_potential":1,"strategic_value":7,"completeness":4,"urgency":3,"effort_remaining":5,"summary":"Next.js agent dashboard, 3 files. Deployed but broken JSX. Needs fix."}'
$PY "NarrativeReactor" '{"category":"INFRA","revenue_potential":4,"strategic_value":6,"completeness":5,"urgency":2,"effort_remaining":4,"summary":"AI content engine for SignalHaus marketing, 165 files. Blotato integration built."}'
$PY "doc-pipeline" '{"category":"INFRA","revenue_potential":1,"strategic_value":4,"completeness":5,"urgency":1,"effort_remaining":6,"summary":"Document processing pipeline, 33 files. Voyage AI embeddings configured."}'
$PY "mission-control" '{"category":"INFRA","revenue_potential":1,"strategic_value":4,"completeness":3,"urgency":1,"effort_remaining":5,"summary":"Earlier dashboard attempt (Next.js + Convex), 10 files. Superseded by agent-ops-center."}'
$PY "n8n-workflows" '{"category":"INFRA","revenue_potential":2,"strategic_value":5,"completeness":4,"urgency":1,"effort_remaining":6,"summary":"n8n workflow library, 0 source files. Config/docs only."}'
$PY "postiz-railway" '{"category":"INFRA","revenue_potential":1,"strategic_value":3,"completeness":5,"urgency":1,"effort_remaining":7,"summary":"Postiz social media tool deployed on Railway. Fork, minimal customization."}'
$PY "fast-browser-search" '{"category":"INFRA","revenue_potential":2,"strategic_value":3,"completeness":4,"urgency":1,"effort_remaining":4,"summary":"Rust + graph DB browser history search, 24 files. Best as OSS portfolio piece."}'

# === TEMPLATE — Starters, boilerplate ===
$PY "railway-ai-chatbot-template" '{"category":"TEMPLATE","revenue_potential":1,"strategic_value":2,"completeness":7,"urgency":1,"effort_remaining":8,"summary":"Railway AI chatbot starter, 16 files. Template only."}'
$PY "railway-api-marketplace" '{"category":"TEMPLATE","revenue_potential":1,"strategic_value":2,"completeness":5,"urgency":1,"effort_remaining":7,"summary":"Railway API marketplace template, 15 files."}'
$PY "railway-saas-template" '{"category":"TEMPLATE","revenue_potential":1,"strategic_value":2,"completeness":6,"urgency":1,"effort_remaining":7,"summary":"Railway SaaS starter, 22 files."}'
$PY "thinkchain" '{"category":"TEMPLATE","revenue_potential":1,"strategic_value":2,"completeness":7,"urgency":1,"effort_remaining":8,"summary":"Claude streaming demo fork, 19 files. Most complete, least differentiated."}'

# === LEGACY — Old/deprecated ===
$PY "cb-forwardlane-sites" '{"category":"LEGACY","revenue_potential":1,"strategic_value":2,"completeness":6,"urgency":1,"effort_remaining":7,"summary":"Old Contentful-based ForwardLane sites, 56 files. Historical reference."}'
$PY "fl-web-widgets" '{"category":"LEGACY","revenue_potential":1,"strategic_value":2,"completeness":6,"urgency":1,"effort_remaining":6,"summary":"FL web widgets, 108 files. Older embeddable components."}'
$PY "fl_web" '{"category":"LEGACY","revenue_potential":1,"strategic_value":2,"completeness":5,"urgency":1,"effort_remaining":5,"summary":"Old FL web app, 32 files. Superseded."}'
$PY "demo-client-view" '{"category":"LEGACY","revenue_potential":2,"strategic_value":3,"completeness":5,"urgency":1,"effort_remaining":6,"summary":"Demo client view, 18 files. May have reusable demo patterns."}'
$PY "wealth-advisor-webapp" '{"category":"LEGACY","revenue_potential":2,"strategic_value":3,"completeness":5,"urgency":1,"effort_remaining":5,"summary":"Wealth advisor webapp, 19 files. Earlier advisor-facing UI."}'
$PY "front-end-ai" '{"category":"LEGACY","revenue_potential":1,"strategic_value":1,"completeness":2,"urgency":1,"effort_remaining":2,"summary":"Empty/minimal AI frontend experiment, 0 files."}'
$PY "generative-ai" '{"category":"LEGACY","revenue_potential":1,"strategic_value":2,"completeness":2,"urgency":1,"effort_remaining":2,"summary":"Generative AI experiments, 0 files. Placeholder."}'
$PY "web-site" '{"category":"LEGACY","revenue_potential":1,"strategic_value":1,"completeness":2,"urgency":1,"effort_remaining":2,"summary":"Generic website, 0 files. Empty."}'

# Generate summary
python3 /data/workspace/scripts/score-projects.py summary
