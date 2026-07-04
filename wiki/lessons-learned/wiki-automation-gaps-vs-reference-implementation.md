---
type: lesson
tags: [wiki, knowledge-management, automation, roadmap]
Title: Wiki Automation Gaps Found by Comparing Against a Reference Implementation
Sources: Session reflection, 2026-07-04
Raw: "[../../raw/lessons-learned/2026-07-04-wiki-automation-gaps-vs-reference-implementation.md](../../raw/lessons-learned/2026-07-04-wiki-automation-gaps-vs-reference-implementation.md)"
Updated: 2026-07-04
---

# Wiki Automation Gaps Found by Comparing Against a Reference Implementation

Comparing this ingest→compile→query pipeline against a public reference implementation of the same "LLM curates, human queries" pattern (built on a note-taking app with PARA + Zettelkasten organization, shipping five distinct skills plus a structured edit surface) surfaced four automation gaps worth closing, independent of the taxonomy differences between the two systems.

## Method: separate workflow automation from taxonomy

When comparing two systems that share a core loop but differ in substrate, split the comparison into "automation ideas" (lint, retopology, decoupled resource-import — these generalize regardless of substrate) versus "taxonomy" (PARA/Zettelkasten — this does not generalize to a narrower-scope wiki like this one, which only covers lessons and conventions). Conflating the two produces a comparison that either over- or under-values the reference implementation.

## Gap 1: No health-check pass

This pipeline only ever ingests and grows `wiki/`; nothing periodically checks for broken links, orphaned articles, stale claims, or duplicate topics. The reference implementation's dedicated lint skill catches exactly this class of drift. A lint pass — report-only to start, matching the deterministic-vs-heuristic split already used elsewhere in this pipeline (see the Lint section of the `karpathy-llm-wiki` skill) — is the natural fix. (As of this writing, the skill already has a Lint mode covering index consistency, internal links, Raw references, and See Also; the heuristic half — factual contradictions, orphan pages, stale claims — still depends on being invoked, since nothing runs it automatically.)

## Gap 2: Flat topic folders never get revisited

Topic structure is decided once at ingest time (whatever subdirectory a new article lands in) and never reorganized. A retopology-style pass — re-bucketing or splitting a topic folder once it grows past a size where a flat structure stops being useful — is missing entirely. `lessons-learned/` in this wiki is the folder most likely to hit that threshold first, given its growth rate relative to `conventions/` and `knowledge-formats/`.

## Gap 3: Ingestion bottlenecked on one machine — partially mitigated

The compiling skill only works where it's locally installed, which blocks any other session (a fresh container, a session rooted in a different repo) from doing anything beyond dropping a file into `raw/` and leaving a note that ingestion is pending. The reference implementation avoids this with a structured, tool-based edit surface rather than a skill-only compile step.

Note: this project's own `CLAUDE.md` (at the wiki root) already documents a partial mitigation — a git branch-and-PR protocol that lets any session with repo write access drop a raw source and open a PR, with a note that compilation awaits the skill running on the main machine. That solves *write access* but not the underlying gap: compilation itself is still a single-machine operation.

## Gap 4: Ingestion and reflection are conflated

`raw/` sources mostly arrive via the `/reflect` session-retrospective path today. There's no separate, first-class path for importing external reading material (articles, other repos, reference docs) that isn't a session reflection. Stretching one path to fit both use cases risks warping either the reflection format or the external-import format to accommodate the other.

## Action items

1. Design a lint pass for `wiki/` covering broken links, orphan articles, stale claims, and duplicate topics — report-only, deterministic-vs-heuristic split.
2. Design a retopology pass that reorganizes topic folders once one grows past a usability threshold.
3. Consider a structured, non-skill-dependent write path for `wiki/` so compilation isn't bottlenecked on one machine.
4. Keep a distinct ingestion path for external resource imports, separate from `/reflect`-sourced session retrospectives.

## See Also

- [Wiki Ingest and Cleanup Discipline](wiki-ingest-and-cleanup-discipline.md) — per-ingest hygiene rules this gap analysis complements at the pipeline level
