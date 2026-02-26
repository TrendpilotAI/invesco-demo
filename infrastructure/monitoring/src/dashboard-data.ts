import { writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { checkAll, SERVICES, type HealthResult } from "./healthcheck.js";
import { MetricsStore, type ServiceMetrics } from "./metrics.js";

export interface StatusCard {
  name: string;
  url: string;
  status: HealthResult["status"];
  httpCode: number | null;
  responseTimeMs: number;
  metrics: ServiceMetrics;
}

export interface DashboardData {
  generatedAt: string;
  overall: "operational" | "degraded" | "outage";
  services: StatusCard[];
}

export function buildDashboard(results: HealthResult[], metricsStore: MetricsStore): DashboardData {
  const services: StatusCard[] = results.map((r) => ({
    name: r.service,
    url: r.url,
    status: r.status,
    httpCode: r.httpCode,
    responseTimeMs: r.responseTimeMs,
    metrics: metricsStore.getMetrics(r.service),
  }));

  const hasDown = services.some((s) => s.status === "down");
  const hasDegraded = services.some((s) => s.status === "degraded");
  const overall = hasDown ? "outage" : hasDegraded ? "degraded" : "operational";

  return {
    generatedAt: new Date().toISOString(),
    overall,
    services,
  };
}

export function writeDashboard(data: DashboardData, path: string): void {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2));
}

const STATUS_PATH = "/data/workspace/dashboard/status.json";

// CLI entry
if (process.argv[1]?.includes("dashboard-data")) {
  const store = new MetricsStore();
  checkAll(SERVICES).then((results) => {
    store.recordAll(results);
    const dashboard = buildDashboard(results, store);
    writeDashboard(dashboard, STATUS_PATH);
    console.log(`Dashboard written to ${STATUS_PATH}`);
    console.log(JSON.stringify(dashboard, null, 2));
  });
}
