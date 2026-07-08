---
source: https://towardsdatascience.com/llm-wikis-are-over-engineered-i-replaced-mine-with-a-pure-python-compiler/
collected: 2026-07-08
published: 2026-07-03
---

# LLM Wikis Are Over-Engineered — I Replaced Mine With a Pure Python Compiler

Publication: Towards Data Science.

## Core Argument

The author challenges the trend of using LLM agents to build personal knowledge wikis, arguing instead for a deterministic Python compiler approach. Rather than routing existing local text through probabilistic systems, a parser-based pipeline delivers consistent, reproducible outputs without token costs or external APIs.

## Key Claims

**Problem with Agent-Based Wikis:**
- Every document addition triggers token-consuming re-reads and rewrites
- Network latency or compute costs accumulate unnecessarily
- Non-deterministic outputs produce different results from identical inputs

Quote: "If your input is deterministic, your pipeline should be too. Otherwise, you're just adding randomness where none existed."

**The Compiler Solution:**
A four-stage pipeline transforms raw markdown notes deterministically:
1. Regex metadata extraction — handles inconsistent formatting
2. Graph builder — creates cross-reference links via word-indexed phrase matching
3. Section-aware rewriter — preserves hand-edited content while regenerating machine sections
4. Linter — identifies broken links and orphaned pages

## Technical Achievements

**Performance Optimization:**
The graph builder evolved from O(n²) pairwise regex matching to word-indexed matching:
- 5,000 files: reduced from 107 seconds to under 1 second
- Scales far more efficiently than naive approaches

**Bug Documentation:**
The linter initially miscounted orphans by including "Referenced By" section links. The fix isolated counting to the "Related" section only.

**Benchmarking:**
At 5,000 files, full compilation takes ~12.4 seconds on Windows hardware with zero token cost. Results proved deterministic and identical across Linux and Windows machines.

## Limitations Acknowledged

- Requires reasonably structured source data
- Semantic linking impossible (only exact name matches)
- Cannot understand meaning without additional enhancement layers

## Code Details

- Pure Python using only standard library (no external dependencies)
- 17 unit and integration tests using `unittest`
- Full codebase referenced at GitHub repo `wiki-compiler/`

## Key Insight

Quote: "An agent decides what your wiki might look like. A compiler guarantees what it must look like." For deterministic organizational tasks, parser-based solutions outperform probabilistic systems in cost, speed, and reliability.
