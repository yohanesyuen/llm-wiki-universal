---
type: lesson
tags: [database, safety, verification, shell-scripting]
Title: Verify a Credential's Environment and a Script's Own Safety Claims Independently
Sources: Session reflection, 2026-07-17
Raw: "[../../raw/lessons-learned/2026-07-17-prod-db-safety-verification.md](../../raw/lessons-learned/2026-07-17-prod-db-safety-verification.md)"
Updated: 2026-07-17
---

# Verify a Credential's Environment and a Script's Own Safety Claims Independently

The first use of any write-capable credential, and the first run of any script that claims to be safe-by-default, both deserve an independent check before being trusted — neither a credential's apparent label nor a script's own success message is proof.

## Identify a credential's target environment before the first write

A database credential's environment (development vs. production) was not confirmed before the first write-capable test run against it. That should be the very first question the moment a usable write credential comes into scope — a one-line hostname check, never the credential's value itself — not something inferred later from side effects. Confirming it after the fact, once something looked off, required stopping and independently re-querying state to rule out unintended writes, rather than continuing.

## Verify a "nothing destructive happened" claim by independent observation

A cleanup script's whole purpose was proving a dry-run mode was safe by default. Its own printed success message was not proof — the dry-run flag itself was inverted by a shell-scripting bug (a boolean re-derived via a command-substitution idiom, then double-negated) that is invisible to code review and only surfaces by running the script and independently re-querying the state it claims to have left untouched. A separate read, a separate count, catches this; trusting the script's own log line does not.

## Pass boolean flags across a process boundary unchanged, not re-derived

A string variable holding `"true"`/`"false"` is safe to check directly. Re-deriving a *new* flag from it via a logical-OR/AND shell idiom before passing it to a subprocess is a second, independent point of failure that can silently invert the value — pass the raw string through unchanged instead.

## A documentation-sync task is worth treating as a bug hunt

Verifying docs against actually-running code (not just reading docs for internal consistency) surfaced a runnable guide that would fail against the real API, and a doc referencing a renamed model that no longer existed. The highest-value fixes came from checking docs against live behavior, not from proofreading in isolation.

## Recognize connection-pool exhaustion on sight

A specific database error pattern ("unable to start a transaction in the given time") indicates connection-pool exhaustion from too many concurrent transactions, not network failure — worth recognizing immediately rather than re-diagnosing from scratch, and worth checking for when a new required dependency means every isolated test-module setup for that service now needs it mocked (a runtime dependency-injection gap static type-checking won't catch).

## See Also

- [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](destructive-op-confirmation-and-background-jobs.md) — adjacent destructive-operation discipline
- [macOS BSD sed Does Not Support \\b Word Boundaries](macos-sed-word-boundary.md) — same "always independently re-verify after a scripted mutation, don't trust the tool's own exit status" pattern in a different shell-scripting context
