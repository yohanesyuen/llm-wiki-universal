---
type: lesson
tags: [agents, build, typescript, monorepo, parallel, testing]
Title: Parallel Agent Waves Need a Build Gate, Not Just a Type Check
Sources: Session reflection, 2026-06-30; Session reflection, 2026-07-06
Raw: "[../../raw/lessons-learned/2026-06-30-parallel-agent-build-gate.md](../../raw/lessons-learned/2026-06-30-parallel-agent-build-gate.md); [2026-07-06-worktree-guard-and-self-merge.md](../../raw/lessons-learned/2026-07-06-worktree-guard-and-self-merge.md)"
Updated: 2026-07-06
---

# Parallel Agent Waves Need a Build Gate, Not Just a Type Check

When parallel agents generate UI code across multiple files, three failure modes appear reliably at build time that are invisible to `tsc --noEmit`:

1. **`tsc --noEmit` ≠ `tsc -b`.** Project-references mode (`tsc -b`, used inside bundlers like Vite) is stricter than a flat type check. Errors caught only by `tsc -b` won't surface until the build runs.
2. **Agents write imports without verifying deps.** An agent that adds `import { X } from 'some-package'` rarely checks whether `some-package` is in `package.json`. The file looks correct in isolation; the build fails when the resolver can't find it.
3. **Style helpers get referenced instead of called.** A common agent pattern: generate `const getStyle = (arg: T): CSSProperties => ({...})`, then use it as `style={getStyle}` instead of `style={getStyle(arg)}`. TypeScript catches this at `tsc -b` but not always at `tsc --noEmit` on stale caches.

## Rule

A wave is not complete until the build is green, not until agents report done.

```bash
pnpm -r build   # or equivalent for your stack
```

## Agent-specific pre-flight checks

- **Before writing any import**: grep the relevant `package.json` for the package; add it if missing.
- **After generating style helpers**: grep new `.tsx` files for `style={[a-zA-Z]` to catch unreferenced functions.

## Why it matters

Each wave that skips the build gate pushes type errors downstream. Catching them per wave costs seconds. Catching them in CI or a remote deploy costs a full pipeline cycle.

## The same principle applies to the test suite, not just the build

Running only the tests for touched files misses regressions in sibling files. Adding a new loading-state label to one component collided with an existing test's regex assertion elsewhere, which started matching two elements instead of one — invisible if only the changed component's own test file had been run. Running the *whole* test suite (not just files changed in the current diff) surfaced this as a genuinely new failure, distinguishable from already-known, pre-existing unrelated failures.

**Rule**: after touching any shared text/label/string, run the full test suite, not just the file you changed — string-matching collisions in sibling test files are easy to miss otherwise.

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md) — same principle applied to single-agent build setup
- [Name the Capability Gap Before Evaluating New Infrastructure](capability-gap-before-infrastructure-eval.md) — verify actual state before declaring work done
