---
type: lesson
tags: [pattern, cross-session, config, automation]
Title: Self-Deleting Instruction Injection
Sources: Session reflection, 2026-07-03
Raw: "[../../raw/lessons-learned/2026-07-03-corpus-cleanup-and-reindex.md](../../raw/lessons-learned/2026-07-03-corpus-cleanup-and-reindex.md)"
Updated: 2026-07-03
---

# Self-Deleting Instruction Injection

When one session needs to leave a one-time actionable note for a different session or environment to pick up, build the note's own removal into it at injection time — don't rely on a future reader to clean it up.

## The pattern

To propagate findings into a different environment, append a marker-delimited block to a config file the target session will read. The block carries three things:

1. **The actionable content** — what the reader needs to know or do.
2. **Explicit self-removal instructions**, embedded in the block's own text, telling the reader to delete the block once it has been acted on.
3. **An idempotency check for re-injection** — so if the injecting process runs again before the block is consumed, it doesn't duplicate the note.

## Why it matters

A one-time pointer that doesn't carry its own removal instructions becomes permanent clutter, because the removal step depends on context the injecting session won't have once it's gone — it has no way to know later whether the note was ever read, let alone acted on. Two failure modes without this pattern:

- **The note never gets read** — nothing surfaces it, so it sits inert.
- **The note lingers forever as clutter** — it gets read and acted on, but nobody removes it, so it accumulates alongside every future injection.

Embedding the self-removal contract in the block itself — rather than in a separate process or in the injecting session's memory — avoids both failure modes, because the instructions travel with the content to wherever it's read.

## Generalization

This generalizes to any case where a session needs to leave a one-time actionable note for a different session or environment without leaving permanent clutter behind: cross-repo findings, hand-off TODOs, config-file annotations for a future run, or any producer/consumer pair that doesn't share process memory.

## See Also

- [Real Timestamps Beat File-Modification Timestamps for Falsifiable Claims](real-timestamps-for-falsifiable-claims.md) — another discipline from the same session
