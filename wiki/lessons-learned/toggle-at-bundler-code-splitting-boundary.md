---
type: lesson
tags: [frontend, bundle-size, feature-toggle, build-tooling]
Title: Toggle at the Bundler's Code-Splitting Boundary for a Reversible Migration
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-bundle-size-verification-pluggable-fallback.md](../../raw/lessons-learned/2026-07-18-bundle-size-verification-pluggable-fallback.md)"
Updated: 2026-07-19
---

# Toggle at the Bundler's Code-Splitting Boundary for a Reversible Migration

When a request says "make this reversible/toggleable" in a bundled frontend app doing code-splitting, put the switch at the exact point the bundler treats as a splitting boundary — for a lazy-loaded route, that's the dynamic `import()` call site itself, not a wrapper/selector component with two static imports.

## Why a generic if/else doesn't deliver the property

A runtime selector module that statically imports both candidate implementations and picks one via an if/else looks like it achieves the same thing, but it silently defeats the entire purpose of the toggle: a bundler can't safely tree-shake a side-effectful, CSS-importing module (or a library singleton's init code) just because its export goes unused in one branch. Both implementations end up pulled into the same chunk regardless of which is "selected" — the exact bundle-size isolation the toggle was meant to provide never actually happens.

## The fix: make the lazy-import line the switch

Pointing the toggle at the lazy-loaded route's single `import()` call guarantees the unselected implementation is never pulled into any chunk — no runtime branching or dead-code-elimination assumptions required, because the bundler's own code-splitting mechanics do the isolation for free.

## Verify both directions by actually building

Don't trust that the code "should" work both ways — build each configuration and read the reported chunk list to confirm the unselected engine's file is genuinely absent both times. Bundler tree-shaking behavior around side-effectful modules is easy to get wrong by inspection alone.

## See Also

- [Check Bundle Budget as Part of the Initial Library Comparison, Not After Implementation](bundle-budget-check-before-library-migration.md) — the same session's earlier lesson about measuring bundle cost before committing to a migration
