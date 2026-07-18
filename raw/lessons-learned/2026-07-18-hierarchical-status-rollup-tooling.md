---
source: session-reflection
collected: 2026-07-18
published: Unknown
---

# Session Reflection: Hierarchical Status Rollup + Reusable Backfill Tooling

**Date**: 2026-07-18
**Session Goal**: Build a parent-status rollup for a task hierarchy (a parent's status derived from its children), then a reusable tool to extract/populate task data from a text source, ending with a refresh of a stale progress-tracking artifact.

---

## What Went Well

- **Never trusted a "success" response at face value.** Twice, an API call returned a 200-level success status but the write had silently no-op'd (a request body field the backend quietly ignored). Habitually re-querying independently after every mutating call, rather than trusting the response body, caught both.
- **Reasoned about worst-case correctness before running a broad rollup.** Before building a parent-status rollup over an arbitrary hierarchy, worked through what happens if it cascades multiple levels up — a grandparent node representing a much larger scope of untracked work could get falsely marked "Completed" the moment one small subtree finished. Kept the rollup deliberately single-level because of this reasoning, and it paid off directly: a later backfill run did legitimately propagate one level up, and having already worked through the safety argument meant the result could be recognized as *correct* immediately, rather than re-investigated from scratch under time pressure.
- **TDD for a genuinely algorithmic bug (multi-level convergence in a backfill script).** Rather than "just add a loop and see," wrote a 2-level failing test first. Since the original buggy code no longer existed (the fix had already been written), temporarily capped the fix back down to the buggy shape to get a genuine RED, confirmed it failed exactly as expected, then restored the fix and confirmed GREEN.
- **Checked for prior art before building a second implementation.** Asked to make a new tool "reusable, we'll use it multiple times," the first draft reinvented an HTTP+auth client from scratch. Checking the repo's existing auth CLI first revealed the real credential/session-handling convention already existed — the draft was rewritten to shell out to the existing tool for every API call, so there's exactly one auth implementation, not two silently drifting apart over time.
- **Dry-run before every live write, on a script touching production data.** A `--dry-run` flag caught two real bugs before a single row was created in the live system.

## What Went Wrong

- **A browser-automation false positive got reported as a real bug.** An automated double-click, followed by an accessibility-tree read that showed no dialog, was reported as "the feature never opens at all." A user screenshot immediately after showed the feature rendering fine — the automated click almost certainly had a timing issue. The finding wasn't caveated as "automation-derived, unconfirmed visually" before being reported as fact, costing a filed-then-retracted bug report.
- **A text search step and a downstream scoring step disagreed on scope.** A search command matched against a full document's text (including a section the code didn't otherwise fetch), but the code's keyword-scoring step only received a truncated view of that document (a single line) and treated "term not found in that truncated view" as "not a real match" — silently discarding correct matches. Caught by comparing tool output against a manual sanity check done minutes earlier, not by any automated check.
- **A title-truncation heuristic split on the wrong character.** Splitting on any colon truncated titles that legitimately contained colons mid-sentence. Only a period-followed-by-space is a safe sentence-boundary split point; colons are too common inside real titles.
- **Session ran very long across many distinct threads** before hitting a context-size wall that forced a compaction. Several of the later threads were each individually substantial enough to warrant their own session; bundling them meant a lot of accumulated context had to be carried for later work that didn't need most of the earlier detail.

## Lessons Learned

1. **Automated UI checks (clicks, accessibility-tree reads) can produce false negatives that look exactly like confirmed bugs.** Before filing a finding derived purely from browser automation as a real defect, either get an independent visual confirmation or explicitly caveat the finding as automation-derived and unconfirmed.
2. **A tool's search step and its scoring/parsing step must agree on what text they're operating over.** If a search matches against field A but the scoring code only received field B, "no match in B" does not mean "no real match" — it means the second step is blind to what the first step actually found. This is a general bug shape (search step and consumption step disagree on scope), not tied to any particular tool.
3. **When asked to make something reusable for repeated future use, search for what already provides that reusability first**, rather than designing a new implementation from scratch. A parallel/duplicate implementation of something like auth is a maintenance liability the moment the original changes and the copy doesn't.
4. **Reasoning explicitly about the worst-case node before running an automated bulk-update (rollup, backfill, migration) pays for itself later**, even if that worst case doesn't materialize immediately — it turns "is this output correct?" into a quick sanity check against an already-derived safety argument.
5. **When a bug's original buggy code has already been overwritten by the fix, deliberately reintroducing a minimal, scoped regression is a legitimate way to get a genuine RED test**, rather than skipping the RED step or trusting the GREEN test in isolation.

## Action Items

- [ ] When a finding is based solely on browser-automation output (not a direct visual/API-response confirmation), explicitly label it "unconfirmed, automation-derived" in the first report rather than stating it as fact.
- [ ] For any tool combining a text search step with a downstream scoring/parsing step, write down exactly what text scope each step operates over, to catch a scope mismatch before it ships.
- [ ] Before building a new script/tool for repeated future use, spend one pass checking for existing tooling that already solves part of the problem (especially auth/session handling), before designing from scratch.
- [ ] For sessions that start as a focused fix but keep accumulating "while I'm here" follow-on asks, periodically suggest whether the next follow-on deserves its own fresh session.

## Tips & Tricks for Claude Code

- **Tip**: To get a real RED test for a bug whose original buggy code no longer exists, temporarily cap/limit the fixed version to reproduce the exact old behavior, confirm RED, then restore and confirm GREEN. Faster and more honest than skipping straight to "it's tested."
- **Tip**: If a search command scans a full document/message but your downstream code only receives a truncated field of it, a real match can leave zero trace in that truncated view — don't treat "not found in the truncated field" as "not a real match."
- **Tip**: When a project already has a working auth/session CLI, shell out to it from a new script rather than re-implementing login — check that CLI's own docs for the credentials-file convention it expects.

---

*Generated by `/reflect`*
