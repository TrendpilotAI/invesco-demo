import type { HealthResult } from "./healthcheck.js";

export interface DataPoint {
  timestamp: number;
  responseTimeMs: number;
  status: HealthResult["status"];
  httpCode: number | null;
}

export interface ServiceMetrics {
  uptimePercent: number;
  avgResponseTimeMs: number;
  errorRate: number;
  totalChecks: number;
  lastCheck: DataPoint | null;
}

const RETENTION_MS = 24 * 60 * 60 * 1000; // 24h

export class MetricsStore {
  private data: Map<string, DataPoint[]> = new Map();

  record(result: HealthResult): void {
    const points = this.data.get(result.service) ?? [];
    points.push({
      timestamp: Date.now(),
      responseTimeMs: result.responseTimeMs,
      status: result.status,
      httpCode: result.httpCode,
    });
    this.data.set(result.service, points);
    this.prune(result.service);
  }

  recordAll(results: HealthResult[]): void {
    results.forEach((r) => this.record(r));
  }

  private prune(service: string): void {
    const cutoff = Date.now() - RETENTION_MS;
    const points = this.data.get(service);
    if (points) {
      this.data.set(service, points.filter((p) => p.timestamp >= cutoff));
    }
  }

  getMetrics(service: string): ServiceMetrics {
    const points = this.data.get(service) ?? [];
    if (points.length === 0) {
      return { uptimePercent: 0, avgResponseTimeMs: 0, errorRate: 0, totalChecks: 0, lastCheck: null };
    }
    const healthy = points.filter((p) => p.status === "healthy").length;
    const errors = points.filter((p) => p.status === "down").length;
    const avgMs = points.reduce((s, p) => s + p.responseTimeMs, 0) / points.length;

    return {
      uptimePercent: Math.round((healthy / points.length) * 10000) / 100,
      avgResponseTimeMs: Math.round(avgMs),
      errorRate: Math.round((errors / points.length) * 10000) / 100,
      totalChecks: points.length,
      lastCheck: points[points.length - 1],
    };
  }

  getHistory(service: string): DataPoint[] {
    return this.data.get(service) ?? [];
  }

  getAllServices(): string[] {
    return [...this.data.keys()];
  }
}

export const store = new MetricsStore();
