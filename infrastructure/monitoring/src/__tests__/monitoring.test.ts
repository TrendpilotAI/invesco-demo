import { describe, it, expect, vi, beforeEach } from "vitest";
import { checkService, checkAll, type ServiceConfig, type HealthResult } from "../healthcheck.js";
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
  it("fires alert when service is down", () => {
    const mgr = new AlertManager();
    const result: HealthResult = {
      service: "svc", url: "https://x.com", status: "down",
      httpCode: null, responseTimeMs: 0, checkedAt: new Date().toISOString(),
      error: "timeout",
    };
    const alert = mgr.evaluate(result);
    expect(alert).not.toBeNull();
    expect(alert!.type).toBe("down");
  });

  it("respects cooldown — no duplicate alerts within window", () => {
    const mgr = new AlertManager({ cooldownMs: 60000 });
    const result: HealthResult = {
      service: "svc", url: "https://x.com", status: "down",
      httpCode: null, responseTimeMs: 0, checkedAt: new Date().toISOString(),
    };
    const first = mgr.evaluate(result);
    const second = mgr.evaluate(result);
    expect(first).not.toBeNull();
    expect(second).toBeNull();
  });

  it("fires recovery alert bypassing cooldown", () => {
    const mgr = new AlertManager({ cooldownMs: 999999 });
    const down: HealthResult = {
      service: "svc", url: "https://x.com", status: "down",
      httpCode: null, responseTimeMs: 0, checkedAt: new Date().toISOString(),
    };
    const up: HealthResult = { ...down, status: "healthy", httpCode: 200 };
    mgr.evaluate(down);
    const recovery = mgr.evaluate(up);
    expect(recovery).not.toBeNull();
    expect(recovery!.type).toBe("recovered");
  });
});

// --- Telegram format tests ---

describe("formatTelegramMessage", () => {
  it("formats alert as HTML", () => {
    const msg = formatTelegramMessage({ service: "svc", type: "down", message: "🔴 svc is DOWN", timestamp: 0 });
    expect(msg).toContain("<b>Service Alert</b>");
    expect(msg).toContain("🔴 svc is DOWN");
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
