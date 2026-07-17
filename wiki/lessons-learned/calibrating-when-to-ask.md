---
type: lesson
tags: [clarifying-questions, disambiguation, design-forks]
Title: Calibrating When and How to Ask — Structured Choices Fit Stable Ambiguity, Not Unstable Intent
Sources: Session reflection, 2026-07-12; Session reflection, 2026-07-10
Raw: "[../../raw/lessons-learned/2026-07-12-guided-tutoring-next-loop.md](../../raw/lessons-learned/2026-07-12-guided-tutoring-next-loop.md)"; "[../../raw/lessons-learned/2026-07-10-clarify-and-verify-under-churn.md](../../raw/lessons-learned/2026-07-10-clarify-and-verify-under-churn.md)"
Updated: 2026-07-17
---

# Calibrating When and How to Ask — Structured Choices Fit Stable Ambiguity, Not Unstable Intent

A structured multiple-choice question is the right tool when the *referent* is unclear but the *goal* is fixed. It backfires when the user hasn't decided the goal yet, because it forces a premature commitment — the signal to watch for is repeated interruption of the same restated request.

## Repeated interrupts mean stop structuring, go smaller

When a user interrupts two or more times while restating the same request, that is a signal they are still forming the requirement, not that they want a faster answer. Presenting an N-way structured choice at that point crystallizes a decision that was still in flux — the user may pick an option and then immediately override it. The better response on the second interrupt is the smallest reversible move, or one open-ended question, letting them steer rather than committing to a menu.

## Structured disambiguation fits stable ambiguity

A multiple-choice is ideal when a bare deictic reference ("shouldn't this go under the parent?") has no attached selection and several concrete symbols/sections are plausible — the goal is fixed, only the referent is unclear. It is the wrong tool for exploratory/experimental requests where the goal itself is still shifting.

## Surface genuinely-forked design decisions instead of silently resolving them

Twice, the "right" implementation choice was a real judgment call with no objectively-correct answer (which traversal idiom to use; how far to push a hard exercise). Presenting the tradeoff with a recommendation, rather than silently picking one, changed the outcome each time and was explicitly valued — the fork being visible matters even when the user ultimately agrees with the recommendation.

## A calibration-type preference deserves an explicit ask after the first correction

How much of a skeleton to pre-fill vs. leave blank for a learner is a genuinely per-user preference that can't be assumed correctly on the first try. It took three corrections to converge in one case. After the *first* correction on this kind of calibration axis (density, verbosity, format), ask for the target explicitly rather than guessing a second time — re-guessing costs a second correction that asking would have avoided.

## Tips

- Use structural (AST) analysis, not text matching, to inventory code for a code-wide change — a plain grep for signature patterns misclassifies multi-line definitions, while an AST walk gives exact gaps and doubles as an after-the-fact completeness check.
- A dependency's type that can't be confirmed because it isn't installed in the current interpreter can still be annotated behind a `TYPE_CHECKING` guard at zero runtime cost — verify the import path once an interpreter with the dependency becomes available, rather than leaving the assumption open indefinitely.

## See Also

- [Ask for Domain Rules Before Deriving Proxies](../conventions/ask-for-domain-rules-before-proxies.md) — same "ask rather than infer" discipline, applied to domain/ordering rules instead of design forks
- [Named Size in a Spec Means Example, Not Constraint](named-size-means-example-not-constraint.md) — same "ask before implementing" discipline for a different kind of ambiguity
