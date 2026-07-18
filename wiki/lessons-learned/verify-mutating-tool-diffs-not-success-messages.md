---
type: lesson
tags: [tooling, data-loss, verification, orm]
Title: A Tool's Success Message Describes Intent, Not Effect — Diff the Actual Before/After
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-managed-block-trust-and-drift-detection.md](../../raw/lessons-learned/2026-07-18-managed-block-trust-and-drift-detection.md)"
Updated: 2026-07-19
---

# A Tool's Success Message Describes Intent, Not Effect — Diff the Actual Before/After

For any tool that mutates shared or durable state (a doc file, a git history, a live migration), verify the actual before/after rather than trusting the printed confirmation — this matters most for a tool whose contract is "replace an entire block/file" rather than "append" or "patch," since that class of tool has no partial-failure signal: it either fully replaces or fully fails, with nothing in between to catch a mistake mid-way.

## What happened

A doc-refresh script reported success. Diffing its actual before/after — rather than trusting the message — revealed it had silently deleted a large block of hand-curated content that happened to sit inside the region it was designed to fully replace. Catching this before committing was the highest-value moment of the session. The root cause: running an unfamiliar tool with a destructive-by-design contract without reading that contract first. The tool's own docs stated plainly that it replaces an entire managed region; reading that up front would have caught the risk before it existed, rather than being saved only by a post-hoc diff habit.

## Query the ORM's real mapped name, not its declared model name

Checking whether a database table "exists" by querying an ORM's declared model name (rather than its actual `@@map`'d/mapped table name) produced a false negative that would have led to the wrong fix — reverting a live, already-applied migration — had it not been caught by a broader sanity check. For any ORM with explicit table/column mapping, list all real tables first when unsure whether a feature's data exists.

## Multiple trackers for one fact are independent failure points, not redundancy

Multiple parallel status-tracking mechanisms for the same underlying fact (task checkboxes, hand-written doc prose, a generated progress file, an external issue tracker) are not redundancy — they're independent chances for exactly one of them to go stale while the others update. Every drift incident traced back to exactly one tracker not being updated in lockstep with the others.

## Useful git forensics

`git log -S"<literal string>" -- <path>` (pickaxe search) pinpoints the exact commit that introduced or removed specific text — faster than bisecting or eyeballing full diffs when you know *what* changed but not *when*. `git branch --merged <target>` is a fast, unambiguous check for whether a branch was actually merged, more reliable than comparing file contents by eye.

## See Also

- [A Documented Default Path Is a Claim, Not a Fact — A Schema/Ingestion Audit Checklist](schema-and-ingestion-audit-checklist.md) — same discipline of verifying real state over an assumed one
- [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](worktree-liveness-check-before-destructive-cleanup.md) — sibling lesson about verifying real state before a destructive action
