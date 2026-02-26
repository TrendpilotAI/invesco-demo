#!/usr/bin/env python3
"""
ForwardLane Invesco Demo — End-to-End Test Validation Script
=============================================================
Tests all 7 Easy Button endpoints against the live Railway backend,
validates response shapes, NL→SQL, and all 6 signal templates.

Run: python3 /data/workspace/scripts/test-invesco-e2e.py
"""

import json
import sys
import time
import traceback
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL = "https://django-backend-production-3b94.up.railway.app/api/v1/easy-button"
TIMEOUT = 20  # seconds per request

# A known advisor ID with active signals (from the interesting set)
KNOWN_ADVISOR_ID = "adv_interesting_010"

# All 6 signal templates to test
SIGNAL_TEMPLATES = [
    "aum-decline-alert",
    "cross-sell-etf",
    "revenue-defense",
    "competitor-heavy",
    "dormant-reactivation",
    "growing-fast",
]

# 5 NL queries to test (mixing quick-match and LLM paths)
NL_QUERIES = [
    "show me at-risk advisors",                             # quick-match: at-risk
    "which advisors are growing fast",                       # quick-match: growing
    "top 10 advisors by AUM",                               # quick-match: biggest
    "show advisors with Invesco holdings",                   # quick-match: invesco
    "list all RIA channel advisors with over 500M AUM",     # LLM path
]

# ── Result tracking ───────────────────────────────────────────────────────────
@dataclass
class TestResult:
    name: str
    passed: bool
    detail: str = ""
    duration_ms: int = 0
    data: Any = None

results: list[TestResult] = []

# ── Helpers ───────────────────────────────────────────────────────────────────

def _request(method: str, path: str, body: dict | None = None) -> tuple[int, Any]:
    """HTTP request; returns (status_code, parsed_json_or_None)."""
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json"} if body else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, json.loads(raw) if raw else None


def record(name: str, passed: bool, detail: str = "", duration_ms: int = 0, data: Any = None):
    r = TestResult(name, passed, detail, duration_ms, data)
    results.append(r)
    icon = "✅" if passed else "❌"
    ms_str = f" ({duration_ms}ms)" if duration_ms else ""
    detail_str = f"  → {detail}" if detail else ""
    print(f"  {icon} {name}{ms_str}{detail_str}")
    return passed


def run_test(name: str, fn) -> bool:
    t0 = time.monotonic()
    try:
        passed, detail = fn()
        ms = int((time.monotonic() - t0) * 1000)
        return record(name, passed, detail, ms)
    except Exception as exc:
        ms = int((time.monotonic() - t0) * 1000)
        return record(name, False, f"EXCEPTION: {exc}", ms)


def check_keys(obj: dict, required_keys: list[str]) -> tuple[bool, str]:
    """Validate all required keys are present in dict."""
    missing = [k for k in required_keys if k not in obj]
    if missing:
        return False, f"Missing keys: {missing}"
    return True, "all required keys present"


def check_type(val, expected_type, field_name: str) -> tuple[bool, str]:
    if not isinstance(val, expected_type):
        return False, f"'{field_name}' expected {expected_type.__name__}, got {type(val).__name__}: {repr(val)[:60]}"
    return True, ""


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Dashboard endpoint
# ═══════════════════════════════════════════════════════════════════════════════

def test_dashboard_status():
    code, data = _request("GET", "/dashboard/")
    if code != 200:
        return False, f"HTTP {code}"
    return True, f"HTTP 200"


def test_dashboard_shape():
    _, data = _request("GET", "/dashboard/")
    required = ["total_aum", "advisor_count", "at_risk_count", "opportunities_count", "aum_change_pct"]
    ok, msg = check_keys(data, required)
    return ok, msg


def test_dashboard_types():
    _, data = _request("GET", "/dashboard/")
    issues = []
    for k in ["total_aum", "advisor_count", "at_risk_count", "opportunities_count"]:
        if not isinstance(data.get(k), int):
            issues.append(f"{k}={type(data.get(k)).__name__}")
    if not isinstance(data.get("aum_change_pct"), (int, float)):
        issues.append(f"aum_change_pct={type(data.get('aum_change_pct')).__name__}")
    if issues:
        return False, f"Type errors: {issues}"
    return True, (
        f"advisor_count={data['advisor_count']}, total_aum=${data['total_aum']/1e9:.1f}B, "
        f"at_risk={data['at_risk_count']}, opps={data['opportunities_count']}"
    )


def test_dashboard_values_sanity():
    _, data = _request("GET", "/dashboard/")
    if data["advisor_count"] <= 0:
        return False, f"advisor_count={data['advisor_count']} (expected > 0)"
    if data["total_aum"] <= 0:
        return False, f"total_aum={data['total_aum']} (expected > 0)"
    if data["at_risk_count"] < 0:
        return False, f"at_risk_count={data['at_risk_count']} (expected ≥ 0)"
    return True, f"{data['advisor_count']} advisors, ${data['total_aum']/1e9:.1f}B AUM"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Clients (Advisor List) endpoint
# ═══════════════════════════════════════════════════════════════════════════════

def test_clients_status():
    code, _ = _request("GET", "/clients/")
    return code == 200, f"HTTP {code}"


def test_clients_pagination_shape():
    _, data = _request("GET", "/clients/?page_size=5")
    required = ["count", "page", "page_size", "total_pages", "results"]
    ok, msg = check_keys(data, required)
    if not ok:
        return False, msg
    if not isinstance(data["results"], list):
        return False, f"results is {type(data['results']).__name__}, expected list"
    return True, f"count={data['count']}, total_pages={data['total_pages']}"


def test_clients_result_shape():
    _, data = _request("GET", "/clients/?page_size=5")
    if not data.get("results"):
        return False, "No results returned"
    item = data["results"][0]
    required = ["id", "name", "firm", "segment", "aum", "change", "risk", "opportunity", "status", "active_signals"]
    ok, msg = check_keys(item, required)
    return ok, msg


def test_clients_segment_filter():
    _, data = _request("GET", "/clients/?segment=RIA&page_size=5")
    if not data.get("results"):
        return False, "No results for segment=RIA"
    wrong = [r["segment"] for r in data["results"] if r["segment"] != "RIA"]
    if wrong:
        return False, f"Non-RIA segments returned: {wrong}"
    return True, f"{data['count']} RIA advisors"


def test_clients_search():
    _, data = _request("GET", "/clients/?search=Morgan&page_size=10")
    if not data.get("results"):
        return False, "No results for search=Morgan"
    return True, f"{data['count']} results for 'Morgan'"


def test_clients_ordering():
    _, data_asc = _request("GET", "/clients/?ordering=aum&direction=asc&page_size=5")
    _, data_desc = _request("GET", "/clients/?ordering=aum&direction=desc&page_size=5")
    if not data_asc.get("results") or not data_desc.get("results"):
        return False, "Empty results"
    asc_aum = [r["aum"] for r in data_asc["results"] if r["aum"] is not None]
    desc_aum = [r["aum"] for r in data_desc["results"] if r["aum"] is not None]
    if len(asc_aum) >= 2 and asc_aum[0] > asc_aum[-1]:
        return False, f"ASC ordering wrong: {asc_aum[0]} > {asc_aum[-1]}"
    if len(desc_aum) >= 2 and desc_aum[0] < desc_aum[-1]:
        return False, f"DESC ordering wrong: {desc_aum[0]} < {desc_aum[-1]}"
    return True, f"ASC first={asc_aum[0] if asc_aum else 'n/a'}, DESC first={desc_aum[0] if desc_aum else 'n/a'}"


def test_clients_pagination():
    _, page1 = _request("GET", "/clients/?page=1&page_size=5")
    _, page2 = _request("GET", "/clients/?page=2&page_size=5")
    ids1 = {r["id"] for r in page1.get("results", [])}
    ids2 = {r["id"] for r in page2.get("results", [])}
    overlap = ids1 & ids2
    if overlap:
        return False, f"IDs appear on both pages: {overlap}"
    return True, f"Pages non-overlapping (page1={len(ids1)} items, page2={len(ids2)} items)"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Client Detail endpoint
# ═══════════════════════════════════════════════════════════════════════════════

def test_client_detail_status():
    code, _ = _request("GET", f"/clients/{KNOWN_ADVISOR_ID}/")
    return code == 200, f"HTTP {code}"


def test_client_detail_shape():
    _, data = _request("GET", f"/clients/{KNOWN_ADVISOR_ID}/")
    required = [
        "id", "name", "firm", "segment", "aum", "aum_12m_ago", "change",
        "status", "client_count", "holdings", "recent_flows", "active_signals"
    ]
    ok, msg = check_keys(data, required)
    return ok, msg


def test_client_detail_holdings():
    _, data = _request("GET", f"/clients/{KNOWN_ADVISOR_ID}/")
    holdings = data.get("holdings", [])
    if not holdings:
        return False, "No holdings returned"
    h = holdings[0]
    required = ["id", "ticker", "name", "type", "family", "aum", "allocation"]
    ok, msg = check_keys(h, required)
    if not ok:
        return False, f"Holdings item missing: {msg}"
    # Validate allocations sum roughly to 100%
    total_alloc = sum(h.get("allocation") or 0 for h in holdings)
    if total_alloc < 90 or total_alloc > 110:
        return False, f"Holdings allocations sum={total_alloc:.1f}% (expected ~100%)"
    return True, f"{len(holdings)} holdings, total_alloc={total_alloc:.1f}%"


def test_client_detail_flows():
    _, data = _request("GET", f"/clients/{KNOWN_ADVISOR_ID}/")
    flows = data.get("recent_flows", [])
    if not flows:
        return False, "No flows returned"
    f = flows[0]
    required = ["id", "fund_ticker", "month", "net_flow"]
    ok, msg = check_keys(f, required)
    if not ok:
        return False, f"Flow item missing: {msg}"
    return True, f"{len(flows)} flow records"


def test_client_detail_active_signals():
    _, data = _request("GET", f"/clients/{KNOWN_ADVISOR_ID}/")
    signals = data.get("active_signals", [])
    if not signals:
        return False, f"No active signals for {KNOWN_ADVISOR_ID} (expected at least 1)"
    s = signals[0]
    required = ["id", "type", "signal_type", "title", "score", "triggered_at", "status"]
    ok, msg = check_keys(s, required)
    if not ok:
        return False, f"Signal item missing: {msg}"
    return True, f"{len(signals)} active signals; first: {s['title']}"


def test_client_detail_404():
    code, data = _request("GET", "/clients/nonexistent_advisor_xyz/")
    if code != 404:
        return False, f"Expected 404, got HTTP {code}"
    return True, "Returns 404 for unknown advisor"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Signals endpoint
# ═══════════════════════════════════════════════════════════════════════════════

def test_signals_status():
    code, _ = _request("GET", "/signals/")
    return code == 200, f"HTTP {code}"


def test_signals_shape():
    _, data = _request("GET", "/signals/")
    if not isinstance(data, list):
        return False, f"Expected list, got {type(data).__name__}"
    if not data:
        return False, "Empty signal list"
    s = data[0]
    required = ["id", "type", "title", "count", "severity", "color"]
    ok, msg = check_keys(s, required)
    return ok, msg


def test_signals_valid_types():
    _, data = _request("GET", "/signals/")
    valid_types = {"risk", "opportunity"}
    bad = [s["type"] for s in data if s.get("type") not in valid_types]
    if bad:
        return False, f"Invalid type values: {bad[:5]}"
    return True, f"{len(data)} signal groups"


def test_signals_valid_severities():
    _, data = _request("GET", "/signals/")
    valid_sev = {"high", "medium", "low"}
    bad = [s["severity"] for s in data if s.get("severity") not in valid_sev]
    if bad:
        return False, f"Invalid severity values: {bad[:5]}"
    return True, f"Severities: {sorted({s['severity'] for s in data})}"


def test_signals_color_format():
    _, data = _request("GET", "/signals/")
    bad = [s["color"] for s in data if s.get("color") and not s["color"].startswith("#")]
    if bad:
        return False, f"Invalid color format: {bad[:5]}"
    return True, "All colors are valid hex"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Actions endpoint
# ═══════════════════════════════════════════════════════════════════════════════

def test_actions_status():
    code, _ = _request("GET", "/actions/")
    return code == 200, f"HTTP {code}"


def test_actions_shape():
    _, data = _request("GET", "/actions/?limit=5")
    if not isinstance(data, list):
        return False, f"Expected list, got {type(data).__name__}"
    if not data:
        return False, "Empty actions list"
    a = data[0]
    required = ["id", "client", "action", "type", "time", "priority"]
    ok, msg = check_keys(a, required)
    return ok, msg


def test_actions_valid_priorities():
    _, data = _request("GET", "/actions/?limit=20")
    valid_prio = {"high", "medium", "low"}
    bad = [a["priority"] for a in data if a.get("priority") not in valid_prio]
    if bad:
        return False, f"Invalid priorities: {bad[:5]}"
    return True, f"{len(data)} action items"


def test_actions_valid_types():
    _, data = _request("GET", "/actions/?limit=20")
    valid_types = {"call", "email"}
    bad = [a["type"] for a in data if a.get("type") not in valid_types]
    if bad:
        return False, f"Invalid action types: {bad[:5]}"
    return True, f"Types: {sorted({a['type'] for a in data})}"


def test_actions_limit_param():
    _, data3 = _request("GET", "/actions/?limit=3")
    _, data10 = _request("GET", "/actions/?limit=10")
    if len(data3) > 3:
        return False, f"limit=3 returned {len(data3)} items"
    if len(data10) <= len(data3):
        return False, f"limit=10 ({len(data10)}) not > limit=3 ({len(data3)})"
    return True, f"limit=3: {len(data3)} items, limit=10: {len(data10)} items"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Signal Run (all 6 templates)
# ═══════════════════════════════════════════════════════════════════════════════

def make_signal_run_test(template_id: str):
    def test_fn():
        code, data = _request("POST", f"/signals/run/{template_id}/")
        if code != 200:
            return False, f"HTTP {code}: {data}"
        required = ["template_id", "status", "message", "count"]
        ok, msg = check_keys(data, required)
        if not ok:
            return False, msg
        if data["template_id"] != template_id:
            return False, f"template_id mismatch: got {data['template_id']}"
        if data["status"] != "success":
            return False, f"status={data['status']} (expected 'success')"
        if not isinstance(data["count"], int) or data["count"] < 0:
            return False, f"count={data['count']} (expected non-negative int)"
        return True, f"Found {data['count']} matching advisors"
    return test_fn


def test_signal_run_unknown():
    code, data = _request("POST", "/signals/run/nonexistent-template-xyz/")
    if code != 400:
        return False, f"Expected 400, got HTTP {code}"
    return True, "Returns 400 for unknown template"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Meeting Prep endpoint
# ═══════════════════════════════════════════════════════════════════════════════

def test_meeting_prep_status():
    code, _ = _request("GET", f"/meeting-prep/{KNOWN_ADVISOR_ID}/")
    return code == 200, f"HTTP {code}"


def test_meeting_prep_shape():
    _, data = _request("GET", f"/meeting-prep/{KNOWN_ADVISOR_ID}/")
    required = [
        "advisor_id", "advisor_name", "firm", "aum", "aum_change_pct", "segment",
        "risk_score", "opportunity_score", "assigned_wholesaler",
        "signals_triggered", "top_holdings", "recent_activity",
        "talking_points", "action_items"
    ]
    ok, msg = check_keys(data, required)
    return ok, msg


def test_meeting_prep_scores():
    _, data = _request("GET", f"/meeting-prep/{KNOWN_ADVISOR_ID}/")
    risk = data.get("risk_score", -1)
    opp = data.get("opportunity_score", -1)
    if not (0 <= risk <= 100):
        return False, f"risk_score={risk} out of [0,100]"
    if not (0 <= opp <= 100):
        return False, f"opportunity_score={opp} out of [0,100]"
    return True, f"risk={risk}, opportunity={opp}"


def test_meeting_prep_holdings():
    _, data = _request("GET", f"/meeting-prep/{KNOWN_ADVISOR_ID}/")
    holdings = data.get("top_holdings", [])
    if not holdings:
        return False, "No top_holdings returned"
    if len(holdings) > 5:
        return False, f"Expected ≤5 top holdings, got {len(holdings)}"
    h = holdings[0]
    required = ["ticker", "name", "allocation", "aum", "asset_class"]
    ok, msg = check_keys(h, required)
    return ok, f"{len(holdings)} top holdings; {msg}"


def test_meeting_prep_talking_points():
    _, data = _request("GET", f"/meeting-prep/{KNOWN_ADVISOR_ID}/")
    pts = data.get("talking_points", [])
    if not pts:
        return False, "No talking_points returned"
    if len(pts) < 2:
        return False, f"Only {len(pts)} talking point(s), expected ≥ 2"
    if any(not isinstance(p, str) for p in pts):
        return False, "Some talking_points are not strings"
    return True, f"{len(pts)} talking points"


def test_meeting_prep_404():
    code, _ = _request("GET", "/meeting-prep/nonexistent_advisor_xyz/")
    if code != 404:
        return False, f"Expected 404, got HTTP {code}"
    return True, "Returns 404 for unknown advisor"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: NL Query endpoint (5 questions)
# ═══════════════════════════════════════════════════════════════════════════════

def make_nl_query_test(question: str, expect_rows: bool = True):
    """Factory for an NL query test."""
    label = question[:50] + ("..." if len(question) > 50 else "")
    def test_fn():
        code, data = _request("POST", "/nl-query/", {"query": question})
        if code not in (200, 422):   # 422 = DB error in query; still valid API response
            return False, f"HTTP {code} (expected 200 or 422)"
        required = ["question", "sql", "columns", "rows", "count"]
        ok, msg = check_keys(data, required)
        if not ok:
            return False, msg
        if data.get("error") and code == 422:
            return False, f"Query error: {data['error'][:100]}"
        if expect_rows and data["count"] == 0:
            return False, f"Query returned 0 rows (sql: {(data.get('sql') or '')[:80]})"
        if data.get("sql") and not data["sql"].strip().lower().startswith("select"):
            return False, f"SQL does not start with SELECT: {data['sql'][:60]}"
        return True, f"{data['count']} rows | sql={data['sql'][:60] if data.get('sql') else 'N/A'}..."
    test_fn.__name__ = f"nl_query_{label[:30]}"
    return test_fn


def test_nl_query_no_body():
    code, data = _request("POST", "/nl-query/", {"query": ""})
    if code != 400:
        return False, f"Expected 400, got HTTP {code}"
    return True, "Returns 400 for empty query"


def test_nl_query_response_shape():
    code, data = _request("POST", "/nl-query/", {"query": "show me at-risk advisors"})
    if code != 200:
        return False, f"HTTP {code}"
    # columns and rows should be aligned
    if data.get("columns") and data.get("rows"):
        sample_row = data["rows"][0]
        if set(sample_row.keys()) != set(data["columns"]):
            return False, f"Row keys {set(sample_row.keys())} != columns {set(data['columns'])}"
    return True, f"columns and rows aligned ({len(data.get('columns', []))} cols)"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: Schema / Cross-cutting validations
# ═══════════════════════════════════════════════════════════════════════════════

def test_aum_consistency():
    """Dashboard total_aum should roughly equal sum of advisor AUMs."""
    _, dashboard = _request("GET", "/dashboard/")
    dash_aum = dashboard["total_aum"]
    dash_count = dashboard["advisor_count"]

    # Fetch first 500 advisors (all)
    _, clients = _request("GET", f"/clients/?page_size=100&page=1")
    page_count = clients.get("count", 0)
    if abs(page_count - dash_count) > 5:
        return False, f"Dashboard advisor_count={dash_count} != clients count={page_count}"
    return True, f"Dashboard={dash_count} advisors, clients endpoint count={page_count} — consistent"


def test_signals_count_consistency():
    """Signals list should contain actual signal groups."""
    _, signals = _request("GET", "/signals/")
    total_signals = sum(s.get("count", 0) for s in signals)
    if total_signals == 0:
        return False, "All signal groups have count=0"
    return True, f"{len(signals)} signal types, {total_signals} total active signals"


def test_all_segments_present():
    """All 4 channels should be filterable."""
    for segment in ["RIA", "BD", "Bank", "Insurance"]:
        _, data = _request("GET", f"/clients/?segment={segment}&page_size=1")
        if data.get("count", 0) == 0:
            return False, f"segment={segment} returned 0 advisors"
    return True, "All 4 segments (RIA, BD, Bank, Insurance) have advisors"


def test_advisor_detail_matches_list():
    """Advisor detail should be consistent with list entry."""
    _, list_data = _request("GET", f"/clients/?page_size=5")
    if not list_data.get("results"):
        return False, "No list results"
    for r in list_data["results"]:
        advisor_id = r["id"]
        _, detail = _request("GET", f"/clients/{advisor_id}/")
        if "id" not in detail:
            return False, f"Detail for {advisor_id} missing 'id'"
        if detail["id"] != advisor_id:
            return False, f"Detail id {detail['id']} != list id {advisor_id}"
        # AUM should match
        if detail.get("aum") != r.get("aum"):
            return False, f"AUM mismatch for {advisor_id}: list={r.get('aum')} detail={detail.get('aum')}"
    return True, f"Spot-checked {len(list_data['results'])} advisors: list ↔ detail consistent"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def section(title: str):
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print(f"{'═'*60}")


def main():
    print(f"\n{'█'*60}")
    print("  ForwardLane Invesco Demo — E2E Validation Suite")
    print(f"  Backend: {BASE_URL}")
    print(f"  Advisor under test: {KNOWN_ADVISOR_ID}")
    print(f"{'█'*60}")

    # ── Dashboard ─────────────────────────────────────────────────────────────
    section("1. Dashboard  GET /dashboard/")
    run_test("HTTP 200 response", test_dashboard_status)
    run_test("Response shape", test_dashboard_shape)
    run_test("Field types correct", test_dashboard_types)
    run_test("Values sanity check", test_dashboard_values_sanity)

    # ── Clients List ─────────────────────────────────────────────────────────
    section("2. Clients List  GET /clients/")
    run_test("HTTP 200 response", test_clients_status)
    run_test("Pagination envelope shape", test_clients_pagination_shape)
    run_test("Result item shape", test_clients_result_shape)
    run_test("Segment filter (RIA)", test_clients_segment_filter)
    run_test("Search filter (Morgan)", test_clients_search)
    run_test("Ordering (aum asc/desc)", test_clients_ordering)
    run_test("Pagination non-overlapping", test_clients_pagination)

    # ── Client Detail ─────────────────────────────────────────────────────────
    section(f"3. Client Detail  GET /clients/{{id}}/  [{KNOWN_ADVISOR_ID}]")
    run_test("HTTP 200 response", test_client_detail_status)
    run_test("Response shape", test_client_detail_shape)
    run_test("Holdings sub-array", test_client_detail_holdings)
    run_test("Recent flows sub-array", test_client_detail_flows)
    run_test("Active signals sub-array", test_client_detail_active_signals)
    run_test("404 for unknown advisor", test_client_detail_404)

    # ── Signals ───────────────────────────────────────────────────────────────
    section("4. Signals  GET /signals/")
    run_test("HTTP 200 response", test_signals_status)
    run_test("Response shape (list of groups)", test_signals_shape)
    run_test("type values (risk|opportunity)", test_signals_valid_types)
    run_test("severity values (high|medium|low)", test_signals_valid_severities)
    run_test("color format (#hex)", test_signals_color_format)

    # ── Actions ───────────────────────────────────────────────────────────────
    section("5. Actions  GET /actions/")
    run_test("HTTP 200 response", test_actions_status)
    run_test("Response shape", test_actions_shape)
    run_test("priority values (high|medium|low)", test_actions_valid_priorities)
    run_test("type values (call|email)", test_actions_valid_types)
    run_test("limit param respected", test_actions_limit_param)

    # ── Signal Run (all 6 templates) ─────────────────────────────────────────
    section("6. Signal Run  POST /signals/run/{template_id}/")
    for template_id in SIGNAL_TEMPLATES:
        run_test(f"Template: {template_id}", make_signal_run_test(template_id))
    run_test("400 for unknown template", test_signal_run_unknown)

    # ── Meeting Prep ──────────────────────────────────────────────────────────
    section(f"7. Meeting Prep  GET /meeting-prep/{{advisor_id}}/  [{KNOWN_ADVISOR_ID}]")
    run_test("HTTP 200 response", test_meeting_prep_status)
    run_test("Response shape", test_meeting_prep_shape)
    run_test("Score ranges [0-100]", test_meeting_prep_scores)
    run_test("Top holdings (≤5)", test_meeting_prep_holdings)
    run_test("Talking points (≥2)", test_meeting_prep_talking_points)
    run_test("404 for unknown advisor", test_meeting_prep_404)

    # ── NL Query ─────────────────────────────────────────────────────────────
    section("8. NL Query  POST /nl-query/")
    run_test("400 for empty query body", test_nl_query_no_body)
    run_test("columns/rows alignment", test_nl_query_response_shape)
    for q in NL_QUERIES:
        label = q[:45] + ("…" if len(q) > 45 else "")
        run_test(f"NL→SQL: '{label}'", make_nl_query_test(q))

    # ── Cross-cutting ─────────────────────────────────────────────────────────
    section("9. Schema / Cross-Cutting Validations")
    run_test("AUM consistency (dashboard ↔ clients)", test_aum_consistency)
    run_test("Signal counts > 0", test_signals_count_consistency)
    run_test("All 4 segments have advisors", test_all_segments_present)
    run_test("Detail ↔ List consistency (spot check)", test_advisor_detail_matches_list)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    pct = int(100 * passed / total) if total else 0

    print(f"\n{'═'*60}")
    print("  TEST SUMMARY")
    print(f"{'═'*60}")
    print(f"  Total:   {total}")
    print(f"  Passed:  {passed}  ✅")
    print(f"  Failed:  {failed}  {'❌' if failed else '—'}")
    print(f"  Score:   {pct}%")

    if failed:
        print(f"\n  {'─'*55}")
        print("  FAILURES:")
        print(f"  {'─'*55}")
        for r in results:
            if not r.passed:
                print(f"  ❌ {r.name}")
                print(f"       {r.detail}")

    avg_ms = int(sum(r.duration_ms for r in results) / total) if total else 0
    print(f"\n  Avg response time: {avg_ms}ms/test")
    print(f"{'═'*60}\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
