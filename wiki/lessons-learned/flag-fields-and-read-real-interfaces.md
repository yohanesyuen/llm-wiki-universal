---
type: lesson
tags: [review, code-reuse, clarifying-questions]
Title: Flag Each Surprising Field Separately; Read the Real Interface Before Extending It
Sources: Session reflection, 2026-07-17
Raw: "[../../raw/lessons-learned/2026-07-17-concurrent-session-collision-and-scoped-feature-delivery.md](../../raw/lessons-learned/2026-07-17-concurrent-session-collision-and-scoped-feature-delivery.md)"
Updated: 2026-07-17
---

# Flag Each Surprising Field Separately; Read the Real Interface Before Extending It

When an out-of-band state change is discovered, or an existing abstraction needs extending, resist the pull toward one bundled question or one over-general rebuild — both compress information the recipient (a human, or a future maintainer) needs kept distinct.

## Flag each surprising field on its own, not bundled

After an out-of-band edit to a data record, more than one field looked surprising. Rather than a single vague "does this look right?", each field was called out individually with the specific risk it implied. This let a human confirm one as intentional and correct the other precisely, instead of one ambiguous "yes" accidentally covering both. A single bundled question risks treating approval of the obviously-fine part as approval of the actually-wrong part.

## Read the actual current interface before extending it

For a "just use the thing we already have" instruction, the existing abstraction's real interface was read first rather than assumed — it turned out to support one access pattern (client-driven) but not the one now needed (direct server-side write). The fix was extending it with exactly one new method for the one new need. Reading first sized the actual gap correctly; either extreme — assuming it already covers the new case, or assuming it needs a bigger rebuild than it does — wastes effort in opposite directions.

## Related: a boolean flag is often a caller-controlled-direction smell

A helper accreted a `reversed=` boolean flag. The idiomatic fix is caller-controlled direction (the caller passes the comparator/order it wants) rather than either an internal flag branch or a duplicated second function.

## See Also

- [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](concurrent-session-shared-file-collision.md) — companion lesson from the same problem family, on stopping cold at a mid-task collision and re-verifying fresh once it's resolved
- [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](worktree-liveness-check-before-destructive-cleanup.md) — same theme of a state-check alone being insufficient signal
