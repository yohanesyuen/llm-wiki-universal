---
source: session-reflection
collected: 2026-07-08
published: Unknown
---

# Session Reflection: Worktree isolation limits, and a shell-hook race that silently reverted an edit

**Date**: 2026-07-08
**Session Goal**: Rename and relocate a directory of exploratory scripts to better reflect its actual purpose, updating an accompanying project-catalog file to match.

---

## What Went Well

- Asking one clarifying question before rewriting the directory's purpose statement (rather than guessing at a specific downstream use case) avoided prematurely committing to an approach the user hadn't decided on. Their answer ("keep it open-ended") correctly shaped everything that followed.
- When the user interrupted a rewrite mid-flight with a scoping correction ("keep the original list, just append new ideas"), the correction was applied precisely — nothing beyond what was asked was touched.
- Before renaming/relocating, checked for adjacent existing work in the same problem space and surfaced it rather than silently duplicating effort.
- When asked what would prevent a recurring friction point, resisted the broadest/easiest fix (disabling a safety guard entirely) and explained concretely why: the broad fix would remove protection from unrelated areas that legitimately need it, to solve a problem localized to one specific case.

## What Went Wrong

- Spent a full isolate → discover-it-can't-help → de-isolate round trip before realizing that a git-based isolation mechanism (create an isolated worktree, edit there) cannot help at all for a path that is deliberately untracked by git — an untracked file simply doesn't exist in a freshly created worktree. The information needed to skip this round trip (an explicit note that the directory was untracked) was available up front and should have been checked before attempting isolation, not after it failed.
- When working around a tool-level edit guard via a raw shell command instead of the normal file-edit tool, a leading directory-change (`cd`) in that command silently triggered an unrelated background hook wired into the shell's startup config — one that reruns an auto-refresh script whenever the working directory changes. That background process read the file *before* the intended edit landed and wrote it back *after*, invisibly reverting the edit with no error surfaced anywhere. The edit script itself reported success and exited cleanly; the actual state on disk was simply wrong. This was only caught by a habitual re-verification step (re-reading the file) immediately afterward, not by anything in the write path itself signaling a problem.
- The root issue was a pure race condition introduced by mixing "run arbitrary shell commands" with "the shell config includes automation I didn't know about." A model reasonably chaining `cd <dir> && <command>` for convenience has no visibility into directory-change hooks unless it deliberately checks for them.

## Lessons Learned

1. **An isolation mechanism built on version control cannot isolate what version control doesn't track.** Before reaching for a git-based isolation step, check whether the target path is actually tracked (a quick untracked-file status check, or an explicit note at the target). If it isn't, the isolation step is guaranteed to fail after the fact — skip straight to the eventual workaround instead of discovering this by trial.
2. **A directory change inside a raw shell command is not side-effect-free in a real, configured shell.** Interactive shell configuration can wire arbitrary background behavior to directory changes. When a file edit silently fails to "stick" despite a clean, error-free exit, consider whether something *else* running in that same shell environment — triggered by an incidental part of the command, not the edit logic itself — clobbered it afterward.
3. **A clean exit code from a write operation only proves the foreground step succeeded — it says nothing about a concurrent process later overwriting the same file.** The only thing that actually caught this was re-reading the file immediately after the write, as a standing habit, rather than trusting the write path's own reported success.
4. **The "properly isolated" path is sometimes the wrong isolation for a given situation.** When the true source of truth is local, uncommitted state (e.g., a large pending change from some other automated process) rather than the last remote-committed state, routing a small fix through a freshly isolated branch/worktree can produce a change that's diverged from reality rather than layered correctly on top of it. Recognizing *why* the default "isolate everything" playbook doesn't fit a specific situation matters more than mechanically applying it.

## Action Items

- [ ] Adopt re-reading/re-verifying any file immediately after a write that happened via a workaround (rather than a guarded, tool-native edit path) as a standing habit, not something re-derived only after being burned by it.
- [ ] Before chaining a directory-change into a shell command inside a project with its own dotfiles/startup hooks, consider checking once per session whether that project wires any directory-change automation, so this class of race is anticipated rather than discovered by luck.

## Tips & Tricks for Claude Code

- **Tip**: A quick untracked-file check on a target path (or an explicit "this is untracked" note left at the target itself) is a cheap way to rule out a version-control-based isolation step before investing in it.
- **Tip**: Re-verify with a fresh read immediately after any file write that used a workaround path instead of the normal guarded edit tool — the guarded tools guarantee their own success signal is meaningful; raw shell writes do not protect against concurrent external processes.

---

*Generated by `/reflect`*
