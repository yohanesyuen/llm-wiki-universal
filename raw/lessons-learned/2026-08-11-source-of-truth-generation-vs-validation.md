---
source: session-reflection
collected: 2026-08-11
published: Unknown
---

# Session Reflection: A "source of truth" that only validates isn't one

**Date**: 2026-08-11
**Session Goal**: Take a schema table from purely documentary to "functional" (user's word), then use it to change a class of tracked values.

---

## What Went Well

- **Negcheck discipline caught a self-authored bug before it shipped.** Every enforcement claim (a size mismatch, a color mismatch, a bad enum value) was proven by deliberately corrupting a fixture and confirming the check reacted — not just written and trusted. This caught a real bug: a "resize" helper called the same strict loader that the resize was meant to *fix* the input for, so it could never run on the exact state it existed to repair. A test with a deliberately out-of-sync fixture surfaced this immediately.
- **Reverts were clean and re-verified**, not just assumed correct — measured extents/state after every `git checkout` before moving on.
- **Regression checks used real A/B controls**: when a warning was suspected to be caused by a change, the check was "rebuild against the prior commit and confirm the same warning reproduces," not "it looks unrelated so it's probably fine."

## What Went Wrong

- **The core failure: built a validator when asked for a source of truth.** Given an explicit choice between "verify only" and "single source of truth," I built enforcement — raise if a derived value disagrees with its declared source — and treated that as satisfying the ask. It doesn't. A real source of truth *generates* the dependent value from the one place it's declared; what I built could only complain about drift after a human manually kept two representations in sync by hand. This surfaced only when the user tried to actually use it and I responded with a one-off script instead of the system doing the work. Their exact correction: "should be a max 1 line change if the wiring was done properly, stop cheating" — an accurate diagnosis.
- **Wrong-target picks under a compound, ambiguous instruction.** A follow-up request was scoped via a clarifying-question menu, but one option was offered without first checking whether the underlying data actually matched what its name implied (a "square" classification that, on inspection, only meant "bounding box happens to have equal width/height" — not "is visually a square"). The user caught the mismatch after real data had already been mutated. A cheaper check — inspecting the actual shape before presenting it as an option — would have prevented an entire wrong-and-reverted round trip.
- **First fix attempt edited the wrong representation entirely.** The system had two parallel representations of the same data (a structured record meant to become authoritative, and a legacy generated artifact that was still what the actual pipeline consumed). I edited the first, validated it, ran tests, and reported success — but the pipeline reads the second, so nothing visibly changed. This exact gap was already documented in the project's own notes; I'd read it earlier in the session and still fell into it under the pressure of "just make the change."
- **Iterative repairs stayed local instead of systemic.** Across several corrections in a row, each fix addressed only the most recent complaint, not the underlying mechanism. The same bug (a field set to "empty" while still inheriting from a parent, so "empty" silently meant "ask the parent" rather than "explicitly cleared") bit twice in a row on two different entries before the pattern was generalized.

## Lessons Learned

1. **"Make X a source of truth" is a generation requirement, not a validation requirement — confirm which one before building either.** They're easy to conflate because both close the gap between a declared value and reality. Validation closes it by complaining; generation closes it by deriving. A table is only a real source of truth if changing it and running one command suffices — if a human still has to manually update N other places and then run the checker to confirm they remembered, it's a checklist, not a source.
2. **In an inheritance/override system, "unset" and "explicitly cleared" need visibly distinct representations.** Setting a field to a null/empty value while a parent link is still active usually means "inherit from parent" under standard resolution logic, not "disabled" — this is an easy trap to fall into twice with the same shape before the general lesson lands.
3. **Before touching a derived/generated pipeline artifact, trace which file or representation is actually authoritative for the operation about to be performed.** Don't assume the most recently-edited or most conceptually-central representation is the one that matters — especially when the system already has known, documented gaps between "the intended source of truth" and "what's actually still wired up."
4. **When a correction implies a systemic gap, build the general mechanism, not the next patch.** The turning point was building a real, tested, reusable operation instead of continuing to hand-write one-off scripts per request. That should have been the first move once "make it authoritative" was confirmed as the actual requirement, not the fourth attempt.

## Action Items

- [ ] When a user picks "make X authoritative" from a menu of options, treat that as committing to writing a *generator*, and design any validator as a thin wrapper that calls the generator in check-only mode — never build the two as unrelated code paths that can drift apart.
- [ ] Before editing a value in a pipeline with multiple data representations, identify which representation the actual consuming step reads, and state that explicitly before making the edit.
- [ ] In any parent/inheritance-chain schema, audit whether "unset" and "explicitly cleared" are distinguishable; if not, treat that as worth fixing before it causes a second silent-reinheritance bug elsewhere.

---

*Generated by `/reflect`*
