---
type: lesson
tags: [verification, testing, environment-migration]
Title: Resolve Targets Directly, Don't Infer From a Manifest; Test Through a System's Own API, Not a Generic External One
Sources: Session reflection, 2026-07-12
Raw: "[../../raw/lessons-learned/2026-07-12-shell-migration-verification.md](../../raw/lessons-learned/2026-07-12-shell-migration-verification.md)"
Updated: 2026-07-12
---

# Resolve Targets Directly, Don't Infer From a Manifest; Test Through a System's Own API, Not a Generic External One

Two related verification failures share a root cause: checking a proxy for the real thing (a config manifest instead of a resolved binary; a generic external introspection API instead of the system's own action-triggering mechanism) produces confident-sounding answers that turn out wrong.

## A "will removing X break Y" claim needs a resolved-target check, not a manifest-listing check

An impact assessment claimed that switching an interactive shell would break a specific tool, based on a system PATH-config file listing a path for it. The claim was simply wrong — the tool's actual binary was provided by a different, unrelated PATH entry never checked. Config files and PATH dumps describe what *might* provide something; only directly resolving the real target ("where does this binary actually come from") confirms whether it currently does. This generalizes past shells: any "will changing/removing X break Y" question deserves a direct existence/resolution check on Y, not an inference from a related listing that merely mentions it.

## Test through a system's own API, not a generic external one

A new shell environment kept some of its state (environment variables, aliases) as live internal objects, converting them to conventional plain form only when the shell itself performed an action (spawning a process, resolving an alias by name). Probing that state through a generic external introspection API — bypassing the shell's own action-triggering mechanism — reported "missing" even though the real usage path worked fine, producing a false negative and an extra round of investigation before the test method itself, not the code, was identified as the problem. When a system defers syncing its live state into a conventional form until it performs its own actions, prefer testing through that system's own invocation surface over a bypass.

## Self-healing beats a bounded wait for legitimately detached background work

A background-thread-plus-lock-file pattern permanently stalled after the parent process exited mid-operation and the thread died before its cleanup step ran — the guard treated "lock file exists" as "still running," forever. This differs from a short-lived script's fire-and-forget thread (where the fix is a bounded join before exit): here the job is meant to legitimately outlive one process invocation, so a bounded wait isn't appropriate. The right fix is a staleness check on the lock itself — reclaim it after a timeout — so an interrupted run self-heals instead of permanently disabling the feature.

## Extract shared logic before porting

Pulling duplicated logic out into one standalone, environment-agnostic implementation before porting a helper/config between two shells or environments meant a later "stop duplicating this" cleanup was a small, low-risk edit instead of a second parallel implementation to hand-sync.

## See Also

- [Fire-and-Forget Background Threads in Short-Lived Scripts Need a Bounded Join](fire-and-forget-thread-needs-bounded-join.md) — the short-lived-process counterpart of the staleness-self-heal lesson above; see that article for the boundary between the two fixes
- [Verify a Credential's Environment and a Script's Own Safety Claims Independently](verify-environment-and-safety-claims.md) — same "don't trust a proxy signal, verify the real target" discipline in a database-safety context
