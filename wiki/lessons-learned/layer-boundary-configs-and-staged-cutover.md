---
type: lesson
tags: [docker, networking, tls, migration, secrets]
Title: Layer-Boundary Config Bugs and Staged Service Cutover
Sources: Session reflection, 2026-07-04
Raw: "[../../raw/lessons-learned/2026-07-04-docker-nginx-auth-cutover.md](../../raw/lessons-learned/2026-07-04-docker-nginx-auth-cutover.md)"
Updated: 2026-07-04
---

# Layer-Boundary Config Bugs and Staged Service Cutover

Moving a homelab's reverse proxy, a stateful log store, and a self-built auth gate into Docker Compose surfaced two recurring failure classes — config assumptions that don't survive a layer change, and unilateral shortcuts around interactive tooling — plus one migration pattern worth reusing.

## Config Patterns Don't Survive a Layer Change on Their Own

A config rule proven safe in one context was ported into a different execution/network boundary without re-deriving whether it still holds, twice in the same session:

- **Wildcard TLS certificate depth.** A wildcard cert that covers one subdomain level does not cover a second level nested underneath it — most CAs (and browsers) reject wildcards deeper than one label. The same assumption almost recurred with a cloud provider's free-tier TLS coverage, which has the identical one-level limit. If a naming scheme wants to nest an identifier under a sub-path, collapse it into a single label up front rather than discovering the rejection at deploy time.
- **Loopback-only binding.** A "bind to loopback for safety" pattern copied from the *host's* Docker port-publish layer into the *container's own* proxy config broke the service entirely — inside a container, loopback is the container's own network namespace, not the host's, so the service became unreachable even through Docker's own port-forwarding.

Both were caught by live testing, not by re-reading the config carefully enough beforehand. The generalizable rule: anything that says "bind to X" or "wildcard covers Y" needs to be re-asked "X or Y *of what*, in *this* context" every time it crosses a network or execution boundary (host↔container, one CA↔another, one subdomain depth↔another) — don't pattern-match the previous fix.

## Never Fabricate a Placeholder Secret for a Live Account

An interactive password-reset command failed because the tool had no real terminal to attach to. The fallback taken was to pipe a self-chosen placeholder password rather than asking the user to supply one, or handing back the interactive command for the user to run themselves. The password was (correctly) flagged as compromised immediately after — but the right move was never to choose it unilaterally in the first place. When a credential-reset needs interactivity the tool doesn't have, hand the real interactive command back to the user rather than substituting a value "just to get through" the limitation.

## Treat "File Changed Externally" as a Mandatory Re-Read Trigger

Multiple times in the session, a system note indicated a config file had been restructured by another process or session mid-task. Each time required actively re-reading the file before continuing. In any session with concurrent agents/tools touching the same working directory, a stale in-context assumption about file contents is a real and recurring risk — treat the notice as a hard re-read gate, not an FYI to skim past.

## Staged Cutover Generalizes to Any Single-Writer Stateful Migration

For a stateful cutover (bare-metal process → container, without losing an internet-facing tunnel), the pattern that kept the live-traffic gap to a few seconds and left a free rollback path:

1. Validate the new (containerized) version against a *copy* of the data first.
2. Do the live swap: stop old → start new against the real data directory → repoint the downstream proxy.
3. Leave the old service disabled-but-present for a few days before final cleanup, instead of deleting it immediately.

This generalizes to any single-writer stateful service migration — databases, log stores, anything holding an exclusive file lock — because it isolates the unavoidable "gap" to one small step instead of spreading risk across the whole migration.

## See Also

- [Verify CLI Install Commands from Official Docs](verify-install-commands-from-docs.md) — same discipline of not trusting a remembered/copied pattern without re-checking it in the current context
- [Never Read Secret Values Into Agent Context](../conventions/never-expose-secrets-to-agent-context.md) — adjacent secrets-handling rule: don't expose real secrets to context; this lesson adds don't fabricate one either
- [Smoke-Test the Parts You Can](../conventions/smoke-test-parts-you-can.md) — same "verify with a real check, not just config review" principle applied to routing changes
- [Quarantine a Destructive Script the Moment Its Blind Spot Is Found](quarantine-destructive-scripts-immediately.md) — same "act on a discovered risk immediately" theme
- [Check a Helper's Contract Before Printing Its Output to Inspect Shape; Isolate Shared Namespaces by Default](debug-print-secret-leak.md) — same "don't expose a live secret" concern via a different vector (printing a helper's return value), plus a matching shared-namespace-isolation lesson
