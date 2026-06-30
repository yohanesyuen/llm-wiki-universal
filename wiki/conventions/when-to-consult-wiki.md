---
type: convention
tags: [wiki, knowledge-management]
Title: When to Consult the Wiki
Updated: 2026-06-28
---

# When to Consult the Wiki

Entry point for the read-first rule. Read this file at the start of every non-trivial task (non-trivial = code, config, tooling, or infra change). On the first wiki consult of a session, also read [wiki-consult-procedure.md](wiki-consult-procedure.md) once to load depth limits, pivot definition, and after-reading rules.

Then scan `wiki/index.md` titles and summaries for overlap with the task and read the 1–2 closest matches before acting.

## Hard triggers

Fire regardless of index scan result.

| Situation | Read |
|-----------|------|
| First wiki consult of the session | [wiki-consult-procedure](wiki-consult-procedure.md) |
| Specific size, count, or named slot in implementation | [named-size-means-example-not-constraint](../lessons-learned/named-size-means-example-not-constraint.md) |
| Editing a skill's SKILL.md | [skill-config-and-responsibility](../lessons-learned/skill-config-and-responsibility.md) |
| Changing `settings.json`, MCP permissions, or allow lists | [mcp-permissions-and-allow-list-hygiene](../lessons-learned/mcp-permissions-and-allow-list-hygiene.md) |
| Running `/reflect` or `/karpathy-llm-wiki` | [wiki-ingest-and-cleanup-discipline](../lessons-learned/wiki-ingest-and-cleanup-discipline.md), [skill-config-and-responsibility](../lessons-learned/skill-config-and-responsibility.md) |
| Retrying after a tool call was rejected | [session-tool-efficiency](../lessons-learned/session-tool-efficiency.md) |
| Evaluating whether to add a new tool, server, or infra layer | [capability-gap-before-infrastructure-eval](../lessons-learned/capability-gap-before-infrastructure-eval.md) |
| Build output format, module system, or native bindings | [preflight-checks-before-building](../lessons-learned/preflight-checks-before-building.md) |
| Creating or publishing a public repo | [public-repo-setup-discipline](../lessons-learned/public-repo-setup-discipline.md) |
| Writing docs or a README for external readers | [no-confidential-leak](no-confidential-leak.md) |
| Session script needs live LLM inference | [llm-script-discipline](../lessons-learned/llm-script-discipline.md) |
| Unfamiliar package or library | Scan index for that package name or domain |
| New OS, architecture, or runtime | Scan index for platform-specific lessons |
| Task pivots to a materially different sub-problem | Re-scan index and re-check this table; see [pivot definition](wiki-consult-procedure.md) |
