# TODO 732: Secrets Manager Integration

**Repo:** signal-studio-data-provider  
**Priority:** MEDIUM  
**Effort:** M (2 days)  
**Dependencies:** TODO 590 (SecretStr first)

## Description
Enterprise deployments can't use plaintext credentials in config. Add optional secrets backend support: AWS SSM Parameter Store, HashiCorp Vault, GCP Secret Manager, or env vars (default).

## Acceptance Criteria
- [ ] `OrgConfig.secrets_backend: Literal["env", "aws_ssm", "vault", "gcp_secret_manager"] = "env"`
- [ ] `OrgConfig.secrets_prefix: str = ""` — namespace prefix for secret paths
- [ ] `SecretsLoader` class with `async def load(config: OrgConfig) -> OrgConfig` that hydrates SecretStr fields
- [ ] AWS SSM: `boto3.client("ssm").get_parameter(Name=f"{prefix}/snowflake/password")`
- [ ] Vault: HTTP GET to Vault KV endpoint with `VAULT_TOKEN` env var
- [ ] GCP: `google.cloud.secretmanager.SecretManagerServiceClient`
- [ ] Factory calls `SecretsLoader.load(config)` before creating provider
- [ ] No secrets in logs, repr, or exceptions
- [ ] Tests mock each backend

## Coding Prompt
```python
# secrets/loader.py
class SecretsLoader:
    @classmethod
    async def load(cls, config: OrgConfig) -> OrgConfig:
        if config.secrets_backend == "env":
            return config  # Already loaded from env
        elif config.secrets_backend == "aws_ssm":
            return await cls._load_from_ssm(config)
        elif config.secrets_backend == "vault":
            return await cls._load_from_vault(config)
        # etc.

    @classmethod
    async def _load_from_ssm(cls, config: OrgConfig) -> OrgConfig:
        import boto3
        ssm = boto3.client("ssm")
        prefix = config.secrets_prefix
        
        if config.snowflake:
            password = ssm.get_parameter(
                Name=f"{prefix}/snowflake/password", 
                WithDecryption=True
            )["Parameter"]["Value"]
            config = config.model_copy(
                update={"snowflake": config.snowflake.model_copy(
                    update={"password": SecretStr(password)}
                )}
            )
        return config
```
