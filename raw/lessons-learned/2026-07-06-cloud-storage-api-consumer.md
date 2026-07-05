---
source: session-reflection
collected: 2026-07-06
published: Unknown
---

# Session Reflection: Building a Local Cloud-Storage API Consumer

**Date**: 2026-07-06
**Session Goal**: Find and download large files from a cloud Drive account, which led to building a durable local OAuth-based API consumer for Drive/Calendar/Gmail/Photos.

---

## What Went Well

- **Escalating only when the simple path actually failed.** Started with the built-in Drive connector tool; only moved to a custom OAuth client once it hit a hard 10MB download cap. Didn't over-engineer up front.
- **Verifying before trusting a "faster" alternative.** When told a locally-synced Drive folder might be easier than the API, checked disk usage (`du -h`) before committing — discovered it was a stream-mode virtual filesystem (`ls` shows real size, `du` shows 0B on disk), and a recursive `find` over it timed out. Avoided switching to a slower, riskier path based on a plausible-sounding suggestion.
- **Confirming destructive/irreversible-ish actions at the right granularity.** Before trashing cloud files, verified a byte-matching local copy existed first, and asked for scope confirmation (which files, which direction) rather than assuming "delete the files" meant everything everywhere.
- **Testing assumptions with a cheap probe before building on them.** Before assuming a cloud photo-library API could bulk-list all items, ran a one-off test call and got a clear 403 — confirmed a 2025 platform policy change before investing in a full scanning script that would never have worked.
- **Same probing discipline for delete capability**: instead of assuming a delete function existed (or didn't) based on documentation, directly probed the two most likely endpoints and got flat 404s — settled the question in one round-trip instead of guessing.

## What Went Wrong

- **First attempt at background delegation returned a placeholder, not real work.** Delegated a repetitive pagination task to a background sub-agent; its first "completion" message just restated the task description rather than reporting findings. Had to notice this looked wrong and explicitly re-prompt for the actual results.
- **A resumability gap shipped silently.** A checkpoint/resume feature for a long-running index build was written without persisting the actual pagination cursor — it looked correct (partial data was safely written) but a restart after interruption would silently redo all prior work. Only caught because the user asked directly "does it re-scan on interruption?" — this should have been verified proactively before calling the feature done.
- **A subtle unit/parameter bug produced plausible-but-wrong numbers.** Fetching file sizes for video items via a "download" URL parameter returned a thumbnail's size instead of the real file's size — the values were plausible on their own (small-but-nonzero) but wildly wrong, and only surfaced because the numbers looked suspiciously small compared to known video file sizes.

## Lessons Learned

1. **"Looks similar" data still needs its own permission/size check.** Two adjacent APIs (a general file-storage API and a media-library API) had different scope models — one restricted retroactively by policy, one lacking a features (delete) entirely. Don't extrapolate one API's capabilities onto a sibling API just because they're from the same platform.
2. **Plausible small numbers are a specific failure smell.** When a metadata field comes back non-null and non-zero but suspiciously small relative to expectation, that's a stronger signal of a wrong-parameter bug than an outright error would be — errors get caught immediately, quietly-wrong values slip through review.
3. **State a design decision's failure mode explicitly, don't wait to be asked.** "What happens if this is interrupted halfway" is a question worth answering unprompted for any long-running batch job with local persistence — the cost of stating it is one sentence; the cost of not stating it is a user having to ask and then a scramble to check.
4. **A sub-agent's own summary is not evidence of the work.** When delegating investigative work to a background agent, the returned "result" text should be treated as a claim until the underlying data is spot-checked, especially the first time a fresh agent instance reports back.

## Action Items

- [ ] When building any local cache/index with an incremental "resume" or "sync" mode, explicitly test the interruption path (kill mid-run, confirm resume point) before considering the feature done — don't wait for the user to ask.
- [ ] When a metadata/size value seems suspiciously round or small for the type of resource, sanity-check against a known example before trusting it, rather than only checking for outright errors.
- [ ] When delegating to a background agent for a well-defined enumeration/search task, treat the first returned summary as unverified until it contains concrete extracted data, not just a restatement of the assignment.

## Tips & Tricks for Claude Code

- **Tip**: `du -h` vs `ls -la` size mismatch is a fast, reliable way to detect a virtual/streaming filesystem before wasting time on a slow directory traversal.
- **Tip**: For platform APIs with ambiguous or deprecated capability boundaries (e.g. "does this scope still work for bulk reads?"), write a tiny one-off probe script rather than relying on documentation, which may be stale relative to policy changes.
- **Tip**: When a background/forked agent's task involves heavy pagination through a rate- or size-limited API, checkpoint progress in durable local storage (not just in-memory state) so a kill/resume doesn't have to start over — but verify the checkpoint is actually wired into the resume path, not just written.

---

*Generated by `/reflect`*
