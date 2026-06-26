---
source: https://github.com/session-reflection (wiki/meta/claude-code-agent-workflow-lessons.md)
collected: 2026-06-27
published: 2026-06-25
---

A subagent's confirmation gate is a separate trust boundary from the coordinator's own. After a subagent rejects an action for a stated reason, change the input shape — quote the user's exact words verbatim, or have the user address the subagent directly. Resending a paraphrase of the same relay doesn't change what's being rejected and will be rejected again for the same reason.
