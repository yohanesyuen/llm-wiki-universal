---
source: session-reflection
collected: 2026-07-19
published: Unknown
---

# Session Reflection: Spec-Driven Dogfooding + Safe Speckit Toolchain Use

**Date**: 2026-07-19
**Session Goal**: Continue dogfooding a spec-driven project management tracker against its own project, fix real bugs surfaced by actually running a mobile app, and safely amend an existing far-along spec without destroying its hand-written history.

---

## What Went Well

- **Verifying claims empirically instead of trusting bundler/typecheck success.** A mobile app crash ("main has not been registered") was root-caused by actually starting the bundler and requesting a real bundle — `tsc --noEmit` and the test suite had both been green the whole time and would never have caught it, since the bug was a missing runtime registration call, not a type or logic error. The fix was verified the same way: grepped the compiled bundle for the actual registration call, confirmed absent before the fix and present after — not just "it typechecks now."
- **Checking a tool's actual write behavior before running it, not trusting its name.** Before running any of a spec-kit toolchain's "specify"/"plan"/"tasks"/"converge" commands, read each one's operating-constraints documentation directly. This caught that the "tasks" command does a full **template-based regeneration** of the task file (would have destroyed ~150 tasks of hand-written implementation narrative), while the "converge" command is explicitly "APPEND-ONLY, NEVER REWRITE." Two commands with adjacent-sounding purposes had completely different blast radii.
- **Backup + diff-against-backup as a cheap, repeatable safety net.** Before every manual edit to a spec/tasks/data-model document, copied the file to scratch first, then after editing ran a diff and counted removed lines. A `0` removed-lines count is strong, cheap evidence that an edit was a pure append/localized change, not a corrupting rewrite — did this several times this session and it caught nothing wrong, but the check itself is what made "nothing wrong" a verified fact rather than an assumption.
- **Asking scoping questions before writing a spec requirement, not guessing.** For a "planned vs actual" date-tracking gap, the task explicitly noted it needed requirement-level scoping (variance reporting? baseline snapshots? simple columns?) before a task could be written. Rather than picking one, asked the user directly — got "simple columns, auto-derived from status" in one round-trip instead of writing something that might've needed rework.
- **A backfill pass surfacing a documentation-vs-code drift bug for free.** While syncing a data-model doc's entity block (to add new fields), discovered the doc was already stale — missing an entire relation that a prior feature had shipped without updating the doc. Fixed it in the same edit rather than layering a new gap on top of an old one.

## What Went Wrong

- **A bash array loop misfired under a non-bash shell environment**, silently dropping one iteration without an obvious error. Recovered by checking actual state via API rather than trusting the loop's own output — but the root cause wasn't diagnosed, just worked around by switching to individual calls / a real scripting language for anything with control flow, per this environment's own standing "prefer composite scripts over chained shell commands" convention. Should have followed that convention from the start instead of after the fact.
- **Hand-rolled a shell loop to backfill data before checking for an existing script.** A reusable backfill script already existed in the repo (built in a prior session for exactly this purpose — idempotent, date-derived, handles duplicate ID disambiguation). Only discovered it after the user asked "isn't there a script?" — should have grepped for existing tooling before writing new one-off code, especially for a task the repo had clearly done before (multiple prior similar commits in git log).
- **A full dependency-directory wipe (needed to fix a stale module resolution) silently broke a sibling workspace** (a generated ORM client) because nothing regenerates it automatically on install. This wasn't caught until running a full monorepo-wide check — a reminder that "fix the thing I was looking at" isn't complete until adjacent/shared state is re-verified, not just the original symptom.
- **A commit-order heuristic for a task-dependency graph was proposed and applied to a live system before checking the actual spec docs and code for a real dependency.** The user's "yes, use that heuristic" was fair to act on, but it should have prompted a self-check ("do I have any actual evidence this reflects a real dependency?") before writing to the live tracker, not after. The follow-up "check spec docs/code" turn found the real answer (an explicit spec annotation) contradicted the guess entirely, requiring a revert.

## Lessons Learned

1. **A green typecheck/test suite proves the code is syntactically and logically consistent with itself — it says nothing about whether the code ever actually runs.** For anything with a real runtime entry point (a mobile app's root registration, a server's startup sequence), the only real verification is starting it and observing actual output, not just static analysis. A concrete instance this session: skipping the "actually run it" step would have shipped a completely non-functional app despite every check passing.
2. **When a spec/tasks document has accumulated a lot of hand-written narrative (post-hoc implementation notes, dogfooding history), treat any tool that "generates" that document as destructive by default until proven otherwise.** Read the tool's own operating-constraints documentation for the words "regenerate," "overwrite," or "append-only" before running it — the tool's *name* is not reliable evidence of its write behavior.
3. **"Use X approach" from a user is permission to try X, not evidence that X is correct.** When X produces a claim that will be written to a system others might read (a live tracker's dependency graph, in this case), a fast independent check against ground truth (the spec docs, the actual code) before or immediately after applying it catches wrong guesses before they propagate, cheaper than after a user has to point out the guess was groundless.
4. **Before writing new automation, check for an existing script — not just skim recent conversation for it, but actually search the repo.** This session had a working example of this failure and recovery within the same session: skipped the check once, got called out, then used the check-first pattern successfully for every subsequent similar task.
5. **A destructive operation on shared state needs a repo-wide verification pass afterward, not just a verification of the one workspace you were originally debugging.** The scope of "did this break anything" should match the scope of what was touched, not the scope of what was originally being investigated.

## Action Items

- [ ] When about to run any script/tool/skill that writes to a file, check the tool's own documentation for "regenerate"/"overwrite"/"template" vs "append"/"idempotent" before invoking — treat silence on this question as "assume destructive, verify before trusting."
- [ ] Before hand-rolling a script for a task that touches a project's existing infrastructure, search the repo for prior art first — "has this exact kind of task been automated before" is a cheap, high-value check.
- [ ] After any destructive dependency-directory reset in a monorepo, run a repo-wide check (typecheck/build/test across every workspace) before declaring the original fix complete — not just a check scoped to the workspace that motivated the action.
- [ ] Before applying a heuristic-based guess to live/shared state (not just proposing it), do the "check the actual evidence" pass first — reverse the order used this session (guess → apply → check → revert) to (check → guess only if evidence is absent → apply).

## Tips & Tricks for Claude Code

- **Tip**: A diff-against-backup with a removed-lines count is a fast, cheap sanity check that an edit was additive-only — use it as a standing habit whenever editing a file you've been told (or suspect) is fragile/high-value, not just when explicitly asked to be careful.
- **Tip**: When a package manager reports "already up to date" but you suspect broken linking, that message usually means the lockfile hash is unchanged — it does NOT mean the actual linked files are correct. A real reproduction (actually delete and reinstall) is the only way to verify a postinstall hook or linking behavior works, since a no-op install typically skips lifecycle scripts entirely.
- **Tip**: Structured clarifying questions are worth reaching for specifically at spec-scoping decision points (not just implementation-approach decisions) — "what should this requirement actually require" is exactly the kind of product decision that shouldn't be inferred from context, even when the inference would probably be reasonable.

---

*Generated by `/reflect`*
