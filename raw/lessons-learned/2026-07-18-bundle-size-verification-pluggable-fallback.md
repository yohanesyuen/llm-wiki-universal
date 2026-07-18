---
source: session-reflection
collected: 2026-07-18
published: Unknown
---

# Session Reflection: Verifying Bundle Size Before Committing to a Library Migration, Then Making the Choice Reversible

**Date**: 2026-07-18
**Session Goal**: Migrate a UI component from one third-party rendering library to another (chosen for better native touch support), verify the migration end-to-end, and respond to a request to keep both options available going forward.

---

## What Went Well

- Before writing any migration code, verified the target library's version and license live (`npm view <pkg> versions`, `npm view <pkg> license`) rather than trusting recalled/training-data knowledge — caught that a recent relicense (GPL→MIT) had happened close enough to the knowledge cutoff that a stale answer could have gone either way.
- Read the target library's actual shipped TypeScript definitions and compiled bundle before writing integration code (event hook signatures, config shape, a zoom-extension's direction-of-effect) instead of guessing from memory or a README skim. Caught a real ordering bug this way — a zoom "zoomIn"/"zoomOut" pair whose in/out direction only became clear by reading the extension's actual increment/decrement logic, not by assuming the obvious naming convention was correct.
- After building the full migration and getting a clean typecheck, ran the actual production build rather than declaring success at typecheck. That build failed a pre-existing, intentional bundle-size guard (a per-chunk gzip budget) by roughly 4x — a fact that would have gone unnoticed without an end-to-end build, since typecheck and dev-server behavior gave zero signal about it.
- On finding the budget failure, did not quietly raise the limit to make the error go away. Investigated whether the new library had any documented way to ship a smaller/modular build (checked the npm package's exports, searched, and fetched the library's own GitHub repo/docs) before concluding no such option existed, then surfaced the concrete measured numbers (both libraries' actual gzip sizes) and asked the user how they wanted to proceed, rather than picking a resolution unilaterally.
- When the user's answer to "should we keep researching a lighter option" was "is there any way to build it smaller," treated that as a literal, answerable question — went back to primary sources (GitHub repo, docs) again rather than re-asserting the same conclusion, and got a clear negative answer before recommending reverting.
- When later asked to restore the abandoned migration but make it reversible, designed the "reversibility" mechanism around how the bundler actually behaves: a lazy-loaded route's dynamically-imported module is the unit of code-splitting, so making the *lazy-import line itself* the single switch point guarantees the unselected implementation is never pulled into any chunk — no runtime branching or dead-code-elimination assumptions required. This is a case of designing a "toggle" around a build-tool's real mechanics rather than around a generic feature-flag pattern that wouldn't actually deliver the bundle-size property it needed to deliver.
- Extended a shared, reusable build-time guard (a bundle-budget Vite plugin used across the whole monorepo) with a scoped, opt-in per-chunk exception mechanism, rather than either weakening the global default or hardcoding a special case directly in the plugin logic — kept the guard's original purpose (catching accidental regressions everywhere else) fully intact while allowing one deliberate, documented exception.
- Verified both sides of the finished toggle by actually building each configuration and reading the reported chunk sizes against their respective budgets, instead of trusting that the code merely "should" work both ways.

## What Went Wrong / Near-Miss

- The initial recommendation to migrate libraries had been made in an earlier part of the session based only on touch-support and license criteria — bundle size was never checked at that stage. It was only measured after a full implementation was already built, which meant real (if modest) rework: the migration itself turned out to be sound, but the decision to *ship it as the only option* had to be walked back once a concrete number appeared. Checking a "will this even fit the project's own constraints" question (bundle budget, in this case) before writing the integration, not just after, would have saved the build-then-revert round trip.
- A prior git-status check nearly conflated two unrelated things: an in-progress, deliberately-unmerged worktree/branch that had a legitimate reason to remain unmerged, and the general policy of flagging "stale" worktrees. The distinction (a worktree with no uncommitted changes and no open PR is not automatically "stale" if the project's own docs already say it's intentionally paused) needed to be checked against the actual git history (`log branch..base`, ahead/behind counts) rather than assumed from surface signals alone.

## Lessons Learned

1. **A production build (not just a typecheck) is where bundle-size and bundling-tool guardrails actually surface — run it before declaring a migration complete**, especially in a repo known to enforce a bundle-size budget. Typecheck and unit tests are silent on this axis entirely.
2. **When a build-time guard fails, the correct instinct is to ask "is this guard telling me something true and important" before touching the guard's threshold.** Widening a limit that exists specifically to catch this class of regression defeats its purpose unless the exception is deliberate, scoped, and visible — which is a different action than just bumping a number.
3. **"Is there a way to make X smaller" is a researchable, falsifiable question — answer it by checking the library's actual package structure/exports/repo, not by reasoning from general priors about what libraries "usually" support.** Got a clean, sourced "no" this time by checking the actual npm package contents and the project's GitHub docs, which made the revert-vs-continue decision much easier to make with the user.
4. **When asked to make a decision "reversible" or "toggleable" in the presence of a build tool doing code-splitting, design the toggle at the exact point the bundler treats as a code-splitting boundary** (here: the dynamic `import()` call site) rather than adding an abstraction layer on top — a generic if/else re-export wrapper around two statically-imported modules would have silently defeated the entire reason the toggle was requested (bundle-size isolation), since both branches would have been pulled into one chunk regardless of which was "active."
5. **A guard mechanism that's shared across a whole monorepo (a plugin used by multiple apps) can gain a scoped exception without weakening its coverage everywhere else** — adding an optional, keyed override map is a small, surgical change compared to either a blanket threshold increase or a one-off bypass hardcoded for a single app.
6. **A worktree/branch with no uncommitted changes, a remote copy, and no open PR is not automatically "stale"** — check whether the project's own documentation already explains why it's intentionally sitting unmerged before flagging it as needing cleanup.

## Action Items

- [ ] When evaluating a UI/rendering library migration, check the project's actual build-time constraints (bundle budgets, in this repo's case) as part of the *initial* comparison, not only after a full implementation is built and typechecked.
- [ ] When a request implies "make this reversible/toggleable" in a bundled frontend app, verify the toggle mechanism actually achieves the isolation implied (e.g., by building both configurations and reading real chunk sizes) rather than assuming a code-level if/else accomplishes it.
- [ ] Before flagging any worktree/branch as stale, check ahead/behind counts and open-PR status, and cross-reference the project's own docs for an intentional-pause note, before recommending cleanup.

## Tips & Tricks for Claude Code

- **Tip**: `gzipSync(Buffer.from(code)).length` (or just piping a built chunk through `gzip -c | wc -c`) against a library's raw compiled bundle is a fast way to get a real, comparable size number for two competing dependencies before committing to one — cheaper than instrumenting a full build for both.
- **Tip**: For "does this npm package support a smaller/modular build," check the package's own `files`/`exports` in `package.json` and its GitHub repo's real build scripts (not just the README's feature list) — a Community/free edition often ships one monolithic bundle even when other tiers of the same product support modular builds.
- **Tip**: For a lazy-loaded route in a Vite/Rollup-based app, the single dynamic `import()` call is the natural, bundler-respecting toggle point when a component needs a swappable implementation with mutually-exclusive bundle costs — simpler and more correct than a runtime selector module.

---

*Generated by `/reflect`*
