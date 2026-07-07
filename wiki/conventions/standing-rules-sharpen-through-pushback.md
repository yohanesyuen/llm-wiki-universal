---
type: convention
tags: [rule-design, standing-rules, iteration, self-critique]
Title: Standing Rules Get Sharper Through Live Pushback, Not First-Draft Phrasing
Sources: session-reflection, 2026-07-07
Raw: "[../../raw/lessons-learned/2026-07-07-cache-invalidated-experiment.md](../../raw/lessons-learned/2026-07-07-cache-invalidated-experiment.md)"
Updated: 2026-07-07
---

# Standing Rules Get Sharper Through Live Pushback, Not First-Draft Phrasing

Treat a newly-written standing rule (a CLAUDE.md addition, a self-check gate, a hygiene policy) as a starting draft, not a finished spec. Expect the first real test of it to expose a loophole, and revise the rule itself when that happens rather than just patching the one instance.

## Example

A self-critique gate rule required "citable objections" before agreeing with a plan or claim. In its first-draft form, "citable" was vague enough that a vague, ungrounded hedge ("there could be risks here") could technically satisfy it — which defeats the rule's purpose of preventing ritual hedging. The rule only became non-trivial after direct pushback pointed out the loophole, which led to a concrete three-category citability list (an online source, a prior recorded lesson, or a live verification performed in-session). The same session also refined a separate "CLAUDE.md bloat hygiene" rule the same way: from a declarative principle into a form that cites the specific real gap the pushback identified.

## Pattern

```
draft rule → apply it → pushback surfaces a loophole or edge case →
  rewrite the rule's own wording to close that loophole → re-apply
```

Both refinements in this example happened inside the same session the rule was introduced in — the gap between "sounds right on paper" and "survives a real test" can be immediate, not a slow drift discovered weeks later. Don't treat a rule as done once it's written down; treat it as done once it has survived being pushed on.

## See Also

- [Wiki Ingest and Cleanup Discipline](../lessons-learned/wiki-ingest-and-cleanup-discipline.md) — same "the first version is a draft, iterate on real use" pattern applied to wiki compilation rather than CLAUDE.md rules
