---
type: concept
tags: [knowledge-management, architecture, determinism]
title: Deterministic Compiler vs. Agent-Driven Wiki Architecture
Sources: Towards Data Science, 2026-07-03
Raw: "[2026-07-03-llm-wikis-are-over-engineered.md](../../raw/knowledge-formats/2026-07-03-llm-wikis-are-over-engineered.md)"
Updated: 2026-07-08
---

# Deterministic Compiler vs. Agent-Driven Wiki Architecture

For purely structural, deterministic tasks over already-structured notes (link graphs, metadata extraction, lint checks), a parser-based compiler can outperform an LLM agent on cost, speed, and reproducibility — but it can't do semantic work an agent can.

## The Core Tension

An agent-driven wiki (like this one) re-reads and rewrites content on every ingest, consuming tokens and producing outputs that can vary run to run even on identical input. A counter-argument from a 2026-07-03 Towards Data Science piece: "If your input is deterministic, your pipeline should be too. Otherwise, you're just adding randomness where none existed." The author replaced their personal wiki tooling with a pure-Python, dependency-free compiler.

## The Compiler Pipeline (as described)

1. **Regex metadata extraction** — tolerant of inconsistent frontmatter formatting
2. **Graph builder** — cross-reference links via word-indexed phrase matching (not semantic)
3. **Section-aware rewriter** — regenerates machine-generated sections while preserving hand-edited ones
4. **Linter** — flags broken links and orphaned pages

Performance claim: word-indexing turned an O(n²) pairwise-regex graph builder into a near-linear one — 107s down to under 1s at 5,000 files; full compilation at that scale runs ~12.4s with zero token cost and identical output across OSes.

## Where the Compiler Approach Breaks Down

The source's own acknowledged limits map directly onto why this wiki stays agent-driven:

- **No semantic linking** — only exact name/phrase matches; a compiler can't recognize that two differently-worded notes describe the same concept.
- **No judgment calls** — merge-vs-new-article decisions (see this wiki's own Compile step), conflict annotation between contradicting sources, and cascade-update scoping all require reading comprehension, not pattern matching.
- **Requires already-structured input** — the compiler assumes clean, consistent source notes; this wiki's raw/ material is heterogeneous (session reflections, spec docs, third-party articles).

## Takeaway for This Wiki

The two approaches aren't strictly competing — they target different layers. Deterministic, structural maintenance (broken-link detection, orphan-page detection, index consistency) is exactly what this wiki's own Lint step already does without an LLM judgment call for the "Deterministic Checks" category. The compiler article is best read as validation that mechanical checks belong in deterministic code, while merge/new-article/conflict-annotation decisions stay with the agent because they require semantic understanding the compiler explicitly disclaims.

## See Also

- [Open Knowledge Format (OKF)](open-knowledge-format.md) — the format spec this wiki already follows; a compiler pipeline like the one described here could target OKF-conformant bundles directly
