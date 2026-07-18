---
source: session-reflection
collected: 2026-07-18
published: Unknown
---

# Session Reflection: Trusting Mutating Tools, and Detecting Silent State Drift

**Date**: 2026-07-18
**Session Goal**: A chain of routine maintenance tasks in a monorepo (test flakiness, coverage gaps, doc tooling) surfaced two unrelated but structurally similar incidents: a script silently destroying hand-curated content, and a schema change landing in an unintended place.

---

## What Went Well

- **Root-causing over patching a flaky test.** Before changing a timeout, I measured actual latency in isolation and under load, confirmed the bound in question was a test-harness artifact rather than a real regression against the underlying requirement, and left a comment distinguishing the two so a future reader wouldn't mistake a wider CI margin for a relaxed real requirement.
- **Diffing after a mutating tool reports success, instead of trusting the message.** A doc-refresh script reported success; diffing its actual before/after revealed it had silently deleted a large block of hand-curated content that happened to be sitting inside the region it was designed to fully replace. Catching this before committing was the single highest-value moment of the session.
- **Using pickaxe search (`git log -S`) to find the exact origin of an unexpected change**, rather than guessing. This turned a vague "why is this here" into a concrete, citable finding.
- **Searching prior session history to establish an actual root cause** rather than speculating about one — confirming the real mechanism (one long session doing two sequenced pieces of work back-to-back) instead of assuming a tooling bug.
- **Verifying a live system's actual state directly, rather than trusting a file-level diff's implications.** An assumption that a change was "just inert declarative text" turned out to be wrong once the live system was checked directly — which reversed the recommended fix entirely.

## What Went Wrong

- **Ran an unfamiliar tool with a destructive-by-design contract without reading that contract first.** The tool's documentation stated plainly that it replaces an entire managed region rather than patching it; running it first and only checking the diff afterward worked out, but reading the contract beforehand would have caught the risk before it existed.
- **Misread a database query result as a negative** because it queried an ORM's declared model name rather than the ORM's actual mapped table name — a false negative that would have led to the wrong fix had it not been caught by a broader sanity check.
- **A first fix for a missing-dependency problem was session-local, not durable** — it solved the immediate blocker but had to be redone properly once a future-proof version was requested.

## Lessons Learned

1. **A tool's own success message describes intent, not effect — for anything that mutates shared/durable state, verify the actual before/after rather than trusting the printed confirmation.** This matters most for any tool whose contract is "replace a whole block/file" rather than "append" or "patch," since that class of tool has no partial-failure signal — it either fully replaces, or fully fails, with nothing in between to catch a mistake mid-way.
2. **When two pieces of work coexist in one long working session — one deliberately isolated, one not — the isolation only holds if commit-boundary discipline is applied everywhere, not just in the isolated part.** The actual mistake happened on the *unrelated* side, not the isolated one. Long sessions are exactly where this kind of context-tracking silently erodes.
3. **A live system's actual state and its tracked history can drift in either direction, and the correct fix depends entirely on which direction it went.** Two drift patterns can look superficially identical but require opposite remedies — always check the live state directly before deciding which way the drift runs.
4. **Multiple parallel status-tracking mechanisms for the same fact are not redundancy — they're independent chances for exactly one of them to go stale while the others update.** Every drift incident in this session traced back to exactly one tracker not being updated in lockstep with the others.

## Action Items

- [ ] Before running any unfamiliar script that mutates shared files, read what it *writes* and how (append vs. replace) before running it — not just what it's for.
- [ ] When checking whether an ORM-declared entity "exists" in a live database, resolve the ORM's actual mapped name first, rather than querying by the model's declared name.
- [ ] Default fixes for tooling/dependency gaps to a durable, scoped location rather than a session-local workaround, unless durability genuinely doesn't matter for the task.

## Tips & Tricks for Claude Code

- **Tip**: `git log -S"<literal string>" -- <path>` pinpoints the exact commit that introduced or removed specific text in a file's history — faster than bisecting or eyeballing full diffs when you know *what* changed but not *when*.
- **Tip**: `git branch --merged <target>` is a fast, unambiguous check for whether a branch was actually merged — more reliable than comparing file contents by eye, since identical-looking content doesn't always mean an actual merge happened.
- **Tip**: For any ORM with explicit table/column mapping, always list all real tables first when unsure whether a feature's data exists — querying by the ORM's declared model name can silently return a false negative.

---

*Generated by `/reflect`*
