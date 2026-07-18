---
source: session-reflection
collected: 2026-07-17
published: Unknown
---

# Session Reflection: Doc-Sync Bug Hunting, Scope Creep, and a Production Near-Miss

**Date**: 2026-07-17
**Session Goal**: A documentation-sync task grew into real feature work and cross-cutting backend changes, including a production-database near-miss and a real bug in a safety-oriented cleanup script.

---

## What Went Well

- **Treating a "sync the docs" task as a bug hunt, not a copy-edit, caught real bugs.** Verifying documentation against the actual running code/schema (rather than just reading docs for internal consistency) surfaced a runnable quickstart guide that would 400 against the real API, and a doc referencing a renamed data model that no longer existed.
- **A one-line user aside about an edge case led to finding a real latent bug**, not just a spec gap — investigating "is this actually broken" (reading the real validation code, the real service function) instead of assuming the aside was purely hypothetical.
- **Verify-after-destroy habitually caught a real bug before it caused more damage.** A cleanup script with an intended "dry-run by default" safety mode actually had its dry-run flag inverted by a shell scripting bug. This was caught almost immediately because the habit was to independently re-query state after any action that touched a database, rather than trusting the script's own printed success message.
- **Stopping to verify environment identity, once something looked off, prevented compounding a mistake.** A stray clue revealed that a "local" database credential actually pointed at production, after several test runs had already used it. Rather than continuing, the session stopped and used targeted read-only queries to confirm no unintended writes had landed (a large concurrent-write stress test had, fortunately, never actually committed due to how the process was terminated).
- **A structured clarifying-question tool was used at a genuine decision fork**, not performatively — when a design decision had several real shapes, the question presented concrete tradeoffs instead of guessing and hoping.
- **Test-first discipline held under scope pressure.** When asked to do two separate pieces of cross-cutting work at once, the response was still: write the failing test first, confirm it fails for the right reason, implement, confirm it passes. This caught a dependency-injection wiring break in unrelated existing tests immediately, rather than as a later mystery failure.

## What Went Wrong

- **A credential's target environment wasn't verified before it was first used.** The first database-backed test run happened without first confirming whether the credential pointed at a development or production database — that should be the very first question the moment a usable database credential is in scope, not something discovered accidentally several steps later.
- **A safety-oriented cleanup script shipped with a real bug on first delivery.** A boolean dry-run flag was derived via a shell idiom that treated a string variable as a command and then double-negated the result before passing it to a subprocess — a bug that's invisible by code review and only surfaces by running it and independently verifying the claimed no-op actually happened.
- **A background test process was left hanging for several minutes** before recognizing the actual cause (a connection-pool exhaustion from too many concurrent database transactions) — the error message was a clear pool-starvation signal that could have been recognized sooner instead of first suspecting network connectivity.

## Lessons Learned

1. **Before using any credential for a write action, identify which environment it targets as the very first step — never infer it from side effects discovered later.** A one-line check of just the hostname (never the credential itself) before the first write prevents an entire detour of "did I just damage something."
2. **When a script's whole purpose is proving nothing destructive happens by default, verify that claim by independent observation — a separate read, a separate count — never by trusting the script's own printed message.** This single habit turned a real bug into a two-minute fix instead of an unnoticed mutation.
3. **Boolean flags passed across a process boundary in shell scripts should be passed through unchanged, not re-derived.** A conditional check on a string variable holding `"true"`/`"false"` is safe; re-deriving a *new* flag from it via a command-substitution idiom is a second, independent point of failure that can silently invert the value.
4. **A documentation-sync task is worth treating as a bug hunt.** The highest-value fixes came from verifying docs against actually-running code, not from reading docs in isolation.
5. **A specific database error message pattern ("unable to start a transaction in the given time") indicates connection-pool exhaustion, not network failure** — worth recognizing on sight rather than re-diagnosing from scratch each time.

## Action Items

- [ ] Before any test run or script execution using a credential from a local config file, explicitly state which environment it targets before proceeding.
- [ ] For any script with a dry-run/execute mode, write the independent verification step into the same turn as the first real test run, not as an afterthought.
- [ ] When passing boolean flags across a shell-to-subprocess boundary, pass the raw string through unchanged rather than re-deriving it with logical-OR/AND idioms.

## Tips & Tricks for Claude Code

- **Tip**: When a search tool fails unexpectedly and repeatedly for unclear reasons, don't retry the identical command — switch immediately to a different tool or approach (e.g. reading files directly, or a small script using a language's own file-walking primitives).
- **Tip**: For any cleanup/audit script touching data with foreign-key relations, keep the "what's safe to touch" diagnostic as a visually separate, explicit list from the "what will actually be touched" list in the script's own output — so a human skimming the terminal catches a wrong decision before it executes.
- **Tip**: When a service under test gains a new required dependency, every isolated test-module setup for that service needs the new dependency mocked — this is a runtime dependency-injection concern that static type-checking will not catch.

---

*Generated by `/reflect`*
