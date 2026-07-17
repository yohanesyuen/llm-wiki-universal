---
type: lesson
tags: [empirical-verification, caching, live-systems]
Title: Probe a Live Runtime Instead of Theorizing; Key a Cache by Entity, Not by a Shared Evicting Scope
Sources: Session reflection, 2026-07-10
Raw: "[../../raw/lessons-learned/2026-07-10-empirical-probes-cache-isolation.md](../../raw/lessons-learned/2026-07-10-empirical-probes-cache-isolation.md)"
Updated: 2026-07-10
---

# Probe a Live Runtime Instead of Theorizing; Key a Cache by Entity, Not by a Shared Evicting Scope

For "how does system X identify/map to Y" questions in a live system, running the actual tools (process listings, environment inspection, a parent-process walk) turns an apparently unsolvable external-inference problem into a trivial internal read — many agent/CLI runtimes export their own identity (a session id, an executable path, an "am I running under it" flag) into every child process's environment, which is far more reliable than inferring identity from file mtimes or argv.

## Reproduce the exact failing path before attributing a break

A "this broke" report can be environmental or temporal — a record that a fixed time window auto-excludes as it ages, not a code change — rather than an actual regression from recent work. Running the exact failing code before assuming self-attribution avoided a wrong diagnosis.

## Separate reproduced from inferred, explicitly

State which defects were *reproduced* (run repeatedly, observed to flap) versus *inferred by reading the code* (never actually triggered at the scale that would expose them) — and say which is which, rather than reporting both with the same confidence.

## A shared, evicting cache is incompatible with a "complete per-entity index" requirement

Key a cache by the entity it belongs to, and isolate that entity's maps under its own scope rather than a shared global cache that can evict entries out from under an in-progress lookup. Evict whole entities at once. This makes lookups leak-proof and complete, and stops derived structures from silently depending on eviction order or state left over from a prior run.

## Tail a live append-only file by advancing past complete lines only

Advance the read offset only past complete, newline-terminated lines, and leave a mid-write partial line unconsumed so it gets re-read whole on the next pass — this is the cheap, deterministic way to support incremental tailing of a file another process is actively appending to.

## Filter at the view layer, not the parse layer

A "hide these types" filter belongs at the render/view stage. Pushing it into the parse stage silently severs structural links that routed *through* the hidden items — parse complete, filter the view, so nothing downstream loses reachability to data that's merely hidden, not absent.

## Tips

- To test file-tailing/liveness deterministically, monkeypatch a module-level path lookup and grow/rotate a temp file by hand, rather than depending on a real long-running process.
- Maintain a progress/todo list through multi-step work, or don't open one — a stale list left unmaintained past the first couple of updates is noise, not tracking.
- When work is framed as discrete steps and one step requires touching more than its nominal scope to keep things working, confirming the boundary first is cleaner than expanding and flagging after the fact.

## See Also

- [Real Timestamps Beat File-Modification Timestamps for Falsifiable Claims](real-timestamps-for-falsifiable-claims.md) — same "don't trust filesystem-adjacent proxies, use the real signal" discipline
