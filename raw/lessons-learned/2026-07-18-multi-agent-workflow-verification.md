---
source: session-reflection
collected: 2026-07-18
published: Unknown
---

# Session Reflection: Verifying Multi-Agent Workflow Output

**Date**: 2026-07-18
**Session Goal**: Orchestrate a multi-stage, TDD-gated, review-pipelined agent workflow to implement a moderately complex backend+frontend feature, then verify and ship it.

---

## What Went Well

- **Evidence-based pushback before building anything.** Before implementing a request that implied finer time granularity than the underlying data model actually stored, checked the real schema and the real UI capabilities first, then said plainly that the request rested on a false premise rather than faking a result that would silently fail.
- **Independent re-verification after a multi-agent workflow finished.** Instead of trusting a review-agent's self-reported "tests pass, security checks pass," independently re-ran the actual test suite and typecheck, and read the real diff to confirm a flagged critical finding was genuinely fixed. The numbers matched — but the discipline of re-checking, not the match itself, is the transferable habit.
- **Reused an existing project-specific orchestration policy** instead of inventing a new multi-agent pipeline structure from scratch — found a pre-existing document describing the exact TDD-writer → TDD-reviewer → implementer → code-reviewer gate sequence this project already used, and modeled the new workflow on it.
- **Diagnosed an unexpected concurrent-edit collision with concrete evidence** (process list, git commit metadata) rather than guessing, then confirmed via direct message to the other active process that there was no real conflict.

## What Went Wrong

- **A forked/delegated subagent got confused about its own role when resumed mid-task** and produced more confusion instead of useful output on a second nudge. Should have recognized the first confused reply as a signal to abandon that path and do the (cheap) task directly, rather than spending another round-trip trying to recover it.
- **Attempted a sensitive live-system command without asking first**, got blocked by a permission gate, then had to ask anyway — the extra round-trip was avoidable by asking up front given the command's known sensitivity.
- **A shell command failed on a JSON payload containing punctuation** (parentheses inside a string argument) due to shell parsing, rather than defaulting to writing the payload to a file first.
- **Subagents completed real implementation work but left bookkeeping (status tracking) unfinished**, which only surfaced because a downstream review step happened to flag it, and a related dogfooding step (using the new feature on the project's own tracking data) was missed entirely until pointed out.

## Lessons Learned

1. **A subagent's self-report is a claim, not a verification.** Even with a review stage built into the pipeline, the orchestrating session should independently re-run the actual verification commands and read the actual diff for any flagged critical finding — especially when everything reportedly passed, since that's when it's easiest to skip the check.
2. **Treat a confused reply from a resumed forked subagent as terminal, not as something a clarifying nudge fixes.** A fork inherits full context, which can bleed ambiguity from the parent conversation into a confused "who am I" response. For cheap tasks, cut losses after one confused reply and do the task directly.
3. **Concrete process/history evidence (not assumption) is the right way to diagnose an unexpected concurrent-edit collision** in a shared working environment — turning "something changed unexpectedly" into a specific, checkable claim lets a human resolve it in one step instead of several rounds of guessing.
4. **Self-applying a newly built capability to the project's own tracking/meta-data should be a scripted step of the workflow, not a separate manual follow-up** — it's an easy thing to miss once the "real" feature work is done.

## Action Items

- [ ] Default to writing JSON/shell payloads containing punctuation to a scratch file before invoking them via a command-line tool, rather than inlining and risking shell-quoting failures.
- [ ] Before attempting any command against a known-sensitive live system, ask for confirmation up front rather than attempting and hitting a permission block first.
- [ ] When authoring subagent prompts in a multi-stage workflow, explicitly instruct implementer/fix-stage agents to update any relevant status/tracking artifact themselves, rather than relying on a later reconciliation pass.

## Tips & Tricks for Claude Code

- **Tip**: Process-list plus version-control metadata inspection is a fast, concrete way to confirm whether a surprising change came from a real concurrent process versus your own prior action.
- **Tip**: A direct message to another live process/session (where such messaging is available) can resolve "is this a real conflict" ambiguity in one round trip, faster than inferring intent from diffs alone.
- **Tip**: When a workflow orchestration tool logs each stage's structured return value, reading that log directly (rather than raw per-agent output) is a fast way to spot a real finding worth surfacing mid-run, before the whole run completes.

---

*Generated by `/reflect`*
