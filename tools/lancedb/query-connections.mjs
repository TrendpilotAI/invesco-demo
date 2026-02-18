import * as lancedb from "@lancedb/lancedb";
import fs from "fs";

const DB_PATH = "/data/workspace/tools/lancedb/db";

async function main() {
  const db = await lancedb.connect(DB_PATH);
  const table = await db.openTable("projects");
  
  // Find auth-related files across projects
  const authFiles = await table.search(makeQuery("auth")).limit(20).toArray();
  console.log("\n=== AUTH FILES ACROSS PROJECTS ===");
  for (const r of authFiles) {
    if (r.content.toLowerCase().includes("auth")) {
      console.log(`  ${r.project}/${r.file} (${r.type})`);
    }
  }
  
  // Find API/webhook files
  const apiFiles = await table.search(makeQuery("api")).limit(30).toArray();
  console.log("\n=== API/WEBHOOK FILES ===");
  for (const r of apiFiles) {
    if (r.type === "api" || r.content.toLowerCase().includes("webhook") || r.content.toLowerCase().includes("endpoint")) {
      console.log(`  ${r.project}/${r.file} (${r.type})`);
    }
  }
  
  // Find shared UI components
  const uiFiles = await table.search(makeQuery("component")).limit(30).toArray();
  console.log("\n=== UI COMPONENTS ===");
  const uiByProject = {};
  for (const r of uiFiles) {
    if (r.type === "component") {
      uiByProject[r.project] = (uiByProject[r.project] || 0) + 1;
    }
  }
  console.log(`  Components per project: ${JSON.stringify(uiByProject)}`);
  
  // Find payment/billing code
  console.log("\n=== PAYMENT/BILLING ===");
  const allRecords = await table.search(makeQuery("payment")).limit(50).toArray();
  for (const r of allRecords) {
    if (r.content.toLowerCase().includes("stripe") || r.content.toLowerCase().includes("payment") || r.content.toLowerCase().includes("billing")) {
      console.log(`  ${r.project}/${r.file}`);
    }
  }
  
  // Find test infrastructure
  console.log("\n=== TEST COVERAGE ===");
  const testRecords = await table.search(makeQuery("test")).limit(100).toArray();
  const testsByProject = {};
  for (const r of testRecords) {
    if (r.type === "test") {
      testsByProject[r.project] = (testsByProject[r.project] || 0) + 1;
    }
  }
  console.log(`  Test files per project: ${JSON.stringify(testsByProject)}`);
  
  // Find deployment configs
  console.log("\n=== DEPLOYMENT CONFIGS ===");
  const configRecords = await table.search(makeQuery("config")).limit(50).toArray();
  for (const r of configRecords) {
    if (r.file.includes("deploy") || r.file.includes("docker") || r.file.includes("railway") || r.file.includes("vercel") || r.file.includes("netlify") || r.file.includes("firebase")) {
      console.log(`  ${r.project}/${r.file}`);
    }
  }
}

function makeQuery(focus) {
  const vec = new Array(128).fill(0);
  switch(focus) {
    case "auth": vec[27] = 1; vec[21] = 1; break;
    case "api": vec[1] = 1; vec[26] = 1; break;
    case "component": vec[0] = 1; vec[30] = 1; break;
    case "payment": vec[22] = 1; break;
    case "test": vec[2] = 1; vec[21] = 1; break;
    case "config": vec[3] = 1; break;
  }
  return vec;
}

main().catch(console.error);
