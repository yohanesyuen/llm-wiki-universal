---
type: lesson
tags: [architecture, data-model, validation, source-of-truth]
title: A "Source of Truth" That Only Validates Isn't One — It Generates
sources: Session reflection, 2026-08-11
raw: "[../../raw/lessons-learned/2026-08-11-source-of-truth-generation-vs-validation.md](../../raw/lessons-learned/2026-08-11-source-of-truth-generation-vs-validation.md)"
updated: 2026-08-11
---

# A "Source of Truth" That Only Validates Isn't One — It Generates

Given an explicit choice between "verify only" and "make it a single source of truth," building enforcement that raises when a derived value disagrees with its declared source does not satisfy "source of truth" — a real one *generates* the dependent value from the one place it's declared, closing the gap by deriving rather than by complaining after a human manually kept two representations in sync by hand.

## "Make X a source of truth" is a generation requirement, confirm which one before building either

Validation and generation are easy to conflate because both close the gap between a declared value and reality, but they close it differently: validation complains, generation derives. A table is a real source of truth only if changing it and running one command suffices — if a human still has to manually update N other places and then run a checker to confirm they remembered, it's a checklist, not a source. The exact failure this produces: the system responds to a request to actually use the "source of truth" with a one-off script instead of the system doing the work — the tell that only a validator was ever built.

## In an inheritance/override system, "unset" and "explicitly cleared" need visibly distinct representations

Setting a field to a null/empty value while a parent link is still active usually means "inherit from parent" under standard resolution logic, not "disabled." This is an easy trap to fall into twice with the same shape (it bit two different entries in a row) before the general pattern is recognized and a distinct sentinel or an explicit "parent: null" requirement is introduced.

## Trace which representation is actually authoritative before touching a derived pipeline artifact

Don't assume the most recently-edited or most conceptually-central representation is the one the consuming step actually reads — especially when a system already has known, documented gaps between "the intended source of truth" and "what's actually still wired up." Editing, validating, and testing the wrong representation can look like a complete, successful change while the pipeline that matters reads a different file entirely.

## When a correction implies a systemic gap, build the general mechanism, not the next patch

The turning point in the session that produced this lesson was building a real, tested, reusable generator instead of continuing to hand-write one-off scripts per request — that should be the first move once "make it authoritative" is confirmed as the actual requirement, not a late-stage recovery after several patches.

## See Also

- [A Destructive Live Migration and Its Matching Code Deploy Are One Atomic Unit](migration-deploy-atomicity-and-real-data-default.md) — adjacent theme of verifying a system's real, deeper state before trusting a derived signal about it
