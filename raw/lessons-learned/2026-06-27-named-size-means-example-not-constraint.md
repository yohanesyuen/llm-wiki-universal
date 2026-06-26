---
source: session-reflection
collected: 2026-06-27
published: Unknown
---

# Lesson: A Named Size in a Feature Spec Is Usually an Example, Not a Constraint

When a feature is described around a specific grid size, tier count, or slot count ("2x2 grid", "3-tier system", "single-column layout"), that number is almost always illustrative — the use case that motivated the feature — not a hard architectural constraint.

## The pattern

A spec describes feature X for a 2x2 case. The implementation hardcodes 2x2. The user asks for NxM. One full implementation cycle is thrown away.

## The lesson

Before implementing anything that names a specific size:

1. **Extract the concept from the example.** "Block inventory from source zones, rendered into a table zone" is the concept. "Top-left + top-right source, bottom-left table" is the 2x2 example. Implement the concept.

2. **Ask explicitly if the size is fixed.** "Is the 2x2 a hard constraint or should this generalize to NxM?" costs one sentence. A mid-implementation redesign costs much more.

3. **Parametric up-front is cheaper than pivot mid-way.** The marginal cost of writing `compute_grid(cols, rows)` instead of `compute_grid_2x2()` is small. The cost of redesigning after one full implementation cycle is high.

## Corollary: backward compatibility via thin wrappers

When generalizing an existing interface (e.g., replacing `compute_grid_zones()` with `compute_grid(cols, rows)`), keep the old function as a thin wrapper. Existing callers and tests continue to pass unchanged. This is strictly cheaper than updating every call site.
