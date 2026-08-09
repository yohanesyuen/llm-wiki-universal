---
type: lesson
tags: [verification, runtime, tooling, testing]
title: Green Static Checks Don't Prove the Code Ever Runs
sources: Session reflection, 2026-07-19
raw: "[../../raw/lessons-learned/2026-07-19-spec-toolchain-safety-and-runtime-verification.md](../../raw/lessons-learned/2026-07-19-spec-toolchain-safety-and-runtime-verification.md)"
updated: 2026-08-09
---

# Green Static Checks Don't Prove the Code Ever Runs

A green type-check and a green test suite prove the code is syntactically and logically consistent *with itself*. They say nothing about whether the code ever actually runs. For anything with a real runtime entry point — an app's root registration, a server's startup sequence — the only real verification is starting it and observing actual output.

A concrete instance from this session: an app crashed at launch on a missing runtime registration call. The type-check and the test suite had both been green the entire time and never could have caught it — the bug was neither a type error nor a logic error. Both the diagnosis and the fix were verified the same way: by starting the bundler, requesting a real bundle, and grepping the *compiled* output for the actual registration call — confirmed absent before the fix and present after. Not "it type-checks now."

Skipping the "actually run it" step would have shipped a completely non-functional app despite every check passing.

## Tip: an additive-only edit is cheaply verifiable by removed-line count

When editing a file you've been told (or suspect) is fragile or high-value, copy it to scratch first, then after editing diff the backup against the current file and count *removed* lines. A `0` removed-lines count is strong, cheap evidence that the edit was a pure append or localized change rather than a corrupting rewrite. The check is what turns "nothing was destroyed" from an assumption into a verified fact — worth doing as a standing habit, not only when explicitly asked to be careful.

## Tip: "already up to date" is a lockfile claim, not a linking guarantee

When a package manager reports "already up to date" but you suspect broken linking, that message means the lockfile hash is unchanged — it does *not* mean the linked files on disk are correct. A no-op install typically skips lifecycle/postinstall scripts entirely, so a real reproduction (actually delete and reinstall) is the only way to verify a postinstall hook or linking behavior works.

## See Also

This session produced four other lessons already covered by existing articles; they are cross-linked here rather than restated:

- [A Tool's Success Message Describes Intent, Not Effect — Diff the Actual Before/After](verify-mutating-tool-diffs-not-success-messages.md) — treat any tool that "generates" a hand-narrated file as destructive-by-default; read its write-contract (regenerate vs append-only) *before* running it, since two adjacently-named commands can have completely different blast radii
- [A Request Built on a False Premise Deserves a Correction, Not Silent Compliance](false-premise-scoping-and-diff-before-git-reconcile.md) — "use X approach" from a user is permission to try X, not evidence X is correct; check ground truth before writing a guess to shared state
- [Reason About the Worst-Case Node Before a Bulk Rollup; Search for Prior Art Before Building a Second Implementation](rollup-safety-reasoning-and-check-for-prior-art.md) — grep the repo for an existing script before hand-rolling new automation for a task the repo has clearly done before
- [Parallel Agent Waves Need a Build Gate](parallel-agent-build-gate.md) — a destructive operation on shared state needs a verification pass scoped to *what was touched* (repo-wide), not to what was originally being debugged
