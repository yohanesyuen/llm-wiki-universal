---
type: lesson
tags: [fact-verification, hallucination, self-critique, domain-facts]
Title: Statutory and Legal Figures Need a Live Citation, Not Recalled Confidence
Sources: Session reflection, 2026-07-17
Raw: "[../../raw/lessons-learned/2026-07-17-statutory-fact-hallucination.md](../../raw/lessons-learned/2026-07-17-statutory-fact-hallucination.md)"
Updated: 2026-07-19
---

# Statutory and Legal Figures Need a Live Citation, Not Recalled Confidence

A specific, confident-sounding statutory or legal number (an entitlement day-count, a rate, a threshold) is a distinct risk category from ordinary domain knowledge — it must be verified against a primary source at the moment of writing, not recalled from training data.

## Why this category is different

Architectural conventions and coding placeholders are fine to approximate and iterate on. Jurisdiction-specific regulatory figures are exact, change over time, and are trusted at face value by future readers (human or agent) precisely because they're written with citation-free confidence. A wrong number that's *directionally plausible* (in the right ballpark) is the most dangerous kind, because it doesn't trigger the "this seems off" instinct that an obviously wrong value would.

## A correction is a signal to sweep the whole cluster, not patch one item

When one figure in a table of related generated values gets corrected, treat that as evidence about all of them, not just the one flagged. In the case that produced this lesson, a single corrected leave-entitlement figure led to re-verifying every other entitlement in the same file — and caught two more wrong or mischaracterized values the user hadn't mentioned. Values generated together, in the same unverified pass, tend to fail together.

## The self-critique gate has to fire on artifacts, not just replies

A standing "objections must be citable" self-critique policy is typically framed around responses made *to the user*. This incident shows the same discipline lapses for facts written into code comments, seed data, or specs — those don't feel like "a claim to the user" in the moment of writing, so they slip past a gate that's only mentally applied to conversational turns. Any statutory/legal figure written into a durable artifact needs the same live-verification step before it's written, not just before a response is finalized.

## Practical pattern

Fetch the primary regulator's own page with a targeted request (e.g. "give the exact figures per the official table") rather than trusting a web-search summary — search snippets are often aggregator sites with stale or simplified numbers. Cite the source URL inline next to the value; this turns a static assertion into a self-documenting, future-checkable claim, and made it trivial on re-read to confirm which adjacent figures were fine and which weren't.

## See Also

- [Verify CLI Install Commands from Official Docs](verify-install-commands-from-docs.md) — same "verify against the primary source, not recall" discipline applied to a different domain
- [Calibrating When and How to Ask](calibrating-when-to-ask.md) — related judgment about when confidence should trigger a check rather than an assumption
