---
type: lesson
tags: [git, worktree, concurrency, multi-agent, hooks, testing]
Title: Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check
Sources: Session reflection, 2026-07-05
Raw: "[../../raw/lessons-learned/2026-07-05-worktree-cleanup-collision.md](../../raw/lessons-learned/2026-07-05-worktree-cleanup-collision.md)"
Updated: 2026-07-05
---

# Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check

A stale-looking git worktree was removed after checking its git state and getting explicit user authorization — but a different, concurrently running agent session was actively working in it at the time, and lost work as a result.

## The collision

Before removing a worktree, `git status`/`git log` were checked and the uncommitted changes present were described to the user, who then explicitly authorized discarding it. Shortly after the removal, a message arrived from a different, concurrently running agent session reporting that it had been actively working in that exact worktree and lost a round of uncommitted work when it was deleted out from under it.

Checking git state and getting human authorization are both real, necessary steps — and neither one answers the question that actually mattered: *is some other live process still treating this worktree as current?* In any environment where multiple agents or processes can share worktrees under one repository, a destructive action needs a **liveness check**, not just a **state check**. A worktree with no uncommitted changes can still be mid-use (about to be written to); one with uncommitted changes might be genuinely abandoned. Neither signal alone proves the other. Human authorization to discard something is real, but a human giving that authorization typically can't see another agent's in-flight state either — so it doesn't close the gap.

## Build the automated fix, but know its limits

A mechanical safeguard (an automated hook that removes worktrees whose branch is already merged and has no locally tracked changes) closes the "did anyone remember to clean this up" gap — it removes the burden of a human/agent deciding to clean up at all. But it is built on the same git-state check that caused the original incident: merged + clean is still not proof that nothing is actively using the worktree. Building the automation is real progress; documenting what it still doesn't cover (rather than presenting it as a full fix) matters just as much.

## Test new destructive automation against a real fixture, not just the happy path

Before wiring a new destructive-action hook into live configuration, a throwaway git repository was built specifically to exercise the failure taxonomy that the incident itself suggested: merged+clean, unmerged, merged-with-untracked-only, merged-with-tracked-changes. Running the hook logic against all four states (rather than just confirming it worked on one) surfaced a real bug — the worktree-discovery step used a fixed-depth glob pattern that silently missed worktrees living at a different nesting depth than the one case that had been eyeballed. Code review alone likely would not have caught it; only actually exercising each state did.

**Generalizable pattern**: when building automation for a class of destructive action, construct a small fixture that reproduces the actual state matrix the real incident revealed, and assert against it before wiring the automation into anything live.

## See Also

- [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](destructive-op-confirmation-and-background-jobs.md) — related git-safety discipline; that lesson covers re-confirming at the moment of escalation, this one covers why confirmation alone isn't sufficient once another live process is involved
- [Confirm Scope Before Building Automation; Gate Anything Self-Modifying](../conventions/scope-before-autonomous-automation.md) — same theme of a mechanical fix needing an explicit accounting of what it does and doesn't cover
- [Check a Helper's Contract Before Printing Its Output to Inspect Shape; Isolate Shared Namespaces by Default](debug-print-secret-leak.md) — from the same session; a secret-scan hook flagged legitimate credential-adjacent code, reinforcing that false positives cluster around security-sensitive code precisely where a human is already inclined to double-check
- [Quarantine a Destructive Script the Moment Its Blind Spot Is Found](quarantine-destructive-scripts-immediately.md) — same "destructive automation has a blind spot" theme, from an earlier incident
- [A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope](guard-scope-vs-verbal-override.md) — from the following day's session; a verbal override of this same worktree-isolation guard only covered a subset of the actions it gates
