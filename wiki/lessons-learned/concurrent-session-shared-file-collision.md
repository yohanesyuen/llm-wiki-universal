---
type: lesson
tags: [concurrency, multi-agent, coordination, incident, authorization]
Title: A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap
Sources: Session reflection, 2026-07-06
Raw: "[../../raw/lessons-learned/2026-07-06-shared-file-env-var-collision.md](../../raw/lessons-learned/2026-07-06-shared-file-env-var-collision.md)"
Updated: 2026-07-17
---

# A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap

Two independently-running agent sessions edited the same shared config file within moments of each other — one renamed an environment variable, the other deployed against the pre-rename name it had last synced — and took production down until the mismatch was found.

## The collision was a missing claim-before-edit signal, not a slow message

Faster message delivery between the two sessions would have shortened the window in which the collision could happen, but would not have closed it: both sessions acted within the same few seconds, before either message could plausibly have been read and acted on. The actual fix is a claim-before-edit protocol — "I am now touching this file, don't touch it until I say clear" — enforced before either session writes, not a faster relay of after-the-fact status updates. Without that claim step, two agents can still collide even with instant delivery.

## Re-sync on every externally-observed change to a shared resource, not just at task start

A system notification flagging "this file changed since you last read it" was the signal that actually caught the rename in time to avoid a second, deeper collision. When two agents may be modifying the same shared resource, treat that kind of notification as a hard stop-and-recheck point on every occurrence, not only when first picking up the task — the file has to be re-read immediately before the next write, every time it's flagged as externally changed.

## Broad delegation ("you have control") does not satisfy a guard asking for a specific action

Mid-incident, the user delegated broad authority ("the other session has authority to act, you have control") to keep momentum. An automated safety check correctly treated this as too unspecific to authorize a follow-on secret-store write, and asked for the exact action to be named. This cost a round-trip but was the right call: broad delegation language is for keeping momentum, not for pre-authorizing a specific irreversible action a guard is built to gate individually. The fix on the agent side is to restate the specific action back for one-line confirmation, not to treat the earlier broad statement as sufficient on its own.

## A wildcard DNS/proxy protection doesn't necessarily cover every hostname under it

Separately, in the same incident, a subdomain believed to be protected by an existing edge-proxy gate (via a wildcard DNS entry) turned out to have its own more-specific DNS record pointing straight at a different, ungated origin. More-specific DNS records silently override wildcard behavior — a wildcard-level protection assumption needs verifying per-hostname, not assumed to blanket-cover everything nominally under it.

## See Also

- [Layer-Boundary Config Bugs and Staged Service Cutover](layer-boundary-configs-and-staged-cutover.md) — same "treat file-changed-externally notices as a mandatory re-read gate" discipline, from an earlier session in the same problem family
- [A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope](guard-scope-vs-verbal-override.md) — same "broad statement doesn't cover a specific guarded action" pattern, applied here to delegated authority instead of a verbal guard override
- [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](destructive-op-confirmation-and-background-jobs.md) — same "serialize writes to a shared store" principle; this session shows the concrete failure mode when that serialization isn't enforced across two independent agents
- [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](worktree-liveness-check-before-destructive-cleanup.md) — same family of multi-agent-on-shared-state gaps, different resource (worktree vs. config file)
- [Git-Based Isolation Can't Isolate What Git Doesn't Track; a Directory-Change Hook Can Silently Revert a Workaround Edit](worktree-isolation-untracked-files-and-shell-hook-race.md) — same theme of a concurrent process racing an edit to the same file, this time a single session's own shell hook rather than a second agent
- [Flag Each Surprising Field Separately; Read the Real Interface Before Extending It](flag-fields-and-read-real-interfaces.md) — companion lesson from a later collision in the same problem family
- [Stale In-Context File State Is Indistinguishable From a Hallucination — Re-Read Before Asserting or Editing](stale-mutable-state-reread-discipline.md) — the single-agent counterpart: re-reading a live-edited file matters even without a second agent involved
