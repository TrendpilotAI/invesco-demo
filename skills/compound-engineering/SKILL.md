# Compound Engineering Plugin

AI-powered development tools that make each unit of engineering work easier than the last. Ported from the Claude Code plugin by Every Inc.

## Key Workflows

### `/workflow: plan` — Plan a feature, bug fix, or improvement
**Command:** `commands/workflows/plan.md`
Transforms feature descriptions into structured plans with research, spec analysis, and phased implementation.

### `/workflow: work` — Execute a plan
**Command:** `commands/workflows/work.md`
Implements a plan file step by step.

### `/workflow: review` — Review code changes
**Command:** `commands/workflows/review.md`
Multi-perspective code review.

### `/workflow: brainstorm` — Explore ideas
**Command:** `commands/workflows/brainstorm.md`
Structured brainstorming with research.

### `/workflow: compound` — Compound learnings
**Command:** `commands/workflows/compound.md`
Document learnings for future reuse.

## Agents (29)
- **Review (15):** architecture-strategist, code-simplicity-reviewer, security-sentinel, performance-oracle, pattern-recognition, TypeScript/Rails/Python reviewers, etc.
- **Research (5):** best-practices, framework-docs, git-history, learnings, repo-research
- **Design (3):** figma-sync, design-iterator, implementation-reviewer
- **Workflow (5):** spec-flow-analyzer, style-editor, bug-reproduction, PR resolver, lint
- **Docs (1):** README writer

## Skills (19)
agent-browser, agent-native-architecture, brainstorming, compound-docs, create-agent-skills, document-review, file-todos, frontend-design, gemini-imagegen, git-worktree, orchestrating-swarms, rclone, resolve-pr-parallel, setup, skill-creator, and more.

## Usage
Read the relevant command file from `commands/` or agent from `agents/` for detailed instructions. Plans are saved to `docs/plans/`.

## Source
https://github.com/EveryInc/compound-engineering-plugin
