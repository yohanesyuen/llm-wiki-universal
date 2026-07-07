---
type: lesson
tags: [prompt-caching, experiment-design, subagents, tokens, anthropic-api]
Title: Prompt Caching Can Invalidate "Fresh Session" A/B Experiments
Sources: session-reflection, 2026-07-07
Raw: "[../../raw/lessons-learned/2026-07-07-cache-invalidated-experiment.md](../../raw/lessons-learned/2026-07-07-cache-invalidated-experiment.md)"
Updated: 2026-07-07
---

# Prompt Caching Can Invalidate "Fresh Session" A/B Experiments

When comparing two conditions (e.g. an English vs. a translated system prompt) across separate subagent or session dispatches that share a system-prompt prefix, prompt caching can silently make the second call reuse the first call's cached content — so the "fresh" condition never actually saw the change under test.

## The failure

A two-subagent comparison was designed to measure whether swapping a system-prompt file changed token usage. When asked "what about just the input tokens?", a closer look at the raw usage block showed session B's `cache_read_input_tokens` count exactly matched session A's `cache_creation_input_tokens` count. That match is proof the two calls reused byte-identical cached content — the on-disk file swap between the two dispatches never reached the model call the experiment depended on. The result wasn't "no difference found"; the experiment's premise was invalid from the start.

This was the second failed attempt at the same measurement. The first attempt (an in-session re-read of the same file) failed a different way: the Read tool deduped the unchanged file and returned a "wasted call" notice instead of content, which also went unnoticed until the output was inspected directly.

## The check

Before trusting any cross-call comparison that shares a system-prompt prefix, diff the raw usage block:

- `cache_creation_input_tokens` on the first call vs. `cache_read_input_tokens` on the second call.
- An exact match is a strong signal of byte-identical cached reuse — the second call saw exactly what the first one cached, not the intended variant.

This is a known Anthropic API behavior (prompt caching reusing content across calls with a shared prefix), not a surprise that needs mid-experiment discovery. Treat it as a pre-flight check baked into the experiment design, not a post-hoc diagnosis run only when a result looks suspicious.

## Pattern

```
✗ design A/B dispatch → run both → report the number
✓ design A/B dispatch → plan for cache reuse across the shared prefix → run both →
  diff cache_creation vs cache_read before trusting the comparison → report
```

Reporting "the experiment's premise was invalid" instead of a spun "no difference found" is the correct outcome when the check fails — a misleading number is worse than an admitted null result.

## See Also

- [Real Timestamps Beat File-Modification Timestamps for Falsifiable Claims](real-timestamps-for-falsifiable-claims.md) — same family of lesson: anchor a before/after claim to a signal that can't be silently stale
- [Session Tool Efficiency](session-tool-efficiency.md) — related caching/reuse behavior at the tool-call level rather than the model-call level
