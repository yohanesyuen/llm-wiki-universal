---
type: lesson
tags: [shell, debugging, false-positive, xonsh]
Title: An "Is the Variable Still Defined" Check Proves Nothing If the Script Deliberately Deletes It
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-debugging-shell-rc-false-positives.md](../../raw/lessons-learned/2026-07-18-debugging-shell-rc-false-positives.md)"
Updated: 2026-07-19
---

# An "Is the Variable Still Defined" Check Proves Nothing If the Script Deliberately Deletes It

When a shell rc-file edit "isn't taking effect," check the actual observable side effect it was supposed to produce — not a proxy variable the script may deliberately clean up afterward.

## The false-positive pattern

A PATH entry was added to a shell config file, then tested by checking whether a temporary variable used to build that entry was still defined after the config loaded. But the config explicitly deletes that variable after use — a deliberate cleanup convention already used elsewhere in the same file. Checking for the variable's *absence* was therefore consistent with correct execution, not evidence of failure. This produced a wrong hypothesis ("the back half of the file isn't running at all") and led to an unnecessary bisection of the file by truncating it at different line numbers to find where execution supposedly stopped.

Before writing any diagnostic check against a script, look for cleanup statements (`del`, `unset`) that would make an "is it still defined" check meaningless — check for the real side effect the code was supposed to produce (e.g. the final contents of `$PATH` itself), not a variable that's intentionally transient.

## A second, compounding trap: nested-shell variable expansion

Testing via `interpreter -c "print($SOME_VAR)"`, invoked through a wrapper shell, let the *wrapper* shell expand `$SOME_VAR` before the target interpreter ever saw the string — producing a syntax error that looked like a bug in the target interpreter's parser, when it was actually the wrapper substituting its own unrelated environment variable inline. Write the test as a small file and have the target interpreter `source`/execute that file, instead of inlining variable-heavy code across a shell-wrapper boundary in a `-c` string.

## A related smell: DB-gated tests marked done

A checklist item marked `[x]` is not proof a test still passes, especially for tests gated behind an optional environment variable (so they're invisible to default CI). Those are exactly the tests most likely to silently rot after a schema/API migration, since nothing forces a re-run. Worth periodically spot-checking gated integration tests specifically, not just trusting their checkbox state.

## See Also

- [macOS BSD sed Does Not Support \b Word Boundaries](macos-sed-word-boundary.md) — a sibling case of a shell/tooling assumption breaking silently across environments
- [A Documented Default Path Is a Claim, Not a Fact — A Schema/Ingestion Audit Checklist](schema-and-ingestion-audit-checklist.md) — same "verify the observable state, not the assumed one" discipline
