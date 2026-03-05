use anyhow::Result;
use regex::Regex;
use serde::Serialize;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize)]
pub struct MemoryLog {
    pub date: String,
    pub sessions: Vec<MemorySession>,
}

#[derive(Debug, Clone, Serialize)]
pub struct MemorySession {
    pub timestamp: String,
    pub model: String,
    pub goals: String,
    pub tags: Vec<String>,
    pub summary: String,
}

/// Parse memory/YYYY-MM-DD.md files into structured logs
pub fn parse_memory_logs(workspace: &Path) -> Result<Vec<MemoryLog>> {
    let memory_dir = workspace.join("memory");
    if !memory_dir.exists() {
        return Ok(vec![]);
    }

    let date_re = Regex::new(r"^(\d{4}-\d{2}-\d{2})\.md$")?;
    let session_re = Regex::new(r"## Session — (.+)")?;
    let model_re = Regex::new(r"\*\*Model:\*\*\s*(.+)")?;
    let goals_re = Regex::new(r"\*\*Goals:\*\*\s*(.+)")?;
    let tags_re = Regex::new(r"\*\*Tags:\*\*\s*(.+)")?;

    let mut logs = Vec::new();

    let mut entries: Vec<_> = fs::read_dir(&memory_dir)?
        .filter_map(|e| e.ok())
        .collect();
    entries.sort_by_key(|e| e.file_name());

    for entry in entries {
        let fname = entry.file_name().to_string_lossy().to_string();
        if let Some(caps) = date_re.captures(&fname) {
            let date = caps.get(1).unwrap().as_str().to_string();
            let content = fs::read_to_string(entry.path()).unwrap_or_default();

            let sessions = parse_sessions(&content, &session_re, &model_re, &goals_re, &tags_re);
            if !sessions.is_empty() {
                logs.push(MemoryLog { date, sessions });
            }
        }
    }

    Ok(logs)
}

fn parse_sessions(
    content: &str,
    session_re: &Regex,
    model_re: &Regex,
    goals_re: &Regex,
    tags_re: &Regex,
) -> Vec<MemorySession> {
    let mut sessions = Vec::new();
    let mut current_lines: Vec<&str> = Vec::new();
    let mut current_ts: Option<String> = None;

    for line in content.lines() {
        if let Some(caps) = session_re.captures(line) {
            // Flush previous session
            if let Some(ts) = current_ts.take() {
                let block = current_lines.join("\n");
                sessions.push(parse_session_block(&ts, &block, model_re, goals_re, tags_re));
                current_lines.clear();
            }
            current_ts = Some(caps.get(1).unwrap().as_str().to_string());
        } else if current_ts.is_some() {
            current_lines.push(line);
        }
    }

    // Flush last
    if let Some(ts) = current_ts {
        let block = current_lines.join("\n");
        sessions.push(parse_session_block(&ts, &block, model_re, goals_re, tags_re));
    }

    sessions
}

fn parse_session_block(
    ts: &str,
    block: &str,
    model_re: &Regex,
    goals_re: &Regex,
    tags_re: &Regex,
) -> MemorySession {
    let model = model_re
        .captures(block)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().trim().to_string())
        .unwrap_or_default();

    let goals = goals_re
        .captures(block)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().trim().to_string())
        .unwrap_or_default();

    let tags = tags_re
        .captures(block)
        .and_then(|c| c.get(1))
        .map(|m| {
            m.as_str()
                .split(',')
                .map(|t| t.trim().to_string())
                .collect()
        })
        .unwrap_or_default();

    // Everything after the metadata lines is the summary
    let summary_lines: Vec<&str> = block
        .lines()
        .skip_while(|l| {
            l.starts_with("**Model:")
                || l.starts_with("**Goals:")
                || l.starts_with("**Tags:")
                || l.trim().is_empty()
        })
        .collect();

    MemorySession {
        timestamp: ts.to_string(),
        model,
        goals,
        tags,
        summary: summary_lines.join("\n").chars().take(4000).collect(),
    }
}
