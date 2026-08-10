---
type: lesson
tags: [scoping, self-critique, debate, stop-signal]
title: Scope Drift in Open-Ended Debate Is Invisible From Inside the Accumulation
sources: Session reflection, 2026-08-10
raw: "[../../raw/lessons-learned/2026-08-10-schema-debate-scope-drift.md](../../raw/lessons-learned/2026-08-10-schema-debate-scope-drift.md)"
updated: 2026-08-10
---

# Scope Drift in Open-Ended Debate Is Invisible From Inside the Accumulation

A request to debate or scope a plan escalated step-by-step into implementing a large, unrelated feature — each individual step was locally justified, but the cumulative path never circled back to check whether it still served the original ask.

## Debate/exploration needs an explicit return-to-topic check

After resolving each sub-argument, restate "does this still serve the original ask" before continuing into implementation — especially when every individual step feels justified in isolation ("this is needed to demonstrate correctness," "the user asked for this specific fix"). Scope drift by accumulation can't be caught by vigilance at the start; it needs a periodic outside-view check repeated through the session, because each step looks fine locally right up until the cumulative path has left the original topic entirely. The user had to call this out more than once before it was addressed.

## A "no evidence found" conclusion is provisional, not final

Checking git log/docs before asserting something is right practice, but the check only covers what's already written down — real-world context the requester hasn't yet stated can overturn it. Hold a "no evidenced need" conclusion loosely enough to reverse it immediately once new facts arrive, without defending the prior position out of momentum.

## "Stop" means the next action, not "finish this step first"

When a user signals to halt, mid-task tidiness ("let me just finish this one edit for consistency") is not a valid reason to continue. The cost of stopping one step early is near zero; the cost of one more unwanted action after an explicit stop is not. Treat a stop/halt instruction as applying to the very next tool call, including mid-sequence.

## See Also

- [A Request Built on a False Premise Deserves a Correction, Not Silent Compliance or Refusal](false-premise-scoping-and-diff-before-git-reconcile.md) — same "provisional conclusion, verify before asserting" discipline, applied to premise-checking rather than scope-drift detection
- [A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope](guard-scope-vs-verbal-override.md) — related theme of a stated intent (here, a stop signal) not automatically covering every following action unless explicitly re-checked
