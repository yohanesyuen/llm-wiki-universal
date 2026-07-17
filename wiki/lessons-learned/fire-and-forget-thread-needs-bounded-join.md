---
type: lesson
tags: [silent-failure, hooks, threading, logging, fail-loudly]
Title: Fire-and-Forget Background Threads in Short-Lived Scripts Need a Bounded Join
Sources: session-reflection, 2026-07-07
Raw: "[../../raw/lessons-learned/2026-07-07-cache-invalidated-experiment.md](../../raw/lessons-learned/2026-07-07-cache-invalidated-experiment.md)"
Updated: 2026-07-17
---

# Fire-and-Forget Background Threads in Short-Lived Scripts Need a Bounded Join

A short-lived script (a hook, a CLI one-shot) that spawns a daemon thread to do background work — an HTTP POST, a log flush — and then exits without joining that thread will race the process exit against the background work. The process can exit before the thread finishes, silently dropping the work every time, with no exception and no error output.

## The failure

A statusline logging hook spawned a daemon thread to POST its log line, then let the script exit. Nothing failed loudly — there was no exception, no stack trace, nothing in stderr. It simply never logged, 100% of the time, until directly investigated. This is exactly the kind of silent-failure class that a "fail loudly" principle is meant to catch, except it was happening in an environment (a Claude Code hook script) outside normal version-controlled review, so nothing surfaced it until someone went looking.

The fix was confirmed empirically, not assumed from reading the code: 0/3 successful log deliveries before adding a bounded join, 3/3 after.

## The rule

Any fire-and-forget background work in a short-lived process — a daemon thread, an unawaited async call — is a suspect for silent failure by default. Before considering such a change complete:

1. Join the thread (or await the task) with a bounded timeout before the process is allowed to exit, so the exit can't outrace the work.
2. Verify end-to-end by checking the actual sink (the log line landed, the POST was received) — not just "no exception was thrown," which proves nothing when the failure mode is exactly "nothing happens and nothing complains."

This applies with extra weight to scripts that run on every hook invocation but live outside the normal review/test loop — a silent no-op there can persist indefinitely because nothing ever calls attention to it.

## Bounded join vs. staleness self-heal: pick by lifecycle, not by pattern shape

This bounded-join fix applies to a **short-lived process** — a hook or CLI one-shot that spawns background work and then wants to exit. It is the wrong fix for a background-thread-plus-lock-file job that is *meant* to legitimately outlive one process invocation (e.g. triggered on an event, not a one-shot script): forcing that kind of job to wait-before-exit isn't appropriate, and the corresponding failure mode is different — a lock file left behind when the parent exits mid-operation, permanently mistaken for "still running." The right fix there is a staleness check on the lock itself (reclaim it after a timeout) so an interrupted run self-heals. See [Resolve Targets Directly, Don't Infer From a Manifest; Test Through a System's Own API, Not a Generic External One](resolve-targets-test-through-own-api.md) for the concrete incident and the self-heal fix.

## See Also

- [Root-Cause UI Bugs to the Shared Primitive Behind Them](root-cause-shared-styling-primitives.md) — a green result (no exception, a passing build) doesn't confirm correctness; check the real sink/screenshot
- [Hook Authoring Discipline](hook-authoring-discipline.md) — other hook-script-specific pitfalls that don't get caught by normal review
- [Git-Based Isolation Can't Isolate What Git Doesn't Track; a Directory-Change Hook Can Silently Revert a Workaround Edit](worktree-isolation-untracked-files-and-shell-hook-race.md) — same shape of bug in a different setting: a shell directory-change hook silently reverted a write, with a clean exit code and no error to signal it
- [Resolve Targets Directly, Don't Infer From a Manifest; Test Through a System's Own API, Not a Generic External One](resolve-targets-test-through-own-api.md) — the staleness-self-heal counterpart for detached, cross-invocation background jobs
