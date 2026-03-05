use anyhow::Result;
use regex::Regex;
use serde::Serialize;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize)]
pub struct TodoItem {
    pub task_id: String,
    pub filename: String,
    pub status: String,
    pub priority: String,
    pub project_name: String,
    pub title: String,
    pub body: String,
    pub tags: Vec<String>,
}

/// Parse TODO files from the todos/ directory.
/// Filename pattern: {id}-{status}-{priority}-{project}-{slug}.md
/// e.g. 004-pending-critical-forwardlane-backend-fix-sql-injection-order-by.md
pub fn parse_todos(workspace: &Path) -> Result<Vec<TodoItem>> {
    let todos_dir = workspace.join("todos");
    if !todos_dir.exists() {
        tracing::warn!("No todos/ directory found");
        return Ok(vec![]);
    }

    let filename_re = Regex::new(
        r"^(\d+)-(complete|done|pending|ready|blocked|in.progress)-(p[0-3]|critical|high|medium|low)-(.+)\.md$"
    )?;

    let mut items = Vec::new();

    let mut entries: Vec<_> = fs::read_dir(&todos_dir)?
        .filter_map(|e| e.ok())
        .collect();
    entries.sort_by_key(|e| e.file_name());

    for entry in entries {
        let fname = entry.file_name().to_string_lossy().to_string();
        if !fname.ends_with(".md") {
            continue;
        }

        let content = fs::read_to_string(entry.path()).unwrap_or_default();

        // Try regex parse on filename
        if let Some(caps) = filename_re.captures(&fname.clone()) {
            let id = caps.get(1).unwrap().as_str();
            let status = caps.get(2).unwrap().as_str();
            let priority = caps.get(3).unwrap().as_str();
            let rest = caps.get(4).unwrap().as_str();

            // Extract project name — first segment before the slug
            // e.g. "forwardlane-backend-fix-sql-injection" → project might be in the content
            let project_name = extract_project_from_content(&content)
                .unwrap_or_else(|| extract_project_from_slug(rest));

            let title = extract_title(&content).unwrap_or_else(|| rest.replace('-', " "));

            let tags = extract_frontmatter_tags(&content);

            let kanban_status = normalize_status(status);

            items.push(TodoItem {
                task_id: format!("todo-{}", id),
                filename: fname,
                status: kanban_status,
                priority: normalize_priority(priority),
                project_name,
                title,
                body: content.chars().take(2000).collect(),
                tags,
            });
        } else {
            // Fallback: just use the filename
            let title = fname.trim_end_matches(".md").replace('-', " ");
            items.push(TodoItem {
                task_id: format!("todo-{}", fname.split('-').next().unwrap_or("0")),
                filename: fname,
                status: "todo".to_string(),
                priority: "p2".to_string(),
                project_name: "unknown".to_string(),
                title,
                body: content.chars().take(2000).collect(),
                tags: vec![],
            });
        }
    }

    Ok(items)
}

fn extract_project_from_content(content: &str) -> Option<String> {
    // Look for **Repo:** or **Project:** in content
    let re = Regex::new(r"(?i)\*\*(?:repo|project):\*\*\s*(.+)").ok()?;
    re.captures(content)?
        .get(1)
        .map(|m| m.as_str().trim().to_string())
}

fn extract_project_from_slug(slug: &str) -> String {
    // Take first 1-3 segments as project name
    let parts: Vec<&str> = slug.split('-').collect();
    if parts.len() <= 2 {
        parts.join("-")
    } else {
        // Heuristic: known project prefixes
        let known = [
            "signal-studio", "forwardlane-backend", "signal-builder-backend",
            "signal-builder-frontend", "invesco-retention", "flip-my-era",
            "ultrafone", "signal-studio-auth", "signal-studio-data-provider",
            "signal-studio-frontend", "signal-studio-templates",
        ];
        for k in &known {
            if slug.starts_with(k) {
                return k.to_string();
            }
        }
        parts[..2.min(parts.len())].join("-")
    }
}

fn extract_title(content: &str) -> Option<String> {
    // First # heading
    for line in content.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("# ") {
            return Some(trimmed[2..].trim().to_string());
        }
    }
    None
}

fn extract_frontmatter_tags(content: &str) -> Vec<String> {
    // Look for tags: [x, y, z] in YAML frontmatter
    let re = Regex::new(r"tags:\s*\[([^\]]+)\]").ok();
    re.and_then(|r| {
        r.captures(content).map(|c| {
            c.get(1)
                .unwrap()
                .as_str()
                .split(',')
                .map(|t| t.trim().to_string())
                .collect()
        })
    })
    .unwrap_or_default()
}

fn normalize_status(s: &str) -> String {
    match s {
        "complete" | "done" => "done".to_string(),
        "pending" | "ready" => "todo".to_string(),
        "blocked" => "blocked".to_string(),
        s if s.contains("progress") => "in_progress".to_string(),
        _ => "todo".to_string(),
    }
}

fn normalize_priority(p: &str) -> String {
    match p {
        "critical" => "p0".to_string(),
        "high" => "p1".to_string(),
        "medium" => "p2".to_string(),
        "low" => "p3".to_string(),
        other => other.to_string(),
    }
}
