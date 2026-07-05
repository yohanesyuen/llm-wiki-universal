---
type: lesson
tags: [guardrails, hooks, worktree, git, automation]
Title: A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope
Sources: Session reflection, 2026-07-06
Raw: "[../../raw/lessons-learned/2026-07-06-worktree-guard-and-self-merge.md](../../raw/lessons-learned/2026-07-06-worktree-guard-and-self-merge.md)"
Updated: 2026-07-06
---

# A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope

Two observations from the same session, both with the same shape: a human's stated intent was real and present in the conversation, but the automated guard checking for it only recognized a narrower slice of that intent than the human meant.

## A spoken override of one guard doesn't cover every tool call the guard's rule touches

A verbal "override the isolation rule for this session" was given, intending to cover the whole task. The harness enforces a git-worktree-isolation requirement at the tool level, independent of what was said in conversation — and the override only took effect for the class of action it had actually been scoped to (e.g., committing in place), not for a different guarded action (editing files) that came up moments later. The block on file edits persisted until isolation was actually set up as a real worktree, regardless of the earlier verbal statement.

**Lesson**: when a human overrides a technical guard verbally, don't assume the override is blanket. Guards are typically wired to specific tool calls or action classes, not to "the session's general intent." Confirm which specific actions an override is meant to cover, and expect that guarded actions outside that scope will still fire — the correct response is to actually satisfy the guard's real precondition (e.g., setting up the worktree properly), not to assume the earlier override silently extends further.

## A safety guard's decision may depend on exactly where in the conversation it looks

A policy guard around a sensitive, hard-to-reverse action (merging a session's own pull request) declined the action on its first evaluation, even though a relevant human instruction was present earlier in the same conversation. The guard appeared to weigh only a narrow window of local context around the action itself, not the full conversation history — so context that a human reading the whole transcript would consider obviously relevant wasn't necessarily what the guard's check was built to look at.

**Lesson**: don't assume a guard on a high-stakes, self-referential action (approving, merging, or deleting one's own work) has "seen" everything a human has said in the conversation. When such a guard declines, that is a real signal to stop and get the human to confirm explicitly, in the moment, rather than treating an earlier general statement as sufficient authorization on its own. The gap is a reason for more caution and a fresh, explicit check-in — not a puzzle to be worked around.

## The Common Thread

Both observations are instances of the same principle: **a guard's enforcement surface is narrower than a human's conversational intent, by default.** Neither guard was wrong to fire — each was doing exactly the check it was built for. The safe response in both cases is the same: don't treat one broad statement (an override, an instruction) as automatically covering every downstream action that looks related; instead, re-establish the real precondition (isolation actually set up) or get fresh, explicit human confirmation at the point a sensitive guarded action is about to execute.

## See Also

- [Confirm Scope Before Building Automation; Gate Anything Self-Modifying](../conventions/scope-before-autonomous-automation.md) — same theme of guard/automation scope needing explicit confirmation, from the builder's side rather than the operator's side
- [Passive Signals vs Hard Gates](passive-signals-vs-hard-gates.md) — a hard gate cannot be talked past by an advisory statement; both guards described here are hard gates that need the right-shaped, explicit signal, not just any prior mention, before a sensitive action proceeds
- [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](worktree-liveness-check-before-destructive-cleanup.md) — same worktree-guard subject area, from the prior day's session, covering a different gap (no cross-session liveness signal) in the same guard family
