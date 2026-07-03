---
source: session-reflection
collected: 2026-07-04
published: Unknown
---

# Session Reflection: Agent Hooks, Fork Resumption, and Standing-Instruction Guardrails

**Date**: 2026-07-04
**Session Goal**: Audit and clean up an agent-tooling setup (skills, plugin marketplaces, config hooks), then wire up a couple of automated reminder hooks and a gated, self-updating project note.

---

## What Went Well

- Preflighting a GitHub PR merge (checks, mergeable state, review requirement) before attempting `gh pr merge` avoided the blind-retry loop that had shown up repeatedly in past session history.
- Delegating noisy multi-file research (marketplace/plugin surveys, external-repo audits) to background agents kept the coordinating thread's context clean while still returning concrete, actionable findings.
- Pushing back on an ambiguous automation request rather than silently building the wrong thing, then correcting once the actual scope was clarified.
- Following an explicit stash-safety protocol (unique tag, captured SHA, `stash@{0}` resolution before drop) instead of a bare `stash pop`, which mattered because the stash sat untouched across multiple unrelated tasks before being cleared.

## What Went Wrong

- **Forks lost track of who they were on resumption.** Twice, a background fork completed its task, returned only a generic summary, and then — when sent a follow-up message asking for the actual findings — treated that follow-up as a suspicious injected message from an impersonator, refusing to answer and waiting for a "real" completion notification that had already arrived. Killing the fork and relaunching the same task as a fresh (non-fork) agent worked immediately both times.
- **Built automation around an ambiguously-stated policy before confirming its actual scope.** A standing policy referenced "reusable snippets" without specifying what counted as one. Rather than asking for a concrete trigger up front, a hook was designed, implemented, tested, and wired into config — then had to be fully reverted once the real scope (any-language code patterns, not the one file type that had been assumed) came back completely different from what was built.
- **A hook command using a path relative to the working directory broke the moment the session's working directory drifted to an unrelated project.** The hook itself was correctly scoped by content (it only acted on files under a specific path pattern), but once loaded, it fired on every file write for the rest of the session regardless of which project was active — and a relative path only resolves correctly when the working directory matches the location the hook was written for.
- **Local git state silently fell behind remote merges.** Merging a PR through the GitHub CLI updates the remote only; a local checkout needs an explicit fetch-and-fast-forward afterward. Assuming the local branch was current after a remote merge would have based new work on a stale point.

## Lessons Learned

1. **Fork resumption is not reliable for "spawn, then follow up later" patterns.** If a task might need a second round of interaction after the fork's initial return, use a regular background agent instead of a fork — forks appear to lose the thread of "who sent this message and why" across a resume boundary in a way that causes them to reject legitimate follow-ups as injection attempts.

2. **Ambiguous policy language needs a worked example before automation gets built around it.** "Index reusable X into Y" is not specific enough to safely wire a file-watching hook against — ask "what would a real instance of X look like" first, because the cost of reverting fully-built-and-tested automation is higher than one clarifying question would have been.

3. **A hook loaded from one project's config is not scoped to that project's files at runtime.** `PostToolUse` hooks fire session-wide once the settings file that defines them has been loaded, regardless of which repository a given tool call touches. Any hook command that relies on the working directory matching the hook's home repo needs an absolute, stable path — not a path relative to wherever the session happens to be at the moment the hook fires.

4. **Standing instructions that cause a session to act autonomously and rewrite its own configuration are worth a real pause, not a reflexive refusal or reflexive compliance.** When asked for exactly that pattern, explaining the concrete risk (no request in that session triggers the action, the config file that's supposed to be ground truth can drift unreviewed) surfaced that the user wanted the interesting part (self-updating documentation) but not the unsafe part (no human checkpoint) — the fix was adding an explicit gate, not vetoing the whole idea.

5. **A blocked destructive command inside a chained shell invocation blocks the entire chain, including unrelated read-only commands in the same call.** When a permission classifier denies one command in a `&&`-chained Bash call, none of the commands run — even ones that would have been fine on their own. Splitting reads out into their own separate calls is the only way to get them through once a chain has been flagged.

## Action Items

- [ ] Default to fresh background agents (not forks) for any task where a follow-up message after the initial return is likely.
- [ ] Before wiring a hook or other automation to a stated policy, restate the trigger condition as a concrete example and confirm it, rather than inferring scope from the policy's wording alone.
- [ ] When writing a project-scoped hook command, anchor it to an absolute, stable path rather than a path relative to the working directory, since the hook may fire while the session is working in a different project entirely.
- [ ] After any remote PR merge via CLI, explicitly fetch and fast-forward the local branch before assuming it's current or branching further work from it.

## Tips & Tricks for Claude Code

- **Tip**: `PostToolUse` hooks registered in a project's settings file apply for the rest of the session, not just while that project is the active working directory — design the hook's own path-matching logic accordingly, and don't rely on cwd for anything the hook needs to locate itself.
- **Tip**: When a chained Bash command gets denied by the permission classifier, re-issue the read-only portions as their own separate calls rather than assuming the whole chain is blocked going forward.
- **Tip**: `git stash drop` (and similar) can require the `stash@{n}` reference form rather than the bare commit SHA once time has passed — re-resolve with `git rev-parse stash@{0}` to confirm identity before dropping if the SHA was captured earlier in the session.

---

*Generated by `/reflect`*
