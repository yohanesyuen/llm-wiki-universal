---
Title: Hook Authoring Discipline
Sources: Session reflection, 2026-06-29; Session reflection, 2026-07-04
Raw: "[../../raw/lessons-learned/2026-06-29-hook-authoring-discipline.md](../../raw/lessons-learned/2026-06-29-hook-authoring-discipline.md); [../../raw/lessons-learned/2026-07-04-agent-hooks-and-guardrails.md](../../raw/lessons-learned/2026-07-04-agent-hooks-and-guardrails.md)"
Updated: 2026-07-07
type: article
---

# Hook Authoring Discipline

Lessons from wiring a PreToolUse wiki-index-lookup hook and a Stop corrections-detection hook into Claude Code settings — covering portable path resolution, memory scoping, hook event migration, and the distinction between memory and wiki as knowledge destinations.

## What Went Well

- Pipe-tested the hook script before wiring it into settings — zero integration bugs at the point of wiring.
- When moving a hook between event types, caught all three required changes in one pass: the event key in settings, the `hookEventName` in the script output, and the stdin payload field references.
- Validated settings JSON with `jq -e` after each edit.

## What Went Wrong

- **Hardcoded home directory on first draft**: The script embedded an absolute path containing the home directory. Hook scripts are reusable artifacts and must use portable path resolution from the start, not after correction.
- **Wrong implementation language**: Wrote the hook in bash when Python was preferred. Implementation language preference should be checked before drafting.
- **Memory scoped to CWD**: Saved a feedback lesson to the project-derived memory path (only loads when that directory is the CWD) instead of the explicitly configured user-scoped memory directory.
- **Bypassed wiki ingest for a generic lesson**: Wrote the feedback item straight to memory rather than deferring to the reflect → ingest flow. Generic corrections belong in the wiki.
- **Privacy violation in first draft**: The initial raw reflection draft for the public wiki included the literal home directory path containing the username. Public wiki content must be fully sanitized — no usernames, no absolute paths.

## Lessons Learned

1. **Portable paths in hook scripts**: Use `Path.home()` in Python or `$HOME`/`~` in shell. Never embed an absolute home path containing a username. Apply on the first draft — not after correction.

2. **Auto-memory is CWD-scoped by default**: The default memory path is derived from the working directory and only loads in that context. Configure an explicit user-scoped memory directory (`autoMemoryDirectory` in user `settings.json`) for lessons that should persist across all projects.

3. **Hook event migration is a three-part change**: Moving a hook between events requires updating (a) the event key in settings, (b) the `hookEventName` in the script output, and (c) any stdin field references — payload shape differs per event.

4. **Generic corrections belong in the wiki, not memory**: When a user correction reveals a reusable rule, the right destination is the wiki via the reflect → ingest flow. Memory is for mid-session recall of facts; the wiki is for durable, cross-session lessons.

5. **Public wiki drafts must be sanitized before writing**: Scan for usernames, absolute paths, project names, and issue numbers before writing to any public repo. The check belongs at draft time, not after rejection.

6. **A hook loaded from one project's config is not scoped to that project's files at runtime.** `PostToolUse` (and other) hooks fire session-wide once the settings file defining them has loaded, regardless of which repository a given tool call touches. A hook that filters by content (e.g., only acts on files under a specific path pattern) is scoped correctly for *which files it acts on*, but if the hook command itself uses a path relative to the working directory to locate its own script or data, it breaks the moment the session's working directory drifts to an unrelated project — because a relative path only resolves correctly when cwd matches the location the hook was written for. Anchor hook commands to an absolute, stable path, not one relative to wherever the session happens to be when the hook fires.

## Tips & Tricks for Claude Code

- **Tip**: Pipe-test hook scripts with a synthetic stdin payload before adding them to `settings.json`. For `PreToolUse`, the payload is `{"tool_name": "...", "tool_input": {...}}` — construct a realistic example for the target tool.
- **Tip**: When moving a hook between events, treat it as a three-field change: settings key, `hookEventName` in output JSON, and stdin field references.
- **Tip**: `autoMemoryDirectory` in user `~/.claude/settings.json` sets a single memory directory that loads regardless of working directory — use it for user-scoped lessons.
- **Tip**: `PostToolUse` hooks registered in a project's settings file apply for the rest of the session, not just while that project is the active working directory — design the hook's own path-matching logic accordingly, and don't rely on cwd for anything the hook needs to locate itself.

## See Also

- [Allowlist Audit and Session Hygiene](allowlist-audit-and-session-hygiene.md) — Stop hooks as session-end triggers
- [Wiki Ingest and Cleanup Discipline](wiki-ingest-and-cleanup-discipline.md) — when to use the wiki vs. other storage
- [Confirm Scope Before Building Automation; Gate Anything Self-Modifying](../conventions/scope-before-autonomous-automation.md) — confirm a hook's trigger scope, and gate anything self-modifying, before wiring it into config
- [Fire-and-Forget Background Threads in Short-Lived Scripts Need a Bounded Join](fire-and-forget-thread-needs-bounded-join.md) — a hook-specific silent-failure mode: a daemon thread racing process exit dropped 100% of log deliveries with no error surfaced

---

*Generated by `/reflect`*
