---
source: session-reflection
collected: 2026-07-05
published: Unknown
---

# Session Reflection: Verifying a Connection-String Helper Leaked a Live Credential

**Date**: 2026-07-05
**Session Goal**: Give two services sharing one Postgres instance their own isolated schemas, after discovering they'd collided on the same default-schema table name.

---

## What Went Well

- **Row-count checks caught a live-service near-outage before it mattered.** After rebuilding and redeploying a service, checking actual row counts (not just "container is up") revealed the deployed code was stale relative to the new environment config, silently falling back to an empty data store. Caught and reverted within minutes because verification checked real data, not process status.
- **Inspected the target schema before trusting a migration script.** Before running data-copy logic against a shared database, listed its existing tables first — this surfaced a genuine name collision with an unrelated service's table (same name, completely different columns) before any write could silently corrupt it.
- **Treated each destructive action as needing its own confirmation**, including a second time when a materially identical situation recurred later in the same session — didn't treat an earlier one-time approval as blanket cover.
- **Verified through the real consumer, not just a raw query**, after moving data between schemas — called the actual application-level function, not just a count check.

## What Went Wrong

**Printed a live credential into the conversation while debugging.** To verify a small code change (a helper function that builds a database connection string, now scoping it to the right schema), the return value was printed directly to inspect its shape. That helper wasn't a pure string transform — with no override provided, it actively read a live password from disk and returned it embedded in the connection string. The full string, real password included, landed in the transcript.

The specific failure mode: minutes earlier, an analogous-looking helper had been tested the same way, safely — by deliberately feeding it a placeholder value first. But that first helper only ever echoed back whatever input it was given; it never resolved a secret on its own. The second helper had the opposite contract (resolves a live secret by default), and that difference wasn't re-checked before reusing the "just print it to see the format" habit from the safer case.

## Lessons Learned

1. **Before printing a function's return value purely to inspect its shape or formatting, check whether the function's contract is "pure transform of its input" or "resolves something live from an external source" (a secret store, an env var with a real default, a file on disk).** Two functions that look interchangeable in a debugging session can have opposite safety properties — confirming one is safe to print says nothing about the other.
2. **Name collisions on shared infrastructure aren't hypothetical — they show up on the very first real write.** Any service sharing a namespace (a database's default schema, a shared bucket's root prefix, a shared key-value store's default keyspace) with other services should get its own isolated namespace by default, checked before the first write rather than discovered via a downstream error.
3. **A one-time approval for a destructive action covers that specific instance, not every future occurrence of the same-shaped action**, even within the same session.
4. **Mechanical enforcement beats "be more careful next time."** The durable fix wasn't a mental note — it was an automated check (a hook that scans command output for credential-shaped strings and warns immediately) that catches this class of mistake regardless of which specific function produced it.

## Action Items

- [x] Add an automated output scanner that flags credential-shaped strings (connection strings with an embedded password, `KEY=VALUE` secret patterns) in command output.
- [ ] Before printing an unfamiliar helper's output "just to check the format," glance at its source once to see whether it resolves a live secret internally.
- [ ] Rotate the credential that was exposed in the transcript.

## Tips & Tricks for Claude Code

- Moving a table between schemas in Postgres (`ALTER TABLE ... SET SCHEMA`) is a metadata-only operation — no data copy, works even on a large already-populated table, and preserves indexes/constraints. Good for retrofitting namespace isolation after the fact.
- When multiple services share one datastore instance, scope each connection to its own schema/namespace explicitly in the connection config, rather than relying on the datastore's shared default.
- A quick "list what currently exists in the target namespace" check before running any migration/write script against shared infrastructure is cheap insurance against exactly this class of collision.

## Generalization Opportunities

- **Automated-check candidate (built this session)**: a general output-scanning check for credential-shaped strings — not tied to any one datastore or language, applicable to any debugging session where a helper's output might embed a live secret.
- **Pattern**: "every service on shared infrastructure gets its own namespace by default" generalizes across databases, object storage, message queues, and key-value stores alike.

---

*Generated by `/reflect`-style incident writeup (single-issue, not full session retro)*
