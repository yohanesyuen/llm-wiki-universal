---
type: lesson
tags: [testing, dependency-injection, shell, incident-response, verification]
title: Mocked Tests Validate Logic, Not Wiring — Plus Habits From Root-Causing a Self-Inflicted Outage
sources: Session reflection, 2026-07-19
raw: "[../../raw/lessons-learned/2026-07-19-notification-worker-outage-rca.md](../../raw/lessons-learned/2026-07-19-notification-worker-outage-rca.md)"
updated: 2026-08-09
---

# Mocked Tests Validate Logic, Not Wiring — Plus Habits From Root-Causing a Self-Inflicted Outage

A provider/factory that constructs a real third-party client (a queue, a cache, an HTTP client, a DB pool) can be 100% correct in its *logic* while fatally wrong in its *construction arguments* — an invalid name, a malformed URL, a bad option. Mocked unit tests structurally cannot catch this: the thing whose construction is broken is exactly the thing the mock replaces. Every mocked test passed cleanly here; the bug only surfaced when a throwaway smoke test actually instantiated the real module (with fake config values) and the underlying library threw a hard construction-time error.

The consequence was real: the construction bug was found only in a *later* task via a deliberate instantiation test — meaning the *earlier* commit had already auto-deployed and crash-looped in production before the bug was even known. The mocked tests gave false confidence that the provider was correct.

**Standard extra step:** for any task that adds a component constructing a real external-library client, run a cheap "instantiate the real module" smoke test — even with fake environment values — as a required step, not an optional nice-to-have. A throwaway one-off test file (write it, run it, delete it) does this without committing scaffolding that doesn't belong in the permanent suite.

## Stop when a fix requires forcing a tool past a structural incompatibility

A module-format (ESM vs CommonJS) incompatibility in the test runner became a rabbit hole. Each config tweak *almost* worked, which made one-more-tweak tempting. The real stop signal was not a config gap — it was that the dependency's own source code contained a construct that structurally could not execute under the test runner's module wrapper. No transform configuration fixes a genuine module-format contradiction.

The correct fix (intercept at the module-resolution boundary and stub the module, rather than forcing the real thing to load) was simpler and safer than any "make it actually work" attempt — but required stepping back to see it. When a fix "sort of" works but needs a *second consecutive* tweak to keep working, treat that as the trigger to pause and get a second opinion, not to iterate a third time.

## A pipe hides the real exit code inside a shell `&&`-chain

`risky_command | tail -20 && echo done` prints "done" even when `risky_command` failed, because `&&` only observes the *pipe's last command's* exit code — `tail`'s, not the original command's. A type-check piped through a line-limiting filter reported success while the underlying command had actually failed.

When verifying that a build or type-check step succeeded — especially one that precedes a commit — check the exit code directly (no pipe), or use a shell that propagates `pipefail`. Do not read success through a truncating pipe.

## Root-causing an incident is a shrinking-search problem, not a single lookup

Jumping straight to "check the logs" shows whatever is *currently* healthy — almost never the state that was active during a past incident. The effective sequence narrows the search space step by step:

1. List all deployments with timestamps.
2. Correlate against known event times (e.g. your own commit/push times).
3. Narrow to the *specific* deployment active during the incident window.
4. Pull *that* deployment's logs by ID — not the current/latest stream, which is a different instance.
5. Search that log for error signatures.

Here this landed on an exact, quoted stack trace matching the bug already found and fixed earlier in the same session — primary-source evidence, not inference. When the evidence made authorship unambiguous, the honest move was to say plainly that an earlier commit caused the outage, rather than describe it as an unrelated platform blip.

## Verify a stale "already built" claim with a direct code search

A planning/spec doc claimed a shared piece of infrastructure "was already built" — a claim that gated other work. A direct code search before trusting it caught that the infrastructure genuinely did not exist yet. Prerequisite claims in planning docs are records of past belief; verify them against the actual codebase before building on them, especially when they gate ordering decisions.

## Tips

- When an MCP tool reports an authentication failure, try the equivalent CLI directly before assuming the whole capability is blocked — an MCP server and its CLI sometimes use different credential stores.
- Fetch a *specific* deployment's logs by ID from a deployment-history listing rather than relying on the default "latest deployment" stream.

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md) — checking the ESM/CJS exports map *before* choosing an output format is the up-front counterpart to recognizing a module-format dead end mid-debug
- [Green Static Checks Don't Prove the Code Ever Runs](green-checks-dont-prove-it-runs.md) — the same "a passing static gate says nothing about runtime" theme, from the same day's spec-toolchain session
