---
type: lesson
tags: [secrets, debugging, database, migration, namespace-isolation]
Title: Check a Helper's Contract Before Printing Its Output to Inspect Shape; Isolate Shared Namespaces by Default
Sources: Session reflection, 2026-07-05; Session reflection, 2026-07-06
Raw: "[../../raw/lessons-learned/2026-07-05-secret-print-during-debug.md](../../raw/lessons-learned/2026-07-05-secret-print-during-debug.md); [2026-07-06-worktree-guard-and-self-merge.md](../../raw/lessons-learned/2026-07-06-worktree-guard-and-self-merge.md)"
Updated: 2026-07-06
---

# Check a Helper's Contract Before Printing Its Output to Inspect Shape; Isolate Shared Namespaces by Default

Two habits from a session that gave two services sharing one Postgres instance their own isolated schemas — one a near-miss that leaked a live credential, one a save that caught a table-name collision before any write happened.

## Printing a Return Value to Check Its Shape Assumes the Function Is a Pure Transform

To verify a connection-string helper after scoping it to a new schema, its return value was printed directly to inspect the format — a habit that had just worked safely on an analogous-looking helper minutes earlier. That earlier helper only echoed back whatever input it was given; it never touched anything live. The second helper had the opposite contract: with no override supplied, it actively resolved a live password from disk and embedded it in the returned string. The full credential landed in the transcript.

Two functions that look interchangeable in a debugging session can have opposite safety properties. Before printing a function's return value purely to inspect its shape or formatting, check whether its contract is "pure transform of its input" or "resolves something live from an external source" (a secret store, an env var with a real default, a file on disk) — confirming one is safe to print says nothing about the other, even if it was tested the same way one command ago.

The durable fix wasn't a mental note for next time — it was an automated output scanner that flags credential-shaped strings (connection strings with an embedded password, `KEY=VALUE` secret patterns) in command output, catching this class of mistake regardless of which specific function produced it.

## Namespace Collisions on Shared Infrastructure Show Up on the First Write

Before running data-copy logic against a shared database, listing its existing tables first surfaced a genuine name collision with an unrelated service's table — same name, completely different columns — before any write could silently corrupt it.

Any service sharing a namespace (a database's default schema, a shared bucket's root prefix, a shared key-value store's default keyspace) with other services should get its own isolated namespace by default, checked before the first write rather than discovered via a downstream error. In Postgres specifically, `ALTER TABLE ... SET SCHEMA` is a metadata-only operation — no data copy, works on an already-populated table, preserves indexes/constraints — which makes retrofitting namespace isolation after the fact cheap once the collision is found.

## A Second, Milder False Positive: Flagging a Variable Name, Not a Value

A later session hit a lighter-weight version of the same false-positive class: a security-scanning hook flagged a code diff for a "credential-shaped string" warning because it pattern-matched on `key: value`-shaped text — but the actual match was an environment-variable *name* reference, not a real secret value. This class of false positive is worth recognizing on sight so it doesn't cause needless alarm, while still treating each individual warning as worth a second look rather than dismissing it reflexively just because a past instance turned out benign.

## See Also

- [Never Read Secret Values Into Agent Context](../conventions/never-expose-secrets-to-agent-context.md) — same secrets-exposure concern, applied to shell commands that read secret files/env vars directly rather than a helper function's return value
- [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](destructive-op-confirmation-and-background-jobs.md) — a prior approval for a destructive action covers that instance only, the same discipline this session reapplied to a second, materially identical case
- [Layer-Boundary Config Bugs and Staged Service Cutover](layer-boundary-configs-and-staged-cutover.md) — same "never fabricate/expose a live secret" concern plus a related staged-migration pattern for shared stateful infrastructure
- [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](worktree-liveness-check-before-destructive-cleanup.md) — from a later session; a secret-scan hook's false positives clustered around this same kind of security-adjacent code, reinforcing where such scanners need the most care
