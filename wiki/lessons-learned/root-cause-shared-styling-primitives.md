---
type: lesson
tags: [ui, css, debugging, root-cause, testing]
Title: Root-Cause UI Bugs to the Shared Primitive Behind Them, Not the Symptom Where They Appear
Sources: Session reflection, 2026-07-06
Raw: "[../../raw/lessons-learned/2026-07-06-worktree-guard-and-self-merge.md](../../raw/lessons-learned/2026-07-06-worktree-guard-and-self-merge.md)"
Updated: 2026-07-06
---

# Root-Cause UI Bugs to the Shared Primitive Behind Them, Not the Symptom Where They Appear

Two UI bugs fixed in the same session both had a real fix one layer below where the symptom appeared — and in both cases, patching the visible symptom would have "worked" without addressing the actual defect.

## Contrast bugs: trace into the color-generation system, not the component

A "dark text on dark background" report led back to the actual tonal color-palette generation code, not the component rendering the text. The real defect was a tonal color system where two nearby tone values were both dark — one component was using a color token that was meant for light backgrounds, applied against a dynamically dark background. Patching the one component's hardcoded color would have fixed that one instance while leaving the same tonal collision live everywhere else the token was used.

## "Table doesn't reflow on mobile" bugs: check the flex ancestor before the table markup

A table that "doesn't scroll on mobile, it clips" already had correct scroll-wrapper CSS on the table itself. The actual bug was a missing `min-width: 0` on an ancestor flex container — a far more common but easy-to-miss root cause than the table markup, because flex children default to `min-width: auto`, which prevents them from shrinking below their content size and silently defeats an otherwise-correct `overflow-x: auto` wrapper further down the tree.

## The Generalizable Pattern

When a bug report describes something as "systemic across many places" (many components with a contrast problem, many tables that don't reflow), search for the shared styling/config primitive behind it — a design-token object, a shared utility class, a common style dictionary, a layout ancestor — rather than fixing each visible occurrence independently.

- **Contrast/color bugs**: check the token/palette-generation layer before touching individual component styles.
- **Clipping/overflow bugs in flex layouts**: check for a missing `min-width: 0` (or `min-height: 0` for column flex) on a flex ancestor before assuming the inner scroll-wrapper CSS is wrong — the wrapper is frequently already correct.

Root-causing to the shared primitive surfaces every affected spot in one pass and produces a more defensible fix than patching the symptom, even when the symptom-level patch would visually resolve the one reported instance.

## Verification note

Typecheck and build passing was not sufficient to confirm either fix — only an actual rendered screenshot via a browser automation tool confirmed the contrast fix displayed correctly. For visual bugs, budget for a real visual check, not just a green build.

## See Also

- [Parallel Agent Waves Need a Build Gate, Not Just a Type Check](parallel-agent-build-gate.md) — same "a green type-check/build is not sufficient proof" theme, applied to build correctness rather than visual correctness
