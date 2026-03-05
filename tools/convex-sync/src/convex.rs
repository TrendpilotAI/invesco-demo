use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use serde_json::Value;

/// Client for Convex HTTP Actions / Mutations API
pub struct ConvexClient {
    url: String,
    deploy_key: String,
    http: reqwest::Client,
}

#[derive(Debug, Serialize)]
struct MutationRequest {
    path: String,
    args: Value,
    format: String,
}

#[derive(Debug, Deserialize)]
struct ConvexResponse {
    status: Option<String>,
    value: Option<Value>,
    #[serde(rename = "errorMessage")]
    error_message: Option<String>,
}

impl ConvexClient {
    pub fn new(url: &str, deploy_key: &str) -> Self {
        Self {
            url: url.trim_end_matches('/').to_string(),
            deploy_key: deploy_key.to_string(),
            http: reqwest::Client::new(),
        }
    }

    /// Call a Convex mutation
    pub async fn mutation(&self, function_path: &str, args: Value) -> Result<Value> {
        let url = format!("{}/api/mutation", self.url);

        let body = MutationRequest {
            path: function_path.to_string(),
            args,
            format: "json".to_string(),
        };

        let resp = self
            .http
            .post(&url)
            .header("Authorization", format!("Convex {}", self.deploy_key))
            .header("Content-Type", "application/json")
            .json(&body)
            .send()
            .await
            .context("Failed to call Convex mutation")?;

        let status = resp.status();
        let text = resp.text().await.context("Failed to read response")?;

        if !status.is_success() {
            anyhow::bail!("Convex mutation failed ({}): {}", status, text);
        }

        let parsed: ConvexResponse =
            serde_json::from_str(&text).context("Failed to parse Convex response")?;

        if let Some(err) = parsed.error_message {
            anyhow::bail!("Convex error: {}", err);
        }

        Ok(parsed.value.unwrap_or(Value::Null))
    }

    /// Call a Convex query
    pub async fn query(&self, function_path: &str, args: Value) -> Result<Value> {
        let url = format!("{}/api/query", self.url);

        let body = MutationRequest {
            path: function_path.to_string(),
            args,
            format: "json".to_string(),
        };

        let resp = self
            .http
            .post(&url)
            .header("Authorization", format!("Convex {}", self.deploy_key))
            .header("Content-Type", "application/json")
            .json(&body)
            .send()
            .await
            .context("Failed to call Convex query")?;

        let status = resp.status();
        let text = resp.text().await.context("Failed to read response")?;

        if !status.is_success() {
            anyhow::bail!("Convex query failed ({}): {}", status, text);
        }

        let parsed: ConvexResponse =
            serde_json::from_str(&text).context("Failed to parse Convex response")?;

        if let Some(err) = parsed.error_message {
            anyhow::bail!("Convex error: {}", err);
        }

        Ok(parsed.value.unwrap_or(Value::Null))
    }

    /// Batch upsert — calls a mutation for each item, returns count of successes
    pub async fn batch_upsert(
        &self,
        function_path: &str,
        items: &[Value],
        batch_size: usize,
    ) -> Result<u64> {
        let mut success_count = 0u64;

        for chunk in items.chunks(batch_size) {
            let args = serde_json::json!({ "items": chunk });
            self.mutation(function_path, args).await?;
            success_count += chunk.len() as u64;
        }

        Ok(success_count)
    }
}
