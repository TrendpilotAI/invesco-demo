# TODO-837: Upgrade AWS SDK v2 → v3 (forwardlane_advisor)

**Repo:** forwardlane_advisor  
**Priority:** P1  
**Effort:** Medium (2-3 days)  
**Status:** pending

## Description
AWS SDK v2 reached end-of-life in 2023. forwardlane_advisor uses `aws-sdk@^2.2.28` for S3 and DynamoDB. Must migrate to modular SDK v3 (`@aws-sdk/client-s3`, `@aws-sdk/client-dynamodb`).

## Coding Prompt
In `/data/workspace/projects/forwardlane_advisor/`:
1. `npm uninstall aws-sdk`
2. `npm install @aws-sdk/client-s3 @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb`
3. Find all `require('aws-sdk')` usages: `grep -r "aws-sdk" app/ --include="*.js"`
4. For each S3 usage, replace with `S3Client` + `PutObjectCommand`, `GetObjectCommand`, etc.
5. For each DynamoDB usage, replace with `DynamoDBDocumentClient` pattern
6. Update environment variable handling (SDK v3 reads from env automatically)
7. Test S3 upload/download flows and DynamoDB reads

## Acceptance Criteria
- No `aws-sdk` v2 dependency in package.json
- All S3 and DynamoDB operations work with v3 clients
- `npm audit` shows no AWS SDK CVEs

## Dependencies
- None
