---
type: lesson
tags: [timestamps, evidence, cross-referencing]
Title: Real Timestamps Beat File-Modification Timestamps for Falsifiable Claims
Sources: Session reflection, 2026-07-03
Raw: "[../../raw/lessons-learned/2026-07-03-corpus-cleanup-and-reindex.md](../../raw/lessons-learned/2026-07-03-corpus-cleanup-and-reindex.md)"
Updated: 2026-07-07
---

# Real Timestamps Beat File-Modification Timestamps for Falsifiable Claims

When a claim compares two independent timelines, anchor both sides to real event times — not to filesystem mtimes, which reflect when a file happened to be touched, not when the underlying event occurred.

## What worked

Stamping each artifact with its actual originating-session start/end time — extracted from structured log timestamps rather than filesystem mtime — enabled hour-level-precision comparisons against a separate system's commit history. This supported a specific, falsifiable claim ("this workaround was used N hours after the proper fix had already shipped") that approximate dates would not have supported.

## Why it matters

A claim like "X happened before/after Y" only holds up under scrutiny if both X and Y are anchored to real event times. File mtimes are contaminated by unrelated operations — a copy, a re-save, a git checkout, an export step — any of which can shift the timestamp without the underlying event having moved at all. Once mtime drift is possible, the claim becomes unfalsifiable: a skeptic can always attribute the ordering to the contaminating operation instead of the claimed cause.

## The rule

Whenever a claim needs to be falsifiable — especially "this was used after that already existed" or "this predates that" — spend the extra effort to extract the real event timestamp from structured data (log lines, commit metadata, message headers) rather than relying on when a file was last written to disk. The extraction cost is worth it precisely because it's what makes the claim defensible.

## See Also

- [Self-Deleting Instruction Injection](self-deleting-instruction-injection.md) — another discipline from the same session focused on getting one-shot mechanics right
- [Prompt Caching Can Invalidate "Fresh Session" A/B Experiments](prompt-caching-invalidates-fresh-session-experiments.md) — same family of lesson: anchor a before/after claim to a signal that can't be silently stale, this time the raw token-usage block instead of a file mtime
