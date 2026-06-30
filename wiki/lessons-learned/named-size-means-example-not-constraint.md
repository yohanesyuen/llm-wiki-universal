---
type: lesson
tags: [specification, clarification, planning]
Title: Named Size in a Spec Means Example, Not Constraint
Updated: 2026-06-27
Sources: session reflection, 2026-06-27
Raw: "[2026-06-27-named-size-means-example-not-constraint.md](../../raw/lessons-learned/2026-06-27-named-size-means-example-not-constraint.md)"
---

# Named Size in a Spec Means Example, Not Constraint

## Rule

When a feature spec names a specific size ("2x2 grid", "3-tier", "single-column"), treat it as an **example of the use case**, not a hard architectural constraint. Extract the parametric concept; ask whether the size is fixed before writing code.

## Why

The number describes the motivating use case, not the intended scope. Building to the stated size then discovering the user wanted NxM throws away one implementation cycle. The question "Is this size fixed or should it generalize?" costs one sentence.

## How to apply

1. Separate the *concept* from the *example* when reading the spec.
2. Ask if the size is fixed before writing anything size-specific.
3. If parametric: implement generically; the specific size becomes a default.

## Corollary: thin wrappers for backward compat

When generalizing an existing interface, keep the old function as a thin wrapper over the new one. Existing callers and tests pass unchanged at zero migration cost.
