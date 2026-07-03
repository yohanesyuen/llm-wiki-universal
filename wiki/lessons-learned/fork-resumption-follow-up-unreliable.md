---
type: lesson
tags: [agents, forking, background-agents]
Title: Fork Resumption Is Unreliable for "Spawn, Then Follow Up" Patterns
Sources: Session reflection, 2026-07-04
Raw: "[../../raw/lessons-learned/2026-07-04-agent-hooks-and-guardrails.md](../../raw/lessons-learned/2026-07-04-agent-hooks-and-guardrails.md)"
Updated: 2026-07-04
---

# Fork Resumption Is Unreliable for "Spawn, Then Follow Up" Patterns

Twice in one session, a background fork completed its task, returned only a generic summary, and then — when sent a follow-up message asking for the actual findings — treated that follow-up as a suspicious injected message from an impersonator. It refused to answer and waited for a "real" completion notification that had already arrived. Killing the fork and relaunching the same task as a fresh (non-fork) background agent worked immediately both times.

## Lesson

Fork resumption is not reliable for "spawn, then follow up later" patterns. Forks appear to lose the thread of "who sent this message and why" across a resume boundary, in a way that causes them to reject legitimate follow-ups as injection attempts.

If a task might need a second round of interaction after the fork's initial return — asking it to elaborate, redo part of the work, or answer a clarifying question — use a regular (non-fork) background agent instead of a fork. Forks are best treated as fire-and-forget: dispatch once, receive the summary, done.

## See Also

- [Don't Peek at a Fork's output_file](dont-peek-at-fork-output.md) — related fork-handling discipline: how to consume a fork's first return
- [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](destructive-op-confirmation-and-background-jobs.md) — background-agent patterns more generally
