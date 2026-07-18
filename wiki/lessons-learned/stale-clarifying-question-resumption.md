---
type: lesson
tags: [clarification, context-tracking, status-drift, preference-persistence]
Title: A Rejected Clarifying Question Doesn't Stay "Live" Context Across a Topic Shift
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-stale-context-and-live-verification.md](../../raw/lessons-learned/2026-07-18-stale-context-and-live-verification.md)"
Updated: 2026-07-19
---

# A Rejected Clarifying Question Doesn't Stay "Live" Context Across a Topic Shift

Once a multi-choice clarifying question is rejected and the user pivots to a different framing, treat any later short back-reference ("the first one," "that one") as ambiguous by default rather than resolving it against the original menu — especially if several other substantive exchanges happened in between.

## What happened

A structured clarifying question was rejected by the user, who then gave a different, more general answer instead. Several turns later, after unrelated topics had been discussed, the user made a short back-reference. The reference was assumed to mean the first option from the *original rejected* question, and a feature started getting built around that stale context — going fairly deep before the user interrupted to say it had been misread. The actual ask was much simpler than what had been started. One clarifying question is cheap; several tool calls built on a wrong resolution are not.

## Status artifacts can drift independently of each other

When reconciling a stale progress-tracking file, the more-detailed task-checklist file wasn't trusted either — the actual code/schema on disk was checked to confirm a phase had genuinely completed. A more granular tracking file isn't automatically more trustworthy than a coarser one; both can go stale independently, and only checking real system state settles which is right.

## Stated-but-unpersisted preferences are a recurring gap

A user noted a formatting preference had been "stated repeatedly across sessions" — meaning it had never once been written into durable config or memory. Worth proactively checking whether a stated preference already exists in persistent storage whenever a user's phrasing implies repetition, rather than waiting to be explicitly asked to "make it permanent."

## Building and testing hooks properly

For two new lifecycle hooks, following a strict sequence — dedup check → construct → pipe-test with synthetic input → fix → validate JSON schema → live-fire proof → cleanup — caught a real bug: a warning message built via shell string concatenation embedded a literal two-character `\n` instead of an actual newline. The pipe-test surfaced this before it ever reached a live firing; JSON encoding alone can't catch this class of bug since it faithfully round-trips whatever bytes it's given.

## See Also

- [Calibrating When and How to Ask — Structured Choices Fit Stable Ambiguity, Not Unstable Intent](calibrating-when-to-ask.md) — sibling lesson on when a clarifying question is the right tool
- [Stale In-Context File State Is Indistinguishable From a Hallucination — Re-Read Before Asserting or Editing](stale-mutable-state-reread-discipline.md) — same "don't trust remembered state" theme applied to files instead of conversation
