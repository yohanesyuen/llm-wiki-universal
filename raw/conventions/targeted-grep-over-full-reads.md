---
source: https://github.com/session-reflection (wiki/meta/claude-code-agent-workflow-lessons.md)
collected: 2026-06-27
published: 2026-06-25
---

When the question is specific ("is convention X used elsewhere in this codebase?"), grep for the specific signal — a dispatcher table, an import line, a decorator — rather than reading entire sibling files end-to-end to infer the answer. Reading large files in full to answer a question a single targeted grep plus a glance at one dict would have answered is real, avoidable context cost.
