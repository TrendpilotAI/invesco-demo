# TODO-574: AWS SDK v2 → v3 Migration — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P2  
**Status:** pending

## Description
AWS SDK v2 is in maintenance mode. Migrate to modular v3 packages.

## Steps
1. `npm install @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb @aws-sdk/client-ses`
2. Remove `aws-sdk` from package.json
3. Update all DynamoDB client instantiation to v3
4. Update all DynamoDB operations (put, get, query, scan) to v3 API
5. Update SES email client to v3
6. Test all AWS-dependent features

## Acceptance Criteria
- No `aws-sdk` imports anywhere
- DynamoDB reads/writes work correctly
- SES email sending works
- Bundle size reduced via tree-shaking

## Dependencies
TODO-567 (CVE audit)
