use anyhow::Result;
use serde::Serialize;
use serde_json::Value;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize)]
pub struct ProjectData {
    pub name: String,
    pub scores: ProjectScores,
    pub composite: f64,
    pub sdlc_stage: String,
    pub services: Vec<String>,
    pub updated_at: String,
}

#[derive(Debug, Clone, Serialize, Default)]
pub struct ProjectScores {
    pub sdlc_completeness: f64,
    pub code_quality: f64,
    pub security_posture: f64,
    pub qa_quality: f64,
    pub deployment_health: f64,
    pub gtm_readiness: f64,
    pub sales_pipeline: f64,
    pub revenue_proximity: f64,
    pub strategic_value: f64,
    pub velocity: f64,
    pub tech_debt: f64,
    pub market_timing: f64,
}

/// Parse project scores from .orchestrator/project-scores.json and BRAINSTORM.md headers
pub fn parse_projects(workspace: &Path) -> Result<Vec<ProjectData>> {
    let mut projects = Vec::new();

    // Source 1: project-scores.json from orchestrator
    let scores_file = workspace.join(".orchestrator/project-scores.json");
    if scores_file.exists() {
        let content = fs::read_to_string(&scores_file)?;
        let data: Value = serde_json::from_str(&content)?;

        if let Some(scores_map) = data.get("project_scores").and_then(|v| v.as_object()) {
            for (name, score_val) in scores_map {
                if let Some(proj) = parse_score_entry(name, score_val) {
                    projects.push(proj);
                }
            }
        }
    }

    // Source 2: Scan projects/ for BRAINSTORM.md with score headers
    let projects_dir = workspace.join("projects");
    if projects_dir.exists() {
        if let Ok(entries) = fs::read_dir(&projects_dir) {
            for entry in entries.filter_map(|e| e.ok()) {
                if !entry.file_type().map(|ft| ft.is_dir()).unwrap_or(false) {
                    continue;
                }
                let name = entry.file_name().to_string_lossy().to_string();

                // Skip if already found in scores file
                if projects.iter().any(|p| p.name == name) {
                    continue;
                }

                let brainstorm = entry.path().join("BRAINSTORM.md");
                if brainstorm.exists() {
                    if let Ok(content) = fs::read_to_string(&brainstorm) {
                        if let Some(proj) = parse_brainstorm_scores(&name, &content) {
                            projects.push(proj);
                        }
                    }
                }
            }
        }
    }

    Ok(projects)
}

fn parse_score_entry(name: &str, val: &Value) -> Option<ProjectData> {
    let obj = val.as_object()?;

    let get_f = |key: &str| -> f64 {
        obj.get(key)
            .and_then(|v| v.as_f64())
            .unwrap_or(0.0)
    };

    let scores = ProjectScores {
        sdlc_completeness: get_f("sdlc_completeness"),
        code_quality: get_f("code_quality"),
        security_posture: get_f("security_posture"),
        qa_quality: get_f("qa_quality"),
        deployment_health: get_f("deployment_health"),
        gtm_readiness: get_f("gtm_readiness"),
        sales_pipeline: get_f("sales_pipeline"),
        revenue_proximity: get_f("revenue_proximity"),
        strategic_value: get_f("strategic_value"),
        velocity: get_f("velocity"),
        tech_debt: get_f("tech_debt"),
        market_timing: get_f("market_timing"),
    };

    let composite = get_f("composite_score");

    Some(ProjectData {
        name: name.to_string(),
        scores,
        composite,
        sdlc_stage: obj.get("sdlc_stage")
            .and_then(|v| v.as_str())
            .unwrap_or("unknown")
            .to_string(),
        services: vec![],
        updated_at: obj.get("updated_at")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_string(),
    })
}

fn parse_brainstorm_scores(name: &str, content: &str) -> Option<ProjectData> {
    // Parse scores from BRAINSTORM.md header lines like:
    // **Status:** ... Completeness: 8/10. Urgency: 10/10.
    // or SCORES: revenue_potential=8, strategic_value=9, ...
    let re = regex::Regex::new(
        r"(?i)(?:completeness|score)[:\s]*(\d+(?:\.\d+)?)\s*/\s*10"
    ).ok()?;

    let composite = re.captures(content)
        .and_then(|c| c.get(1))
        .and_then(|m| m.as_str().parse::<f64>().ok())
        .unwrap_or(5.0);

    Some(ProjectData {
        name: name.to_string(),
        scores: ProjectScores::default(),
        composite,
        sdlc_stage: "unknown".to_string(),
        services: vec![],
        updated_at: chrono::Utc::now().to_rfc3339(),
    })
}
