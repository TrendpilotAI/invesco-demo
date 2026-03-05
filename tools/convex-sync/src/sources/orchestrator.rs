use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrchestratorTask {
    pub id: String,
    pub task: String,
    pub model: String,
    #[serde(default)]
    pub agent_alias: String,
    pub status: String,
    pub created_at: String,
    #[serde(default)]
    pub completed_at: Option<String>,
    #[serde(default)]
    pub result: Option<String>,
    #[serde(default)]
    pub branch: Option<String>,
}

/// Parse orchestrator tasks from .orchestrator/tasks.json
pub fn parse_tasks(workspace: &Path) -> Result<Vec<OrchestratorTask>> {
    let tasks_file = workspace.join(".orchestrator/tasks.json");
    if !tasks_file.exists() {
        tracing::warn!("No .orchestrator/tasks.json found");
        return Ok(vec![]);
    }

    let content = fs::read_to_string(&tasks_file)?;
    let tasks: Vec<OrchestratorTask> = serde_json::from_str(&content)?;
    Ok(tasks)
}
