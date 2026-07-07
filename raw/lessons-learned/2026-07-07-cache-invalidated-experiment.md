---
source: session-reflection
collected: 2026-07-07
published: Unknown
---

# Session Reflection: Cache-Invalidated Experiment, Bloat/Gate Rulemaking, and a Silent-Failure Bug Hunt

**Date**: 2026-07-07
**Session Goal**: A long, multi-thread session spanning a storage migration, CLAUDE.md hygiene work, a conlang audit/fix, a statusline bug fix, a token-efficiency experiment, and cross-session coordination.

---

## What Went Well

- **Root-causing a broken experiment instead of reporting a misleading number.** A two-subagent "fresh session" comparison (English vs. Chinese system prompt) was designed to measure token-efficiency impact. When the user asked "what about just the input tokens?", a deeper look at the raw usage blocks (`cache_creation_input_tokens` vs `cache_read_input_tokens`) showed session B's cache-read count exactly matched session A's cache-creation count — proof the two calls reused byte-identical cached content, meaning the on-disk file swap never reached the model call the experiment depended on. Reporting "the experiment's premise was invalid" instead of a spun "no difference found" result was the right call and was explicitly rewarded ("Oh yes, thanks for pointing it out" on a related citability catch).
- **Self-critique gate, once stated as a rule, immediately caught a real mistake in the same session.** While documenting `gmail_send.py` in a README, an Edit inserted an awkward non-sequitur line; it was caught and reverted before the next edit, rather than compounding it.
- **Using a temp-file `curl --data @file` instead of inline `-d '...'`** immediately fixed a shell-quoting failure when broadcasting a message containing apostrophes/special characters to bus.test. Small, mechanical, but worth keeping as a default habit for any curl payload with unpredictable text content.
- **Grounding new standing rules in real incidents, not abstract principle.** Both the "CLAUDE.md bloat hygiene" and "Self-critique gate" rules were refined through direct user pushback into a form that cites *why* (a real gap the user pointed out) rather than staying declarative-only.

## What Went Wrong

- **The Chinese-vs-English token experiment was run twice before its fatal flaw was found.** First attempt (in-session re-read of the same file) silently failed a different way — the Read tool deduped/cache-skipped the unchanged file and returned a "wasted call" notice instead of content, which wasn't caught until output was inspected. The second attempt (two fresh subagents) hit the prompt-caching artifact. In hindsight, the caching risk should have been anticipated *before* designing the two-subagent version — prompt caching reusing content across calls with the same prefix is a known Anthropic API behavior, not a surprise that needed discovery mid-experiment.
- **A statusline logging bug (daemon thread killed before its HTTP POST completed) was present and silently failing 100% of the time** until directly investigated. Nothing failed loudly — it just never logged. This is exactly the kind of silent-failure class the project's own "Fail loudly" principle warns against, just in an environment (Claude Code hook script) outside version-controlled review.

## Lessons Learned

1. **Prompt caching can invalidate "fresh session" experiment designs.** When comparing two conditions across separate subagent/session dispatches that share a system-prompt prefix, check `cache_creation_input_tokens`/`cache_read_input_tokens` in the raw usage block *before* trusting the comparison — an exact match between one call's cache-creation count and another's cache-read count means the second call never actually saw the changed content. This should be a pre-flight check for any future "does changing X in a config/prompt file affect behavior" experiment via subagent dispatch, not a post-hoc diagnosis.
2. **Standing rules get sharper through live pushback, not first-draft phrasing.** The self-critique gate's "objections must be citable" clause only became non-trivial (i.e., resistant to ritual hedging) after the user pointed out ungrounded hedges were a loophole, prompting the three-category citability list (online source / prior lesson / live verification). First-draft rules in CLAUDE.md are a starting point, not the final form — expect to revise on the first real test.
3. **Fire-and-forget daemon threads in short-lived scripts need an explicit join with a bounded timeout**, or the process exit races the background work and silently drops it — confirmed empirically (0/3 before the fix, 3/3 after) rather than assumed from reading the code.

## Action Items

- [ ] Before designing any future subagent-based "does live file state X affect model behavior" experiment, first check whether prompt caching could mask the manipulation (same system-prompt prefix reused across calls) — plan for it rather than discovering it after the fact.
- [ ] When editing scripts that already run silently on every hook invocation (statusline, other hooks), treat any fire-and-forget background work (threads, unawaited async calls) as a suspect for silent failure and verify end-to-end (check the actual sink, not just "no exception thrown") before considering the change complete.

## Tips & Tricks for Claude Code

- **Tip**: For `curl` payloads with apostrophes, quotes, or other shell-special characters in the JSON body, default to writing the payload to a temp file and using `--data @file` rather than inline `-d '...'` — avoids shell-quoting breakage entirely instead of hand-escaping.
- **Tip**: To check whether two model calls (e.g. across subagents) actually saw different input content, diff `cache_creation_input_tokens` on the first call against `cache_read_input_tokens` on the second — an exact match is a strong signal of byte-identical cached reuse.

---

*Generated by `/reflect`*
