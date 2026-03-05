use anyhow::Result;
use serde_json::json;

use crate::convex::ConvexClient;
use crate::sources::{memory, orchestrator, projects, todos};

const BATCH_SIZE: usize = 50;

/// Sync TODO items → tasks + kanban tables
pub async fn sync_todos(client: &ConvexClient, todos: &[todos::TodoItem]) -> Result<u64> {
    let items: Vec<serde_json::Value> = todos
        .iter()
        .map(|t| {
            json!({
                "taskId": t.task_id,
                "task": t.title,
                "model": "judge-swarm",
                "status": t.status,
                "priority": t.priority,
                "projectName": t.project_name,
                "createdAt": "",
                "logs": [],
                "tags": t.tags,
                "filename": t.filename,
            })
        })
        .collect();

    client.batch_upsert("tasks:batchUpsert", &items, BATCH_SIZE).await
}

/// Sync orchestrator tasks → tasks table
pub async fn sync_orchestrator_tasks(
    client: &ConvexClient,
    tasks: &[orchestrator::OrchestratorTask],
) -> Result<u64> {
    let items: Vec<serde_json::Value> = tasks
        .iter()
        .map(|t| {
            json!({
                "taskId": format!("orch-{}", t.id),
                "task": t.task.chars().take(500).collect::<String>(),
                "model": t.model,
                "status": normalize_orch_status(&t.status),
                "priority": "p1",
                "projectName": extract_project_from_task(&t.task),
                "createdAt": t.created_at,
                "completedAt": t.completed_at,
                "result": t.result.as_deref().map(|r| r.chars().take(2000).collect::<String>()),
                "logs": [],
            })
        })
        .collect();

    client.batch_upsert("tasks:batchUpsert", &items, BATCH_SIZE).await
}

/// Sync project data → projects table
pub async fn sync_projects(
    client: &ConvexClient,
    projects: &[projects::ProjectData],
) -> Result<u64> {
    let items: Vec<serde_json::Value> = projects
        .iter()
        .map(|p| {
            json!({
                "name": p.name,
                "color": project_color(&p.name),
                "type": "product",
                "sdlcStage": p.sdlc_stage,
                "scores": {
                    "sdlc_completeness": p.scores.sdlc_completeness,
                    "code_quality": p.scores.code_quality,
                    "security_posture": p.scores.security_posture,
                    "qa_quality": p.scores.qa_quality,
                    "deployment_health": p.scores.deployment_health,
                    "gtm_readiness": p.scores.gtm_readiness,
                    "sales_pipeline": p.scores.sales_pipeline,
                    "revenue_proximity": p.scores.revenue_proximity,
                    "strategic_value": p.scores.strategic_value,
                    "velocity": p.scores.velocity,
                    "tech_debt": p.scores.tech_debt,
                    "market_timing": p.scores.market_timing,
                },
                "services": p.services,
                "score": p.composite,
                "updatedAt": p.updated_at,
            })
        })
        .collect();

    client.batch_upsert("projects:batchUpsert", &items, BATCH_SIZE).await
}

/// Sync memory logs → conversations table
pub async fn sync_memory_logs(
    client: &ConvexClient,
    logs: &[memory::MemoryLog],
) -> Result<u64> {
    let mut count = 0u64;

    for log in logs {
        for session in &log.sessions {
            let item = json!({
                "sessionKey": format!("memory-{}-{}", log.date, session.timestamp),
                "projectName": session.goals.split(',').next().unwrap_or("general").trim(),
                "messages": [{
                    "role": "system",
                    "content": session.summary,
                    "timestamp": session.timestamp,
                }],
                "startedAt": session.timestamp,
                "updatedAt": session.timestamp,
                "model": session.model,
                "tokensUsed": 0,
                "status": "complete",
            });

            client
                .mutation("conversations:upsert", item)
                .await?;
            count += 1;
        }
    }

    Ok(count)
}

fn normalize_orch_status(s: &str) -> &str {
    match s {
        "completed" => "done",
        "dispatched" | "running" => "in_progress",
        "failed" | "cancelled" => "blocked",
        _ => "todo",
    }
}

fn extract_project_from_task(task: &str) -> String {
    // Try to find project name in task description
    let known = [
        "NarrativeReactor", "invesco-retention", "forwardlane-backend",
        "signal-studio", "signal-builder", "flip-my-era", "ultrafone",
        "signal-studio-auth", "signal-studio-data-provider",
        "signal-studio-frontend", "signal-studio-templates",
    ];
    for k in &known {
        if task.contains(k) {
            return k.to_string();
        }
    }
    "general".to_string()
}

fn project_color(name: &str) -> &'static str {
    match name {
        "invesco-retention" => "#ef4444",
        "signal-studio" | "signal-studio-frontend" => "#3b82f6",
        "forwardlane-backend" => "#8b5cf6",
        "flip-my-era" => "#ec4899",
        "ultrafone" => "#f59e0b",
        "NarrativeReactor" => "#10b981",
        _ => "#6b7280",
    }
}
