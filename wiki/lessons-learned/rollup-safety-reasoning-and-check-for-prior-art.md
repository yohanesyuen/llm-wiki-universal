---
type: lesson
tags: [data-integrity, tdd, tooling-reuse, hierarchical-rollup]
Title: Reason About the Worst-Case Node Before Running a Bulk Rollup; Search for Prior Art Before Building a Second Implementation
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-hierarchical-status-rollup-tooling.md](../../raw/lessons-learned/2026-07-18-hierarchical-status-rollup-tooling.md)"
Updated: 2026-07-19
---

# Reason About the Worst-Case Node Before Running a Bulk Rollup; Search for Prior Art Before Building a Second Implementation

Before building an automated status rollup over an arbitrary hierarchy (a parent's status derived from its children), work through what happens at the worst-case node — a grandparent representing a much larger scope of untracked work could get falsely marked "Completed" the moment one small subtree finishes. This particular risk is why a rollup was deliberately kept single-level rather than cascading multiple levels up automatically. The payoff came later: when a backfill run legitimately propagated one level up, the safety argument had already been worked through, so the result could be recognized as *correct* immediately rather than re-investigated from scratch under time pressure.

## Never trust a "success" response at face value

Twice in the same session, an API call returned a 200-level success status but the write had silently no-op'd (a request body field the backend quietly ignored). Habitually re-querying independently after every mutating call — not trusting the response body — caught both. This generalizes: a tool's own reported success describes what it attempted, not necessarily what actually changed.

## Reintroduce the bug deliberately to get a genuine RED test

For a genuinely algorithmic bug (multi-level convergence in a backfill script), the original buggy code no longer existed once the fix had already been written. Rather than skipping the RED step or trusting the GREEN test in isolation, the fix was temporarily capped back down to the buggy shape, confirmed to fail exactly as expected, then restored and confirmed to pass. This is a reusable technique whenever a bug's original buggy code has already been overwritten by its fix.

## Check for existing tooling before building "reusable"

Asked to make a new tool "reusable, we'll use it multiple times," a first draft reinvented an HTTP+auth client from scratch. Checking the repo's existing auth CLI first revealed the real credential/session-handling convention already existed — the draft was rewritten to shell out to the existing tool for every API call, avoiding a second, silently-drifting auth implementation.

## A search step and a scoring step must agree on scope

A search command matched against a document's full text, but a downstream keyword-scoring step only received a truncated view of that same document — and treated "term not found in the truncated view" as "not a real match," silently discarding correct results. If a search matches against field A but a downstream step only receives field B, "no match in B" does not mean "no real match" — it means the second step is blind to what the first step actually found. This is a general bug shape (search step and consumption step disagreeing on scope), not tied to any specific tool.

## See Also

- [Browser Automation False Positives Look Exactly Like Confirmed Bugs](browser-automation-false-positive.md) — a companion lesson from the same session
- [Resolve Targets Directly, Don't Infer From a Manifest; Test Through a System's Own API, Not a Generic External One](resolve-targets-test-through-own-api.md) — related discipline around trusting a system's real interface over an assumption
