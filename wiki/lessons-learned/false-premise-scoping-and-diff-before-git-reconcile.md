---
type: lesson
tags: [scoping, self-critique, git, concurrent-editing]
Title: A Request Built on a False Premise Deserves a Correction, Not Silent Compliance or Refusal
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-evidence-based-scoping-and-concurrent-git-conflicts.md](../../raw/lessons-learned/2026-07-18-evidence-based-scoping-and-concurrent-git-conflicts.md)"
Updated: 2026-07-19
---

# A Request Built on a False Premise Deserves a Correction, Not Silent Compliance or Refusal

When a request like "enable X for all users" assumes X already exists and that its current restriction is an oversight, investigate before acting — silently building something that contradicts a recorded design decision, or silently refusing without checking whether the requester actually wants that decision reversed, are both worse than stating the facts and asking.

## Verify the premise first

In the case that produced this lesson, the feature's UI didn't exist yet (only backend plumbing did), and an already-written spec explicitly listed the requested scope expansion as a deliberate non-goal. Surfacing both facts plainly, then asking a clarifying question, let the requester make an informed call instead of having a stale assumption silently reinterpreted in either direction.

## Checklists are a record of past belief, not a live oracle

A task marked "not done" turned out to already be shipped under a different task's implementation — verified by reading the actual source file, not by trusting the checklist. This is the same category of lesson as re-verifying dry-run scripts and stale doc references, applied to a task-tracker checkbox: before trusting or acting on what a checklist says is done, check the actual artifact when the cost of being wrong (redoing work, or skipping needed work) is non-trivial.

## "Confirmed" is a factual claim — verify it's literally true before writing it

There's a strong pull to write a tidy, authoritative-sounding justification for a scoping decision — it's easy for "I decided this myself, for time reasons" to quietly upgrade into "this was agreed upon" without a deliberate check first. Before writing that something was "confirmed," "agreed," or "approved" in any status note, commit message, or doc update, re-verify against the actual conversation that this literally happened, especially under time or effort pressure where the shortcut phrase is tempting.

## Diff before you resolve a rejected push

When a routine push is rejected as non-fast-forward because a concurrent session pushed to the same shared remote, don't reach for a forced push. Diff the two divergent commits byte-for-byte (`diff <(git show <local-sha>) <(git show <remote-sha>)`, ignoring the first line since the commit hash always differs) to check whether it's a real conflict or just a duplicate produced by two sessions independently fixing the same thing. If content-identical, `git pull --rebase --autostash` safely auto-drops the duplicate — then re-run the full test suite on the rebased tree before pushing again, rather than trusting that a clean rebase means the code still works.

## See Also

- [A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope](guard-scope-vs-verbal-override.md) — related theme of verifying assumed state rather than trusting a conversational shortcut
- [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](concurrent-session-shared-file-collision.md) — sibling concurrent-editing lesson from a related project window
