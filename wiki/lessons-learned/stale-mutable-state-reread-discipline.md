---
type: lesson
tags: [stale-state, verification, live-editing]
Title: Stale In-Context File State Is Indistinguishable From a Hallucination — Re-Read Before Asserting or Editing
Sources: Session reflection, 2026-07-12; Session reflection, 2026-07-08
Raw: "[../../raw/lessons-learned/2026-07-12-verify-mutable-state-and-tool-anchoring.md](../../raw/lessons-learned/2026-07-12-verify-mutable-state-and-tool-anchoring.md)"; "[../../raw/lessons-learned/2026-07-08-live-coedit-sdk-explorer.md](../../raw/lessons-learned/2026-07-08-live-coedit-sdk-explorer.md)"; "[../../raw/lessons-learned/2026-07-08-settings-dedup-concurrent-edit.md](../../raw/lessons-learned/2026-07-08-settings-dedup-concurrent-edit.md)"
Updated: 2026-07-17
---

# Stale In-Context File State Is Indistinguishable From a Hallucination — Re-Read Before Asserting or Editing

Config files, ignore files, and small state files get edited during a session — by the user, by another process, or by an earlier step in the same conversation. Any claim about their current contents must come from a fresh read, not a remembered copy: "I saw it several turns ago" is not "it says now," and to the person reading the claim, a stale assertion looks exactly like a hallucination.

## Treat a "file was modified" notice as full invalidation, not a diff to patch

A partial diff shown via a system notification is not the whole file. When a live-edited file changes mid-session, the correct response is to fetch full authoritative state before the next edit — not to reason from the partial diff, and not to draft a rewrite before confirming the file has settled. Drafting first and re-reading only after a stale-write rejection wastes a round-trip that reading first would have avoided. The same applies to *analysis* built on top of a prior read, not just the next edit: re-run the underlying logic from scratch against fresh content rather than trying to diff-patch previous conclusions, since the concurrent edit may have already resolved the exact issue that analysis was about to flag.

## A quick post-edit validation check is cheap insurance

Running a syntax/structure check (e.g. parsing the file as JSON) after any structural edit confirms both "the edit applied" and "the file is still well-formed" in one shot — this matters more, not less, when another party might be editing the same file concurrently and interleaving changes.

## Anchor an open-ended build to an existing tool's model early

When a bespoke helper keeps mutating shape across several iterations (in one case: an in-process runner → a reporting plugin → a subprocess with captured output → a subprocess with streamed output, four shapes in a row), stop and ask "what established tool already does roughly this?" Its behavior collapses the remaining design space; the user naming an existing reference tool ended the churn instantly. Reaching for that anchor earlier avoids a multi-attempt churn the user otherwise has to interrupt to redirect.

## Own generation failures and wrong claims flatly

A caught degeneration or a false claim about file contents is corrected in one line — acknowledge, re-derive from a live read, move on. Neither defensiveness nor an over-apologetic response adds anything; both waste the correction.

## Distinguish confidently-subsumed redundancy from genuinely ambiguous cases

When cleaning up overlapping rules (e.g. permission allow-list entries), some redundancies are unambiguous under any reasonable reading of the matching semantics; others depend on an unconfirmed assumption about how matching actually works. Flag the ambiguous ones to a human rather than silently resolving them — the risk is asymmetric: removing something that wasn't actually redundant narrows what's auto-approved (a later surprise), while keeping something that is redundant is just harmless clutter.

## See Also

- [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](concurrent-session-shared-file-collision.md) — the multi-agent version of the same "re-sync on every externally-observed change" discipline
- [Session Tool Efficiency](session-tool-efficiency.md) — the complementary rule: skip a re-read only when nothing could plausibly have changed the file since the last read in the same session
