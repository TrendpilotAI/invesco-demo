import { checkAll, SERVICES } from "./healthcheck.js";
import { store } from "./metrics.js";
import { AlertManager, formatTelegramDigest } from "./alerting.js";
import { buildDashboard, writeDashboard } from "./dashboard-data.js";

const STATUS_PATH = "/data/workspace/dashboard/status.json";

async function main() {
  console.log("🔍 Running health checks...");
  const results = await checkAll(SERVICES);
  store.recordAll(results);

  const alertMgr = new AlertManager();
  const alerts = alertMgr.evaluateAll(results);

  if (alerts.length > 0) {
    console.log("\n⚠️ Alerts:");
    console.log(formatTelegramDigest(alerts));
  } else {
    console.log("\n✅ All services operational");
  }

  const dashboard = buildDashboard(results, store);
  writeDashboard(dashboard, STATUS_PATH);
  console.log(`\n📊 Dashboard written to ${STATUS_PATH}`);
  console.log(JSON.stringify(dashboard, null, 2));
}

main().catch(console.error);
