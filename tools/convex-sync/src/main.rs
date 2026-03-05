use anyhow::Result;
use clap::Parser;
use std::path::PathBuf;

mod convex;
mod sources;
mod sync;

#[derive(Parser, Debug)]
#[command(name = "convex-sync", about = "Sync local agent state to Convex")]
struct Cli {
    /// Workspace root directory
    #[arg(long, default_value = "/data/workspace")]
    workspace: PathBuf,

    /// Convex deployment URL (e.g. https://your-deployment.convex.cloud)
    #[arg(long, env = "CONVEX_URL")]
    convex_url: String,

    /// Convex deploy key for admin mutations
    #[arg(long, env = "CONVEX_DEPLOY_KEY")]
    convex_deploy_key: String,

    /// Only sync specific sources (comma-separated: todos,tasks,projects,memory,scores)
    #[arg(long)]
    only: Option<String>,

    /// Dry run — parse and report but don't push
    #[arg(long, default_value_t = false)]
    dry_run: bool,
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "convex_sync=info".into()),
        )
        .init();

    let cli = Cli::parse();

    let sources_filter: Option<Vec<String>> = cli.only.map(|s| {
        s.split(',').map(|x| x.trim().to_lowercase()).collect()
    });

    let client = convex::ConvexClient::new(&cli.convex_url, &cli.convex_deploy_key);

    let mut total_synced = 0u64;

    let should_sync = |name: &str| -> bool {
        sources_filter.as_ref().map_or(true, |f| f.contains(&name.to_lowercase()))
    };

    // 1. Sync TODOs → tasks + kanban
    if should_sync("todos") {
        tracing::info!("📋 Syncing TODOs...");
        let todos = sources::todos::parse_todos(&cli.workspace)?;
        tracing::info!("  Parsed {} TODO files", todos.len());
        if !cli.dry_run {
            let n = sync::sync_todos(&client, &todos).await?;
            total_synced += n;
            tracing::info!("  Synced {} tasks to Convex", n);
        } else {
            tracing::info!("  [dry-run] Would sync {} tasks", todos.len());
        }
    }

    // 2. Sync orchestrator tasks
    if should_sync("tasks") {
        tracing::info!("🤖 Syncing orchestrator tasks...");
        let tasks = sources::orchestrator::parse_tasks(&cli.workspace)?;
        tracing::info!("  Parsed {} orchestrator tasks", tasks.len());
        if !cli.dry_run {
            let n = sync::sync_orchestrator_tasks(&client, &tasks).await?;
            total_synced += n;
            tracing::info!("  Synced {} orchestrator tasks to Convex", n);
        } else {
            tracing::info!("  [dry-run] Would sync {} tasks", tasks.len());
        }
    }

    // 3. Sync project scores
    if should_sync("projects") || should_sync("scores") {
        tracing::info!("📊 Syncing project scores...");
        let projects = sources::projects::parse_projects(&cli.workspace)?;
        tracing::info!("  Parsed {} projects", projects.len());
        if !cli.dry_run {
            let n = sync::sync_projects(&client, &projects).await?;
            total_synced += n;
            tracing::info!("  Synced {} projects to Convex", n);
        } else {
            tracing::info!("  [dry-run] Would sync {} projects", projects.len());
        }
    }

    // 4. Sync memory/daily logs → conversations
    if should_sync("memory") {
        tracing::info!("🧠 Syncing memory logs...");
        let logs = sources::memory::parse_memory_logs(&cli.workspace)?;
        tracing::info!("  Parsed {} daily logs", logs.len());
        if !cli.dry_run {
            let n = sync::sync_memory_logs(&client, &logs).await?;
            total_synced += n;
            tracing::info!("  Synced {} memory entries to Convex", n);
        } else {
            tracing::info!("  [dry-run] Would sync {} logs", logs.len());
        }
    }

    tracing::info!("✅ Sync complete — {} total items pushed to Convex", total_synced);
    Ok(())
}
