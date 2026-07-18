---
source: session-reflection
collected: 2026-07-18
published: Unknown
---

# Session Reflection: Schema Migration Sequencing and a Real-Data-Over-Mock-Data Correction

**Date**: 2026-07-18
**Session Goal**: Extend a project-tracking feature's dependency model from a single-parent relationship to a genuine many-to-many one, in a live/continuously-deployed environment with a shared database.

---

## What Went Well

- Before building a "reusable" orchestration script that already existed, actually read it first rather than assuming it was generic — it turned out to be hardcoded to one specific past task (wrong OS path baked in, task IDs hardcoded), so building a genuinely parameterized version was the right call instead of reusing something that looked reusable but wasn't.
- When asked to integrate a third-party data library (holiday dates for a specific jurisdiction) as a source of truth, actually installed and ran it in a scratch directory to see its real output before wiring it into a code path, rather than assuming the library's data matched a previously-hand-verified reference set. This surfaced a real inconsistency in the library's own day-substitution logic before it became load-bearing.
- Followed a "specs before code" discipline for a nontrivial schema change (rewrote the design doc, the API contract doc, and a historical note in an already-closed adjacent spec) before touching the schema or the service layer — meant the documentation was never stale, even transiently.
- After a live-database migration broke the currently-deployed API (see below), diagnosed it correctly and immediately by hitting the actual live endpoint rather than assuming from the migration's own "success" output that everything was fine.

## What Went Wrong

- **The core failure**: after running a schema migration directly against the live/shared database (with a proper data-preserving step, not blind), I continued doing more work in the same session — rewriting the service layer, tests, and frontend, running the full suite — *before* committing and pushing the matching code. The already-deployed server kept querying the column the migration had just dropped, so every request to that feature returned a server error for the whole gap between migration and push. The migration itself was fine; the sequencing around it was the bug.
- I was, separately, mid-way through building a mock-data preview page when a correction arrived: use real, already-existing project data instead of synthetic placeholder data. This was a good catch on the requester's part — a preview built against fabricated names/dates is far less useful for review purposes than one showing the actual thing being tracked — but it's a preference I should default to without being told, given that real data was already available.
- Attempted to patch an existing record's field directly and got a hard rejection from a business rule I hadn't checked for first (an immutability constraint introduced by a different, already-shipped feature). Had to pivot to an alternative mechanism instead. Not a bug exactly, but time was spent because "can I edit this field" wasn't checked before attempting the edit.

## Lessons Learned

1. **A destructive-to-currently-deployed-code migration and its matching code deploy should be treated as one atomic unit of work, not two.** Once a migration lands on a live database that a running service depends on, every minute before the matching code deploys is live-broken time. The fix is procedural: have the code fully written and staged *before* running the migration, and commit immediately after the migration succeeds — not after continuing to build/test more things in the same sitting.
2. **When real reference data already exists, default to using it over synthetic placeholders**, especially for anything meant to be reviewed by a human for accuracy or usefulness — a preview/mockup against real content is a fundamentally more useful artifact than one against fabricated content, and this should be the default assumption, not something that needs to be requested.
3. **Check whether a field is mutable before batch-editing across several records, not per-record via trial and error.** A single failed attempt revealed a systemic constraint that then applied to every subsequent record in the same batch — worth a one-time check up front rather than discovering it once and then working around it repeatedly.

## Action Items

- [ ] Before running any migration against a database a live/deployed service depends on, confirm the corresponding code change is fully written, tested, and ready to commit — then commit and push immediately after the migration succeeds, before doing any further unrelated work in the same session.
- [ ] When building a preview, mockup, or demo artifact and real reference data exists in the system already, use it by default rather than generating placeholder data, unless there's a specific reason synthetic data is preferable (e.g. testing an edge case the real data doesn't have).
- [ ] Before scripting a batch of similar writes (e.g. edits across several records of the same type), do one exploratory write first to confirm the target field is actually mutable, rather than assuming and discovering constraints one failure at a time.

## Tips & Tricks for Claude Code

- **Tip**: When told to integrate a third-party library as a source of truth for domain data (dates, rates, reference tables), install it in a scratch directory and actually run it against the real inputs first — comparing its live output against any previously hand-verified reference is far more reliable than trusting the library's reputation or documentation claims alone.
- **Tip**: If an "existing reusable tool" is offered as a starting point, read it fully before reusing it — a script or workflow that looks generic at a glance can be hardcoded to a prior, unrelated task in ways only visible on inspection (a hardcoded path, hardcoded IDs), and reusing it as-is would silently fail or misbehave on the new task.

---

*Generated by `/reflect`*
