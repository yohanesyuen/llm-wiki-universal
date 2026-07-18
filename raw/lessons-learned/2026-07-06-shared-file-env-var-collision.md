---
source: session-reflection
collected: 2026-07-06
published: Unknown
---

# Session Reflection: A Shared-Config Rename Collision Between Two Concurrent Sessions

**Date**: 2026-07-06
**Session Goal**: Migrate a small backend service and its frontend to a new hosting platform, close a live unauthenticated-data-exposure incident found mid-migration, and add real per-user auth — while a second, independently-running agent session worked on the same repo in parallel.

---

## What Went Well

- On discovering a live data-exposure incident (an endpoint serving real personal data with no auth in front of it), stopped to flag the exposure and its severity before proceeding, rather than quietly patching it.
- Broadcast progress to the other concurrent session proactively at each milestone, and checked an inbox for replies before taking an action another session might already be mid-flight on (a stale-looking piece of infra state turned out to belong to that other session, confirmed by asking rather than assuming and overwriting).
- When a hand-rolled auth code sample (from an external source) had multiple real bugs — a non-existent auth endpoint, a malformed OAuth scope, a hardcoded fallback secret, no account allowlist check — reviewed it critically instead of wiring it in as-is, and explained each bug concretely before writing a corrected version.
- Verified cryptographic logic (JWT sign/verify round-trip, tamper rejection, wrong-account rejection) with a real local unit test before deploying it, rather than trusting that code "looks right."
- Repeatedly declined to guess at unverifiable infra details (a proxy's SSL mode, a specific hostname format) and asked instead of proceeding on an assumption — one of those guesses (a plausible-looking hostname pattern) was wrong and did cause a failed deploy, validating the caution applied elsewhere.

## What Went Wrong

- Two independently-running sessions both decided, at nearly the same moment, to fix the same shared config file (adding an environment-variable-backed secret check). Session A added it under one variable name; Session B (this session) had synced to an earlier version of that name and deployed against it moments after Session B renamed it — production went down (500s on every request) until the mismatch was found and fixed.
- The messaging channel used to coordinate between sessions worked, but only via manual polling — a reply from the other session didn't surface automatically at any point; a human had to relay it into context by hand. This meant repeated round-trips of "check for a reply" before the actual reply was available, and the collision above happened in exactly that polling gap.
- A "the other session has authority to act, you have control" delegation from the user, given in the middle of an active incident, was treated by an automated safety check as insufficiently specific to authorize a follow-on secret-store write — which was the right call in this instance, but meant an extra round-trip to get the same authorization restated in more specific terms.

## Lessons Learned

1. **A shared-file collision between concurrent agents is a coordination-protocol gap, not a speed-of-communication gap.** Faster message delivery would have shortened the window in which the collision could happen, but the actual fix is a claim-before-edit signal ("I am now touching this file, don't touch it until I say clear") — without that, two sessions can still collide even with instant delivery if they act within the same few seconds of each other.
2. **When two agents may be modifying the same shared resource, resync immediately after any externally-observed change to that resource, not just at the start of the task.** A system notification that flagged "this file changed since you last read it" was the actual signal that caught the rename — treating that kind of notification as a hard stop-and-recheck point avoided a second, deeper collision.
3. **A hand-rolled security-critical code sample from an external source is a review target, not a starting point to lightly edit.** All four bugs found in the sample (wrong endpoint, malformed scope, insecure fallback, missing allowlist check) were the kind that would pass a casual read but fail in production — worth a line-by-line pass against known-correct references before adapting, not just before running.
4. **"You have control" is not the same authorization as "do this specific irreversible thing."** Broad delegation language is useful for keeping momentum during an incident, but a safety gate that asks for the exact action to be named explicitly — especially for secret-store or DNS changes — is doing its job even when it costs a round-trip; the fix is to state the specific action back for confirmation, not to treat the broad delegation as sufficient on its own.
5. **A domain fronted by one edge proxy can still silently bypass that proxy for a specific record.** A wildcard DNS entry protected most subdomains via an existing gate, but a single subdomain had its own more-specific DNS record pointing straight at a different, ungated origin — more-specific DNS records silently override wildcard behavior, so a wildcard-level protection assumption needs verifying per-hostname, not assumed to cover everything under it.

## Action Items

- [ ] For any shared-file work between concurrent agents, treat "another session may edit this same file" as reason to re-read it immediately before writing, not just before starting the task.
- [ ] When delegated broad authority mid-incident, restate the specific destructive/secret-touching action back to the user for one-line confirmation before taking it, even if that costs a round-trip.
- [ ] Before trusting "this domain is protected because it's behind that gateway," check DNS per-hostname rather than assuming a wildcard/catch-all rule actually applies to the specific one in question.

## Tips & Tricks for Claude Code

- **Tip**: When verifying a signed-token (JWT-style) auth scheme, write three cheap local test cases before deploying: valid token round-trip, tampered-token rejection, and wrong-identity-but-validly-signed-token rejection. All three are fast to write and catch a different class of bug than "does it import."
- **Tip**: When a proxy/CDN sits in front of a serverless backend, check whether the backend's direct connection host is dual-stack — a serverless platform with no IPv6 egress will fail silently against an IPv6-only direct host, while a connection-pooler endpoint for the same backend is often the documented workaround and usually resolves dual-stack.

---

*Generated by `/reflect`*
