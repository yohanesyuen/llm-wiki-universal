---
type: lesson
tags: [debugging, audit-logs, data-modeling, root-cause]
Title: A "Grant/Revoke" Field Must Be Derived From Both Sides of a Transition, Never One
Sources: Session reflection, 2026-07-17
Raw: "[../../raw/lessons-learned/2026-07-17-audit-log-classification-bug.md](../../raw/lessons-learned/2026-07-17-audit-log-classification-bug.md)"
Updated: 2026-07-19
---

# A "Grant/Revoke" Field Must Be Derived From Both Sides of a Transition, Never One

A boolean meant to describe a *transition* (grant vs. revoke, increase vs. decrease) has to be computed by comparing before-state and after-state together — deriving it from only one side is a classic, easy-to-miss bug.

## The bug shape

A permission-change audit log kept mislabeling no-op writes as `PERMISSION_REVOKED`. The root cause was a single-sided check: `isGrant = !existing || existing.accessLevel === 'NoAccess'`. This is correct only when the prior state happens to be the sentinel "no access" value — for every other case, including true no-ops, it silently evaluates the wrong direction. Any boolean that claims to describe a *transition* but is computed from only the "before" or only the "after" value should be treated as suspect on sight.

## The tell: a contradictory log entry

The bug was found by noticing something illogical in the log itself: entries recorded `PERMISSION_REVOKED` where `beforeJson` and `afterJson` held the *identical* value — a revoke that changed nothing. A repeated identical before/after pair in an audit or history log is a strong, general-purpose smell test for a classification bug in the write path, not a real event. If a logged "change" shows no actual change in its payload, the labeling logic — not the data capture — is almost always the culprit.

## Investigate live state before code

The original question ("why did user X get permission denied") had no answer derivable from static code reading. Querying the running system's actual account permissions and cross-referencing the audit history came first; reading the frontend/backend guard chain (route guard → hook → API call → backend guards → resolver) explained what *could* cause a denial, but only the live audit trail explained what *did* happen. For "why did X happen" questions, pull the audit/history log for the affected entity early — it's often the highest-signal source and can shortcut a multi-hop code trace.

## See Also

- [Flag Each Surprising Field Separately; Read the Real Interface Before Extending It](flag-fields-and-read-real-interfaces.md) — same session-era discipline of treating unexpected data as a signal to investigate, not dismiss
- [Verify a System's Deeper Invariant Before Building On It; Validate a Debugger's Signal Against a Known-Good Baseline](verify-invariants-and-validate-debugging-signals.md) — same theme of treating an anomalous signal as informative rather than noise
