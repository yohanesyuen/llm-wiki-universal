---
type: lesson
tags: [git, security, sanitization, docker, verification]
Title: Git History Scrubbing Has Two Leak Surfaces; a Moved Mount Isn't Done Until the Consumer Restarts
Sources: Session reflection, 2026-07-06
Raw: "[../../raw/lessons-learned/2026-07-06-cross-session-repo-cleanup.md](../../raw/lessons-learned/2026-07-06-cross-session-repo-cleanup.md)"
Updated: 2026-07-06
---

# Git History Scrubbing Has Two Leak Surfaces; a Moved Mount Isn't Done Until the Consumer Restarts

A mixed infra-hygiene session (CORS allowlisting, scrubbing sensitive data from git history, moving an app directory under a live bind mount, standing up a new private upstream) surfaced two verification gaps and one retention convention worth generalizing.

## Git History Scrubbing: File Content and Commit Messages Are Separate Leak Surfaces

Sanitizing a committed data file and rewriting history to remove it took two passes instead of one. The first rewrite targeted file content only; a re-check still showed hits — not because the rewrite failed, but because the search was walking the rewrite tool's own backup ref, and because commit *messages* (not just diffs) had leaked detail directly in prose.

- Check both surfaces up front, before deciding what needs scrubbing: `git log -p` (diffs) and `git log --format="%B"` (messages). Treating messages as a second pass after "the diffs are clean" wastes a full rewrite cycle.
- Scope the verification sweep to the branch you actually care about (e.g. `git log main -p`), not `--all` — an unscoped sweep also surfaces the rewrite tool's own backup refs mid-process, producing false "still leaking" hits. Inspect and delete those backup refs as a separate, explicit step.

## A Config Edit to a Live Mount/Reference Isn't Done Until the Consumer Is Restarted and Checked

After moving an app directory and editing a container's bind-mount path, the change was not called done at "the edit looks right." The compose config was resolved to confirm the actual source path, then the container was recreated and inspected directly to confirm it served content from the new location. Editing the pointer is necessary but not sufficient whenever something resolved a path once at startup — a container, a running process — and won't see the change until it's recreated. This is the same discipline as [Smoke-Test the Parts You Can](../conventions/smoke-test-parts-you-can.md), applied specifically to path/mount changes: config review proves the edit is textually correct, not that the running consumer picked it up.

## Retain Real Data at a Location Matching an Existing Convention Before Destroying It

Before sanitizing a committed data file and rewriting history to strip it, the real data was copied out to an untracked location first — matching a retention convention already established elsewhere in the same project family, rather than inventing a new one. This mattered beyond the immediate task: the retained copy later became the seed data for an unrelated migration, discovered by a separate concurrent session without any explicit hand-off being required. When retiring or replacing a data file, parking the real data at a conventional location (not an ad-hoc one) makes it discoverable to other work that didn't know to ask for it.

## See Also

- [Smoke-Test the Parts You Can](../conventions/smoke-test-parts-you-can.md) — same "verify the running behavior, not just the diff" principle
- [No Confidential Information in Code or Git History](../conventions/no-confidential-leak.md) — the broader rule this scrubbing task was enforcing; also covers why a status broadcast about the cleanup needed its own sanitization pass
- [Layer-Boundary Config Bugs and Staged Service Cutover](layer-boundary-configs-and-staged-cutover.md) — adjacent "a config edit doesn't take effect until the consumer crosses the relevant boundary" theme, for network/TLS config rather than mounts
