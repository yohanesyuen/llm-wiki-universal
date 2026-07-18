---
type: lesson
tags: [frontend, bundle-size, library-migration, build-verification]
Title: Check Bundle Budget as Part of the Initial Library Comparison, Not After Implementation
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-bundle-size-verification-pluggable-fallback.md](../../raw/lessons-learned/2026-07-18-bundle-size-verification-pluggable-fallback.md)"
Updated: 2026-07-19
---

# Check Bundle Budget as Part of the Initial Library Comparison, Not After Implementation

When comparing candidate libraries for a migration, compare their real gzip bundle size against the project's own build-time size guard up front — alongside license and feature checks — not only after a full implementation is built and typechecked.

## The build, not the typecheck, is where this surfaces

A migration was fully implemented and passed a clean typecheck before a production build failed a pre-existing, intentional per-chunk gzip budget by roughly 4x. Typecheck and dev-server behavior gave zero signal about this; only running the actual production build revealed it. Any repo enforcing a bundle-size or bundling-tool guard needs that guard run before a migration is declared complete — checking it during the initial comparison phase, not as a post-hoc surprise, avoids a build-then-partial-revert round trip.

## When a guard fails, ask what it's protecting before touching its threshold

The instinct on hitting a failing size budget should be "is this guard telling me something true and important," not "raise the limit." Investigate whether the new dependency has any documented modular/tree-shakeable build option (check the package's own `files`/`exports` fields and its real GitHub build scripts — not just marketing copy, since a free/community tier often ships one monolithic bundle even when a paid tier supports modular builds) before concluding no lighter option exists. Report the concrete measured numbers to the user rather than resolving it unilaterally.

## A shared guard can gain a scoped exception without weakening globally

Rather than raising a global threshold or hardcoding a special case inside the guard's own logic, add an optional, keyed override map (e.g. a `chunkOverrides: Record<string, number>` matched against a chunk's filename) to the shared plugin. This keeps the guard's original purpose — catching accidental regressions everywhere else — fully intact while allowing one deliberate, documented, visible exception.

## Quick sizing check

`gzip -c <built-or-installed-bundle.js> | wc -c` (or `gzipSync(Buffer.from(code)).length` in Node) gives a fast, real, comparable size for two competing libraries before committing engineering time to a full migration of either.

## See Also

- [Toggle at the Bundler's Code-Splitting Boundary for a Reversible Migration](toggle-at-bundler-code-splitting-boundary.md) — same session, the follow-up "make it reversible" request
