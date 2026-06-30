---
type: lesson
tags: [speckit, workflow, tooling, git]
Title: Speckit Setup Scripts Resolve FEATURE_DIR by Git Branch
Sources: Session reflection, 2026-06-30
Raw: "[../../raw/lessons-learned/2026-06-30-speckit-script-branch-resolution.md](../../raw/lessons-learned/2026-06-30-speckit-script-branch-resolution.md)"
Updated: 2026-06-30
---

# Speckit Setup Scripts Resolve FEATURE_DIR by Git Branch

`setup-tasks.sh`, `setup-plan.sh`, and `check-prerequisites.sh` all resolve `FEATURE_DIR` by matching the current git branch name against `specs/NNN-*` directories. Passing a spec number as an argument to `/speckit-tasks 004` does **not** override this branch-based resolution. When the current branch is `main` (or any branch whose name doesn't match a `specs/` subdirectory), the scripts silently fall back to the most recently active spec.

## Failure mode

Invoking `/speckit-tasks 004` on `main` resolves `FEATURE_DIR` to the wrong spec directory. Output files are written to the wrong location, and downstream steps (like issue deduplication) check against the wrong task list — with no error or warning emitted.

## Rule

Before running any `/speckit-*` skill that reads `FEATURE_DIR`, verify the current branch matches the target spec:

```bash
git branch --show-current  # must match specs/NNN-* for the right spec
```

## Workarounds

**Option A (preferred):** Switch to the spec's feature branch before invoking the skill.

```bash
git checkout feat/spec-004-auth
# /speckit-tasks 004 and /speckit-taskstoissues now resolve correctly
```

**Option B (bypass):** Skip the skill entirely when on `main`. Read spec artifacts directly, write `tasks.md` to the correct path, and create issues with a direct loop:

```bash
python3 -c "..." | while read tid desc; do
  gh issue create --title "$tid: $desc" --body "..."
done
```

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md) — verify tool context before invoking, same principle
