---
type: lesson
tags: [git, multi-agent, concurrency, worktree, diff-discipline]
title: Diff Every Multi-Paragraph Edit Before Committing It, and Fetch Before Every Push in a Shared Repo
sources: Session reflection, 2026-08-11
raw: "[../../raw/lessons-learned/2026-08-11-shared-repo-plan-scoping.md](../../raw/lessons-learned/2026-08-11-shared-repo-plan-scoping.md)"
updated: 2026-08-11
---

# Diff Every Multi-Paragraph Edit Before Committing It, and Fetch Before Every Push in a Shared Repo

Two commit-hygiene gaps let a shared-repo session get away with unsafe habits until one of them didn't: a document edit shipped a dangling duplicate fragment because no diff was read before commit, and several single-file pushes went out with no pre-push fetch check while a peer session was confirmed actively committing to the same branch.

## Diff before every commit that follows a multi-paragraph edit, unconditionally

A merge/replace operation on a multi-paragraph document didn't fully consume text that coincidentally repeated nearby, leaving stale lines stitched onto new content. It reached the shared branch before being caught and needed a separate fix-up commit. The failure is invisible in the editing tool's own success signal and only surfaces on a later, unrelated read — so the fix is to diff unconditionally after a multi-paragraph edit, not just when something already looks suspicious. Other commits in the same session that did diff first never hit this.

## A push that "happens to" auto-resolve is a near-miss, not evidence the pattern is safe

Several rapid single-file commits went directly to a shared branch without a pre-push fetch check, while a peer session was confirmed actively committing to the same repo. Every push happened to auto-fast-forward cleanly. That is not the same as being safe by design — in an actively multi-agent shared repository, prefer checking for upstream movement immediately before pushing whenever other agents are confirmed active, rather than treating repeated lucky outcomes as proof the no-pre-fetch habit generalizes.

## A worktree spun up for one anticipated collision is disposable the moment it resolves

An isolated worktree created for one specific, named file collision was torn down (worktree + branch, both) the moment it held zero commits — checked for uncommitted/unmerged work first, per the standing "confirm no unmerged work first" rule. Don't let the sunk cost of having already set up the worktree become a reason to keep or use it once the collision it was built for turns out unnecessary.

## See Also

- [A Request Built on a False Premise Deserves a Correction, Not Silent Compliance or Refusal](false-premise-scoping-and-diff-before-git-reconcile.md) — companion diff discipline: diffing the two sides of a *rejected* push to tell a real conflict from a harmless duplicate, versus this lesson's diff-before-commit and fetch-before-push habits
- [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](concurrent-session-shared-file-collision.md) — same multi-agent-shared-state family; that lesson's fix is a claim-before-edit signal, this one's is diff/fetch discipline around commits and pushes
- [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](worktree-liveness-check-before-destructive-cleanup.md) — same worktree-disposability theme; this session's teardown (checked for zero commits before removing) is the liveness check that lesson argues is necessary
