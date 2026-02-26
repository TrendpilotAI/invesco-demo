#!/usr/bin/env node
// Aggregates all judge reports into a daily scorecard
import fs from 'fs';
import path from 'path';

const REPORTS_DIR = '/data/workspace/reports';
const today = new Date().toISOString().split('T')[0];

const projects = ['flipmyera', 'secondopinion', 'narrativereactor', 'trendpilot', 'railway-saas'];
const projectNames = {
  'flipmyera': 'FlipMyEra',
  'secondopinion': 'Second-Opinion',
  'narrativereactor': 'NarrativeReactor',
  'trendpilot': 'Trendpilot',
  'railway-saas': 'Railway SaaS'
};

const categories = ['ux_design', 'capabilities', 'code_quality', 'performance', 'ease_of_use', 'production_readiness', 'x_factor'];
const catNames = {
  'ux_design': 'UX/Design',
  'capabilities': 'Capabilities',
  'code_quality': 'Code Quality',
  'performance': 'Performance',
  'ease_of_use': 'Ease of Use',
  'production_readiness': 'Prod Ready',
  'x_factor': 'X-Factor'
};

function loadReport(project) {
  const file = path.join(REPORTS_DIR, `judge-${project}-${today}.json`);
  try {
    return JSON.parse(fs.readFileSync(file, 'utf-8'));
  } catch {
    return null;
  }
}

function generateMarkdown(reports) {
  let md = `# 🍯 Project Scorecard — ${today}\n\n`;
  
  // Summary table
  md += `## Overall Scores\n\n`;
  md += `| Project | UX | Caps | Code | Perf | Ease | Prod | X | **Total** |\n`;
  md += `|---------|:--:|:----:|:----:|:----:|:----:|:----:|:-:|:---------:|\n`;
  
  for (const [key, report] of Object.entries(reports)) {
    if (!report) continue;
    const s = report.scores;
    const scores = categories.map(c => s[c]?.score ?? '-');
    md += `| ${report.project} | ${scores.join(' | ')} | **${report.weighted_total?.toFixed(1) ?? '-'}** |\n`;
  }
  
  md += `\n`;
  
  // Detailed breakdowns
  for (const [key, report] of Object.entries(reports)) {
    if (!report) continue;
    md += `---\n\n## ${report.project}\n\n`;
    md += `**Overall: ${report.weighted_total?.toFixed(1) ?? 'N/A'}/10**\n\n`;
    md += `> ${report.summary}\n\n`;
    
    // Category details
    for (const cat of categories) {
      const s = report.scores[cat];
      if (!s) continue;
      md += `### ${catNames[cat]}: ${s.score}/10\n`;
      md += `${s.commentary}\n`;
      if (s.strengths?.length) md += `- ✅ ${s.strengths.join('\n- ✅ ')}\n`;
      if (s.weaknesses?.length) md += `- ❌ ${s.weaknesses.join('\n- ❌ ')}\n`;
      md += `\n`;
    }
    
    // Recommendations
    if (report.recommendations?.length) {
      md += `### Top Recommendations\n`;
      report.recommendations.forEach((r, i) => {
        md += `${i + 1}. ${r}\n`;
      });
      md += `\n`;
    }
    
    // Feature inventory
    if (report.feature_inventory?.length) {
      md += `### Feature Inventory\n`;
      md += `| Feature | Status | Tests |\n|---------|--------|-------|\n`;
      for (const f of report.feature_inventory) {
        const status = f.status === 'complete' ? '✅' : f.status === 'partial' ? '🔶' : '⬜';
        const tests = f.has_tests ? '✅' : '❌';
        md += `| ${f.feature} | ${status} ${f.status} | ${tests} |\n`;
      }
      md += `\n`;
    }
  }
  
  // Trend tracking (append to history)
  md += `---\n\n## Historical Trend\n\n`;
  md += `*Daily scores will accumulate here over time.*\n\n`;
  md += `| Date | FlipMyEra | Second-Opinion | NarrativeReactor | Trendpilot | Railway SaaS |\n`;
  md += `|------|:---------:|:--------------:|:----------------:|:----------:|:------------:|\n`;
  
  const totals = projects.map(p => reports[p]?.weighted_total?.toFixed(1) ?? '-');
  md += `| ${today} | ${totals.join(' | ')} |\n`;
  
  return md;
}

// Main
const reports = {};
let found = 0;
for (const p of projects) {
  reports[p] = loadReport(p);
  if (reports[p]) found++;
}

console.log(`Found ${found}/${projects.length} judge reports for ${today}`);

if (found > 0) {
  const md = generateMarkdown(reports);
  const outPath = path.join(REPORTS_DIR, `scorecard-${today}.md`);
  fs.writeFileSync(outPath, md);
  console.log(`Scorecard written to ${outPath}`);
  
  // Also save raw data for trending
  const historyPath = path.join(REPORTS_DIR, 'score-history.json');
  let history = [];
  try { history = JSON.parse(fs.readFileSync(historyPath, 'utf-8')); } catch {}
  
  const entry = { date: today, scores: {} };
  for (const [key, report] of Object.entries(reports)) {
    if (report) {
      entry.scores[key] = {
        total: report.weighted_total,
        categories: Object.fromEntries(
          categories.map(c => [c, report.scores[c]?.score ?? null])
        )
      };
    }
  }
  history.push(entry);
  fs.writeFileSync(historyPath, JSON.stringify(history, null, 2));
  console.log(`History updated (${history.length} entries)`);
} else {
  console.log('No reports found yet — judges may still be running.');
}
