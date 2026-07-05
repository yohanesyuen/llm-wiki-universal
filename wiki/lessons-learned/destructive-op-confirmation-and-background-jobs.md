---
type: lesson
tags: [git, concurrency, background-jobs, confirmation]
Title: Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs
Sources: Session reflection, 2026-07-03
Raw: "[../../raw/lessons-learned/2026-07-03-corpus-cleanup-and-reindex.md](../../raw/lessons-learned/2026-07-03-corpus-cleanup-and-reindex.md)"
Updated: 2026-07-03
---

# Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs

Three small operational habits from the same session, each cheap to apply and each avoiding a distinct failure mode.

## Re-confirm at the moment a routine op becomes a destructive one

Prior authorization for a routine operation doesn't automatically cover a destructive fallback. When a downstream repo turned out to have diverged from a force-pushed remote (local branch ahead by one commit, behind by many, plus uncommitted changes), the right move was not to unilaterally hard-reset. The available options were presented to the user explicitly, and the reset was only executed after an explicit choice — followed by verifying the locally-only commit's content still existed on the remote under different hashes before discarding it.

Reach for an explicit confirmation step specifically at the moment a routine operation turns out to require escalating to a destructive one (e.g., a plain `git pull` turning into a required `git reset --hard`).

## Serialize writes to a shared on-disk store

Two long-running ingestion jobs needed to write into the same data store. Running them sequentially rather than concurrently avoided any risk of write races, even without confirming the store's exact concurrency guarantees either way. When two long-running jobs must write to the same store, either confirm its concurrency guarantees first or default to serializing them — the cost of serializing is usually far lower than the cost of diagnosing a corrupted store afterward.

## Background long jobs and wait for the completion notification

A multi-minute batch job (LLM summarization per chunk, run across hundreds of items) was run in the background with no manual status polling. Backgrounding plus waiting for the completion signal, instead of repeatedly checking status, keeps the session focused and avoids burning turns on "is it done yet" checks.

## See Also

- [Don't Peek at a Fork's output_file](dont-peek-at-fork-output.md) — same "wait for the notification, don't poll" discipline applied to forked agents instead of background shell jobs
- [Feature-Branch Git Workflow for AI-Assisted Development](../conventions/feature-branch-git-workflow.md) — related git-safety conventions
- [A Denied Command Inside a Chained Shell Call Blocks the Whole Chain](chained-command-denial-blocks-whole-chain.md) — a related shell-permission failure mode
- [Check a Helper's Contract Before Printing Its Output to Inspect Shape; Isolate Shared Namespaces by Default](debug-print-secret-leak.md) — same one-time-approval-isn't-blanket discipline reapplied to a second, materially identical case in the same session
- [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](worktree-liveness-check-before-destructive-cleanup.md) — a case where confirmation and a state check both happened, but a concurrent live process still lost work; confirmation alone isn't sufficient once another agent may be mid-use
