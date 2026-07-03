---
type: convention
tags: [automation, hooks, autonomy, human-in-the-loop]
Title: Confirm Scope Before Building Automation; Gate Anything Self-Modifying
Sources: Session reflection, 2026-07-04
Raw: "[../../raw/lessons-learned/2026-07-04-agent-hooks-and-guardrails.md](../../raw/lessons-learned/2026-07-04-agent-hooks-and-guardrails.md)"
Updated: 2026-07-04
---

# Confirm Scope Before Building Automation; Gate Anything Self-Modifying

Two related failure modes from wiring up automated hooks and self-updating project notes in one session.

## Restate an ambiguous trigger as a concrete example before automating it

A standing policy referenced "reusable snippets" without specifying what counted as one. Rather than asking for a concrete trigger up front, a hook was designed, implemented, tested, and wired into config on an inferred scope — then had to be fully reverted once the real scope (any-language code patterns, not the one file type that had been assumed) came back completely different from what was built.

**Lesson**: ambiguous policy language ("index reusable X into Y") is not specific enough to safely wire a file-watching hook or other automation against. Ask "what would a real instance of X look like?" first, and confirm it. The cost of reverting fully-built-and-tested automation is higher than the cost of one clarifying question.

## Gate anything that lets a session rewrite its own configuration autonomously

When asked to build a pattern where a session acts autonomously and rewrites its own configuration, the concrete risk is worth surfacing rather than reflexively refusing or reflexively complying: no explicit request in that session triggers the action, and the config file that's supposed to be ground truth can drift unreviewed. Naming that risk surfaced that the actual goal (self-updating documentation) was fine — what was missing was a human checkpoint before the write took effect.

**Lesson**: standing instructions that cause a session to act autonomously and modify its own configuration deserve a real pause, not a knee-jerk response in either direction. The fix is usually adding an explicit human-approval gate, not vetoing the automation outright.

## See Also

- [Pre-Flight Checks Before Building](../lessons-learned/preflight-checks-before-building.md) — same "verify before building" theme, applied to technical compatibility rather than policy scope
- [Hook Authoring Discipline](../lessons-learned/hook-authoring-discipline.md) — mechanics of writing correct, portable hooks once scope is confirmed
- [Passive Signals vs Hard Gates](../lessons-learned/passive-signals-vs-hard-gates.md) — when a constraint needs a hard gate rather than an advisory reminder
