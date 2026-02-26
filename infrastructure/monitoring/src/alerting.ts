import type { HealthResult } from "./healthcheck.js";

export interface Alert {
  service: string;
  type: "down" | "slow" | "recovered";
  message: string;
  timestamp: number;
}

export interface AlertConfig {
  responseTimeThresholdMs: number;
  cooldownMs: number;
}

const DEFAULT_CONFIG: AlertConfig = {
  responseTimeThresholdMs: 5000,
  cooldownMs: 60 * 60 * 1000, // 1 hour
};

export class AlertManager {
  private lastAlertTime: Map<string, number> = new Map();
  private lastStatus: Map<string, HealthResult["status"]> = new Map();
  private config: AlertConfig;
  private sentAlerts: Alert[] = [];

  constructor(config: Partial<AlertConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  evaluate(result: HealthResult): Alert | null {
    const prev = this.lastStatus.get(result.service);
    this.lastStatus.set(result.service, result.status);

    let alert: Alert | null = null;

    if (result.status === "down") {
      alert = {
        service: result.service, type: "down",
        message: `🔴 ${result.service} is DOWN${result.error ? `: ${result.error}` : ""} (HTTP ${result.httpCode ?? "N/A"})`,
        timestamp: Date.now(),
      };
    } else if (result.responseTimeMs > this.config.responseTimeThresholdMs) {
      alert = {
        service: result.service, type: "slow",
        message: `🟡 ${result.service} is SLOW: ${result.responseTimeMs}ms (threshold: ${this.config.responseTimeThresholdMs}ms)`,
        timestamp: Date.now(),
      };
    } else if (prev === "down" && result.status === "healthy") {
      alert = {
        service: result.service, type: "recovered",
        message: `🟢 ${result.service} has RECOVERED (${result.responseTimeMs}ms)`,
        timestamp: Date.now(),
      };
      // Recovery alerts bypass cooldown
      this.lastAlertTime.set(result.service, Date.now());
      this.sentAlerts.push(alert);
      return alert;
    }

    if (!alert) return null;

    // Cooldown check
    const lastTime = this.lastAlertTime.get(result.service) ?? 0;
    if (Date.now() - lastTime < this.config.cooldownMs) return null;

    this.lastAlertTime.set(result.service, Date.now());
    this.sentAlerts.push(alert);
    return alert;
  }

  evaluateAll(results: HealthResult[]): Alert[] {
    return results.map((r) => this.evaluate(r)).filter((a): a is Alert => a !== null);
  }

  getSentAlerts(): Alert[] {
    return this.sentAlerts;
  }
}

// Telegram message formatter
export function formatTelegramMessage(alert: Alert): string {
  return [
    `<b>Service Alert</b>`,
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
