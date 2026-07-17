---
type: lesson
tags: [data-flow, filtering, api-design]
Title: A New Parameter Is a Data-Flow Change, Not a Signature Change; Filter Every Structure the Record Leaks Into
Sources: Session reflection, 2026-07-10
Raw: "[../../raw/lessons-learned/2026-07-10-thread-opt-out-param-through-pipeline.md](../../raw/lessons-learned/2026-07-10-thread-opt-out-param-through-pipeline.md)"
Updated: 2026-07-10
---

# A New Parameter Is a Data-Flow Change, Not a Signature Change; Filter Every Structure the Record Leaks Into

Adding a pass-through parameter to a pipeline is not "add an arg" — it's "find every hop between the public entry point and the point of use, and thread it through each one." A parameter that stops halfway is a silent no-op.

## Enumerate every hop before the first edit

Trace the parameter's full future path (entry function → intermediate stages → public entry point) before editing anything, and edit every hop in one pass. Editing hops incrementally as they're discovered risks a half-wired feature that appears to work at the entry point but silently drops before reaching where it matters. A single targeted grep for every reference to the thing being filtered (a type name, a field) — the accepted-set, the dispatch branch, every caller — turns the change into a mechanical edit once the map exists.

## Prefer denylist defaults for filters over new/unknown inputs

When filtering a set of known types, subtracting an opt-out (denylist) set lets future unknown types keep flowing through by default. An allowlist silently drops anything new the moment it appears. Choose based on which failure mode is safer for the specific pipeline, and state which was chosen and why — this is a genuine, reversible design fork worth surfacing rather than silently picking one.

## A filter must also exclude from every side index the record leaks into

A parse function populated not just the returned list but also a shared lookup cache and a parent→children index. A record skipped from the main output still has to be kept out of *those* too, or it stays reachable via a secondary lookup or a parent link even though it's absent from the primary result. "Filter" means filter everywhere the record leaks — ask explicitly whether the excluded item also lives in a cache, reverse-index, or secondary structure.

## Verify a filter by diffing aggregate counts, not by eyeballing

`Counter(type)` before vs. after a filter change is a cheap, unambiguous verification: confirms the exact intended records left and nothing else moved. Run it against real data, not a toy fixture — a one-off harness (list a real input → run the pipeline twice → diff the counts) is often a faster and more convincing check than adding a formal test file, especially for an exploratory or notebook-backed tool.

## Tips

- Editor "variable not accessed" hints after a partial multi-hop edit are a useful progress checklist — each one marks a hop still to wire, and they clear as the thread completes. Don't mistake them for errors.

## See Also

- [Probe Sibling APIs Directly; Plausible-Small Numbers Are a Bug Smell](api-capability-probing-and-plausible-wrong-values.md) — same "verify against real data/output, not by inspection alone" discipline
