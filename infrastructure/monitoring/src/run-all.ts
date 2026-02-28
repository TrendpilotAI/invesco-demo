import { checkAll, SERVICES } from "./healthcheck.js";
import { store } from "./metrics.js";
import { AlertManager, formatTelegramMessage, formatTelegramDigest } from "./alerting.js";
import { buildDashboard, writeDashboard } from "./dashboard-data.js";
import { AlertStateManager } from "./alert-state.js";
import { Notifier } from "./notifier.js";

const STATUS_PATH = "/data/workspace/dashboard/status.json";
const ALERT_STATE_PATH = "/data/workspace/dashboard/alert-state.json";

async function main() {
  console.log("🔍 Running health checks...");
  const results = await checkAll(SERVICES);
  store.recordAll(results);

  // Persistent state — survives across cron runs
  const stateManager = new AlertStateManager(ALERT_STATE_PATH);
  const alertMgr = new AlertManager({}, stateManager);
  const notifier = new Notifier();

  const alerts = alertMgr.evaluateAll(results);

  // Save updated state
  stateManager.save();

  // Send individual alerts (each fires immediately so timing is precise)
  if (alerts.length > 0) {
    console.log(`\n⚠️  ${alerts.length} alert(s) to send:`);
    for (const alert of alerts) {
      console.log(" •", alert.message);
      await notifier.send(formatTelegramMessage(alert));
    }
  } else {
    console.log("\n✅ All services operational");
  }

  const dashboard = buildDashboard(results, store);
  writeDashboard(dashboard, STATUS_PATH);
  console.log(`\n📊 Dashboard written to ${STATUS_PATH}`);
}

main().catch(console.error);
