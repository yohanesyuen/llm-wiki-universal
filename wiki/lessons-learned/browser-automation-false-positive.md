---
type: lesson
tags: [browser-automation, false-positive, verification]
Title: Browser Automation False Positives Look Exactly Like Confirmed Bugs
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-hierarchical-status-rollup-tooling.md](../../raw/lessons-learned/2026-07-18-hierarchical-status-rollup-tooling.md)"
Updated: 2026-07-19
---

# Browser Automation False Positives Look Exactly Like Confirmed Bugs

An automated click followed by an accessibility-tree read showing no result is not proof a feature is broken — it's frequently a timing artifact of the automation itself, indistinguishable at the API/tree level from a real defect.

## What happened

An automated double-click, followed by an accessibility-tree read that showed no dialog, was reported as "the feature never opens at all." A user screenshot taken immediately afterward showed the feature rendering fine. The automated click almost certainly had a timing issue — but the finding was reported as fact rather than caveated as automation-derived and unconfirmed, costing a filed-then-retracted bug report.

## The fix is cheap: get independent confirmation first

Before filing a finding derived purely from browser automation as a real defect, either get an independent visual confirmation (a screenshot, a direct API response check) or explicitly label the finding "unconfirmed, automation-derived" in the first report. The cost of a retraction (re-filing, rewriting spec/tracker entries, walking back a claim) is consistently higher than the cost of one extra screenshot up front.

## See Also

- [Reason About the Worst-Case Node Before Running a Bulk Rollup; Search for Prior Art Before Building a Second Implementation](rollup-safety-reasoning-and-check-for-prior-art.md) — the session this lesson is drawn from
