---
type: lesson
tags: [git, worktree, untracked-files, shell-hooks, race-condition, verification]
Title: Git-Based Isolation Can't Isolate What Git Doesn't Track; a Directory-Change Hook Can Silently Revert a Workaround Edit
Sources: Session reflection, 2026-07-08
Raw: "[../../raw/lessons-learned/2026-07-08-worktree-isolation-and-background-refresh-race.md](../../raw/lessons-learned/2026-07-08-worktree-isolation-and-background-refresh-race.md)"
Updated: 2026-07-08
---

# Git-Based Isolation Can't Isolate What Git Doesn't Track; a Directory-Change Hook Can Silently Revert a Workaround Edit

A git worktree was created to isolate an edit to a file that turned out to be untracked — an isolation mechanism built on version control cannot isolate what version control doesn't know exists, and it failed only after a full round trip instead of being ruled out up front.

## Check trackedness before reaching for git-based isolation

A worktree is a checkout of tracked history; an untracked file simply doesn't exist in a freshly created one. This is obvious in hindsight but easy to miss when isolation is the reflexive first move for "edit safely." A cheap `git status`/untracked check on the target path (or an explicit note left at the target itself) rules this out before any time is invested — if the path is untracked, skip straight to whatever the real workaround is instead of discovering the failure by trial.

## A `cd` inside a raw shell command is not side-effect-free in a configured shell

Working around a tool-level edit guard by dropping to a raw shell command (instead of the normal guarded file-edit tool) chained a directory change into the same command: `cd <dir> && <edit command>`. That `cd` silently triggered an unrelated background hook wired into the shell's own startup config — one that reruns an auto-refresh script on every working-directory change. The hook's background process read the file *before* the intended edit landed and wrote it back *after*, invisibly reverting the edit. Nothing in the write path surfaced an error: the edit command reported success and exited cleanly. The actual state on disk was simply wrong, and only a re-read caught it.

This generalizes past this one shell config: a model chaining `cd <dir> && <command>` for convenience has no visibility into directory-change hooks unless it deliberately checks for them first. Any interactive shell with its own dotfiles can wire arbitrary background behavior to directory changes, and a clean exit code from the foreground command says nothing about a concurrent process racing it on the same file.

## A clean exit proves the foreground step succeeded, not that nothing else touched the file

The only thing that caught the silent revert was a standing habit of re-reading the file immediately after a workaround write, independent of the write path's own reported success. Guarded, tool-native edit operations carry a meaningful success signal by construction; a raw shell write that routes around that guard does not — it can't protect against a second process clobbering the same file a moment later. Treat any workaround-path write as unverified until read back, not just when something already seems off.

## See Also

- [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](worktree-liveness-check-before-destructive-cleanup.md) — same worktree-isolation mechanism, a different failure mode: that one is a state-vs-liveness gap during cleanup, this one is a trackedness gap during setup
- [A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope](guard-scope-vs-verbal-override.md) — same underlying guard family (worktree isolation for edits), this session hit its trackedness limit rather than its override scope
- [Fire-and-Forget Background Threads in Short-Lived Scripts Need a Bounded Join](fire-and-forget-thread-needs-bounded-join.md) — same shape of bug: background/concurrent work silently failing to land with no error surfaced, caught only by checking the real sink instead of trusting "no exception thrown"
- [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](concurrent-session-shared-file-collision.md) — same theme of a concurrent process racing an edit to the same file, at the multi-agent layer instead of a single session's own shell hook
