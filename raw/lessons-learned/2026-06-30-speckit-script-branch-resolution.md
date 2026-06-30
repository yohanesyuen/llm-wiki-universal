---
source: session-reflection
collected: 2026-06-30
published: Unknown
---

# Speckit Setup Scripts Resolve FEATURE_DIR by Git Branch, Not by Argument

**Date**: 2026-06-30
**Tags**: speckit, workflow, tooling

---

## Lesson

`setup-tasks.sh`, `setup-plan.sh`, and `check-prerequisites.sh` all resolve `FEATURE_DIR` by matching the current git branch name against `specs/NNN-*` directories. Passing a spec number argument to `/speckit-tasks 004` does NOT override this branch-based resolution. When the current branch is `main` (or any branch whose name doesn't match a `specs/` subdirectory), the scripts fall back to the most recently active spec — silently.

## Failure Mode

`/speckit-tasks 004` and `/speckit-taskstoissues` were invoked on branch `main`. Both resolved `FEATURE_DIR` to `specs/005-portal-rbac-users` (the branch-matched spec) rather than `specs/004-portal-auth`. `tasks.md` was written to the wrong directory. `/speckit-taskstoissues` checked dedup against spec-005's task IDs instead of spec-004's, causing 56 of 64 issues to be silently skipped. Neither command emitted an error or warning about the mismatch.

## Workarounds

**Option A (preferred)**: Switch to the spec's feature branch before invoking the skill.

```bash
git checkout feat/spec-004-auth
# now /speckit-tasks 004 and /speckit-taskstoissues resolve correctly
```

**Option B (bypass)**: Skip the skill entirely when on `main`. Read spec artifacts directly, write `tasks.md` to the correct path manually, then create issues with a direct `gh issue create` loop.

```bash
# create issues without relying on the skill's FEATURE_DIR resolution
python3 -c "..." | while read tid desc; do
  gh issue create --title "$tid: $desc" --body "..."
done
```

## Rule

Before running any `/speckit-*` skill that reads `FEATURE_DIR`, verify `git branch --show-current` matches the target spec's directory name. If it doesn't, switch branches first or use Option B.
