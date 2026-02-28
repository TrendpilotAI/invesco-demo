import { describe, it, expect, vi, beforeEach } from "vitest";
import { checkService, type HealthResult } from "../healthcheck.js";
import { MetricsStore } from "../metrics.js";
import { AlertManager, formatTelegramMessage, formatTelegramDigest } from "../alerting.js";
import { buildDashboard } from "../dashboard-data.js";

// --- Healthcheck tests ---

describe("checkService", () => {
  it("returns healthy for a 200 response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 200 }));
    const result = await checkService({ name: "test", url: "https://example.com" });
    expect(result.status).toBe("healthy");
    expect(result.httpCode).toBe(200);
    expect(result.service).toBe("test");
    vi.unstubAllGlobals();
  });

  it("returns down for a 500 response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 500 }));
    const result = await checkService({ name: "test", url: "https://example.com" });
    expect(result.status).toBe("down");
    expect(result.httpCode).toBe(500);
    vi.unstubAllGlobals();
  });

  it("returns down on network error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("ECONNREFUSED")));
    const result = await checkService({ name: "test", url: "https://example.com" });
    expect(result.status).toBe("down");
    expect(result.httpCode).toBeNull();
    expect(result.error).toBe("ECONNREFUSED");
    vi.unstubAllGlobals();
  });
});

// --- Metrics tests ---

describe("MetricsStore", () => {
  let store: MetricsStore;
  const makeResult = (status: HealthResult["status"], ms: number): HealthResult => ({
    service: "svc", url: "https://x.com", status, httpCode: 200, responseTimeMs: ms,
    checkedAt: new Date().toISOString(),
  });

  beforeEach(() => { store = new MetricsStore(); });

  it("computes uptime and average response time", () => {
    store.record(makeResult("healthy", 100));
    store.record(makeResult("healthy", 200));
    store.record(makeResult("down", 5000));
    const m = store.getMetrics("svc");
    expect(m.totalChecks).toBe(3);
    expect(m.uptimePercent).toBeCloseTo(66.67, 1);
    expect(m.avgResponseTimeMs).toBeCloseTo(1767, 0);
    expect(m.errorRate).toBeCloseTo(33.33, 1);
  });

  it("returns zero metrics for unknown service", () => {
    const m = store.getMetrics("unknown");
    expect(m.totalChecks).toBe(0);
    expect(m.uptimePercent).toBe(0);
  });
});

// --- Alerting tests ---

describe("AlertManager", () => {
  const makeResult = (status: HealthResult["status"], ms = 100): HealthResult => ({
    service: "svc", url: "https://x.com", status,
    httpCode: status === "down" ? null : 200,
    responseTimeMs: ms, checkedAt: new Date().toISOString(),
    error: status === "down" ? "timeout" : undefined,
  });

  it("fires 'down' alert when service first goes down", () => {
    const mgr = new AlertManager();
    const alerts = mgr.evaluate(makeResult("down"));
    expect(alerts).toHaveLength(1);
    expect(alerts[0].type).toBe("down");
  });

  it("deduplicates — no duplicate 'down' alerts within dedupe window", () => {
    const mgr = new AlertManager({ dedupeWindowMs: 60_000 });
    const first  = mgr.evaluate(makeResult("down"));
    const second = mgr.evaluate(makeResult("down"));
    expect(first).toHaveLength(1);
    expect(second).toHaveLength(0); // still in dedupe window
  });

  it("fires escalation alert after escalationMs while still down", () => {
    // Use tiny windows to force escalation immediately
    const mgr = new AlertManager({ dedupeWindowMs: 0, escalationMs: 0 });
    mgr.evaluate(makeResult("down"));  // first down
    const second = mgr.evaluate(makeResult("down"));
    expect(second.some((a) => a.type === "escalation")).toBe(true);
  });

  it("fires recovery alert when service comes back up", () => {
    const mgr = new AlertManager({ dedupeWindowMs: 999_999 });
    mgr.evaluate(makeResult("down"));
    const alerts = mgr.evaluate(makeResult("healthy"));
    expect(alerts.some((a) => a.type === "recovered")).toBe(true);
  });

  it("fires slow alert for degraded response time", () => {
    const mgr = new AlertManager({ responseTimeThresholdMs: 100 });
    const alerts = mgr.evaluate(makeResult("healthy", 9999));
    expect(alerts.some((a) => a.type === "slow")).toBe(true);
  });

  it("evaluateTask detects FAILED transition", () => {
    const mgr = new AlertManager();
    const alerts = mgr.evaluateTask("my-job", "FAILED");
    expect(alerts.some((a) => a.type === "task_failed")).toBe(true);
  });

  it("evaluateTask detects recovery from FAILED → SUCCESS", () => {
    const mgr = new AlertManager({ dedupeWindowMs: 0 });
    mgr.evaluateTask("my-job", "FAILED");
    const recovery = mgr.evaluateTask("my-job", "SUCCESS");
    expect(recovery.some((a) => a.type === "task_recovered")).toBe(true);
  });
});

// --- Telegram format tests ---

describe("formatTelegramMessage", () => {
  it("formats alert as HTML", () => {
    const msg = formatTelegramMessage({ service: "svc", type: "down", message: "🔴 svc is DOWN", timestamp: 0 });
    expect(msg).toContain("<b>🚨 Service Alert</b>");
    expect(msg).toContain("🔴 svc is DOWN");
  });
});

describe("formatTelegramDigest", () => {
  it("returns operational message for empty alerts", () => {
    expect(formatTelegramDigest([])).toContain("operational");
  });
  it("lists all alerts", () => {
    const alerts = [
      { service: "a", type: "down" as const, message: "🔴 a DOWN", timestamp: 0 },
      { service: "b", type: "slow" as const, message: "🟡 b SLOW", timestamp: 0 },
    ];
    const msg = formatTelegramDigest(alerts);
    expect(msg).toContain("2 Alert(s)");
    expect(msg).toContain("🔴 a DOWN");
  });
});

// --- Dashboard tests ---

describe("buildDashboard", () => {
  it("reports outage when any service is down", () => {
    const store = new MetricsStore();
    const results: HealthResult[] = [
      { service: "a", url: "https://a.com", status: "healthy", httpCode: 200, responseTimeMs: 50, checkedAt: "" },
      { service: "b", url: "https://b.com", status: "down", httpCode: null, responseTimeMs: 0, checkedAt: "" },
    ];
    store.recordAll(results);
    const dash = buildDashboard(results, store);
    expect(dash.overall).toBe("outage");
    expect(dash.services).toHaveLength(2);
  });

  it("reports operational when all healthy", () => {
    const store = new MetricsStore();
    const results: HealthResult[] = [
      { service: "a", url: "https://a.com", status: "healthy", httpCode: 200, responseTimeMs: 50, checkedAt: "" },
    ];
    store.recordAll(results);
    const dash = buildDashboard(results, store);
    expect(dash.overall).toBe("operational");
  });
});
