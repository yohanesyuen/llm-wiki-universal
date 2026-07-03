---
type: lesson
tags: [shell, permissions, tooling]
Title: A Denied Command Inside a Chained Shell Call Blocks the Whole Chain
Sources: Session reflection, 2026-07-04
Raw: "[../../raw/lessons-learned/2026-07-04-agent-hooks-and-guardrails.md](../../raw/lessons-learned/2026-07-04-agent-hooks-and-guardrails.md)"
Updated: 2026-07-04
---

# A Denied Command Inside a Chained Shell Call Blocks the Whole Chain

When a permission classifier denies one command in a `&&`-chained shell invocation, none of the commands in that call run — even ones that would have been fine on their own, including unrelated read-only commands bundled into the same chain.

## Lesson

Splitting reads out into their own separate calls is the only way to get them through once a chain has been flagged. Don't assume a denial only blocks the specific denied sub-command; treat the entire chained call as blocked and re-issue the safe portions independently.

## Practical implication

Avoid bundling a command likely to require confirmation (destructive ops, unfamiliar CLIs, anything outside an established allowlist) into the same `&&` chain as routine read-only commands. If a chain does get denied, don't retry the same chain — decompose it and re-issue the read-only pieces as their own calls.

## See Also

- [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](destructive-op-confirmation-and-background-jobs.md) — related discipline around confirming before an operation escalates
- [Passive Signals vs Hard Gates](passive-signals-vs-hard-gates.md) — how permission gates interact with session behavior
