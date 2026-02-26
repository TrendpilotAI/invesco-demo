export interface ServiceConfig {
  name: string;
  url: string;
  timeout?: number;
}

export interface HealthResult {
  service: string;
  url: string;
  status: "healthy" | "degraded" | "down";
  httpCode: number | null;
  responseTimeMs: number;
  checkedAt: string;
  error?: string;
}

export const SERVICES: ServiceConfig[] = [
  { name: "n8n", url: "https://primary-production-4244.up.railway.app" },
  { name: "FlipMyEra", url: "https://flipmyera.com" },
  { name: "SignalHaus", url: "https://www.signalhaus.ai" },
];

export async function checkService(svc: ServiceConfig): Promise<HealthResult> {
  const timeout = svc.timeout ?? 10000;
  const start = performance.now();
  const checkedAt = new Date().toISOString();

  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);
    const res = await fetch(svc.url, {
      method: "GET",
      signal: controller.signal,
      redirect: "follow",
    });
    clearTimeout(timer);
    const responseTimeMs = Math.round(performance.now() - start);

    let status: HealthResult["status"] = "healthy";
    if (res.status >= 500) status = "down";
    else if (res.status >= 400) status = "degraded";
    else if (responseTimeMs > 5000) status = "degraded";

    return { service: svc.name, url: svc.url, status, httpCode: res.status, responseTimeMs, checkedAt };
  } catch (err: any) {
    const responseTimeMs = Math.round(performance.now() - start);
    return {
      service: svc.name, url: svc.url, status: "down",
      httpCode: null, responseTimeMs, checkedAt,
      error: err?.message ?? "Unknown error",
    };
  }
}

export async function checkAll(services: ServiceConfig[] = SERVICES): Promise<HealthResult[]> {
  return Promise.all(services.map(checkService));
}

// CLI entry
if (process.argv[1]?.includes("healthcheck")) {
  checkAll().then((r) => console.log(JSON.stringify(r, null, 2)));
}
