---
type: lesson
tags: [database-migration, deployment, outage, defaults]
Title: A Destructive Live Migration and Its Matching Code Deploy Are One Atomic Unit
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-schema-migration-sequencing-and-real-data-preference.md](../../raw/lessons-learned/2026-07-18-schema-migration-sequencing-and-real-data-preference.md)"
Updated: 2026-07-19
---

# A Destructive Live Migration and Its Matching Code Deploy Are One Atomic Unit

Once a schema migration lands on a live database that a running service depends on, every minute before the matching code deploys is live-broken time. Treat the migration and its code deploy as one atomic unit of work, not two separate steps done in the same sitting.

## What went wrong

After running a schema migration directly against a live/shared database (with a proper data-preserving step, not blind), work continued in the same session — rewriting the service layer, tests, and frontend, running the full suite — *before* committing and pushing the matching code. The already-deployed server kept querying the column the migration had just dropped, so every request to that feature returned a server error for the whole gap between migration and push. The migration itself was fine; the sequencing around it was the bug.

## The procedural fix

Have the corresponding code fully written, tested, and staged *before* running the migration. Commit and push immediately after the migration succeeds — resist the urge to keep building or testing more in the same sitting first.

## Default to real data over synthetic placeholders

Separately, a mock-data preview page was underway when a correction arrived: use real, already-existing project data instead of synthetic placeholder data. A preview built against fabricated names/dates is far less useful for review purposes than one showing the actual thing being tracked. When real reference data already exists, default to using it — especially for anything meant to be reviewed by a human for accuracy — rather than waiting to be told.

## Check mutability before a batch of edits

Attempting to patch an existing record's field directly can hit a business-rule rejection (e.g. an immutability constraint from an unrelated, already-shipped feature) that applies to every record in a planned batch. Do one exploratory write first to confirm a target field is actually mutable, rather than discovering the constraint by trial and error across N records.

## See Also

- [Layer-Boundary Config Bugs and Staged Service Cutover](layer-boundary-configs-and-staged-cutover.md) — related theme of sequencing a cutover so nothing is left in a half-migrated state
- [Verify a System's Deeper Invariant Before Building On It; Validate a Debugger's Signal Against a Known-Good Baseline](verify-invariants-and-validate-debugging-signals.md) — same session-era discipline of verifying a third-party library's real output before trusting it as a source of truth
