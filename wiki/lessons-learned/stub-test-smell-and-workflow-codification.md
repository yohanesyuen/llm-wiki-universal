---
type: lesson
tags: [testing, tdd, workflow-automation]
Title: A Test That Passes Against an Unimplemented Stub Is a Smell; Codify a Repeated Workflow the Moment It Repeats
Sources: Session reflection, 2026-07-12
Raw: "[../../raw/lessons-learned/2026-07-12-guided-tutoring-next-loop.md](../../raw/lessons-learned/2026-07-12-guided-tutoring-next-loop.md)"
Updated: 2026-07-12
---

# A Test That Passes Against an Unimplemented Stub Is a Smell; Codify a Repeated Workflow the Moment It Repeats

Two independent, cheap habits compound over a long series of similar tasks: every authored test should fail against an unimplemented stub, and a multi-step cycle that will run many times benefits from being turned into a single invocable unit the first time it repeats, not the fifth.

## A test passing against a stub is not a pass

Every authored test should either fail against an empty/`NotImplementedError` stub, or be a deliberately documented no-op/exclusion guard. The recurring offender is a weak "does the program run" test that asserts an output feature present *regardless* of whether the core logic actually works — a label or substring that shows up either way. Adopt a standing pre-lock check: for each test, confirm it fails against the stub, or mark explicitly why it doesn't. Catching this reactively, twice, in the same session is a sign it should have become a standing check after the first instance.

## Codify a repeated multi-step cycle as a command immediately

A per-iteration cycle (verify current state green → archive it → scaffold the next skeleton → author its tests → update docs → report red/green) was turned into a single project-local command early, and ran cleanly roughly ten times afterward. This removed per-iteration drift in the mechanical steps and let attention go entirely to the judgment calls (test design, calibration). The trigger to act on is the first sign a workflow will repeat N times, not the Nth repetition itself.

## Two supporting habits

- **Argue-out-before-locking.** A one-line "objection + resolution" comment written above each test, before committing to its expectation, forces edge cases (boundary thresholds, whether a construct is counted) to surface before the expectation is locked in.
- **Verify tooling config empirically before documenting it.** A test-runner config change was exercised in every one of its modes before being written into docs, which caught a real mis-collection bug (a "run everything" invocation silently dropping the active test set) that reading the config alone would have missed.

## Tips

- A shared test fixture that derives the module-under-test path from the test file's own name removes per-file harness boilerplate entirely.
- To keep a fast focused loop while retaining a regression net, exclude the finished/archived set from default test collection and run it explicitly as a separate command — don't pass both the active and excluded paths to one invocation, which can mis-collect.
- When loading a domain reference for an audit, check whether it actually covers the specific library in play; if not, downgrade claims to "verify against the library's own docs" instead of asserting from a related-but-different reference.

## See Also

- [Parallel Agent Waves Need a Build Gate](parallel-agent-build-gate.md) — same "don't trust a partial signal as a pass" discipline, at the build/type-check layer instead of the individual-test layer
