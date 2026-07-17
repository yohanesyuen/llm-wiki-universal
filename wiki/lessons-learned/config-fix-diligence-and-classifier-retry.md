---
type: lesson
tags: [safety-classifiers, config, hooks, telemetry]
Title: Verify a Settings Knob Covers the Real Mechanism; Disclose a Vendored Patch's Fragility Up Front; State a Telemetry Window
Sources: Session reflection, 2026-07-08
Raw: "[../../raw/lessons-learned/2026-07-08-hook-patching-and-classifier-retry.md](../../raw/lessons-learned/2026-07-08-hook-patching-and-classifier-retry.md)"
Updated: 2026-07-08
---

# Verify a Settings Knob Covers the Real Mechanism; Disclose a Vendored Patch's Fragility Up Front; State a Telemetry Window

Three separate diligence habits from the same session, each cheap and each avoiding a specific failure mode: verifying a config fix actually addresses the mechanism, disclosing a patch's fragility before being asked to automate around it, and stating a telemetry finding's time window alongside its count.

## "Is there a setting for this?" needs verification, not assumption

A settings schema can expose a plausible-looking field (e.g. something that gates a skill's visibility to the model) that does not cover a related-but-different mechanism (e.g. a plugin's own raw hook script, which runs unconditionally regardless of that field). Before promising a clean config-only fix, trace the actual code path that produces the unwanted behavior — reading the real implementation, not just the schema, is what avoided proposing a fix that wouldn't have worked here.

## Disclose a vendored-file patch's fragility before being asked to automate around it

Any patch that lives inside a plugin's install cache or another vendored/dependency location — rather than user-owned config — should come with an explicit, unprompted caveat that a future update will silently revert it, stated at the time the patch is made, not only after being asked to make it stick. If the user wants it durable, that means building (and round-trip testing both directions: already-patched no-ops correctly, freshly-reverted gets repaired) a self-healing check rather than relying on manual re-application.

## A telemetry-based finding needs its collection window stated alongside the count

"Zero invocations" is a materially different claim when the underlying log history spans four days versus four months. Any usage-count or telemetry-audit finding should surface the window size next to the number — and cross-reference raw counts against enabled/disabled state where relevant, since a large installed-but-currently-disabled surface isn't necessarily dead weight; it may be a decision the user already made.

## A safety-classifier denial is not necessarily final

When a tool call is blocked as a self-modification or similarly-flagged pattern, the right move is to stop, explain exactly what was being attempted and why, and let the human decide. If they respond with clear, explicit re-confirmation, retrying the identical action is reasonable and may succeed — these classifiers appear to weigh recent conversational context, not only the isolated command, so a single denial is not automatically a permanent wall. This nuances rather than contradicts a hard-gate framing: a `deny` still blocks the call every time it's evaluated as-is, but a genuinely re-confirmed retry is a *new* evaluation with different context, not a bypass of the same one.

## See Also

- [Passive Signals vs Hard Gates](passive-signals-vs-hard-gates.md) — the base framework this nuance applies to: what a hard gate is, and when a denial should prompt a scope/pattern fix rather than a retry
- [Hook Authoring Discipline](hook-authoring-discipline.md) — mechanics of the hook layer a vendored patch typically lives inside
- [Feature-Branch Git Workflow for AI-Assisted Development](../conventions/feature-branch-git-workflow.md) — covers the same session's PR-merge preflight discipline
