---
type: lesson
tags: [scripts, safety, session]
Title: Quarantine a Destructive Script the Moment Its Blind Spot Is Found
Sources: Session reflection, 2026-07-03
Raw: "[../../raw/lessons-learned/2026-07-03-corpus-cleanup-and-reindex.md](../../raw/lessons-learned/2026-07-03-corpus-cleanup-and-reindex.md)"
Updated: 2026-07-03
---

# Quarantine a Destructive Script the Moment Its Blind Spot Is Found

A one-off utility script that mutates a directory should be deleted or clearly quarantined the instant its blind spot is discovered — not just remembered.

## What went wrong

A batch of files had been hand-renamed to purpose-derived names. Later in the same session, a leftover automated rename script was run again against the same directory. Its naming logic had no awareness that files might already carry more-specific hand-given names, and it silently reverted a large batch of correct names back to generic auto-derived ones on its first post-rename run. The mistake was caught by re-diffing output, not by any warning from the script itself, then fixed by manually re-deriving the lost names.

The retirement of the script happened only as a later cleanup step. It should have happened the instant the blind spot was identified.

## The rule

"I'll remember not to run this" is not a control. An unused mutating script sitting next to live data is one wrong invocation away from repeating the damage — by the same session, a future session, or a different agent that doesn't have the context of why it's unsafe.

Prefer **deleting** a known-destructive script outright over leaving a warning docstring in place. A warning only protects a reader who opens the file first; deletion protects against every invocation path, including ones that never read the file at all (a glob, a `for f in *.py; do python $f; done`, a scheduled job).

If the script has ongoing value, quarantine it: move it out of the working directory, rename it with an unambiguous unsafe-marker prefix, or add an explicit guard clause that refuses to run against a directory containing already-processed markers.

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md) — same theme of checking before acting rather than discovering the failure mode reactively
