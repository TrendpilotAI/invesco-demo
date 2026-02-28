import type { HealthResult } from "./healthcheck.js";
import type { AlertStateManager } from "./alert-state.js";

export interface Alert {
  service: string;
  type: "down" | "slow" | "recovered" | "task_failed" | "task_recovered" | "escalation";
  message: string;
  timestamp: number;
}

export interface AlertConfig {
  /** Response time threshold before a "slow" alert fires (ms). Default 5000 */
  responseTimeThresholdMs: number;
  /** Deduplication window — don't re-alert for same issue within this ms. Default 30 min */
  dedupeWindowMs: number;
  /** Escalation — re-alert if service stays down longer than this ms. Default 15 min */
  escalationMs: number;
}

const DEFAULT_CONFIG: AlertConfig = {
  responseTimeThresholdMs: 5000,
  dedupeWindowMs: 30 * 60 * 1000,   // 30 minutes
  escalationMs:   15 * 60 * 1000,   // 15 minutes
};

export class AlertManager {
  private config: AlertConfig;
  private stateManager: AlertStateManager | null;
  /** In-memory fallback when no stateManager provided */
  private memState: Map<string, {
    lastStatus: string | null;
    lastAlertSentAt: number | null;
    downSince: number | null;
    escalatedAt: number | null;
    taskLastResult: string | null;
  }> = new Map();

  constructor(config: Partial<AlertConfig> = {}, stateManager?: AlertStateManager) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.stateManager = stateManager ?? null;
  }

  // ── State helpers ─────────────────────────────────────────────────────────

  private getState(service: string) {
    if (this.stateManager) return this.stateManager.get(service);
    if (!this.memState.has(service)) {
      this.memState.set(service, { lastStatus: null, lastAlertSentAt: null, downSince: null, escalatedAt: null, taskLastResult: null });
    }
    return this.memState.get(service)!;
  }

  private patchState(service: string, patch: Partial<{
    lastStatus: string | null;
    lastAlertSentAt: number | null;
    downSince: number | null;
    escalatedAt: number | null;
  }>) {
    if (this.stateManager) {
      this.stateManager.set(service, patch);
      return;
    }
    const cur = this.getState(service);
    Object.assign(cur, patch);
  }

  // ── Cooldown helpers ──────────────────────────────────────────────────────

  private inDedupe(service: string): boolean {
    const { lastAlertSentAt } = this.getState(service);
    if (lastAlertSentAt == null) return false;
    return Date.now() - lastAlertSentAt < this.config.dedupeWindowMs;
  }

  private markAlertSent(service: string): void {
    this.patchState(service, { lastAlertSentAt: Date.now() });
  }

  // ── Core evaluation ───────────────────────────────────────────────────────

  evaluate(result: HealthResult): Alert[] {
    const now = Date.now();
    const svc = result.service;
    const state = this.getState(svc);
    const prevStatus = state.lastStatus;
    const alerts: Alert[] = [];

    // ── Down transition ───────────────────────────────────────────────────
    if (result.status === "down") {
      if (prevStatus !== "down") {
        // First time going down
        this.patchState(svc, { downSince: now, escalatedAt: null });
        if (!this.inDedupe(svc)) {
          alerts.push({
            service: svc, type: "down",
            message: `🔴 <b>${svc}</b> is DOWN${result.error ? `: ${result.error}` : ""} (HTTP ${result.httpCode ?? "N/A"})`,
            timestamp: now,
          });
          this.markAlertSent(svc);
        }
      } else {
        // Still down — check escalation
        const downSince = state.downSince ?? now;
        const downDurationMs = now - downSince;
        const lastEscalated = state.escalatedAt ?? state.lastAlertSentAt ?? 0;

        if (downDurationMs >= this.config.escalationMs &&
            now - lastEscalated >= this.config.escalationMs) {
          const downMin = Math.round(downDurationMs / 60000);
          alerts.push({
            service: svc, type: "escalation",
            message: `🚨 <b>${svc}</b> STILL DOWN (${downMin}min)${result.error ? `: ${result.error}` : ""}`,
            timestamp: now,
          });
          this.patchState(svc, { escalatedAt: now });
        }
      }
    }

    // ── Recovery ──────────────────────────────────────────────────────────
    else if (prevStatus === "down" && result.status !== "down") {
      const downSince = state.downSince ?? now;
      const downDurationMs = now - downSince;
      const downMin = Math.round(downDurationMs / 60000);
      alerts.push({
        service: svc, type: "recovered",
        message: `🟢 <b>${svc}</b> RECOVERED after ${downMin}min (${result.responseTimeMs}ms)`,
        timestamp: now,
      });
      this.patchState(svc, { downSince: null, escalatedAt: null });
      this.markAlertSent(svc);
    }

    // ── Slow ──────────────────────────────────────────────────────────────
    else if (result.responseTimeMs > this.config.responseTimeThresholdMs && result.status !== "down") {
      if (!this.inDedupe(svc)) {
        alerts.push({
          service: svc, type: "slow",
          message: `🟡 <b>${svc}</b> SLOW: ${result.responseTimeMs}ms (threshold: ${this.config.responseTimeThresholdMs}ms)`,
          timestamp: now,
        });
        this.markAlertSent(svc);
      }
    }

    // Update last status
    this.patchState(svc, { lastStatus: result.status });

    return alerts;
  }

  evaluateAll(results: HealthResult[]): Alert[] {
    return results.flatMap((r) => this.evaluate(r));
  }

  /**
   * Evaluate a task result string (e.g. "SUCCESS" | "FAILED").
   * Fires on transitions and deduplicates within window.
   */
  evaluateTask(service: string, result: string): Alert[] {
    const now = Date.now();
    const state = this.getState(service) as any;
    const prev: string | null = state.taskLastResult ?? null;
    const alerts: Alert[] = [];

    if (prev !== result) {
      if (result.toUpperCase().includes("FAIL") || result.toUpperCase().includes("ERROR")) {
        if (!this.inDedupe(service)) {
          alerts.push({
            service, type: "task_failed",
            message: `❌ <b>${service}</b> task FAILED (was: ${prev ?? "unknown"}, now: ${result})`,
            timestamp: now,
          });
          this.markAlertSent(service);
        }
      } else if (prev?.toUpperCase().includes("FAIL") || prev?.toUpperCase().includes("ERROR")) {
        alerts.push({
          service, type: "task_recovered",
          message: `✅ <b>${service}</b> task RECOVERED (${prev} → ${result})`,
          timestamp: now,
        });
        this.markAlertSent(service);
      }
    }

    if (this.stateManager) {
      this.stateManager.set(service, { taskLastResult: result });
    } else {
      (this.getState(service) as any).taskLastResult = result;
    }

    return alerts;
  }
}

// ── Formatters ───────────────────────────────────────────────────────────────

export function formatTelegramMessage(alert: Alert): string {
  return [
    `<b>🚨 Service Alert</b>`,
    ``,
    alert.message,
    ``,
    `<i>${new Date(alert.timestamp).toISOString()}</i>`,
  ].join("\n");
}

export function formatTelegramDigest(alerts: Alert[]): string {
  if (alerts.length === 0) return "✅ All services operational.";
  return [
    `<b>⚠️ ${alerts.length} Alert(s)</b>`,
    "",
    ...alerts.map((a) => a.message),
    "",
    `<i>${new Date().toISOString()}</i>`,
  ].join("\n");
}
