---
type: lesson
tags: [database, schema, audit, checklist]
Title: A Documented Default Path Is a Claim, Not a Fact — A Schema/Ingestion Audit Checklist
Sources: Session reflection, 2026-07-10
Raw: "[../../raw/lessons-learned/2026-07-10-schema-audit-verify-on-disk.md](../../raw/lessons-learned/2026-07-10-schema-audit-verify-on-disk.md)"
Updated: 2026-07-10
---

# A Documented Default Path Is a Claim, Not a Fact — A Schema/Ingestion Audit Checklist

Auditing a database ingestion schema surfaces a recurring shape of bug: something that reads as correct in code, and reads as correct in docs, but is only actually correct once checked against the live filesystem or the live table.

## A documented path is a claim, not a fact

When code has a default file path and a doc states a different one, neither is authoritative until checked on disk (`ls`, not a re-read of either source). The stale one silently breaks fresh setups — the file simply isn't there — and nothing in either source alone reveals which is right.

## Naive datetime into a `TIMESTAMPTZ` column silently shifts times

Parsing a UTC timestamp as timezone-aware and then stripping `tzinfo` before insert makes the database reinterpret it in the *session's* timezone. The bug is invisible whenever the session's timezone happens to be UTC, so it hides until it doesn't. Keep timestamps timezone-aware end to end; grep the producing code for `.replace(tzinfo=None)` or naive `datetime.now()` calls as suspects on any `TIMESTAMPTZ` write.

## `CREATE TABLE IF NOT EXISTS` is not a migration

It no-ops against an already-existing table, so any column added later inside the create statement never actually applies to a live database. A schema that will ever evolve needs an explicit, append-only `ALTER ... ADD COLUMN IF NOT EXISTS` list run alongside the create statement, not folded into it.

## Don't stack two backgrounding mechanisms

Launching a slow batch with a trailing shell `&` *inside* a harness's own "run in background" tool call makes the harness's tracker watch the wrong process (the launcher shell, which returns instantly) and fire a false "completed" notification while the real work — a separate PID — is still running. Pick one backgrounding mechanism; if polling is needed, wait on the real PID with an `until ! ps -p <pid>` loop.

## Supporting habits

- Read the whole schema surface (every module that touches the shared table) before judging, not just one file — cross-file issues (a column defined in one place, filtered in another with no index) only surface that way.
- Separate clear-cut bugs from judgment calls before acting; ask which to fix now versus which are scale-dependent improvements, rather than over-fixing a maintenance task.
- Cross-check a reported success count against the actual persisted state (`COUNT(*)`), not just the log line — `ON CONFLICT DO NOTHING` and similar constructs make "processed" and "stored" diverge silently.
- A secret-materialization guard blocking a `grep` of shell profiles/env mid-audit is usually a signal to remove the secret from the plan entirely — the audit rarely needs the value in context, only its name.

## See Also

- [macOS BSD sed Does Not Support \\b Word Boundaries](macos-sed-word-boundary.md) — same "always grep-verify after a scripted mutation, don't trust exit status" discipline
- [Verify a Credential's Environment and a Script's Own Safety Claims Independently](verify-environment-and-safety-claims.md) — same "verify independently, don't trust the tool's own claim" discipline for database write safety
