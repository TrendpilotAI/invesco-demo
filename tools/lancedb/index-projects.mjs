import * as lancedb from "@lancedb/lancedb";
import fs from "fs";
import path from "path";

const PROJECTS_DIR = "/data/workspace/projects";
const DB_PATH = "/data/workspace/tools/lancedb/db";

function getProjectFiles(projectDir, projectName) {
  const files = [];
  const exts = [".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".yaml", ".yml", ".css"];
  const ignore = ["node_modules", ".next", "dist", "build", ".git", "coverage", "__pycache__", ".cache"];
  
  function walk(dir, depth = 0) {
    if (depth > 6) return;
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        if (ignore.includes(entry.name) || entry.name.startsWith(".")) continue;
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          walk(fullPath, depth + 1);
        } else if (exts.some(e => entry.name.endsWith(e))) {
          try {
            const content = fs.readFileSync(fullPath, "utf-8");
            if (content.length > 0 && content.length < 50000) {
              files.push({
                project: projectName,
                file: path.relative(projectDir, fullPath),
                content: content.substring(0, 4000),
                fullContent: content,
                size: content.length,
                ext: path.extname(entry.name),
                type: categorize(entry.name, fullPath),
              });
            }
          } catch {}
        }
      }
    } catch {}
  }
  walk(projectDir);
  return files;
}

function categorize(name, p) {
  if (name.includes("test") || name.includes("spec")) return "test";
  if (name === "package.json" || name.endsWith(".config.ts") || name.endsWith(".config.js")) return "config";
  if (name.endsWith(".md")) return "docs";
  if (p.includes("/api/") || name.includes("route") || name.includes("api")) return "api";
  if (name.endsWith(".tsx") || name.endsWith(".jsx")) return "component";
  if (name.endsWith(".css")) return "style";
  if (name.includes("hook") || name.includes("util") || name.includes("lib")) return "utility";
  return "source";
}

function makeVector(f) {
  const vec = new Array(128).fill(0);
  const c = f.content;
  
  // Type (0-7)
  const types = ["component","api","test","config","docs","style","utility","source"];
  const ti = types.indexOf(f.type);
  if (ti >= 0) vec[ti] = 1;
  
  // Tech stack (8-31)
  const markers = [
    "React", "express", "useState", "async", "fetch", "test(", "stripe",
    "supabase", "firebase", "openai", "webhook", "auth", "postgres",
    "redis", "tailwind", "router", "clerk", "sentry", "vite", "next",
    "prisma", "jwt", "middleware", "cron"
  ];
  markers.forEach((m, i) => {
    vec[8 + i] = c.toLowerCase().includes(m.toLowerCase()) ? 1 : 0;
  });
  
  // Patterns (32-47)
  vec[32] = Math.min((c.match(/export /g) || []).length / 20, 1);
  vec[33] = Math.min((c.match(/import /g) || []).length / 20, 1);
  vec[34] = Math.min((c.match(/function /g) || []).length / 10, 1);
  vec[35] = Math.min((c.match(/interface /g) || []).length / 5, 1);
  vec[36] = Math.min(c.length / 4000, 1);
  vec[37] = Math.min((c.match(/\n/g) || []).length / 200, 1);
  vec[38] = c.includes("TODO") || c.includes("FIXME") ? 1 : 0;
  vec[39] = c.includes("@deprecated") ? 1 : 0;
  
  // Project (48-63)
  const projs = ["Second-Opinion","flip-my-era","NarrativeReactor","Trendpilot",
    "forwardlane-website","signalhaus-website","mission-control","doc-pipeline",
    "fast-browser-search","thinkchain","n8n-workflows","postiz-railway"];
  const pi = projs.indexOf(f.project);
  if (pi >= 0) vec[48 + pi] = 1;
  
  // Cross-project references (64-79)
  projs.forEach((p, i) => {
    if (c.toLowerCase().includes(p.toLowerCase())) vec[64 + i] = 1;
  });
  
  // Domain (80-95)
  const domains = ["medical","health","ebook","taylor","trend","signal","content",
    "marketing","payment","subscription","analytics","dashboard","deploy","monitor",
    "email","social"];
  domains.forEach((d, i) => {
    vec[80 + i] = c.toLowerCase().includes(d) ? 1 : 0;
  });
  
  // Fill rest with normalized metrics
  vec[96] = f.ext === ".tsx" ? 1 : 0;
  vec[97] = f.ext === ".ts" ? 1 : 0;
  vec[98] = f.ext === ".md" ? 1 : 0;
  vec[99] = f.ext === ".json" ? 1 : 0;
  
  return vec;
}

async function main() {
  const projects = fs.readdirSync(PROJECTS_DIR).filter(d => {
    try { return fs.statSync(path.join(PROJECTS_DIR, d)).isDirectory(); } catch { return false; }
  });

  console.log(`Indexing ${projects.length} projects...`);

  const allFiles = [];
  const analysis = {};

  for (const proj of projects) {
    const projDir = path.join(PROJECTS_DIR, proj);
    const files = getProjectFiles(projDir, proj);
    allFiles.push(...files);
    
    // Deep analysis
    const pkgPath = path.join(projDir, "package.json");
    let pkg = {};
    try { pkg = JSON.parse(fs.readFileSync(pkgPath, "utf-8")); } catch {}
    
    // Find cross-project references
    const crossRefs = {};
    for (const f of files) {
      for (const otherProj of projects) {
        if (otherProj === proj) continue;
        if (f.fullContent.toLowerCase().includes(otherProj.toLowerCase())) {
          crossRefs[otherProj] = (crossRefs[otherProj] || 0) + 1;
        }
      }
    }
    
    // Find API endpoints
    const endpoints = [];
    for (const f of files) {
      const matches = f.fullContent.match(/(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*['"`]([^'"`]+)/g) || [];
      endpoints.push(...matches.map(m => m.replace(/.*\(['"`]/, "").replace(/['"`].*/, "")));
    }
    
    // Find shared tech
    const allDeps = { ...pkg.dependencies, ...pkg.devDependencies };
    
    // Detect architecture patterns
    const patterns = [];
    const allContent = files.map(f => f.fullContent).join("\n");
    if (allContent.includes("webhook")) patterns.push("webhooks");
    if (allContent.includes("middleware")) patterns.push("middleware");
    if (allContent.includes("JWT") || allContent.includes("jwt")) patterns.push("jwt-auth");
    if (allContent.includes("rate limit")) patterns.push("rate-limiting");
    if (allContent.includes("queue") || allContent.includes("worker")) patterns.push("job-queue");
    if (allContent.includes("websocket") || allContent.includes("socket.io")) patterns.push("realtime");
    if (allContent.includes("cron") || allContent.includes("schedule")) patterns.push("scheduled-tasks");
    if (allContent.includes("cache")) patterns.push("caching");
    
    analysis[proj] = {
      files: files.length,
      byType: {},
      byExt: {},
      dependencies: Object.keys(pkg.dependencies || {}),
      devDeps: Object.keys(pkg.devDependencies || {}),
      scripts: pkg.scripts || {},
      description: pkg.description || "",
      crossRefs,
      endpoints: [...new Set(endpoints)],
      patterns,
      hasTests: files.some(f => f.type === "test"),
      hasDocs: files.some(f => f.type === "docs"),
      hasCI: fs.existsSync(path.join(projDir, ".github")),
      totalLines: files.reduce((s, f) => s + (f.fullContent.match(/\n/g) || []).length, 0),
    };
    
    for (const f of files) {
      analysis[proj].byType[f.type] = (analysis[proj].byType[f.type] || 0) + 1;
      analysis[proj].byExt[f.ext] = (analysis[proj].byExt[f.ext] || 0) + 1;
    }
    
    console.log(`  ${proj}: ${files.length} files, ${analysis[proj].totalLines} lines, ${analysis[proj].dependencies.length} deps, patterns: [${patterns.join(", ")}]`);
  }

  // Create LanceDB table
  const db = await lancedb.connect(DB_PATH);
  
  const records = allFiles.map((f, i) => ({
    id: i,
    project: f.project,
    file: f.file,
    content: f.content,
    type: f.type,
    ext: f.ext,
    size: f.size,
    vector: makeVector(f),
  }));

  try { await db.dropTable("projects"); } catch {}
  await db.createTable("projects", records);
  console.log(`\nLanceDB: ${records.length} records indexed`);

  // Write full analysis
  fs.writeFileSync("/data/workspace/tools/lancedb/project-analysis.json", JSON.stringify(analysis, null, 2));
  console.log("Analysis written to project-analysis.json");
  
  // Find integration opportunities
  const integrations = [];
  for (const [p1, a1] of Object.entries(analysis)) {
    for (const [p2, a2] of Object.entries(analysis)) {
      if (p1 >= p2) continue;
      const sharedDeps = a1.dependencies.filter(d => a2.dependencies.includes(d));
      const sharedPatterns = a1.patterns.filter(p => a2.patterns.includes(p));
      if (sharedDeps.length > 3 || sharedPatterns.length > 1 || a1.crossRefs[p2] || a2.crossRefs[p1]) {
        integrations.push({
          projects: [p1, p2],
          sharedDeps: sharedDeps.length,
          sharedPatterns,
          crossRefs: (a1.crossRefs[p2] || 0) + (a2.crossRefs[p1] || 0),
        });
      }
    }
  }
  
  fs.writeFileSync("/data/workspace/tools/lancedb/integrations.json", JSON.stringify(integrations, null, 2));
  console.log(`Found ${integrations.length} integration opportunities`);
}

main().catch(console.error);
