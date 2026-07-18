---
source: session-reflection
collected: 2026-07-12
published: Unknown
---

# Session Reflection: Verify Mutable State, Anchor to Existing Tools, Own Failures

**Date**: 2026-07-12
**Session Goal**: Build out a file-watch dev harness (run tests + auto-commit on save) and continue a guide-only tutoring series, advancing tasks via a repeatable command.

---

## What Went Well

- **Empirical probes before designing on an assumption.** Three times a design hinged on "does the platform/library actually behave this way?", and each time a 10-line probe settled it instead of a guess: (1) a single-file filesystem watch turned out to deliver **zero** events on the macOS backend (it silently watches directories only), which killed a "two separate file watches" design before it was built; (2) running the test-runner in a non-main thread was verified not to blow up on signal registration; (3) a green-gate was confirmed by pointing it at a known-RED target and watching it refuse. Cheap probe << expensive wrong design.
- **Reasoning through event ordering caught a race.** An "activate on config change" trigger was going to fire *before* the artifact it depended on was created. Walking the event sequence by hand surfaced it, and the fix was to make the activation write the *last* step (atomic "everything's in place" signal).
- **Naming the mechanization boundary explicitly.** When asked to "mechanize what can be done programmatically," I split the workflow into deterministic transforms (move/rename/flag files from existing state → scriptable) vs. judgment calls (authoring test expectations, naming things → not scriptable). That line kept the automation honest instead of over-promising.
- **Held the guide-only vs. implement line correctly per surface.** For the learner's exercises I explained/pseudocoded (LCA-by-identity, type-hint narrowing, line-length) without writing the solution; for the tooling I implemented. Same session, two modes, kept straight by *what file* was in question.
- **Reviewed a helper against a known code smell with a citation.** A user helper grew a boolean `reversed=` flag; flagged it as the flag-argument/boolean-trap smell and recommended caller-controlled direction over either a flag or a two-function split (which would've been WET).

## What Went Wrong

- **Asserted a fact from stale memory instead of reading the file.** Claimed a file was still listed in an ignore-file (making it "tracked-and-ignored") — but that line had been removed many turns earlier. The config file had *mutated during the session* and I was quoting an old copy. Reading the file took one tool call and flipped the conclusion entirely.
- **A response degenerated into token repetition** ("it it it it…" for dozens of lines) — a raw generation failure the user caught. Nothing to defend; the fix is to own it plainly and not paper over it.
- **The test-running approach churned through four shapes before landing.** In-process runner → reporting plugin → subprocess-with-captured-output → subprocess-streamed-live. The user eventually named the target ("basically like [the existing watch-test tool]"), which collapsed the remaining ambiguity instantly. I should have reached for the existing tool as the reference model *earlier* instead of iterating from first principles.

## Lessons Learned

1. **Re-read mutable state before asserting anything about it.** Config files, ignore files, and small state files get edited *during* a session (by the user or by tooling). Any claim about their current contents must come from a fresh read, not from a copy seen earlier — "I saw it 20 turns ago" is not "it says now." This is the single highest-value fix from the session: a stale assertion is indistinguishable from a hallucination to the user.
2. **Anchor an open-ended build to an existing tool's model early.** When a helper keeps mutating shape across iterations, stop and ask "what established tool already does roughly this?" — its behavior is a spec that collapses the design space. Iterating a bespoke thing from first principles is how you end up in a four-attempt churn the user has to pull you out of.
3. **Own generation failures and wrong claims flatly.** When caught degenerating or asserting something false, correct the record in one line without hedging or over-apologizing, then verify the true state. Defensiveness or manufactured confessions both waste the correction.
4. **A one-call probe beats a confident guess about platform/library behavior.** Filesystem-event granularity, threading/signal constraints, exit-code semantics — verify with a tiny script rather than reasoning from a possibly-wrong prior, especially before building a design on top of the assumption.

## Action Items

- [ ] Before stating what any config/ignore/state file contains, re-Read it that turn — never quote a remembered copy.
- [ ] When a self-authored helper reaches its 2nd–3rd reshaping, pause and name the closest existing tool as the target model before continuing.
- [ ] On any caught degeneration or false claim, immediately (a) acknowledge in one line, (b) re-derive from a live read, (c) move on — no defensiveness.

## Tips & Tricks for Claude Code

- **Tip**: To check whether a filesystem-watch design is even viable, probe event delivery empirically — some backends accept a single-file watch target silently but deliver no events (directory-granularity only).
- **Tip**: A green-gate ("refuse to proceed unless tests pass") is cleanly verified by running it against a *known-failing* target and confirming it refuses and changes nothing — a non-destructive test of a destructive operation.
- **Tip**: When a background/automation step depends on an artifact existing, make the "activate" signal the *last* write in the sequence, so anything reacting to it sees a complete state.

## Generalization Opportunities

- Nothing new to generalize into an artifact this session — the advance-loop command already exists; the mechanization work extended it rather than revealing a new reusable pattern. (Deliberately skipping a forced generalization.)

---

*Generated by `/reflect`*
