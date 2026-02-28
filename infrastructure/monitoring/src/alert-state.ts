/**
 * Persistent alert state manager.
 *
 * Tracks per-service:
 *  - lastStatus          (previous health status)
 *  - lastAlertSentAt     (unix ms, for deduplication cooldown)
 *  - downSince           (unix ms when first went down, for escalation)
 *  - escalatedAt         (unix ms of last escalation alert)
 *  - taskLastResult      (last known task result string, e.g. "SUCCESS" | "FAILED")
 */

import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { dirname } from "path";

export interface ServiceAlertState {
  lastStatus: string | null;          // "healthy" | "degraded" | "down" | null
  lastAlertSentAt: number | null;     // unix ms
  downSince: number | null;           // unix ms (null = not currently down)
  escalatedAt: number | null;         // unix ms of last escalation
  taskLastResult: string | null;      // last task result string
}

export type AlertStateMap = Record<string, ServiceAlertState>;

const DEFAULT_SERVICE_STATE: ServiceAlertState = {
  lastStatus: null,
  lastAlertSentAt: null,
  downSince: null,
  escalatedAt: null,
  taskLastResult: null,
};

export class AlertStateManager {
  private path: string;
  private state: AlertStateMap;

  constructor(statePath: string) {
    this.path = statePath;
    this.state = this.load();
  }

  private load(): AlertStateMap {
    try {
      const raw = readFileSync(this.path, "utf8");
      return JSON.parse(raw) as AlertStateMap;
    } catch {
      return {};
    }
  }

  save(): void {
    mkdirSync(dirname(this.path), { recursive: true });
    writeFileSync(this.path, JSON.stringify(this.state, null, 2));
  }

  get(service: string): ServiceAlertState {
    if (!this.state[service]) {
      this.state[service] = { ...DEFAULT_SERVICE_STATE };
    }
    return this.state[service];
  }

  set(service: string, patch: Partial<ServiceAlertState>): void {
    this.state[service] = { ...this.get(service), ...patch };
  }
}
