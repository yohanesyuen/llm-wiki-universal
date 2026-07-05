---
type: lesson
tags: [api, verification, agents, planning]
Title: Probe Sibling APIs Directly; Plausible-Small Numbers Are a Bug Smell
Sources: Session reflection, 2026-07-06
Raw: "[../../raw/lessons-learned/2026-07-06-cloud-storage-api-consumer.md](../../raw/lessons-learned/2026-07-06-cloud-storage-api-consumer.md)"
Updated: 2026-07-06
---

# Probe Sibling APIs Directly; Plausible-Small Numbers Are a Bug Smell

Building a durable local API consumer surfaced four separable lessons: don't extrapolate one API's capabilities onto a sibling API, treat a suspiciously-small-but-nonzero value as a stronger bug signal than an outright error, state a design decision's failure mode unprompted, and never trust a sub-agent's first summary as evidence.

## Don't extrapolate capabilities across sibling APIs

Two APIs from the same platform (a general file-storage API and a media-library API) had different scope models — one was retroactively restricted by a policy change, the other lacked a capability (delete) entirely. Adjacent APIs under the same vendor umbrella are not guaranteed to share a permission or feature surface just because they look similar or share auth. Before building on an assumed capability, run a cheap, direct probe:

- Suspect a scope was revoked or narrowed by policy? Make one test call and read the status code rather than trusting documentation, which may be stale relative to policy changes (a bulk-list call returning a clean 403 settled a 2025 policy change in one round-trip).
- Suspect a capability (e.g. delete) doesn't exist? Call the most likely endpoints directly and read the response — two flat 404s settled the question immediately instead of guessing from docs.

This generalizes the "verify before building" instinct from [Pre-Flight Checks Before Building](preflight-checks-before-building.md) to API capability surfaces specifically, and pairs with escalating only when the simple path actually fails (starting with a built-in connector, only moving to a custom OAuth client once it hit a hard download-size cap; verifying a "faster" locally-synced-folder alternative with `du -h` before committing to it, which revealed a stream-mode virtual filesystem where `ls` shows real size but `du` shows 0B on disk).

## Plausible-small numbers are a stronger bug signal than errors

Fetching file sizes for video items via a "download" URL parameter returned a thumbnail's size instead of the real file's size. The values were individually plausible (small but nonzero) — nothing crashed, nothing errored — and only surfaced as wrong because they looked suspiciously small compared to known video file sizes.

**The smell**: a metadata field that comes back non-null and non-zero but suspiciously small (or otherwise off) relative to expectation is a *stronger* signal of a wrong-parameter bug than an outright error. Errors get caught immediately by normal error handling; quietly-wrong values slip through review because nothing failed. When a numeric or size-like field looks round, small, or otherwise "off" for the type of resource involved, sanity-check it against a known example before trusting it — don't only check for outright failures.

## State a design decision's failure mode before being asked

A checkpoint/resume feature for a long-running index build was written without persisting the actual pagination cursor. It looked correct — partial data was safely written on each step — but a restart after interruption would silently redo all prior work from the beginning. This was only caught because the user directly asked "does it re-scan on interruption?"

For any long-running batch job with local persistence, "what happens if this is interrupted halfway" is worth answering unprompted, in one sentence, the moment the feature is described as done. The cost of stating it upfront is one sentence; the cost of not stating it is the user having to ask and then a scramble to verify after the fact. Concretely: explicitly test the interruption path (kill mid-run, confirm the actual resume point, not just that some data was written) before considering a resume/sync feature done.

## A sub-agent's first summary is a claim, not evidence

A repetitive pagination task was delegated to a background sub-agent. Its first "completion" message just restated the task description rather than reporting findings — a placeholder dressed as a result. This was only caught by noticing the response looked wrong and explicitly re-prompting for actual results.

Treat a freshly-returned sub-agent summary as unverified until it contains concrete extracted data, not just a restatement of the assignment — especially the first time a given agent instance reports back on an enumeration/search task. Spot-check the underlying data before trusting the summary as done.

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md) — same "verify before building" instinct applied to package/model/environment compatibility instead of API capability surfaces
- [Name the Capability Gap Before Evaluating New Infrastructure](capability-gap-before-infrastructure-eval.md) — same escalate-only-when-necessary discipline, applied to infrastructure decisions rather than API client design
- [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](destructive-op-confirmation-and-background-jobs.md) — same re-confirm-before-destructive-action discipline, applied here to trashing cloud files only after verifying a byte-matching local copy and confirming scope
- [Fork Resumption Is Unreliable for "Spawn, Then Follow Up" Patterns](fork-resumption-follow-up-unreliable.md) — a related background-agent failure mode: forks rejecting legitimate follow-ups, versus this session's forked agent returning a placeholder instead of real work
