import * as lancedb from "@lancedb/lancedb";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const DB_PATH = "/data/workspace/tools/lancedb/db";
const MEMORY_DIR = "/data/workspace/memory";

// Simple text → vector (128d) based on content signals
function textToVector(text) {
  const vec = new Array(128).fill(0);
  const t = text.toLowerCase();
  
  // Topic signals (0-31)
  const topics = [
    "project","deploy","bug","fix","feature","security","auth","api",
    "database","frontend","backend","devops","marketing","sales","finance",
    "strategy","gtm","client","meeting","decision","architecture","performance",
    "testing","ci","monitoring","integration","migration","refactor","design","ux",
    "ai","agent"
  ];
  topics.forEach((topic, i) => { vec[i] = t.includes(topic) ? 1 : 0; });
  
  // Project references (32-47)
  const projects = [
    "flip-my-era","flipmyera","second-opinion","narrativereactor","trendpilot",
    "forwardlane","signalhaus","mission-control","fast-browser-search","thinkchain",
    "ultrafone","contactkiller","postiz","n8n","railway","lancedb"
  ];
  projects.forEach((p, i) => { vec[32 + i] = t.includes(p) ? 1 : 0; });
  
  // Sentiment/type (48-55)
  vec[48] = t.includes("success") || t.includes("completed") || t.includes("shipped") ? 1 : 0;
  vec[49] = t.includes("error") || t.includes("failed") || t.includes("broken") ? 1 : 0;
  vec[50] = t.includes("todo") || t.includes("next") || t.includes("planned") ? 1 : 0;
  vec[51] = t.includes("learned") || t.includes("lesson") || t.includes("insight") ? 1 : 0;
  vec[52] = t.includes("config") || t.includes("setup") || t.includes("install") ? 1 : 0;
  vec[53] = t.includes("credential") || t.includes("key") || t.includes("token") ? 1 : 0;
  vec[54] = t.includes("idea") || t.includes("brainstorm") || t.includes("concept") ? 1 : 0;
  vec[55] = t.includes("workflow") || t.includes("automation") || t.includes("pipeline") ? 1 : 0;
  
  // Text stats (56-63)
  vec[56] = Math.min(text.length / 5000, 1);
  vec[57] = Math.min((text.match(/\n/g) || []).length / 100, 1);
  vec[58] = Math.min((text.match(/- /g) || []).length / 20, 1); // bullet points
  vec[59] = Math.min((text.match(/#{1,3} /g) || []).length / 10, 1); // headers
  
  // Hash-based features for remaining dims (64-127) for diversity
  const hash = crypto.createHash("md5").update(text).digest();
  for (let i = 0; i < 64; i++) {
    vec[64 + i] = (hash[i % 16] >> (i % 8)) & 1 ? 0.5 : 0;
  }
  
  return vec;
}

async function storeSession(entries) {
  const db = await lancedb.connect(DB_PATH);
  
  const records = entries.map((entry, i) => ({
    id: `${entry.date}-${i}-${Date.now()}`,
    date: entry.date,
    category: entry.category || "general",
    title: entry.title,
    content: entry.content,
    tags: (entry.tags || []).join(","),
    source: entry.source || "session",
    vector: textToVector(entry.title + " " + entry.content),
  }));

  try {
    const table = await db.openTable("sessions");
    await table.add(records);
    console.log(`Appended ${records.length} records to sessions table`);
  } catch {
    await db.createTable("sessions", records);
    console.log(`Created sessions table with ${records.length} records`);
  }
}

async function queryLearnings(queryText, limit = 10) {
  const db = await lancedb.connect(DB_PATH);
  const table = await db.openTable("sessions");
  const results = await table.search(textToVector(queryText)).limit(limit).toArray();
  return results;
}

// Main: read from stdin or args
const args = process.argv.slice(2);
if (args[0] === "query") {
  const results = await queryLearnings(args.slice(1).join(" "));
  for (const r of results) {
    console.log(`[${r.date}] ${r.category} — ${r.title}`);
    console.log(`  ${r.content.substring(0, 200)}`);
    console.log();
  }
} else if (args[0] === "store") {
  const dataFile = args[1] || "/dev/stdin";
  const data = JSON.parse(fs.readFileSync(dataFile, "utf-8"));
  await storeSession(Array.isArray(data) ? data : [data]);
} else {
  console.log("Usage:");
  console.log("  node store-session.mjs store <json-file>  — Store session entries");
  console.log("  node store-session.mjs query <text>       — Search learnings");
}
