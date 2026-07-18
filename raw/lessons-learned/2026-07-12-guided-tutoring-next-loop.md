---
source: session-reflection
collected: 2026-07-12
published: Unknown
---

# Session Reflection: Codifying a Guide-Only Tutoring Loop

**Date**: 2026-07-12
**Session Goal**: Tutor a learner through a long series of incremental coding exercises — authoring tests and scaffolding skeletons per exercise, guiding rather than implementing, and advancing through the series with a repeatable workflow.

---

## What Went Well

- **Codifying the repeated cycle as a slash command.** The per-exercise cycle (verify current is green → archive it → scaffold the next skeleton → write its tests → update docs → report red/green) was turned into a single project-local slash command early. It then ran ~10 times cleanly. The deterministic file-management steps stopped being re-improvised each time.
- **Argue-out-before-locking for test expectations.** Writing a one-line "objection + resolution" comment above each test forced edge cases to surface before the expectation was committed (context nodes counted or not, boundary thresholds, attribution of nested constructs).
- **Surfacing genuine design forks to the user instead of guessing.** Twice the "right" approach was a real judgment call (which traversal idiom; how far to take a hard exercise). Presenting the tradeoff — with a recommendation — changed the outcome each time and was explicitly appreciated, versus silently picking one.
- **Grounding tool-specific claims in a reference, and disclaiming what the reference didn't cover.** When auditing code that used an SDK, the loaded reference didn't cover that exact SDK — saying so, and flagging its claims as "verify" rather than asserting, kept the audit honest.
- **Verifying tooling config empirically before documenting it.** A test-runner config change was run in all its modes before being written into the docs — which caught a real mis-collection (a "run everything" invocation silently dropping the active set).

## What Went Wrong

- **The scaffold-density bar took three corrections to converge.** How much of a skeleton to pre-fill vs leave blank was mis-calibrated initially (too sparse), then over-corrected, before settling. This is a genuinely user-specific preference that couldn't be assumed — but I should have asked for the calibration explicitly after the first correction instead of guessing again.
- **The same class of weak test recurred across multiple exercises.** A "does the program run" test repeatedly asserted a substring that appears in the output *regardless* of whether the core logic works (e.g. a name that shows up as a label either way). Caught reactively — twice — via self-critique, but it should have become a standing pre-lock check after the first instance instead of being re-derived each time.

## Lessons Learned

1. **Codify a repeated multi-step workflow as a command the moment it repeats.** A workflow that will run N times benefits enormously from being a single invocable unit with fixed steps — it removes per-iteration drift in the mechanical parts and lets attention go to the judgment parts (test design, scaffold calibration).
2. **A test that passes against an unimplemented stub is a smell, not a pass.** Every test should either fail against an empty/NotImplementedError stub, or be a *deliberately documented* no-op/exclusion guard. "Program runs and prints something" tests are the usual offender: assert an output feature that only appears once the logic works (a computed edge, a specific value), never a substring that's present either way.
3. **Surface genuinely-forked design decisions; don't silently resolve them.** When two approaches are both defensible and the choice materially changes the work, present the tradeoff with a recommendation. Users value the fork being made visible, and it avoids building the wrong thing well.
4. **The "right amount of scaffolding" for a learning skeleton is a calibration to elicit, not assume.** Carry forward established/boilerplate patterns; leave blank only the concept the exercise teaches. But where that line sits is per-user — after the first correction, ask rather than re-guess.
5. **Verify tooling/config behavior empirically before writing it into docs.** Config knobs interact in non-obvious ways; running each mode once surfaces the surprise before it becomes a documented lie.

## Action Items

- [ ] Adopt a standing pre-lock checklist for authored tests: for each test, confirm it fails against the stub, OR mark it explicitly as a documented guard case.
- [ ] For any "entry-point runs" test, assert a post-implementation-only output feature, never a label/substring present regardless of correctness.
- [ ] When a calibration-type preference (scaffold density, verbosity, format) draws one correction, ask for the target explicitly instead of guessing a second time.

## Tips & Tricks for Claude Code

- **Tip**: A slash command can encode an entire verify→archive→scaffold→document→report loop, keeping the mechanical steps identical across many iterations.
- **Tip**: A shared test fixture that derives the module-under-test path from the *test file's own name* removes per-file harness boilerplate entirely — new test files need zero setup code.
- **Tip**: To keep a fast focused test loop while retaining a regression net, exclude the archived/finished set from default collection (a recurse-exclusion config) and run it explicitly as a separate command. Don't pass both the active path and the excluded path in one invocation — exclusion configs mis-collect that shape.
- **Tip**: When loading a domain reference skill, check whether it actually covers the specific library in play; if not, downgrade claims to "verify against X's own docs" rather than asserting.

## Generalization Opportunities

- **Slash Command**: The per-exercise advance loop was already generalized into a project-local command this session — the highest-leverage artifact. The pattern (verify → archive → scaffold-with-carried-forward-boilerplate → author-discriminating-tests → sync docs → report) is reusable for any incremental, test-first tutoring or kata series.

---

*Generated by `/reflect`*
